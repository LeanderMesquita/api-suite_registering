from datetime import datetime


def format_date(raw_date) -> str:
    """Any -> str -> datetime -> format -> str"""
    try:
        return str(datetime.strptime(str(raw_date), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y'))
    except ValueError as e:
        raise e
    
