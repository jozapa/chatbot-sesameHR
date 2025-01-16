from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
class MemoryService:

    def __init__ (self):
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "1"}}
    

    
