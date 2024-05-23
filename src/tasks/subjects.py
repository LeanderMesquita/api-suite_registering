import pyautogui as pya
import pandas as pd
from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill
from utils.logger.logger import log

class Subject(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self):
        return super().execute()
    


class Defendant(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Starting the defendant registering')
        try:
            log.debug('Filling the "TITULAR" field')
            click_and_fill('titular', value=self.row['TITULAR'], delay_before=2) 
            log.debug('Filling the "TIPO PROCESSO" field')
            click_and_fill('tipo_processo', value=self.row['TIPO PROCESSO']) 
            log.debug('Accepting the "TIPO PROCESSO field in system"')
            pya.click(x=1000, y=608, clicks=3, interval=0.5) 
            log.debug('Filling the "PAPEL PARTE" field')
            click_and_fill('papel_parte', delay_before=2) 
            log.debug('Selecting "Réu"')
            click_and_fill('selecionar_reu')
            log.debug('Filling "SUBSIDIARIA" field')
            click_and_fill('subsidiaria', value=self.row['SUBSIDIARIA'], delay_before=2) 
            log.success("Defendant registered!")
        except Exception as e: 
            click_and_fill('anular_reu')
            raise log.error(f"Cannot possible registering the defendant. {e}")
        

class Author(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Starting the author registering')
        try:
            log.debug('Adding counterpart')
            click_and_fill('acrescentar_contraparte')
            log.debug('Adding a new author')
            click_and_fill('novo_autor')

            if not(pd.isna(self.row['CODIGO PESSOA'])):
                log.debug('Filling the "CODIGO PESSOA" input') 
                click_and_fill('codigo_pessoa', str(self.row['CODIGO PESSOA']))
            log.debug('Filling the author name')
            click_and_fill('nome', self.row['AUTOR'])
            log.debug('Filling the author address')
            click_and_fill('endereco', self.row['ENDERECO'])
            
            if not(pd.isna(self.row['CEP'])):
                log.debug('Filling the Author CEP')
                click_and_fill('cep', str(self.row['CEP']))
            log.debug('Filling the author city')
            click_and_fill('cidade', self.row['CIDADE']) 
            
            log.debug('Choosing the person type')
            click_and_fill('tipo_pessoa')

            if not(pd.isna(self.row['CNPJ'])):
                log.debug('Declaring legal entity')
                click_and_fill('pessoa_juridica') 
                log.debug('Filling the author CNPJ')
                click_and_fill('cnpj', str(self.row['CNPJ']))
            elif not(pd.isna(self.row['CPF'])):    
                log.debug('Declaring an individual person')
                click_and_fill('pessoa_fisica')
                log.debug('Affirming the person gender')
                click_and_fill('sexo', self.row['SEXO'])
                log.debug('Filling the author CPF')
                click_and_fill('cpf', str(self.row['CPF']))

            log.debug('Accepting new author register')
            click_and_fill('ok_pessoa')
            log.debug('Accepting existant author')
            click_and_fill('aceitar_existente')
            log.debug('Confirm existent author')
            click_and_fill('confirmar_existente')
            click_and_fill('ok_contraparte')
            log.debug('Claiming as author')
            click_and_fill('tipo_processual_autor', command='doubleClick')
            click_and_fill('selecionar_tipo_autor')
            log.success('Author registered!')
        except Exception as e:
            click_and_fill('anular_novo_autor')
            click_and_fill('anular_contraparte')
            click_and_fill('anular_reu')
            raise log.error(f'Cannot possible registering the current author. {e}')

class Lawyer(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Initiating the lawyer registering')
        try: 
            log.debug('Adding counterpart')
            click_and_fill('acrescentar_contraparte')
            log.debug('Searching by complete visualization')
            click_and_fill('visualizacao_completa')

            if not (pd.isna(self.row['OAB ADVOGADO'])):
                log.debug('Filling the lawyer OAB code')
                click_and_fill('busca_oab_advogado', str(self.row['OAB ADVOGADO']))       
            else:
                log.debug('Filling with the "without lawyer" instruction')
                click_and_fill('busca_oab_advogado', 'SEM ADVOGADO')

            log.debug('Searching')
            click_and_fill('click_busca', delay_after=5)
            log.debug('Selecting the first option')
            click_and_fill('seleciona_advogado', command='doubleClick')
            log.debug('Selecting as a counterpart lawyer')
            click_and_fill('tipo_advogado', 'Adv. contraparte', command='doubleClick')
            click_and_fill('adv_contraparte')
            log.debug('Claiming as a author lawyer')    
            click_and_fill('tipo_processual_adv', command='doubleClick')
            click_and_fill('adv_autor')
            log.success('Lawyer successfull registered!')
            
        except Exception as e:
            click_and_fill('anular_contraparte')
            click_and_fill('anular_reu')
            raise log.error(f'Cannot possible registering the lawyer. {e}')
        
class RelatedProfessionals(Subject):
    def __init__(self, row):
        super().__init__(row)

    def select_office(self, office):
        office_map = {
            'TAUNAY': 'select_taunay',
            'CML ADVOGADOS': 'select_cml',
            'GONDIM': 'select_gondim',
            'URBANO': 'select_urbano',
            'VILLEMOR': 'select_villemor_civel',
            'CLETO GOMES': 'select_cleto_gomes_civel'
        }

        office = office_map.get(office, None)

        if office:
            click_and_fill(office)
        else:
            print("No office defined for this condition.")

    def execute(self):
        try:
            click_and_fill('selecionar_profissionais')
            click_and_fill('selecionar_profissional_responsavel', self.row['RESPONSAVEL'])#ex: 'ENEIDA ZURU' 
            click_and_fill('acrescentar_externo', delay_after=5) 
            click_and_fill('vizualizar_assinados')
            click_and_fill('nominativo', self.row['ESCRITORIO'])#ex: nome do escritorio
            self.select_office(office=self.row['ESCRITORIO'])
            click_and_fill('ok_escritorio_encarregado')
            click_and_fill('ok_detalhe_encarregado')
            click_and_fill('aceitar_valor_incumbencia', delay_after=3)
            click_and_fill('finalizar_profissionais_processo')
        except:
            click_and_fill('anular_detalhe_encarregado')
            click_and_fill('anular_profissional_encarregado')
            click_and_fill('anular_profissionais')
            click_and_fill('anular_dados_iniciais')
            raise DataFillingError(f'Nao foi possivel preencher os profissionais')
    
    
