from tasks.base_task import BaseTask


class Schedule(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self):
        return super().execute()
    

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