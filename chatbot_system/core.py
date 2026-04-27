from typing import List
from .interfaces import ChatContext, IChatModule, IChatRepository

class ChatbotEngine:
    """
    The main engine that processes messages. 
    It is initialized with a specific list of modules (skills) 
    tailored to the user's role.
    """
    
    def __init__(self, modules: List[IChatModule], repository: IChatRepository):
        self.modules = modules
        self.repository = repository
        
    def handle_message(self, user_id: str, user_role: str, text: str) -> str:
        """
        Main entry point.
        1. Creates context.
        2. Finds a module to handle the message.
        3. Returns response.
        (Also saves to DB via repository)
        """
        
        # 1. Save specific User Message
        self.repository.save_message(user_id, text, sender_type="user")
        
        # 2. Setup Context
        context = ChatContext(
            user_id=user_id,
            user_role=user_role,
            message_text=text
        )
        
        # 3. Find Handler
        # Logic: Iterate through modules, first one that says 'True' wins.
        # Fallback should always be the last module (e.g., Generic RAG or Catch-all)
        
        selected_module = None
        for module in self.modules:
            if module.can_handle(context):
                selected_module = module
                break
                
        # 4. Process and Respond
        if selected_module:
            response_text = selected_module.process(context)
        else:
            response_text = "I'm sorry, I didn't understand that. Could you rephrase?"
            
        # 5. Save Bot Response
        self.repository.save_message(user_id, response_text, sender_type="bot")
            
        return response_text
