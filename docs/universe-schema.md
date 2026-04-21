# Universe schema

A universe is a JSON file listing the companies Solstein should research.
It is the single input to the pipeline.

## Minimum

```json
{
  "name": "european-energy-software-2026",
  "description": "optional",
  "companies": [
    { "name": "Acme Energy" }
  ]
}
```

## Full shape per company

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Legal or trading name. |
| `country` | string | no | ISO 3166-1 alpha-2 preferred. |
| `website` | URL | no | Used for identity, not scraping. |
| `revenue_eur` | number | no | Most recent annual revenue. |
| `employees` | int | no | Headcount. |
| `growth_yoy` | number | no | Fractional (0.22 = 22%). |
| `founded_year` | int | no | |
| `github_org` | string | no | Org slug. Triggers GitHub adapter. |

Any field can be provided upfront; anything missing is filled by adapters where possible.

## Rules

- The pipeline **never invents data**. Missing fields stay missing.
- Scoring returns `None` when required signals are absent; companies still appear in the output but are flagged as such.
- Every enriched field carries a `Citation` — you can always trace where a number came from.
