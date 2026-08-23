"""Concrete DocumentWriter — reads from and writes to the real filesystem."""

from __future__ import annotations

from pathlib import Path


class FileDocumentWriter:
    """Reads template.md from the template artifact layer; writes output docs."""

    def read_template(self, doc_dir: str) -> str:
        path = Path(doc_dir) / "template.md"
        if not path.exists():
            raise FileNotFoundError(f"template.md not found: {path}")
        return path.read_text()

    def write(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def shape_path(self, templates_dir: str, phase: str, doc_id: str) -> Path:
        return Path(templates_dir).parent / "shapes" / phase / f"{doc_id}.shacl.ttl"

    def doc_dir(self, templates_dir: str, phase: str, doc_id: str) -> str:
        return str(Path(templates_dir) / phase / doc_id)
