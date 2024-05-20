




class Schedule:
    def __init__(self, row):
        self.row = row

    def execute(self):
        raise NotImplementedError('Subclasses must implements the execute method.')
    

class TermShedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        return super().execute()
    
class HearingSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        return super().execute()
    
class TutelageSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        return super().execute()