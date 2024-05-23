import datetime
import os
import pandas as pd

def store_error(process_number, author_name):

    directory_name = 'relatorios_erro'
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    directory = desktop_path + '/' + directory_name

    
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, f"relatorio_erro_{datetime.now().strftime('%d%m%Y')}.xlsx")
    
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        new_df = pd.DataFrame({'Numero do processo': [process_number]})
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = pd.DataFrame({'Numero do processo': [process_number],'Nome Autor': [author_name]})
    
    updated_df.to_excel(filename, index=False)


def store_success(process_number, author_name):

    directory_name = 'relatorio_cadastrados'
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    directory = desktop_path + '/' + directory_name

    
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, f"cadastrados_{datetime.now().strftime('%d%m%Y')}.xlsx")
    
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        new_df = pd.DataFrame({'Numero do processo': [process_number]})
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = pd.DataFrame({'Numero do processo': [process_number],'Nome Autor': [author_name]})
    
    updated_df.to_excel(filename, index=False)