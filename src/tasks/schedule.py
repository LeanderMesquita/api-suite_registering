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
        log.info('Starting the TermSchedule registering')
        try:
            log.debug('Openning schedule')
            click_and_fill('abrir_agenda', command='rightClick')
            log.debug('Selecting new schedule')
            click_and_fill('nova_agenda')
            log.debug('Selecting the term schedule type')
            click_and_fill('novo_prazo', delay_after=6)
            robot_response = decapitalize_letters(self.row['RECEBIDO POR ROBO'])

            log.info('Registering the distribuition schedule')
            distribuition_date = format_date(self.row['DATA DISTRIBUICAO'])
            pyperclip.copy(distribuition_date)
            log.debug('Selecting the date field')
            click_and_fill('selecionar_data', command='rightClick')
            log.debug('Pasting the distribuition date')
            click_and_fill('colar_data')
            log.debug('Filling the distribuition description')
            click_and_fill('alterar_descricao', value='DATA DE DISTRIBUICAO')
            log.debug('Selecting another note')
            click_and_fill('selecionar_outra_nota')
            log.debug('Accepting the schedule note')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento')
            
            if(robot_response != 'sim'):
                log.info('Registering the quote schedule')
                quote_date = format_date(self.row['DATA CITACAO'])
                pyperclip.copy(quote_date)
                log.debug('Selecting the date field')
                click_and_fill('selecionar_data', command='rightClick')
                log.debug('Pasting the quote date')
                click_and_fill('colar_data')
                log.debug('Inserting the quote time')
                click_and_fill('inserir_horario', str(self.row['HORARIO CITACAO']))
                log.debug('Filling the quote description')
                click_and_fill('alterar_descricao', value='DATA DE CITACAO')
                log.debug('Selecting another note')
                click_and_fill('selecionar_outra_nota')
                log.debug('Accepting the schedule note')
                click_and_fill('aceitar_outra_nota', delay_after=5)
                click_and_fill('ok_data_cumprimento')

            log.info('Registering the receipt schedule')
            receipt_date = format_date(self.row['DATA RECEBIMENTO'])
            pyperclip.copy(receipt_date)
            log.debug('Selecting the date field')
            click_and_fill('selecionar_data', command='rightClick')
            log.debug('Pasting the receipt date')
            click_and_fill('colar_data')
            log.debug('Inserting the receipt time')
            click_and_fill('inserir_horario', str(self.row['HORARIO RECEBIMENTO']))
            receipt_description = 'DATA DE RECEBIMENTO NO BACKOFFICE - VIA TRATAMENTO CONSOLIDADO CAPTURAS' if (robot_response == 'sim') else 'DATA DE RECEBIMENTO NO BACKOFFICE'
            log.debug('Filling the receipt description')
            click_and_fill('alterar_descricao', value=receipt_description)
            log.debug('Saving Schedule')
            click_and_fill('ok_agenda')
            log.debug('Accepting the schedule note')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento', delay_after=20)

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
            log.debug('Openning schedule')
            click_and_fill('abrir_agenda', command='rightClick')
            log.debug('Selecting new schedule')
            click_and_fill('nova_agenda')
            log.debug('Selecting the hearing schedule type')
            click_and_fill('nova_audiencia', delay_after=6)
            hearing_date = format_date(self.row['DATA AUDIENCIA'])
            pyperclip.copy(hearing_date)
            log.debug('Selecting the date field')
            click_and_fill('selecionar_data', command='rightClick')
            log.debug('Pasting the hearing date')
            click_and_fill('colar_data')
            log.debug('Inserting the hearing time')
            click_and_fill('inserir_horario', str(self.row['HORARIO AUDIENCIA']))
            log.debug('Filling the hearing description')
            click_and_fill('alterar_descricao', value='CONCILIACAO')
            log.debug('Saving schedule')
            click_and_fill('ok_agenda')
            log.debug('Accepting the schedule note')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento', delay_after=10)
            log.success('Hearing schedule registered successfully!')
        except Exception as e:
            log.error(f'Error during the hearing schedule registering: {e}')
            raise DataFillingError(f'Error in Hearing schedule registering: {e}')
    
class TutelageSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        try:
            log.debug('Openning schedule')
            click_and_fill('abrir_agenda', command='rightClick')
            log.debug('Selecting new schedule')
            click_and_fill('nova_agenda')
            log.debug('Selecting the decision schedule type')
            click_and_fill('nova_decisao', delay_after=6)
            tutelage_date = format_date(self.row['DATA TUTELA'])
            pyperclip.copy(tutelage_date)
            log.debug('Selecting the date field')
            click_and_fill('selecionar_data', command='rightClick')
            log.debug('Pasting the tutelage date')
            click_and_fill('colar_data')
            log.debug('Filling the tutelage description')
            click_and_fill('alterar_descricao', value='TUTELA - '+self.row['DESCRICAO TUTELA'])
            log.debug('Saving schedule')
            click_and_fill('ok_agenda')
            log.debug('Accepting the schedule note')
            click_and_fill('aceitar_outra_nota', delay_after=5)
            click_and_fill('ok_data_cumprimento', delay_after=10)
            log.success('Tutelage schedule registered successfully!')
        except Exception as e:
            log.error(f'Error during tutelage schedule registering: {e}')
            raise DataFillingError(f'Error during TutelageSchedule registering: {e}')