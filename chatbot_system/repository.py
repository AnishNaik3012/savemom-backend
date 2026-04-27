from typing import List, Any
import uuid
from .interfaces import IChatRepository
from db import SessionLocal
from model import Message, Conversation, User

class SqlAlchemyChatRepository(IChatRepository):
    """
    Implementation interacting with the new schema in model.py.
    """
    def __init__(self, db_session=None):
        self.db_session = db_session or SessionLocal()

    def _get_or_create_conversation(self, user_id_str: str) -> uuid.UUID:
        # Convert user_id_str to UUID if possible, else use a deterministic one for mock
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            # For temp-user or invalid UUID strings, use a fixed namespace UUID
            user_id = uuid.uuid5(uuid.NAMESPACE_DNS, user_id_str)

        # Check for existing conversation for this user
        conv = self.db_session.query(Conversation).filter(
            Conversation.created_by == user_id
        ).first()

        if not conv:
            conv = Conversation(
                id=uuid.uuid4(),
                created_by=user_id,
                is_group=False
            )
            self.db_session.add(conv)
            # We might need to ensure the User exists too if there's a hard FK constraint
            # but for mock/prototype we assume DB is permissive or user exists.
            self.db_session.commit()
        
        return conv.id

    def get_recent_history(self, user_id: str, limit: int = 5) -> List[Any]:
        # Implementation for history - simplified for now
        return []
    
    def save_message(self, user_id: str, text: str, sender_type: str) -> None:
        try:
            conv_id = self._get_or_create_conversation(user_id)
            
            # Map user_id to UUID
            try:
                sender_uid = uuid.UUID(user_id)
            except ValueError:
                sender_uid = uuid.uuid5(uuid.NAMESPACE_DNS, user_id)

            msg = Message(
                id=uuid.uuid4(),
                conversation_id=conv_id,
                sender_id=sender_uid,
                content=str(text),
                message_type="text"
            )
            self.db_session.add(msg)
            self.db_session.commit()
            try:
                print(f"[DB LOG]: Saved {sender_type} message for {user_id}: {text}")
            except:
                print(f"[DB LOG]: Saved {sender_type} message for {user_id} (Text contains non-standard characters)")
        except Exception as e:
            print(f"[DB ERROR]: Failed to save message: {e}")
            self.db_session.rollback()
