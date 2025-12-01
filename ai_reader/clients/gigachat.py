from __future__ import annotations

from typing import Callable
from gigachat import GigaChat


def make_gigachat_client(
    *,
    credentials: str,
    scope: str = "GIGACHAT_API_PERS",
    verify_ssl_certs: bool = False,
) -> Callable[[str], str]:
    """
    Returns a callable that follows ExtractorAI's contract:
    (prompt: str) -> str.

    Internally sends requests to GigaChat.
    """

    def llm_client(prompt: str) -> str:
        with GigaChat(
            credentials=credentials,
            scope=scope,
            verify_ssl_certs=verify_ssl_certs,
        ) as giga:
            resp = giga.chat(prompt)
            return resp.choices[0].message.content

    return llm_client


__all__ = ["make_gigachat_client"]
