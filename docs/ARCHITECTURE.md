# Architecture

## One diagram

```
Universe JSON ─► pipeline.run ─► adapters (concurrent) ─► scoring ─► export
                                                                      │
                                                                      ├── Excel
                                                                      └── Markdown brief
```

## Rules we inherited from v1's mistakes

1. **One pipeline.** `solstein.pipeline.run` is the only path. No dual-writes, no legacy/canonical split, no parallel graph.
2. **One threshold registry.** `solstein.scoring.thresholds` defines every tier boundary. Never defined anywhere else.
3. **No silent defaults.** Scorers return `None` when inputs are missing. Classification only runs on non-`None` composites.
4. **Every enriched field has a citation.** If an adapter populates `github_stars_total`, it attaches a `Citation` to `company.citations["github_stars_total"]`. Full traceability by construction.
5. **No stub agents.** Adapters hit real services or don't exist. No hardcoded mock data ever lands in `Company`.
6. **Small surface.** Target <20 Python files in `src/solstein/`. When we hit 20, we stop and think.

## File budget

| Module | Files (target) | Rule |
|---|---|---|
| `domain.py` | 1 | One file for all shared types. If it grows past 200 lines, split by concept, not by class. |
| `scoring/` | 2-3 | `thresholds.py`, `scorers.py`, `__init__.py`. |
| `adapters/` | 1 per real source | GitHub, SEC EDGAR, Companies House, Crunchbase… add when needed, not before. |
| `enrichment/` | 1 per source | Same rule. |
| `pipeline/` | 1-2 | `run.py`. A second file only if we introduce true staged execution. |
| `export/` | 1 | `writers.py`. |
| `cli/` | 1 | `main.py`. |

## Testing

- **Unit** (`tests/unit/`): pure functions, no I/O, <50ms each.
- **Integration** (`tests/integration/`): real adapters behind `--run-integration` or env gate.
- **Fixtures** (`tests/fixtures/`): frozen universes + expected scores. Eneve is the permanent regression fixture.

## Non-goals

- Multi-tenant SaaS. Not this product.
- External user auth. Not this product.
- REST/GraphQL API surface. Not this product.
- Database. The pipeline is stateless; Universe JSON in, files out.

If any of these become real requirements, that's a new product. Write a new repo.
