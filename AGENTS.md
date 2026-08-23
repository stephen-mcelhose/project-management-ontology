# AGENTS.md — Project Management Ontology

This file documents the repository conventions for both human contributors and
AI coding assistants (agents). Read it before making changes.

---

## What This Repository Is

A formal OWL/Turtle ontology for project management concepts, paired with a
document template layer (YAML gate files, Markdown scaffolds, SHACL shapes)
that an AI agent can use to guide a user through producing PM documents.

**Key directories:**

```
ontology/              ← OWL/Turtle ontology modules
shapes/                ← SHACL validation shapes (per phase/document)
templates/             ← Document template packs (entry.yaml, instructions.yaml, template.md)
  {phase}/
    _manifest.yaml     ← Phase index (single-read entry point for an agent)
    {document}/
      entry.yaml
      instructions.yaml  ← gate sequence; validated by tools/schemas/instructions-schema.json
      template.md
tools/
  schemas/             ← JSON Schema files for artifact-layer files
    instructions-schema.json
  validate/            ← Validation scripts (make validate, make validate-schemas)
  visualize/           ← Ontology visualisation
docs/
  adrs/                ← Architectural Decision Records
  processes/           ← How-to guides for contributors
  prompts/             ← Phase agent prompt scaffolds
  wiki/                ← LLM-maintained knowledge base (llm-wiki pattern)
```

**Glossary:** see `docs/wiki/glossary.md` — defines phase, package, agent,
orchestrator, gate, manifest, template pack, and more.

---

## Development Workflow

### Branches

`main` is protected. **Never push directly to main.** Use feature branches.

| Branch type | Pattern            | Example                        |
| ----------- | ------------------ | ------------------------------ |
| Feature     | `feat/<topic>`     | `feat/planning-manifests`      |
| Fix         | `fix/<topic>`      | `fix/risk-register-gates`      |
| Docs        | `docs/<topic>`     | `docs/glossary`                |
| Chore       | `chore/<topic>`    | `chore/repo-settings`          |

> **Admin override:** As the repo owner you can push directly to main if
> needed (branch protection has `enforce_admins: false`). Treat this as an
> escape hatch, not the default.

### Pull Requests

- Open a PR from your feature branch to `main`
- PRs require no approvals to merge (solo project), but open one anyway —
  the diff view and conversation thread are worth it
- Stale reviews are dismissed automatically when new commits are pushed
- All PR conversations must be resolved before merging
- Branches are deleted automatically after merge

### Merge Strategy

Two strategies are allowed — choose based on the PR:

| Strategy      | When to use                                                    |
| ------------- | -------------------------------------------------------------- |
| **Squash**    | PR has multiple WIP commits; squash into one clean commit      |
| **Rebase**    | PR has a series of well-crafted commits worth preserving       |

Merge commits are disabled. History must stay linear.

---

## Commit Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body — what and why, 72-char wrap>

<footer — Closes #N>
```

### Types

| Type       | Use when                                               | Version bump? |
| ---------- | ------------------------------------------------------ | ------------- |
| `feat`     | New end-user capability in the deployed tool           | Yes (minor)   |
| `fix`      | Bug fix affecting end users                            | Yes (patch)   |
| `chore`    | Maintenance: deps, configs, prompts, skills, templates | No            |
| `docs`     | Documentation, wiki, ADRs                              | No            |
| `refactor` | Restructuring with no behaviour change                 | No            |
| `test`     | Tests only                                             | No            |
| `ci`       | CI/CD pipeline                                         | No            |

**Rule:** if the change doesn't affect what a user experiences in the
deployed tool, it is not `feat` or `fix`. Template packs, agent prompts,
ontology files, and ADRs are `chore` or `docs`.

### Subject line

- 50 chars max
- Imperative mood: "Add" not "Added"
- No period at the end

---

## Artifact Layer Conventions

### Template packs

Every PM document has four files — do not create partial packs:

```
templates/{phase}/{document}/
  entry.yaml           ← OKF frontmatter, dependency chain, ontology class
  instructions.yaml    ← ordered gates (id, prompt, fills, maps_to, required)
  template.md          ← Markdown scaffold with {{placeholders}}
shapes/{phase}/{document}.shacl.ttl  ← SHACL validation shape
```

### Phase manifests

Every phase directory must have a `_manifest.yaml`. This is the single-read
index for the phase — document sequence, dependency DAG, shared context, and
phase completion condition. See `docs/adrs/adr-003-phase-manifest.md`.

### Phase agent prompts

Every phase has a corresponding scaffold prompt in `docs/prompts/`. These are
placeholders until the ADK agent (issue #39) is built. See
`docs/adrs/adr-002-phase-agent-prompts.md`.

### ADRs

Decisions go in `docs/adrs/adr-NNN-<slug>.md`. Use OKF frontmatter
(`type: decision`). Update `docs/wiki/index.md` Decisions section.

---

## Wiki Maintenance

The wiki at `docs/wiki/` is maintained using the `llm-wiki` skill:

- `ingest <source>` — add a new research source
- `query <question>` — synthesise an answer from wiki pages
- `lint` — check for orphans, stale cross-references, missing index entries

Raw sources in `docs/wiki/raw/` are **immutable** — never edit them.
The log at `docs/wiki/log.md` is **append-only** — never rewrite existing entries.

---

## Branch Protection Summary (main)

| Rule                               | Setting              |
| ---------------------------------- | -------------------- |
| Require pull request               | Yes                  |
| Required approvals                 | 0 (solo project)     |
| Dismiss stale reviews              | Yes                  |
| Require linear history             | Yes                  |
| Allow force pushes                 | No                   |
| Allow branch deletion              | No                   |
| Require conversation resolution    | Yes                  |
| Enforce for admins                 | No (admin override)  |
| Auto-delete head branch after merge | Yes                 |
