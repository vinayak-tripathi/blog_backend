from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    id: int
    title: str
    body: str
    published: Optional[bool]=False
    # published: Optional[bool]