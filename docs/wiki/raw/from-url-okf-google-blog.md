# Raw Source — Google Cloud Blog: Open Knowledge Format

Source URL: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
Fetched: 2026-08-23

---

## What is OKF?

The Open Knowledge Format (OKF) is an open specification (v0.1, June 2026) published by Google Cloud's
Data Cloud engineering team. It formalizes the "LLM-wiki" pattern into a portable, interoperable,
vendor-neutral format. An OKF bundle is a directory of markdown files with YAML frontmatter, bound by
a minimal set of agreed-upon conventions.

## Structure

- File path = identity of the concept
- YAML frontmatter block + Markdown body per concept file
- Graph relationships via standard Markdown hyperlinks (not hierarchical folders)
- Reserved files: `index.md` (progressive disclosure), `log.md` (chronological history)

### Directory example

```
sales/
├── index.md
├── datasets/
│   ├── index.md
│   └── orders_db.md
├── tables/
│   ├── index.md
│   ├── orders.md
│   └── customers.md
└── metrics/
    ├── index.md
    └── weekly_active_users.md
```

## Fields (v0.1)

| Field         | Required? | Description                                              |
| ------------- | --------- | -------------------------------------------------------- |
| `type`        | REQUIRED  | Kind of concept (e.g. BigQuery Table, Metric, API)       |
| `title`       | optional  | Human-readable name                                      |
| `description` | optional  | Short summary                                            |
| `resource`    | optional  | URI to the original platform resource                    |
| `tags`        | optional  | Array of keywords                                        |
| `timestamp`   | optional  | ISO 8601 date-time of last update                        |

The design is "minimally opinionated" — only `type` is strictly required.

## Purpose

Solve the "context-assembly problem": fragmented institutional knowledge (schemas, metric definitions,
runbooks, API deprecations) stored across catalogs, wikis, code comments, and engineers' heads.
OKF gives AI agents a shared, unified, evolving markdown library. It is a format, not a service.

## How it improves data sharing

- Vendor-neutral lingua franca — any agent/tool can read/write without proprietary SDKs
- Version-control friendly — lives in Git alongside code
- Decouples producers from consumers — human-written bundles readable by AI and vice versa

## Concrete example (orders.md)

```yaml
---
type: BigQuery Table
title: Orders
description: One row per completed customer order.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, revenue]
timestamp: 2026-05-28T14:30:00Z
---
# Schema
| Column        | Type      | Description                               |
|---------------|-----------|-------------------------------------------|
| `order_id`    | STRING    | Globally unique order identifier.         |
| `customer_id` | STRING    | FK to [customers](/tables/customers.md).  |

# Joins
Joined with [customers](/tables/customers.md) on `customer_id`.
```

## Reference implementations shipped with v0.1

1. Enrichment Agent — scans BigQuery, drafts OKF concept docs, enriches with join paths/citations
2. Static HTML Visualizer — single self-contained file, renders OKF folder as interactive graph
3. Sample datasets — GA4 e-commerce, Stack Overflow, Bitcoin (published on GitHub)
4. Google Cloud Knowledge Catalog — updated to natively ingest OKF for internal/external AI agents
