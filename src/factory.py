from tasks.subjects import Defendant, Author, Lawyer, RelatedProfessionals
from tasks.essential_data import EssentialData
from tasks.record_card import RecordCard
from tasks.schedule import TermSchedule, HearingSchedule, TutelageSchedule
from tasks.register_process import RegisterProcess

class TaskFactory:
    @staticmethod
    def create_task(task_type, row):
        if task_type == 'defendant':
            return Defendant(row)
        elif task_type == 'author':
            return Author(row)
        elif task_type == 'lawyer':
            return Lawyer(row)
        elif task_type == 'essential_data':
            return EssentialData(row)
        elif task_type == 'related_professionals':
            return RelatedProfessionals(row)
        elif task_type == 'record_card':
            return RecordCard(row)
        elif task_type == 'term_schedule':
            return TermSchedule(row)
        elif task_type == 'hearing_schedule':
            return HearingSchedule(row)
        elif task_type == 'tutelage_schedule':
            return TutelageSchedule(row)
        elif task_type == 'register_process':
            return RegisterProcess(row)
        else:
            raise ValueError(f'Unknown task type: {task_type}')
