from time import sleep
import pyautogui as pya
import pyperclip

from api.src.exceptions.data_filling_error import DataFillingError
from api.src.tasks.base_task import BaseTask
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.logger.logger import log
from api.src.utils.screens.screen_analyzer import ScreenAnalyzer
from api.src.utils.functions.format_date import format_date

class EssentialData(BaseTask):
    def __init__(self, row):
        self.row = row
        self.screen = ScreenAnalyzer() 

    def select_court(self, court:str):
        log.debug('Filling the court')
        
        court_map = {
            '2 VARA CIVEL': 'select_2_posicao',
            '3 VARA CIVEL': 'select_4_posicao',
            '4 VARA CIVEL': 'select_7_posicao',
            '5 VARA CIVEL': 'select_6_posicao',
            '6 VARA CIVEL': 'select_6_posicao',
            '7 VARA CIVEL': 'select_6_posicao',
            '8 VARA CIVEL': 'select_6_posicao',
            '9 VARA CIVEL': 'select_6_posicao',
            'JUIZADO ESPECIAL CIVEL': 'select_1_posicao',
            'JUSTICA ITINERANTE DE AREAL': 'select_2_posicao',
            '4 UJEC': 'select_3_posicao',
            'JUIZADO ESPECIAL CIVEL E CRIMINAL': 'select_5_posicao'
        }

        court_key = court_map.get(court, None)
        default_p = 'select_1_posicao'
        
        log.debug(f'Court: {court}')
        if court_key:
            if court == 'JUIZADO ESPECIAL CIVEL':
                pya.click(x=1125, y=424)
                sleep(1)
                pya.mouseDown()
                sleep(1)
                pya.moveTo(x=1125, y=514)
                sleep(1)
                pya.mouseUp()
                sleep(1)
                
            return click_and_fill(court_key, command='doubleClick')
        
        return click_and_fill(default_p, command='doubleClick')
        
        
    def execute(self):
        log.info('Iniciating the Essential data registering')
        try:
            self.screen.validate_image('initial_data_validator')
            click_and_fill('botao_do_contrato')
            pyperclip.copy(self.row['VALOR'])
            click_and_fill('valor_da_causa', command='rightClick')
            click_and_fill('colar_valor')
            click_and_fill('estado_processo', 'INSTRUTORIA')
            click_and_fill('operacao', 'ANDAMENTO')
            click_and_fill('agregado', self.row['AGREGADO'])
            click_and_fill('operacao', 'ANDAMENTO')
            click_and_fill('detalhe', self.row['DETALHE'])
            click_and_fill('serie', self.row['SERIE'])
            click_and_fill('hashtag', self.row['HASHTAG'])
            click_and_fill('dados_registro')
            self.screen.validate_image('register_data_validator')
            click_and_fill('numero_processo', self.row['NUMERO DO PROCESSO'])
            pya.press('tab')
            click_and_fill('adicionar_vara')
            self.screen.validate_image('court_validation')
            click_and_fill('inserir_vara', value=self.row['VARA'])
            self.select_court(self.row['VARA'])
            log.success('Essential date registered successfully!')
        except Exception as e: 
            log.error(f"Error during filling essential data. ERROR: {e}")
            click_and_fill('anular_vara', delay_after=2)
            click_and_fill('anular_dados_iniciais')
            raise DataFillingError(f'Error during essential data filling. ERROR: {e}')
            