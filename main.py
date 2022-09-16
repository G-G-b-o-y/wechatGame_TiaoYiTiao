from pynput.mouse import Button, Controller
import cv2
import time
import random
from grabscreen import grab_screen

class screen_process:
    def __init__(self):
        global img
        self.mode = 0
        self.mouse = Controller()
        screenShoted = grab_screen()
        self.gameWindowHeight = 800
        self.diffvar = 305

        # 加载图片
        tpl = cv2.imread("window.png")
        # target = cv2.imread("1.png")
        target = screenShoted
        th,tw = tpl.shape[:2]    #获取模板图像的高宽
        method = cv2.TM_CCOEFF_NORMED # 标准相关匹配算法
        # 开始匹配
        result = cv2.matchTemplate(target, tpl, method)
        # 在给定的矩阵中寻找最大和最小值
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 如果最大值超过0.7(自己定义的),表示匹配，完全一样基本上就接近1了
        if max_val > 0.7:
            self.tl = max_loc #tl是左上角点
            self.br = (self.tl[0]+tw,self.tl[1]+th+self.gameWindowHeight)    #br右下点
            # cv2.rectangle(target,tl,br,(0,0,255),5)#画矩形
            img = self.cropped = target[self.tl[1]:self.br[1], self.tl[0]:self.br[0]]


    def move_to_target(self):
        # 兩點距離為 distance
        # 水平距離
        x_diff = x1-x0
        # 垂直距離
        y_diff = y1-y0
        distance = (x_diff**2 + y_diff**2)**0.5
        print(f"distance {distance}")
        self.mouse.position = (self.br[0]-self.gameWindowHeight/10-random.randint(0, 100), self.br[1]-self.gameWindowHeight/2-random.randint(0, 100))
        self.mouse.press(Button.left)
        print(f'keeptime {distance/self.diffvar}')
        time.sleep(distance/self.diffvar)
        self.mouse.release(Button.left)
        return


    def OnMouse(self, event, x, y, flags, param):
        global x0, y0, x1, y1
        if self.mode == 0 and event == cv2.EVENT_LBUTTONDOWN:
            x0, y0 = x, y
            cv2.circle(self.cropped, (x, y), 20, (0, 0, 190), 2)
            print('選擇棋子', x, y)
            self.mode = 1

        elif self.mode == 1 and event == cv2.EVENT_LBUTTONDOWN:
            x1, y1 = x, y
            cv2.circle(self.cropped, (x, y), 20, (190, 0, 0), 2)
            print('選擇方塊', x, y)
            time.sleep(1)
            self.move_to_target()
            self.mode = 2

    def start(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.OnMouse)
        while(1):
            cv2.imshow('image', self.cropped)
            k = cv2.waitKey(1)
            if k == ord('e'):
                self.mode = 1
            elif self.mode == 2:
                cv2.destroyAllWindows()
                return True
        cv2.destroyAllWindows()

while 1:
    screen_process().start()
    print('---END---')
    time.sleep(0.8)
