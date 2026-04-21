"""Tests for text-signal extractors."""

from __future__ import annotations

from solstein.text_signals import ai_maturity_from_text, tech_stack_hints


class TestAIMaturityFromText:
    def test_short_text_returns_none(self) -> None:
        score, evidence = ai_maturity_from_text("short text")
        assert score is None
        assert evidence == 0

    def test_text_without_signal_returns_zero_not_none(self) -> None:
        text = "We are a marketing company specializing in brand consulting. " * 10
        score, evidence = ai_maturity_from_text(text)
        assert score == 0.0
        assert evidence == 0

    def test_high_signal_terms_score_high(self) -> None:
        text = (
            "Our MLOps platform combines a feature store, vector database, and "
            "production ML serving to power RAG pipelines with fine-tuning. "
            "Built on a scalable ML platform with LLMOps automation."
        )
        score, evidence = ai_maturity_from_text(text * 3)
        assert score is not None
        assert score >= 7.0
        assert evidence >= 5

    def test_medium_signal_scores_moderate(self) -> None:
        text = (
            "Our product uses machine learning with TensorFlow and PyTorch. "
            "We process natural language with transformers and build LLM "
            "applications on top of Hugging Face models."
        )
        score, _ = ai_maturity_from_text(text * 3)
        assert score is not None
        assert 3.0 <= score <= 8.0

    def test_low_signal_only_scores_low(self) -> None:
        text = (
            "We're an AI-powered automation platform using advanced algorithms "
            "for data-driven insights. Our intelligent system leverages "
            "artificial intelligence."
        )
        score, _ = ai_maturity_from_text(text * 3)
        assert score is not None
        assert score < 3.0

    def test_fluff_without_substance_is_de_rated(self) -> None:
        # Only fluff, no real ML terms
        text = (
            "Revolutionary AI solutions. Game-changing AI technology. "
            "Next-generation AI platform. Cutting-edge AI innovation. "
            "We are AI-first."
        ) * 3
        score, _ = ai_maturity_from_text(text)
        assert score is not None
        assert score < 2.0

    def test_score_is_capped_at_10(self) -> None:
        text = (
            "MLOps LLMOps production ML model serving feature store vector database "
            "RAG pipeline fine-tuning prompt engineering ML platform ML infrastructure "
        ) * 10
        score, _ = ai_maturity_from_text(text)
        assert score is not None
        assert score <= 10.0

    def test_realistic_legacy_marketing_page(self) -> None:
        """A realistic non-AI marketing page should score low or zero."""
        text = (
            "Energy21 is a leading provider of energy trading software. "
            "Our portfolio management platform helps utilities optimize "
            "their trading operations with smart software and data-driven insights. "
            "We serve major European energy companies with reliable, scalable solutions."
        ) * 3
        score, _ = ai_maturity_from_text(text)
        assert score is not None
        assert score < 3.0  # only "smart software", "data-driven" → low signal


class TestTechStackHints:
    def test_finds_common_stacks(self) -> None:
        text = (
            "We use Python and TypeScript. Our backend runs on FastAPI with PostgreSQL. "
            "Frontend is React. Infrastructure on AWS with Kubernetes."
        )
        hints = tech_stack_hints(text)
        assert "python" in hints
        assert "typescript" in hints
        assert "fastapi" in hints
        assert "postgresql" in hints
        assert "react" in hints
        assert "aws" in hints
        assert "kubernetes" in hints

    def test_word_boundaries_prevent_partial_matches(self) -> None:
        # "go" is a stack term; "google" contains g-o but should not match
        text = "We use google cloud. Our team is geographically distributed."
        hints = tech_stack_hints(text)
        assert "go" not in hints

    def test_empty_text_returns_empty_list(self) -> None:
        assert tech_stack_hints("") == []

    def test_returns_sorted(self) -> None:
        text = "We use React, Python, AWS."
        hints = tech_stack_hints(text)
        assert hints == sorted(hints)
