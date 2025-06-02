from .ai_task_extractor import extract_task_from_message
from .strategy_interface import TaskExtractionStrategy

class GeminiExtractionStrategy(TaskExtractionStrategy):
    def extract(self, message: str) -> dict:
        return extract_task_from_message(message)
