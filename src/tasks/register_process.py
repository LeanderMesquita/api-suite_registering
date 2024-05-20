from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from tasks.subjects import Author, Defendant, Lawyer, RelatedProfessionals, Subjects
from tasks.essential_data import EssentialData
from tasks.record_card import RecordCard
from tasks.schedule import Schedule
from utils.functions import click_and_fill

class RegisterProcess(BaseTask):
    def __init__(self, row):
        super().__init__(row)
        self.defendant = Defendant(row)
        self.author = Author(row)
        self.lawyer = Lawyer(row)
        self.essential_data = EssentialData(row)
        self.professionals = RelatedProfessionals(row)
        self.record_card = RecordCard(row)
        self.agenda = Schedule(row)

    def execute(self):
        try:
            self.defendant.execute()
            self.author.execute()
            self.lawyer.execute()
            click_and_fill('ok_sujeitos')
            click_and_fill('aceitar_posicao_arquivo', delay_after=6)
            self.essential_data.execute()
            self.professionals.execute()
            click_and_fill('salvar_processo')
            click_and_fill('aceitar_processo', delay_after=15)
            self.record_card.execute()
            click_and_fill('selecionar_agenda', delay_after=8)
            self.schedule.execute()
        except Exception as e:
            raise DataFillingError(f'An error ocurred in main process {e}')