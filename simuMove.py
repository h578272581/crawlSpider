
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import numpy as np
def simuMove(driver):
    act = ac(driver)
    button = driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')
    onElem = act.click_and_hold(button).perform()
    track = getTrack()
    for x in track():
        onElem.move_by_offset(x, 0).perform()
    time.sleep(.5)
    onElem.release().perform()

def getTrack(distance):
    x = np.arange(-np.pi/2, np.pi/2, np.pi/50)
    y = np.fix(np.sin(x)*distance/2)
    y -= y[0]
    for i in range(len(y)-1):
        y[i] = y[i+1] - y[i]
    y[-1] = 0
    return list(y)

















