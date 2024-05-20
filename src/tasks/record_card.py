import datetime
import pandas as pd
import pyperclip
from exceptions.data_filling_error import DataFillingError
from utils.functions import click_and_fill


class RecordCard:
    def __init__(self, row):
        self.row = row

    def execute(self):
        try:
            click_and_fill('selecionar_grupo_cliente', self.row['GRUPO DO CLIENTE']) 
            if not(pd.isna(self.row['CLIENTE VITAL'])): 
                if(self.row['CLIENTE VITAL'] == 'SIM'):
                    click_and_fill('check_cliente_vital') 

            click_and_fill('selecionar_projeto', self.row['PROJETO']) 
            click_and_fill('inserir_bairro_do_fato', self.row['BAIRRO DO FATO'])

            if not(pd.isna(self.row['HOUVE CORTE']) or self.row['HOUVE CORTE'] == 'SIM'):
                click_and_fill('houve_corte') 

            date_str = str(self.row['DATA INICIAL DO FATO'])
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%d/%m/%Y')

            pyperclip.copy(str(formatted_date))
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

            if not(pd.isna(self.row['TENTATIVAS DE CONTATO'])): 
                pyperclip.copy(str(self.row['TENTATIVAS DE CONTATO']))
                click_and_fill('check_autor_contatou_a_empresa')
                click_and_fill('numero_tentativas_de_contato', command='doubleClick')
                click_and_fill('numero_tentativas_de_contato', command='rightClick') 
                click_and_fill('colar_tentativas_de_contato')

            if not(pd.isna(self.row['SOLICITADO DANO MORAL'])):
                click_and_fill('inserir_valor_dano_moral', str(self.row['SOLICITADO DANO MORAL']))

            if not(pd.isna(self.row['SOLICITADO DANO MATERIAL'])):
                click_and_fill('inserir_valor_dano_material', str(self.row['SOLICITADO DANO MATERIAL']))
            
            click_and_fill('selecionar_observacao')
            click_and_fill('inserir_observacao', self.row['OBSERVACOES'])
            click_and_fill('ok_observacao')

            click_and_fill('ok_ficha', delay_after=20)
            
        except Exception as e:
            #click_and_fill('fechar_ficha', delay_after=10)
            raise DataFillingError(f'Nao foi possivel preencher a ficha do processo. Erro: {e}')