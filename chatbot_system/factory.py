from .core import ChatbotEngine
from .repository import SqlAlchemyChatRepository
from .modules.v2_module import V2ChatModule

class ChatbotFactory:
    """
    Factory to create the appropriate Chatbot Engine.
    Updated to use the V2 Logic agents.
    """
    
    @staticmethod
    def get_engine_for_user(user_role: str, db_session=None) -> ChatbotEngine:
        """
        Returns a ChatbotEngine configured with the V2 Orchestrator module.
        """
        repo = SqlAlchemyChatRepository(db_session)
        
        # In the new design, the V2ChatModule handles intent detection 
        # and role-based routing internally or via agents.
        modules = [V2ChatModule()]
            
        return ChatbotEngine(modules, repo)
