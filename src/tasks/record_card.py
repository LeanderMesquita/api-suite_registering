import datetime
import pandas as pd
import pyperclip
from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill
from utils.functions.format_date import format_date
from utils.logger.logger import log
from utils.screens.screen_analyzer import ScreenAnalyzer

class RecordCard(BaseTask):
    def __init__(self, row):
        self.row = row
        self.screen = ScreenAnalyzer() 

    def execute(self):
        log.info('Starting the record card register')
        try:
            self.screen.validate_image('record_card_validator')
            click_and_fill('selecionar_grupo_cliente', self.row['GRUPO DO CLIENTE'])

            if(self.row['CLIENTE VITAL'].lower() == 'sim'):
                click_and_fill('check_cliente_vital') 
           
            click_and_fill('selecionar_projeto', self.row['PROJETO']) 
            click_and_fill('inserir_bairro_do_fato', self.row['BAIRRO DO FATO'])

            if (self.row['HOUVE CORTE'].lower() == 'sim'):             
                click_and_fill('houve_corte') 

            initial_fact_date = format_date(self.row['DATA INICIAL DO FATO'])
            pyperclip.copy(initial_fact_date)
           
            click_and_fill('inserir_data_do_fato_inicial', command='rightClick')
            click_and_fill('colar_data_fato_inicial')
            click_and_fill('inserir_municipio_do_fato', self.row['MUNICIPIO DO FATO']) 
            click_and_fill('selecionar_objeto_especifico', self.row['OBJETO ESPECIFICO'], delay_before=1)
            click_and_fill('selecionar_segundo_objeto_objeto_especifico', self.row['OBJETO ESPECIFICO'])
            click_and_fill('objeto_geral_civel')
            click_and_fill('selecionar_geral_civel')
            click_and_fill('objeto_diretoria_civel')  
            click_and_fill('selecionar_diretoria_civel')
            click_and_fill('selecionar_origem', self.row['ORIGEM DO PROCESSO']) 
            click_and_fill('clickar_fora')
            click_and_fill('selecionar_complemento', self.row['COMPLEMENTO']) 
            click_and_fill('clickar_fora')

            if not(pd.isna(self.row['TENTATIVAS DE CONTATO']) or self.row['TENTATIVAS DE CONTATO'] == str(0) or self.row['TENTATIVAS DE CONTATO'] == ''): 
                pyperclip.copy(str(self.row['TENTATIVAS DE CONTATO']))
                click_and_fill('check_autor_contatou_a_empresa')
                click_and_fill('numero_tentativas_de_contato', command='doubleClick')
                click_and_fill('numero_tentativas_de_contato', command='rightClick') 
                click_and_fill('colar_tentativas_de_contato')

            if not(pd.isna(self.row['SOLICITADO DANO MORAL']) or self.row['TENTATIVAS DE CONTATO'] == ''):
                click_and_fill('inserir_valor_dano_moral', str(self.row['SOLICITADO DANO MORAL']))

            if not(pd.isna(self.row['SOLICITADO DANO MATERIAL']) or self.row['TENTATIVAS DE CONTATO'] == ''):    
                click_and_fill('inserir_valor_dano_material', str(self.row['SOLICITADO DANO MATERIAL']))
            
            click_and_fill('selecionar_observacao')
            self.screen.validate_image('observation_validator')
            click_and_fill('inserir_observacao', self.row['OBSERVACOES'])
            click_and_fill('ok_observacao')
            click_and_fill('ok_ficha', delay_after=5)
            click_and_fill('inserir_alterar_elemento', delay_after=5)
            log.success('Record card registered successfully!')
        except Exception as e:
            log.error(f'Error during the record card registering. Error: {e}')
            click_and_fill('fechar_ficha', delay_after=10)
            