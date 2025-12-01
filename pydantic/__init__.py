from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Dict, get_type_hints


class ValidationError(Exception):
    """Error simple de validación."""


class BaseModel:
    """Implementación mínima inspirada en Pydantic.

    Permite validar tipos básicos y exportar diccionarios con `model_dump`.
    """

    def __init__(self, **data: Any) -> None:
        annotations = get_type_hints(self.__class__)
        for name, expected_type in annotations.items():
            if name not in data:
                raise ValidationError(f"Falta el campo requerido: {name}")
            value = data[name]
            if expected_type is float and isinstance(value, int):
                value = float(value)
            if expected_type is bool and isinstance(value, str):
                lowered = value.lower()
                if lowered in {"true", "1", "yes"}:
                    value = True
                elif lowered in {"false", "0", "no"}:
                    value = False
            if not isinstance(value, expected_type):
                raise ValidationError(f"{name} debe ser de tipo {expected_type.__name__}")
            setattr(self, name, value)

    def model_dump(self) -> Dict[str, Any]:
        return {name: getattr(self, name) for name in getattr(self, "__annotations__", {})}


__all__ = ["BaseModel", "ValidationError"]
