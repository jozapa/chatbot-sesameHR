from langgraph.checkpoint.memory import MemorySaver


class MemoryService:
    """
    Manages memory operations and configurations.

    Provides functionalities for handling memory saving and configurable
    settings. Encapsulates logic for memory management and storing/retrieving
    memory-related configuration options for specific use cases.
    """

    def __init__(self):
        """
        Initializes the MemoryService with a memory saver instance and default configuration.
        """
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "1"}}
