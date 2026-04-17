from dataclasses import dataclass
from typing import Optional


@dataclass
class Role:
    role_id: str
    name: str
    description: Optional[str] = None
