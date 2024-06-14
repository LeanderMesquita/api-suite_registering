import pyautogui as pya
import numpy as np
import cv2
from utils.constants.index import IMAGE_PATH

class ScreenAnalyzer:
     
    def locate_on_screen(self, template_path, screenshot_path, threshold=0.85):
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            raise ValueError(f"Template not found: {template_path}")
        
        w, h = template.shape[::-1]
        image = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            raise ValueError(f"Image for analysis not found: {screenshot_path}")

        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        points = [(pt[0] + w // 2, pt[1] + h // 2, result[pt[1], pt[0]]) for pt in zip(*loc[::-1])] 

        if points:
            best_point = max(points, key=lambda x: x[2])
            return [(best_point[0], best_point[1])]

        return []

    def validate_image(self, image_alias):
        while True:
            try:
                screenshot = 'src/utils/screens/fullscreen.png'
                pya.screenshot(screenshot)
                image_path = IMAGE_PATH[image_alias]
                if self.locate_on_screen(template_path=image_path, screenshot_path=screenshot):
                    print(f'Founded! initiating: {image_alias}')
                    break
                else:
                    print(f'Not found, researching {image_alias}...')
            except Exception as e:
                print(e)

    def check_if_exist_image(self, image_alias:str, tryes:int):
        i = 0
        while i < tryes:
            try:
                screenshot = 'src/utils/screens/fullscreen.png'
                pya.screenshot(screenshot)
                if self.locate_on_screen(template_path=image_alias, screenshot_path=screenshot):
                    print('found! waiting action')
                    return True
                
                i += 1 
                print(f'researching...({i} try)')                    
            except Exception as e:
                raise e