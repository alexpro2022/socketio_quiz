"""Async interface for future real DB connection."""
from pydantic import BaseModel
from typing import TypeAlias

ModelType: TypeAlias = BaseModel
SeqType: TypeAlias = list[ModelType]


async def _get(seq: SeqType, **kwargs):
    def pred(item):
        for k, v in kwargs.items():
            if getattr(item, k, float('inf')) != v:
                return False
        return True
    return filter(pred, seq)


async def fetch_all(seq: SeqType, **kwargs) -> SeqType:
    res = await _get(seq, **kwargs)
    return list(res)


async def fetch_one(seq: SeqType, **kwargs) -> ModelType | None:
    res = await fetch_all(seq, **kwargs)
    return res[0] if res else None
