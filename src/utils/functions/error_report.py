import os
from openpyxl import load_workbook
import pandas as pd
from datetime import datetime

def log_error(process_number, author_name, error):

    directory_name = 'relatorios_erro'
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    directory = desktop_path + '/' + directory_name

    
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, f"relatorio_erro_{datetime.now().strftime('%d%m%Y')}.xlsx")
    
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        new_df = pd.DataFrame({'Numero do processo': [process_number],'Nome Autor': [author_name], 'ERRO': [error]})
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = pd.DataFrame({'Numero do processo': [process_number],'Nome Autor': [author_name], 'ERRO': [error]})
    
    updated_df.to_excel(filename, index=False)

    # Adjust the column width
    book = load_workbook(filename)
    sheet = book.active

    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column].width = adjusted_width

    book.save(filename)