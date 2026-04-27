from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Optional, Any
import datetime

@dataclass
class ChatContext:
    """Holds the context of the current chat interaction."""
    user_id: str
    user_role: str  # 'mother', 'doctor', 'lab_worker', etc.
    message_text: str
    metadata: dict = field(default_factory=dict)
    
    # Can allow modules to pass data between each other or store state
    session_data: dict = field(default_factory=dict)

class IChatModule(ABC):
    """Interface for a Chat Capability/Skill."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the module."""
        pass

    @abstractmethod
    def can_handle(self, context: ChatContext) -> bool:
        """Determines if this module should handle the current message."""
        pass

    @abstractmethod
    def process(self, context: ChatContext) -> Any:
        """
        Process the message and return a response (string or dict).
        In a real RAG system, this is where the retrieval would happen.
        """
        pass

class IChatRepository(ABC):
    """Interface for database operations (Abstracts SQLAlchemy)."""
    
    @abstractmethod
    def get_recent_history(self, user_id: str, limit: int = 5) -> List[Any]:
        pass
    
    @abstractmethod
    def save_message(self, user_id: str, text: str, sender_type: str) -> None:
        pass
