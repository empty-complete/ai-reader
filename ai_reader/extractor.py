from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
import json
from typing import Any

RULES = """
You must extract structured information strictly in JSON format.

Rules:
1. Reply ONLY using the JSON object.
2. Use the following keys in JSON: {keys}.
3. Do not add additional keys, explanations, comments, or text outside of JSON.
4. If the key does not contain data in the provided text, assign it the value of the empty string "".
5. All values should be simple strings.
6. If there are several values, it should still be a string of the format "value1,value2,vlaue3".
7. JSON must be syntactically correct and available for analysis using json.loads().

Returns ONLY JSON. No markdown, no code blocks, no prose.
"""

class ExtractorAI:
    """Utility class that prepares prompts and sorts extracted data by keys."""

    def __init__(self, *, llm_client: Callable[[str], str] | None = None) -> None:
        self._prepromt = ""
        self._keys: tuple[str, ...] = ()
        self._llm_client = llm_client

    @property
    def prepromt(self) -> str:
        return self._prepromt

    @prepromt.setter
    def prepromt(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("prepromt must be string")
        self._prepromt = value.strip()

    def load_prepromt(self, promt: str) -> None:
        """Store the prefix prompt that must be prepended before each request."""
        self.prepromt = promt

    def load_dict(self, keys: Iterable[str]) -> None:
        """Configure the extraction targets."""
        normalized = tuple(self._normalize_key(key) for key in keys if str(key).strip())
        if not normalized:
            raise ValueError("keys collection cannot be empty")
        self._keys = normalized

    def extract(self, text: str) -> dict[str, str]:
        """Extract information from the text and map it to the configured keys."""
        if not isinstance(text, str):
            raise TypeError("text must be string")
        if not self._keys:
            raise RuntimeError("load_dict must be called before extract")

        payload = self._compose_prompt(text)

        if self._llm_client is not None:
            raw = self._llm_client(payload)
            parsed = self._parse_response(raw)
            if parsed is not None:
                return parsed

        return self._empty_result()

    def _compose_prompt(self, text: str) -> str:
        parts: list[str] = []
        if self.prepromt:
            parts.append(self.prepromt)
        parts.append(RULES)
        parts.append("Collect information on the keys: " + ", ".join(self._keys))
        parts.append("The original text:")
        parts.append(text.strip())
        return "\n\n".join(parts)

    def _parse_response(self, raw: Any) -> dict[str, str] | None:
        if not isinstance(raw, str):
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if not isinstance(data, Mapping):
            return None
        return self._ensure_all_keys(
            {key: self._stringify(data.get(key, "")) for key in self._keys}
        )

    def _ensure_all_keys(self, data: Mapping[str, str]) -> dict[str, str]:
        return {key: data.get(key, "") for key in self._keys}

    def _normalize_key(self, key: str) -> str:
        return str(key).strip()

    def _stringify(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        return json.dumps(value, ensure_ascii=True)

    def _empty_result(self) -> dict[str, str]:
        return {key: "" for key in self._keys}



__all__ = ["ExtractorAI"]
