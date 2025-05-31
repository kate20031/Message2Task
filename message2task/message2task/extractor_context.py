class TaskExtractorContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def extract_task(self, message):
        return self.strategy.extract(message)
