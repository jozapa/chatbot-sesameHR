from langgraph.checkpoint.memory import MemorySaver


class MemoryService:
    # TODO: Docstrings

    def __init__(self):
        # TODO: Docstrings
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "1"}}
