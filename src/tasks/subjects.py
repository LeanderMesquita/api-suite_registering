import pyautogui as pya
import pandas as pd
from exceptions.data_filling_error import DataFillingError
from tasks.base_task import BaseTask
from utils.functions.click_and_fill import click_and_fill
from utils.logger.logger import log
from utils.screens.screen_analyzer import ScreenAnalyzer

class Subject(BaseTask):
    def __init__(self, row):
        self.row = row
        self.screen = ScreenAnalyzer()
    def execute(self):
        return super().execute()
    


class Defendant(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Starting the defendant registering')
        try:
            self.screen.validate_image('defendant_validator')
            click_and_fill('titular', value=self.row['TITULAR']) 
            click_and_fill('tipo_processo', value=self.row['TIPO PROCESSO']) 
            pya.click(x=1000, y=608, clicks=3, interval=0.5) 
            click_and_fill('papel_parte') 
            click_and_fill('selecionar_reu')
            click_and_fill('subsidiaria', value=self.row['SUBSIDIARIA']) 
            log.success("Defendant registered!")
        except Exception as e: 
            log.error(f"Cannot possible registering the defendant. {e}")
            click_and_fill('anular_reu')
            
        

class Author(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Starting the author registering')
        try:
            
            click_and_fill('acrescentar_contraparte')
            self.screen.validate_image('new_author')
            click_and_fill('novo_autor')

            self.screen.validate_image('author_validator')
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
            if(self.screen.check_if_exist_image('existent_validator', tryes=5)):
                click_and_fill('confirmar_existente', delay_before=2)
            click_and_fill('ok_contraparte')
            self.screen.validate_image('defendant_validator')
            click_and_fill('tipo_processual_autor', command='doubleClick')
            click_and_fill('selecionar_tipo_autor')
            log.success('Author registered!')
        except Exception as e:
            log.error(f'Cannot possible registering the current author. {e}')
            click_and_fill('anular_novo_autor')
            click_and_fill('anular_contraparte')
            click_and_fill('anular_reu')
          

class Lawyer(Subject):
    def __init__(self, row):
        super().__init__(row)

    def execute(self):
        log.info('Initiating the lawyer registering')
        try: 
            click_and_fill('acrescentar_contraparte')
            self.screen.validate_image('new_author')
            click_and_fill('visualizacao_completa')

            if not (pd.isna(self.row['OAB ADVOGADO'])):
                click_and_fill('busca_oab_advogado', str(self.row['OAB ADVOGADO']))       
            else:               
                click_and_fill('busca_oab_advogado', 'SEM ADVOGADO')

            click_and_fill('click_busca', delay_after=5)
            click_and_fill('seleciona_advogado', command='doubleClick')
            self.screen.validate_image('defendant_validator')
            click_and_fill('tipo_advogado', 'Adv. contraparte', command='doubleClick')
            click_and_fill('adv_contraparte')
            click_and_fill('tipo_processual_adv', command='doubleClick')
            click_and_fill('adv_autor')
            log.success('Lawyer successfull registered!')
            
        except Exception as e:
            log.error(f'Cannot possible registering the lawyer. {e}')
            click_and_fill('anular_contraparte')
            click_and_fill('anular_reu')
           
class RelatedProfessionals(Subject):
    def __init__(self, row):
        super().__init__(row)

    def select_office(self, office):
        log.debug('Selecting office')
        office_map = {
            'TAUNAY': 'select_taunay',
            'CML': 'select_cml',
            'GONDIM': 'select_gondim',
            'URBANO': 'select_urbano',
            'VILLEMOR': 'select_villemor_civel',
            'CLETO GOMES': 'select_cleto_gomes_civel'
        }

        office = office_map.get(office, None)

        if office:
            log.debug(f'Office: {office}')
            click_and_fill(office)
        else:
            log.warning("No office defined for this condition.")

    def execute(self):
        log.info('Starting the related professionals registering')
        try:
            self.screen.validate_image('register_data_validator')
            click_and_fill('selecionar_profissionais')
            self.screen.validate_image('professionals_validation')
            click_and_fill('selecionar_profissional_responsavel', self.row['RESPONSAVEL'])
            click_and_fill('acrescentar_externo')
            self.screen.validate_image('office_validation')
            click_and_fill('vizualizar_assinados')
            click_and_fill('nominativo', self.row['ESCRITORIO'])
            self.select_office(office=self.row['ESCRITORIO'])
            click_and_fill('ok_escritorio_encarregado')
            self.screen.validate_image('in_charge_detail_validation')
            click_and_fill('ok_detalhe_encarregado')
            click_and_fill('aceitar_valor_incumbencia')
            self.screen.validate_image('professionals_validation')
            click_and_fill('finalizar_profissionais_processo')
            log.success('Related professionals successfully registered!')
        except Exception as e:
            log.error(f'Cannot possible registering the related professionals. {e}')
            click_and_fill('anular_detalhe_encarregado')
            click_and_fill('anular_profissional_encarregado')
            click_and_fill('anular_profissionais')
            click_and_fill('anular_dados_iniciais')
            
    
