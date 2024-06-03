import pyperclip
from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill
from utils.functions.decapitalize_letters import decapitalize_letters
from utils.functions.format_date import format_date
from utils.logger.logger import log

class Schedule(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self):
        raise NotImplementedError('Subclasses must implements the execute method.')

class TermSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)
 
    def execute(self):
        try:
            click_and_fill('abrir_agenda', command='rightClick')
            click_and_fill('nova_agenda')
            click_and_fill('novo_prazo', delay_after=6)
            robot_response = decapitalize_letters(self.row['RECEBIDO POR ROBO'])

            distribuition_date = format_date(self.row['DATA DISTRIBUICAO'])
            pyperclip.copy(distribuition_date)
            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('alterar_descricao', value='DATA DE DISTRIBUICAO')
            click_and_fill('selecionar_outra_nota')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento')
            
            if(robot_response != 'sim'):

                quote_date = format_date(self.row['DATA CITACAO'])
                pyperclip.copy(quote_date)
                click_and_fill('selecionar_data', command='rightClick')
                click_and_fill('colar_data')
                click_and_fill('inserir_horario', str(self.row['HORARIO CITACAO']))
                click_and_fill('alterar_descricao', value='DATA DE CITACAO')
                click_and_fill('selecionar_outra_nota')
                click_and_fill('aceitar_outra_nota', delay_after=5)
                click_and_fill('ok_data_cumprimento')

            receipt_date = format_date(self.row['DATA RECEBIMENTO'])
            pyperclip.copy(receipt_date)
            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('inserir_horario', str(self.row['HORARIO RECEBIMENTO']))
            receipt_description = 'DATA DE RECEBIMENTO NO BACKOFFICE - VIA TRATAMENTO CONSOLIDADO CAPTURAS' if (robot_response == 'sim') else 'DATA DE RECEBIMENTO NO BACKOFFICE'
            click_and_fill('alterar_descricao', value=receipt_description)
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento', delay_after=20)
            
        except Exception as e:
            raise DataFillingError(f'Error in TermSchedule registring: {e}')
        


    
class HearingSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        try:
            click_and_fill('abrir_agenda', command='rightClick')
            click_and_fill('nova_agenda')
            click_and_fill('nova_audiencia', delay_after=6)
            hearing_date = format_date(self.row['DATA AUDIENCIA'])
            pyperclip.copy(hearing_date)
            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('inserir_horario', str(self.row['HORARIO AUDIENCIA']))
            click_and_fill('alterar_descricao', value='CONCILIACAO')
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento', delay_after=10)
        except Exception as e:
            raise DataFillingError(f'Error in HearingSchedule registering: {e}')
    
class TutelageSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        try:
            click_and_fill('abrir_agenda', command='rightClick')
            click_and_fill('nova_agenda')
            click_and_fill('nova_decisao', delay_after=6)
            tutelage_date = format_date(self.row['DATA TUTELA'])
            pyperclip.copy(tutelage_date)
            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('alterar_descricao', value='TUTELA - '+self.row['DESCRICAO TUTELA'])
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento', delay_after=10)
        except Exception as e:
            raise DataFillingError(f'Error during TutelageSchedule registering: {e}')