
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from PIL import Image
from io import BytesIO
import numpy as np

class CrackGeetest:
    def __init__(self, user=None, passwd=None ):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url = 'https://auth.geetest.com/login/'
        if user:
            self.user = user
        else:
            self.user = '%s@qq.com'%np.random.randint(1e8, 1e10)
        if passwd:
            self.passwd = passwd
        else:
            self.passwd = randomPassword()
        self.wait = WebDriverWait(self.driver, 2)
        self.js = 'var q = document.getElementsByTagName("canvas"); q[{number}].setAttribute("style", "opacity: 1;display: block;");'
    def open(self):
        # 打开目标网页   '1','1',
        self.driver.get(self.url)
        user = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="email"]')))
        passwd = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
        user.send_keys(self.user)
        sleep(.5)
        passwd.send_keys(self.passwd)
        sleep(.5)

    def getBtn(self):
        # 并点击，出现图片
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="geetest_radar_tip"]')))
        btn.click()
        sleep(.5)

    def getSlider(self):
        # 获取滑块
        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="geetest_slider_button"]')))
        print('getSlider', slider)
        return slider
    def run(self):
        # 主进口
        self.open()
        self.getBtn()
        # 单击后验证成功，不需要后续验证
        if self.isSuccess():
            print('sucess')
            return 1
        while 1:
            bol = self.crack()
            print('bol: ', bol)
            if bol:
                # self.driver.find_element_by_xpath('//button[@class="ivu-btn ivu-btn-primary-arrow"]').click()
                return
            print('failed, retry once')
            sleep(5)



    def crack(self):

        # 判断验证类型，是文字识别还是滑块
        try:
            tag = self.driver.find_element_by_class_name('geetest_item_img')
            print('captcha is not slide')
            self.driver.refresh()
        except:
            print('captcha is slide')
            pass
        # number = 0: display full backgroud with mask
        # number = 1: display slice
        #  number = 2. display full Backgroud
        fullImg = self.getImg(2)
        fullImg.save('fullImg.png')
        # sliceImg = self.getImg(1)
        # sliceImg.save('sliceImg.png')
        fadeImg = self.getImg(0)
        fadeImg.save('fadeImg.png')
        self.showAll()
        sleep(.5)
        slider = self.getSlider()
        print(slider)
        x, y = self.getGap(fadeImg, fullImg)
        print('x = %s, y = %s'%(x,y))
        # 小滑块距离边缘6 px
        track = self.getTrack(x - 6)
        self.simuMove(slider, track)
        if self.isSuccess():
            print('sucess')
            return 1
        else:
            return 0

    def finishi(self):
        self.driver.close()

    def getPosition(self, num):
        # 获取图片位置
        img = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'canvas')))
        img = self.driver.find_elements_by_tag_name('canvas')[num]
        sleep(.5)
        size = img.size
        location = img.location
        left = location.get('x')
        top = location.get('y')
        right = location.get('x') + size.get('width')
        bottom = location.get('y') + size.get('height')
        return (left, top, right, bottom)

    def isSuccess(self):
        sleep(2)
        try:
            tag = self.driver.find_element_by_class_name('geetest_success_radar_tip')
            if tag.text == '验证成功':
                print('try: geetest_sucess_box')
                return True
        except Exception as e:
            print('try: except, to continue')
            return False

    def getImg(self, number):
        # js = [
        #     'var q = document.getElementsByTagName("canvas"); q[0].setAttribute("style", "display: block");',
        #     'var q = document.getElementsByTagName("canvas"); q[1].setAttribute("style", "display: block");',
        #     'var q = document.getElementsByTagName("canvas"); q[2].setAttribute("style", "display: block");'
        #     ]
        # jsHide: all picturess hide
        js = self.js.format(number = number)
        print(js)
        jsHide = 'var q = document.getElementsByTagName("canvas"); for(var i=0;i<q.length;i++) {q[i].setAttribute("style", "opacity: 0;display: none;");}'
        # save pictures
        self.driver.execute_script(jsHide)
        sleep(.5)
        self.driver.execute_script(js)
        sleep(.5)
        img = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        left, top, right, bottom = self.getPosition(number)
        print(left, top, right, bottom)
        return img.crop((left, top, right, bottom))

    def showAll(self):
        self.driver.execute_script(self.js.format(number = 0))
        self.driver.execute_script(self.js.format(number = 1))

    def getGap(self, img1, img2):
        # 获取缺口位图
        width, height = img1.size
        print(width, height)
        img1 = img1.load()
        img2 = img2.load()
        threshold = 64
        for i in range(width):
            for j in range(height):
                if abs(img1[i, j][1] - img2[i, j][1]) > threshold and abs(img1[i, j][2] - img2[i, j][2]) > threshold and abs(img1[i, j][2] - img2[i, j][2]) > threshold:
                    return (i, j)
        return (0, 0)

    def simuMove(self, slider, track):
        act = AC(self.driver)
        onElem = act.click_and_hold(slider).perform()
        for x in track:
            print(x)
            act.move_by_offset(x, 0).perform()
            act = AC(self.driver)
            sleep(.3)
        sleep(.5)
        act.release().perform()

    def getTrack(self, distance):
        print('independent getTrack')
        a1 = .2 + np.random.random() * .15
        a2 = .9 - a1 + np.random.random() * .1
        a3 = 1 - a1 - a2
        # print(a1, a2, a3, sum([a1, a2, a3]))
        n1 = np.random.randint(5, 10)
        n2 = np.random.randint(10, 15)
        n3 = np.random.randint(5, 10)
        alpha = np.linspace(-np.pi / 2, np.pi / 2, n1)
        beta = np.linspace(-np.pi / 2, np.pi / 2, n2)
        gama = np.linspace(-np.pi / 2, np.pi / 2, n3)
        y1 = np.round(np.cos(alpha), 4)
        y2 = np.round(np.cos(beta), 4)
        y3 = np.round(np.cos(gama), 4)
        # print(y1, y2, y3, sep='\n')
        # print('*-' * 30)
        y1 = np.round(a1 * y1 / np.sum(y1), 4)
        y2 = np.round(a2 * y2 / np.sum(y2), 4)
        y3 = np.round(a3 * y3 / np.sum(y3), 4)
        # print(y1, y2, y3, sep='\n')
        # print('*=' * 30)
        y = np.hstack([y1, y2, y3])
        y = np.round(y * distance, 3)
        while abs(np.sum(np.round(y)) - distance) > 4:
            y /= np.sum(np.round(y)) / distance
            print(np.round(y))
            sleep(.05)
        print(np.sum(np.round(y)))
        return np.round(y)

def randomPassword(least=8, most=12):
    password = ''
    for i in range(np.random.randint(least, most)):
        num = np.random.choice([65 + np.random.randint(2) * 32 + np.random.randint(0, 26), np.random.randint(48, 58)])
        # print(num)
        password += chr(num)
    return password

if __name__ == '__main__':
    user = '%s@qq.com'%np.random.randint(1e8, 1e10)
    print(user)
    passwd = randomPassword()
    print(passwd)
    crack = CrackGeetest(user, passwd)
    crack.run()
    sleep(20)
    crack.finishi()








