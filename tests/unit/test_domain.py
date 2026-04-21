from __future__ import annotations

from solstein.domain import Company, Universe


class TestCompany:
    def test_minimum_valid_company(self) -> None:
        c = Company(name="X")
        assert c.tier == "unknown"
        assert c.composite_score is None
        assert c.completeness() == 0.0

    def test_completeness_fraction(self) -> None:
        c = Company(name="X", revenue_eur=1.0, employees=1, growth_yoy=0.1)
        assert c.completeness() == 3 / 5


class TestUniverse:
    def test_roundtrip(self) -> None:
        u = Universe(name="test", companies=[Company(name="A"), Company(name="B")])
        restored = Universe.model_validate(u.model_dump())
        assert len(restored.companies) == 2
        assert restored.name == "test"
