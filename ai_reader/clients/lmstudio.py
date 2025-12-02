from __future__ import annotations

import json
from typing import Any, Callable, Dict, Optional
from urllib import error, request


def make_lmstudio_client(
    *,
    model: str,
    base_url: str = "http://localhost:1234/v1/chat/completions",
    default_system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    extra_payload: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0,
) -> Callable[[str], str]:
    """
    Returns a callable compatible with ExtractorAI: (prompt: str) -> str.

    The callable sends a chat completion request to LM Studio's local
    OpenAI-compatible HTTP API.
    """

    def llm_client(prompt: str) -> str:
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [],
        }

        if default_system_prompt:
            payload["messages"].append({"role": "system", "content": default_system_prompt})

        payload["messages"].append({"role": "user", "content": prompt})

        if temperature is not None:
            payload["temperature"] = temperature

        if extra_payload:
            payload.update(extra_payload)

        req = request.Request(
            base_url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
        )

        try:
            with request.urlopen(req, timeout=timeout) as resp:
                response_body = resp.read().decode("utf-8")
        except error.URLError as exception:  # pragma: no cover - network dependent
            raise RuntimeError(f"Failed to reach LM Studio at {base_url}") from exception

        data = json.loads(response_body)

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exception:
            raise RuntimeError("Unexpected response from LM Studio") from exception

    return llm_client


__all__ = ["make_lmstudio_client"]
