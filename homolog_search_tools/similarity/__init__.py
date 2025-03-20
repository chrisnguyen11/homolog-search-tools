"""Sequence similarity tools."""

from ._mmseqs2 import MMseqs2
from ._diamond import Diamond

__all__ = [
    "MMseqs2",
    "Diamond"
]
