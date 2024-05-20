import pyautogui as pya
import pandas as pd
from exceptions.data_filling_error import DataFillingError
from utils.functions import click_and_fill

class Subject:
    def __init__(self, row):
        self.row = row

    def execute(self):
        raise NotImplementedError('Subclasses must implements the execute method.')
    


class Defendant(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        try:
            click_and_fill('titular', value=self.row['TITULAR'], delay_before=2) 
            click_and_fill('tipo_processo', value=self.row['TIPO PROCESSO']) 

            pya.click(x=1000, y=608, clicks=3, interval=0.5) ##accept tipo_processo

            click_and_fill('papel_parte', delay_before=2) 
            click_and_fill('selecionar_reu')
            click_and_fill('subsidiaria', value=self.row['SUBSIDIARIA'], delay_before=2) 

        except: 
            click_and_fill('anular_reu')
            raise DataFillingError(f'Nao foi possivel adicionar o reu.')
        

class Author(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        try:
            click_and_fill('acrescentar_contraparte')
            click_and_fill('novo_autor')

            if not(pd.isna(self.row['CODIGO PESSOA'])): 
                click_and_fill('codigo_pessoa', str(self.row['CODIGO PESSOA']))
            
            click_and_fill('nome', self.row['AUTOR'])
            click_and_fill('endereco', self.row['ENDERECO'])
            
            if not(pd.isna(self.row['CEP'])):
                click_and_fill('cep', str(self.row['CEP']))
             
            click_and_fill('cidade', self.row['CIDADE']) 
            
            click_and_fill('tipo_pessoa')

            if not(pd.isna(self.row['CNPJ'])):
                click_and_fill('pessoa_juridica') 
                click_and_fill('cnpj', str(self.row['CNPJ']))
            elif not(pd.isna(self.row['CPF'])):    
                click_and_fill('pessoa_fisica')
                click_and_fill('sexo', self.row['SEXO'])
                click_and_fill('cpf', str(self.row['CPF']))

            click_and_fill('ok_pessoa')
            click_and_fill('aceitar_existente')
            click_and_fill('confirmar_existente')
            click_and_fill('ok_contraparte')
            click_and_fill('tipo_processual_autor', command='doubleClick')
            click_and_fill('selecionar_tipo_autor')

        except:
            click_and_fill('anular_novo_autor')
            click_and_fill('anular_contraparte')
            click_and_fill('anular_reu')
            raise DataFillingError(f'Nao foi possivel cadastrar o autor.')

class Lawyer(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        try: 
            click_and_fill('acrescentar_contraparte')
            click_and_fill('visualizacao_completa')

            if not (pd.isna(self.row['OAB ADVOGADO'])):
                click_and_fill('busca_oab_advogado', str(self.row['OAB ADVOGADO']))       
            else:
                click_and_fill('busca_oab_advogado', 'SEM ADVOGADO')

            click_and_fill('click_busca', delay_after=5)
            click_and_fill('seleciona_advogado', command='doubleClick')

            click_and_fill('tipo_advogado', 'Adv. contraparte', command='doubleClick')
            click_and_fill('adv_contraparte')    
            click_and_fill('tipo_processual_adv', command='doubleClick')
            click_and_fill('adv_autor')
            
        except:
            click_and_fill('anular_contraparte')
            click_and_fill('anular_reu')
            raise DataFillingError(f'Erro no cadastro de advogado')