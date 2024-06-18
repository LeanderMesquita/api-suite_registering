import pyautogui as pya
from time import sleep
from api.src.utils.constants.index import POSITION_PATH
from api.src.utils.logger.logger import log
def click_and_fill(position_name, value:str =None, delay_before: float = 0, delay_after: float = 0.75, command:str='click', interval:float = 0, num_clicks:int = 1):
    x, y = POSITION_PATH[position_name]

    if delay_before > 0:
        sleep(delay_before)

    try:
        action_function = getattr(pya, command)
        if command == 'doubleClick':  action_function(x, y)
        else: action_function(x, y, num_clicks, interval)
        log.debug(f'Clicking at {position_name} ({x}, {y})')
        if value is not None:
            sleep(0.5)
            log.debug(f'Writing: {value}')
            pya.write(value)
            sleep(1)

    except:
        raise pya.FailSafeException
    
    if delay_after > 0:
        sleep(delay_after)