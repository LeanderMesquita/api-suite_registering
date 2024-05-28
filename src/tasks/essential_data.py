import pyautogui as pya
import pyperclip
from utils.logger.logger import log
from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill

class EssentialData(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self):
        log.info('Iniciating the Essential data registering')
        try:
            log.debug('Checking "No contrato"')
            click_and_fill('botao_do_contrato')
            log.debug('Copying the "VALOR DA CAUSA" value')
            pyperclip.copy(self.row['VALOR'])
            log.debug('Right click in VALOR input')
            click_and_fill('valor_da_causa', command='rightClick')
            log.debug('Pasting')
            click_and_fill('colar_valor')
            log.debug('Filling the process loading state')
            click_and_fill('estado_processo', 'INICIAL')
            log.debug('Filling the process operation')
            click_and_fill('operacao', 'ANDAMENTO')
            log.debug('Filling the "AGREGADO" field')
            click_and_fill('agregado', self.row['AGREGADO'])
            log.debug('Confirming the process operation')
            click_and_fill('operacao', 'ANDAMENTO')
            log.debug('Filling the "DETALHE" field')
            click_and_fill('detalhe', self.row['DETALHE'])
            log.debug('Filling the "SERIE" field')
            click_and_fill('serie', self.row['SERIE'])
            log.debug('Filling the "HASHTAG field"')
            click_and_fill('hashtag', self.row['HASHTAG'])
            log.info('Going to registering data')
            click_and_fill('dados_registro')
            log.debug('Filling the process number')
            click_and_fill('numero_processo', self.row['NUMERO DO PROCESSO'])
            pya.press('tab')
            log.debug('Filling the court')
            click_and_fill('adicionar_vara', delay_before=2)
            click_and_fill('inserir_vara', value=self.row['VARA'])
            log.debug('Selecting the current court')
            click_and_fill('selecionar_vara', command='doubleClick')
            log.success('Essential date registered successfully!')
        except Exception as e: 
            log.error(f"ERROR DURING FILLING THE ESSENTIAL DATA. Error: {e}")
            click_and_fill('anular_dados_iniciais')
            raise DataFillingError(f'Nao foi possivel preencher os dados essenciais.')