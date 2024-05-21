from tasks.subjects import Subject, Defendant, Author, Lawyer, RelatedProfessionals
from tasks.essential_data import EssentialData
from tasks.record_card import RecordCard
from tasks.schedule import Schedule
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
        elif task_type == 'schedule':
            return Schedule(row)
        elif task_type == 'register_process':
            return RegisterProcess(row)
        else:
            raise ValueError(f'Unknown task type: {task_type}')
