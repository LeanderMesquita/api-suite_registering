import datetime
import pandas as pd
import pyperclip
from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill
from utils.functions.format_date import format_date
from utils.logger.logger import log

class RecordCard(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self):
        log.info('Starting the record card register')
        try:
            log.debug('Filling the client group')
            click_and_fill('selecionar_grupo_cliente', self.row['GRUPO DO CLIENTE'])
            log.debug('Checking if the client is "VITAL"')  
            if(self.row['CLIENTE VITAL'] == 'SIM'):
                log.debug('Selecting vital client')
                click_and_fill('check_cliente_vital') 
            log.debug('Selecting the project')
            click_and_fill('selecionar_projeto', self.row['PROJETO']) 
            log.debug('Filling the neighborhood')
            click_and_fill('inserir_bairro_do_fato', self.row['BAIRRO DO FATO'])
            if not(pd.isna(self.row['HOUVE CORTE']) or self.row['HOUVE CORTE'] == 'SIM'):
                log.debug('Checking if had energy cut')
                click_and_fill('houve_corte') 
            log.debug('Formatting the initial fact date')
            initial_fact_date = format_date(self.row['DATA INICIAL DO FATO'])
            log.debug('Copying the initial fact date')
            pyperclip.copy(initial_fact_date)
            log.debug('Pasting the date')
            click_and_fill('inserir_data_do_fato_inicial', command='rightClick')
            click_and_fill('colar_data_fato_inicial')
            log.debug('Filling the fact city')
            click_and_fill('inserir_municipio_do_fato', self.row['MUNICIPIO DO FATO']) 
            log.debug('Filling the specific object')
            click_and_fill('selecionar_objeto_especifico', self.row['OBJETO ESPECIFICO'], delay_before=1)
            click_and_fill('selecionar_segundo_objeto_objeto_especifico', self.row['OBJETO ESPECIFICO'])
            log.debug('Selecting the general object')
            click_and_fill('objeto_geral_civel')
            click_and_fill('selecionar_geral_civel')
            log.debug('Selecting the object board')
            click_and_fill('objeto_diretoria_civel')  
            click_and_fill('selecionar_diretoria_civel')
            log.debug('Filling the process origin')
            click_and_fill('selecionar_origem', self.row['ORIGEM DO PROCESSO']) 
            click_and_fill('clickar_fora')
            log.debug('Filling the object complement')
            click_and_fill('selecionar_complemento', self.row['COMPLEMENTO']) 
            click_and_fill('clickar_fora')

            if not(pd.isna(self.row['TENTATIVAS DE CONTATO'])): 
                log.debug('Copying the contact attempts')
                pyperclip.copy(str(self.row['TENTATIVAS DE CONTATO']))
                log.debug('selecting that the author tried to contact')
                click_and_fill('check_autor_contatou_a_empresa')
                log.debug('Pasting the attempts number')
                click_and_fill('numero_tentativas_de_contato', command='doubleClick')
                click_and_fill('numero_tentativas_de_contato', command='rightClick') 
                click_and_fill('colar_tentativas_de_contato')

            if not(pd.isna(self.row['SOLICITADO DANO MORAL'])):
                log.debug('Filling the moral damage value')
                click_and_fill('inserir_valor_dano_moral', str(self.row['SOLICITADO DANO MORAL']))

            if not(pd.isna(self.row['SOLICITADO DANO MATERIAL'])):
                log.debug('Filling the materal damage value')
                click_and_fill('inserir_valor_dano_material', str(self.row['SOLICITADO DANO MATERIAL']))
            
            log.debug('Inserting the observation')
            click_and_fill('selecionar_observacao')
            click_and_fill('inserir_observacao', self.row['OBSERVACOES'])
            click_and_fill('ok_observacao')

            click_and_fill('ok_ficha', delay_after=20)
            log.success('Record card registered successfully!')
        except Exception as e:
            log.error(f'Error during the record card registering. Error: {e}')
            #click_and_fill('fechar_ficha', delay_after=10)
            raise DataFillingError(f'Nao foi possivel preencher a ficha do processo. Erro: {e}')