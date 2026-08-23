"""Tests for agent/settings.py — all env-var driven, no network calls."""

import importlib
import os


def make_settings(monkeypatch, **env):
    """Instantiate Settings with a clean env."""
    # Clear all relevant vars first
    for key in [
        "GOOGLE_GENAI_USE_VERTEXAI",
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
        "AGENT_MODEL",
        "GOOGLE_API_KEY",
        "GEMINI_API_KEY",
    ]:
        monkeypatch.delenv(key, raising=False)
    for key, val in env.items():
        monkeypatch.setenv(key, val)
    # Import fresh each time
    import agent.settings as mod
    importlib.reload(mod)
    return mod.Settings()


class TestUseVertexAI:
    def test_default_is_true(self, monkeypatch):
        s = make_settings(monkeypatch)
        assert s.use_vertexai is True

    def test_false_string(self, monkeypatch):
        for val in ("false", "False", "FALSE", "0", "off", "no"):
            s = make_settings(monkeypatch, GOOGLE_GENAI_USE_VERTEXAI=val)
            assert s.use_vertexai is False, f"Expected False for {val!r}"

    def test_truthy_string(self, monkeypatch):
        for val in ("true", "True", "1", "yes", "on"):
            s = make_settings(monkeypatch, GOOGLE_GENAI_USE_VERTEXAI=val)
            assert s.use_vertexai is True, f"Expected True for {val!r}"

    def test_written_back_to_os_environ(self, monkeypatch):
        make_settings(monkeypatch, GOOGLE_GENAI_USE_VERTEXAI="false")
        assert os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") == "false"


class TestApiKey:
    def test_google_api_key_used(self, monkeypatch):
        s = make_settings(monkeypatch, GOOGLE_API_KEY="gk-test")
        assert s.api_key == "gk-test"

    def test_gemini_api_key_fallback(self, monkeypatch):
        s = make_settings(monkeypatch, GEMINI_API_KEY="gemini-test")
        assert s.api_key == "gemini-test"

    def test_google_api_key_wins_over_gemini(self, monkeypatch):
        s = make_settings(
            monkeypatch, GOOGLE_API_KEY="gk-test", GEMINI_API_KEY="gemini-test"
        )
        assert s.api_key == "gk-test"

    def test_no_key_on_vertex_path_does_not_raise(self, monkeypatch):
        # Vertex AI path needs no key — Settings should not raise
        s = make_settings(monkeypatch, GOOGLE_GENAI_USE_VERTEXAI="true")
        assert s.api_key is None


class TestDefaults:
    def test_location_default(self, monkeypatch):
        s = make_settings(monkeypatch)
        assert s.location == "global"

    def test_model_default(self, monkeypatch):
        s = make_settings(monkeypatch)
        assert s.model == "gemini-2.0-flash"

    def test_location_override(self, monkeypatch):
        s = make_settings(monkeypatch, GOOGLE_CLOUD_LOCATION="us-central1")
        assert s.location == "us-central1"

    def test_model_override(self, monkeypatch):
        s = make_settings(monkeypatch, AGENT_MODEL="gemini-2.5-pro")
        assert s.model == "gemini-2.5-pro"


class TestProjectResolution:
    def test_explicit_project_used(self, monkeypatch):
        s = make_settings(monkeypatch, GOOGLE_CLOUD_PROJECT="my-proj")
        assert s.project == "my-proj"

    def test_missing_project_returns_empty_string_without_adc(self, monkeypatch):
        # Patch google.auth.default to simulate no ADC credentials configured.
        # Raises DefaultCredentialsError (a GoogleAuthError) as the real SDK does.
        import google.auth.exceptions
        from unittest import mock
        with mock.patch(
            "google.auth.default",
            side_effect=google.auth.exceptions.DefaultCredentialsError("no credentials"),
        ):
            s = make_settings(monkeypatch)
            assert s.project == ""


class TestDotenvNonOverride:
    def test_existing_env_wins_over_dotenv(self, monkeypatch, tmp_path):
        # Write a .env file that sets AGENT_MODEL
        env_file = tmp_path / ".env"
        env_file.write_text("AGENT_MODEL=gemini-from-dotenv\n")
        monkeypatch.chdir(tmp_path)
        # Pre-set the env var — it should win
        monkeypatch.setenv("AGENT_MODEL", "gemini-from-shell")
        import agent.settings as mod
        importlib.reload(mod)
        s = mod.Settings()
        assert s.model == "gemini-from-shell"
