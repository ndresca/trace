from dataclasses import dataclass, field


@dataclass
class Entity:
    id: str
    name: str
    aliases: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    popularity_score: float = 0.0
    attributes: dict[str, float] = field(default_factory=dict)


@dataclass
class Question:
    id: str
    text: str
    attribute_key: str
    priority: int = 0
    enabled: bool = True
