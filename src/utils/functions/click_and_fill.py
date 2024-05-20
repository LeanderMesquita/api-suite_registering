import pyautogui as pya
from time import sleep
from utils.constants.index import POSITION_PATH

async def click_and_fill(position_name, value:str =None, delay_before: int = 0, delay_after: int = 2, command:str='click'):
    x, y = POSITION_PATH[position_name]

    if delay_before > 0:
        sleep(delay_before)

    try:
        action_function = getattr(pya, command)
        action_function(x, y)
        
        sleep(1)
        if value is not None:
            pya.write(value)

    except:
        raise pya.FailSafeException
    
    if delay_after > 0:
        sleep(delay_after)