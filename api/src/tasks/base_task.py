class BaseTask:
    def __init__(self, row):
        self.row = row

    def execute(self):
        raise NotImplementedError('Subclasses must implements the execute method.')