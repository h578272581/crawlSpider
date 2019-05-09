
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from PIL import Image
from io import BytesIO
def getImage(driver):
    js = []
    # display full backgroud with mask
    js.append('var q = document.getElementsByTagName("canvas"); q[0].setAttribute("style", "display: block");')
    
    # display slice
    js.append('var q = document.getElementsByTagName("canvas"); q[1].setAttribute("style", "display: block");')
    
    # display full Backgroud
    js.append('var q = document.getElementsByTagName("canvas"); q[2].setAttribute("style", "display: block");')
    
    # all pic hide 
    js.append('var q = document.getElementsByTagName("canvas"); for(var i=0;i<q.length;i++) {q[i].setAttribute("style", "display: none");}')
    name = ['aFade.png', 'aSlice.png', 'aFullBg.png']
    elements = driver.find_elements_by_tag_name('canvas')
    # save pictures
    for i in range(3):
        driver.execute_script(js[3])
        sleep(1)
        driver.execute_script(js[i])
        sleep(1)
        img = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        x, y = elements[i].location.get('x'), elements[i].location.get('y')
        width, height = elements[i].size.get('width'), elements[i].size.get('height')
        left, top, right, bottom = x, y, x+width, y+height
        img.crop((left, top, right, bottom)).save(name[i])
    
    

