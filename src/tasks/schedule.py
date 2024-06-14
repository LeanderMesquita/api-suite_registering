import pyperclip
from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill
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
        log.info('Starting the TermSchedule registering')
        try:
            self.screen.validate_image('schedule_screen_validator')
            click_and_fill('abrir_agenda', command='rightClick')
            click_and_fill('nova_agenda')
            click_and_fill('novo_prazo', delay_after=6)
            robot_response = self.row['RECEBIDO POR ROBO'].lower()
            log.info('Registering the distribuition schedule')
            distribuition_date = format_date(self.row['DATA DISTRIBUICAO'])
            pyperclip.copy(distribuition_date)
            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('alterar_descricao', value='DATA DE DISTRIBUICAO')
            click_and_fill('selecionar_outra_nota')
            click_and_fill('aceitar_outra_nota')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')
            
            if(robot_response != 'sim'):

                log.info('Registering the quote schedule')
                quote_date = format_date(self.row['DATA CITACAO'])
                pyperclip.copy(quote_date)
                click_and_fill('selecionar_data', command='rightClick')
                click_and_fill('colar_data')
                click_and_fill('inserir_horario', str(self.row['HORARIO CITACAO']))
                click_and_fill('alterar_descricao', value='DATA DE CITACAO')
                click_and_fill('selecionar_outra_nota')
                click_and_fill('aceitar_outra_nota')
                if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                    click_and_fill('ok_data_cumprimento')

            log.info('Registering the receipt schedule')
            receipt_date = format_date(self.row['DATA RECEBIMENTO'])
            pyperclip.copy(receipt_date)
            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('inserir_horario', str(self.row['HORARIO RECEBIMENTO']))
            receipt_description = 'DATA DE RECEBIMENTO NO BACKOFFICE - VIA TRATAMENTO CONSOLIDADO CAPTURAS' if (robot_response == 'sim') else 'DATA DE RECEBIMENTO NO BACKOFFICE'
            click_and_fill('alterar_descricao', value=receipt_description)
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')

            log.success('TermSchedule registered successfully!')
            
        except Exception as e:
            log.error('Error during term schedule registering...')
            raise DataFillingError(f'Error in term schedule registring: {e}')
        


    
class HearingSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Starting the Hearing Schedule registering')
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
            click_and_fill('aceitar_outra_nota')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')
            log.success('Hearing schedule registered successfully!')

        except Exception as e:
            log.error(f'Error during the hearing schedule registering: {e}')
            raise DataFillingError(f'Error in Hearing schedule registering: {e}')
    
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
            click_and_fill('selecionar_data_decisao', command='rightClick')
            click_and_fill('colar_data_decisao')
            click_and_fill('alterar_descricao', value='TUTELA - '+self.row['DESCRICAO TUTELA'])
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')
            log.success('Tutelage schedule registered successfully!')

        except Exception as e:
            log.error(f'Error during tutelage schedule registering: {e}')
            raise DataFillingError(f'Error during TutelageSchedule registering: {e}')