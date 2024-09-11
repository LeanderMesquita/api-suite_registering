import pyperclip

from api.src.exceptions.data_filling_error import DataFillingError
from api.src.tasks.base_task import BaseTask
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.logger.logger import log
from api.src.utils.screens.screen_analyzer import ScreenAnalyzer
from api.src.utils.functions.format_date import format_date


class Schedule(BaseTask):
    def __init__(self, row):
        self.row = row
        self.screen = ScreenAnalyzer()
        
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
            click_and_fill('novo_prazo')
            
            
            log.info('Registering the distribuition schedule')
            self.screen.validate_image('inside_schedule_validator')
            distribuition_date = format_date(self.row['DATA DISTRIBUICAO'])
            pyperclip.copy(distribuition_date)

            click_and_fill('adicionar_tipo_nota')
            self.screen.validate_image('inside_note_validator')
            click_and_fill('filtrar_tipo_nota', 'DATA DE DISTRIBUI') 
            click_and_fill('selecionar_nota')
            click_and_fill('aceitar_descricao')
            click_and_fill('ok_nota')

            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('selecionar_outra_nota')
            click_and_fill('aceitar_outra_nota')
            click_and_fill('aceitar_feriado')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')

            robot_response = self.row['RECEBIDO POR ROBO'].lower()
            if(robot_response != 'sim'):

                log.info('Registering the quote schedule')
                self.screen.validate_image('inside_schedule_validator')
                quote_date = format_date(self.row['DATA CITACAO'])
                pyperclip.copy(quote_date)
                
                click_and_fill('adicionar_tipo_nota')
                self.screen.validate_image('inside_note_validator')
                click_and_fill('filtrar_tipo_nota', 'DATA DE CITA') 
                click_and_fill('selecionar_nota')
                click_and_fill('aceitar_descricao')
                click_and_fill('ok_nota')
                
                click_and_fill('selecionar_data', command='rightClick')
                click_and_fill('colar_data')
                click_and_fill('inserir_horario', str(self.row['HORARIO CITACAO']))
                click_and_fill('selecionar_outra_nota')
                click_and_fill('aceitar_outra_nota')
                click_and_fill('aceitar_feriado')
                if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                    click_and_fill('ok_data_cumprimento')

            log.info('Registering the receipt schedule')
            self.screen.validate_image('inside_schedule_validator')
            receipt_date = format_date(self.row['DATA RECEBIMENTO'])
            pyperclip.copy(receipt_date)
            
            click_and_fill('adicionar_tipo_nota')
            self.screen.validate_image('inside_note_validator')
            click_and_fill('filtrar_tipo_nota', 'DATA DE RECEBIMENTO NO BACKOFFICE') 
            click_and_fill('selecionar_nota')
            click_and_fill('aceitar_descricao')
            click_and_fill('ok_nota')
            
            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('inserir_horario', str(self.row['HORARIO RECEBIMENTO']))
            if robot_response == 'sim':
                receipt_description = ' - VIA TRATAMENTO CONSOLIDADO CAPTURAS' 
                click_and_fill('alterar_descricao', value=receipt_description)
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota')
            click_and_fill('aceitar_feriado')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')

            log.success('TermSchedule registered successfully!')
            
        except Exception as e:
            log.error('Error during term schedule registering...')
            click_and_fill('anular_agenda')
            click_and_fill('confirmar_anulamento_agenda', delay_before=1)
            click_and_fill('encerrar_processo')
            raise DataFillingError(f'Error in term schedule registring: {e}')
        


    
class HearingSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Starting the Hearing Schedule registering')
        try:
            self.screen.validate_image('registered_schedule_validator')
            click_and_fill('abrir_agenda', command='rightClick')
            click_and_fill('nova_agenda')
            click_and_fill('nova_audiencia')
            self.screen.validate_image('inside_schedule_validator')
            hearing_date = format_date(self.row['DATA AUDIENCIA'])
            pyperclip.copy(hearing_date)

            click_and_fill('adicionar_tipo_nota')
            self.screen.validate_image('inside_note_validator')
            click_and_fill('filtrar_tipo_nota', 'CONCILIACAO') 
            click_and_fill('selecionar_nota_conciliacao')
            click_and_fill('aceitar_descricao')
            click_and_fill('ok_nota')

            click_and_fill('selecionar_data', command='rightClick')
            click_and_fill('colar_data')
            click_and_fill('inserir_horario', str(self.row['HORARIO AUDIENCIA']))
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota')
            click_and_fill('aceitar_feriado')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')
            log.success('Hearing schedule registered successfully!')

        except Exception as e:
            log.error(f'Error during the hearing schedule registering: {e}')
            click_and_fill('anular_agenda')
            click_and_fill('confirmar_anulamento_agenda', delay_before=1)
            click_and_fill('encerrar_processo')
            raise DataFillingError(f'Error in Hearing schedule registering: {e}')
    
class TutelageSchedule(Schedule):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        try:
            self.screen.validate_image('registered_schedule_validator')
            click_and_fill('abrir_agenda', command='rightClick')
            click_and_fill('nova_agenda')
            click_and_fill('nova_decisao')
            self.screen.validate_image('inside_schedule_validator')
            tutelage_date = format_date(self.row['DATA TUTELA'])
            pyperclip.copy(tutelage_date)

            click_and_fill('adicionar_tipo_nota_decisao')
            self.screen.validate_image('inside_note_validator')
            click_and_fill('filtrar_tipo_nota', 'TUTELA') 
            click_and_fill('selecionar_nota')
            click_and_fill('aceitar_descricao')
            click_and_fill('ok_nota')

            click_and_fill('selecionar_data_decisao', command='rightClick')
            click_and_fill('colar_data_decisao')
            click_and_fill('alterar_descricao', value=f' - {self.row['DESCRICAO TUTELA']}')
            click_and_fill('ok_agenda')
            click_and_fill('aceitar_outra_nota')
            click_and_fill('aceitar_feriado')
            if(self.screen.check_if_exist_image('fullfillment_validator', tryes=5)):
                click_and_fill('ok_data_cumprimento')
            log.success('Tutelage schedule registered successfully!')

        except Exception as e:
            log.error(f'Error during tutelage schedule registering: {e}')
            click_and_fill('anular_agenda')
            click_and_fill('confirmar_anulamento_agenda', delay_before=1)
            click_and_fill('encerrar_processo')
            raise DataFillingError(f'Error during TutelageSchedule registering: {e}')