import pyautogui as pya
import pyperclip

from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill

class EssentialData(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self):
        try:
            click_and_fill('botao_do_contrato')
            pyperclip.copy(self.row['VALOR'])
            click_and_fill('valor_da_causa', command='rightClick')#, value=str(self.row['VALOR'])
            click_and_fill('colar_valor')
            click_and_fill('estado_processo', 'INICIAL')
            click_and_fill('operacao', 'ANDAMENTO')
            
            click_and_fill('agregado', self.row['AGREGADO'])
            click_and_fill('operacao', 'ANDAMENTO')
            click_and_fill('detalhe', self.row['DETALHE'])
            click_and_fill('serie', self.row['SERIE'])
            click_and_fill('hashtag', self.row['HASHTAG'])

            click_and_fill('dados_registro')
            click_and_fill('numero_processo', self.row['NUMERO DO PROCESSO'])
            pya.press('tab')
            click_and_fill('adicionar_vara', delay_before=2)
            click_and_fill('inserir_vara', value=self.row['VARA'])
            click_and_fill('selecionar_vara', command='doubleClick')
        except: 
            click_and_fill('anular_dados_iniciais')
            raise DataFillingError(f'Nao foi possivel preencher os dados essenciais.')