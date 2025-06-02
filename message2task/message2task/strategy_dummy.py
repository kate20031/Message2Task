from .strategy_interface import TaskExtractionStrategy

class DummyExtractionStrategy(TaskExtractionStrategy):
    def extract(self, message: str) -> dict:
        return {
            "Title": "Mock Task",
            "Person": "John",
            "Place": "Office",
            "Date": "25.04.25",
            "Time": "14:00",
            "Link": "https://meet.example.com"
        }
