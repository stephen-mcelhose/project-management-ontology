"""Agent configuration — all values read from environment variables.

Load order:
1. Existing shell environment (highest priority)
2. .env file (populated by load_dotenv with override=False)
3. Defaults defined here

Never hardcode credentials. Never log credential values.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


class Settings:
    def __init__(self) -> None:
        # Non-override: existing shell env wins over .env values
        load_dotenv(override=False)

        raw_vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "true").strip().lower()
        self.use_vertexai: bool = raw_vertex in {"1", "true", "yes", "on"}

        self.location: str = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
        self.model: str = os.environ.get("AGENT_MODEL", "gemini-2.0-flash")

        self._project: str | None = os.environ.get("GOOGLE_CLOUD_PROJECT")

        self.api_key: str | None = os.environ.get("GOOGLE_API_KEY") or os.environ.get(
            "GEMINI_API_KEY"
        )

        # Write back so google-genai SDK picks it up via env
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(self.use_vertexai).lower()

    @property
    def project(self) -> str:
        if self._project:
            return self._project
        try:
            import google.auth
            import google.auth.exceptions

            _, project = google.auth.default()
            self._project = project or ""
        except ImportError:
            # google-auth package not available in this environment
            self._project = ""
        except google.auth.exceptions.GoogleAuthError:
            # No ADC credentials configured (DefaultCredentialsError, etc.)
            self._project = ""
        return self._project
