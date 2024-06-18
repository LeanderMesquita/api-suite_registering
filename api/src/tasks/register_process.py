from api.src.exceptions.data_filling_error import DataFillingError
from api.src.tasks.base_task import BaseTask
from api.src.tasks.subjects import Author, Defendant, Lawyer, RelatedProfessionals
from api.src.tasks.essential_data import EssentialData
from api.src.tasks.record_card import RecordCard
from api.src.tasks.schedule import TermSchedule, HearingSchedule, TutelageSchedule
from api.src.utils.functions.click_and_fill import click_and_fill

import pandas as pd

from api.src.utils.screens.screen_analyzer import ScreenAnalyzer

class RegisterProcess(BaseTask):
    def __init__(self, row):
        super().__init__(row)
        self.defendant = Defendant(row)
        self.author = Author(row)
        self.lawyer = Lawyer(row)
        self.essential_data = EssentialData(row)
        self.professionals = RelatedProfessionals(row)
        self.record_card = RecordCard(row)
        self.term = TermSchedule(row)
        self.hearing = HearingSchedule(row)
        self.tutelage = TutelageSchedule(row)
        self.screen = ScreenAnalyzer()
    def execute(self):
        try:
            self.screen.validate_image('initial_register_screen_validator')
            click_and_fill('novo_processo')
            self.defendant.execute()
            self.author.execute()
            self.lawyer.execute()
            click_and_fill('ok_sujeitos')
            click_and_fill('aceitar_posicao_arquivo')
            self.essential_data.execute()
            self.professionals.execute()
            click_and_fill('salvar_processo', delay_before=1)
            click_and_fill('aceitar_processo')
            self.record_card.execute()
            self.screen.validate_image('initiate_schedule_validator')
            click_and_fill('selecionar_agenda')
            self.term.execute()
            if not (pd.isna(self.row['DATA AUDIENCIA'])):
                self.hearing.execute()
            if not (pd.isna(self.row['DATA TUTELA'])):
                self.tutelage.execute()
            click_and_fill('encerrar_processo')
        except Exception as e:
            raise DataFillingError(f'An error ocurred during full registration {e}')