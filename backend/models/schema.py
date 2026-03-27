from pydantic import BaseModel
from typing import List, Optional, Dict


class QueryRequest(BaseModel):
    question: str
    history: Optional[List[Dict[str, str]]] = None