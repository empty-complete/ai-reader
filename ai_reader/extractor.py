from __future__ import annotations

from collections.abc import Callable, Mapping
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


Additional information you need to know before you start working:
{prepromt}

Here is the text to extract the data from:
{text}
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

    def load_keys(self, *keys: str) -> None:
        """Configure the extraction targets."""
        seen: set[str] = set()
        normalized_list: list[str] = []

        for raw in keys:
            key = self._normalize_key(raw)
            if not key:
                continue
            if key in seen:
                continue
            seen.add(key)
            normalized_list.append(key)

        if not normalized_list:
            raise ValueError("keys collection cannot be empty")

        self._keys = tuple(normalized_list)

    def extract(self, text: str) -> dict[str, str]:
        """Extract information from the text and map it to the configured keys."""
        if not isinstance(text, str):
            raise TypeError("text must be string")
        if not self._keys:
            raise RuntimeError("load_keys must be called before extract")
        
        if self._llm_client is None:
            raise RuntimeError(
                "llm_client is not configured. "
                "Pass a callable to ExtractorAI(llm_client=...) before calling extract()."
            )

        payload = self._compose_prompt(text)

        raw = self._llm_client(payload)
        parsed = self._parse_response(raw)
        if parsed is None:
            raise ValueError(
                "LLM returned a response that could not be parsed as a JSON object "
                "with the configured keys."
            )
        return parsed

    def _compose_prompt(self, text: str) -> str:
        prompt_intro = self.prepromt or "None"
        return RULES.format(
            keys=", ".join(self._keys),
            prepromt=prompt_intro,
            text=text.strip(),
        ).strip()

    def _parse_response(self, raw: Any) -> dict[str, str] | None:
        if not isinstance(raw, str):
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if not isinstance(data, Mapping):
            return None

        result: dict[str, str] = {}
        for key in self._keys:
            value = data.get(key, "")

            # Normalized types:
            # - None -> ""
            # - scalars -> str()
            # - list -> "v1,v2,v3"
            # - another types is error

            if value is None:
                normalized = ""
            elif isinstance(value, str):
                normalized = value
            elif isinstance(value, (int, float, bool)):
                normalized = str(value)
            elif isinstance(value, list):
                normalized = ",".join(str(item) for item in value)
            else:
                # if structure is strange
                return None

            result[key] = normalized

        return self._ensure_all_keys(result)

    def _ensure_all_keys(self, data: Mapping[str, str]) -> dict[str, str]:
        return {key: data.get(key, "") for key in self._keys}

    def _normalize_key(self, key: str) -> str:
        return str(key).strip()



__all__ = ["ExtractorAI"]
