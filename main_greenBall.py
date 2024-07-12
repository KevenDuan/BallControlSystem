import cv2
import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from PidControl import PIDController
import numpy as np

def colorDetect(img):
    cX1, cY1 = -1, -1
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    # 颜色二值化筛选处理
    """
    这里利用hsv去筛选出绿色, 自己根据需求进行调试
    """
    inRange_hsv_green = cv2.inRange(hsv, np.array([35, 170, 46]), np.array([77, 255, 255]))
    # cv2.imshow('inrange_hsv_green', inRange_hsv_green)
    
    """
    try: 用来捕获到没有找到小球坐标的错误
    如果没有捕获小球坐标返回(-1, -1)
    """
    try:
        # 找中心点
        cnts1 = cv2.findContours(inRange_hsv_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        c1 = max(cnts1, key=cv2.contourArea)
        M = cv2.moments(c1)
        cX1 = int(M["m10"] / M["m00"])
        cY1 = int(M["m01"] / M["m00"])
        cv2.circle(img, (cX1, cY1), 3, (0, 0, 255), -1)
        rect = cv2.minAreaRect(c1)
        box = cv2.boxPoints(rect)
        cv2.drawContours(img, [np.int0(box)], -1, (0, 0, 255), 2)
    except:
        print('Not find green ball!')
    return cX1, cY1

def changeAngle(x, y):
    """
    限制x轴舵机和y轴舵机的转角, 防止损坏机械结构
    """
    x_limit = (-25, 25) # x轴范围
    y_limit = (-25, 25) # y轴范围
    # 幅度系数
    k_x = 4.5
    k_y = 8.5
    x = min(max(x * k_x, x_limit[0]), x_limit[1])
    y = min(max(y * k_y, y_limit[0]), y_limit[1])
    print(x, y)

    servo7.angle = (x_angle + x)
    servo8.angle = (y_angle + y)
    # time.sleep(0.03)

def pid():
    now_time = time.time()
    # run_time = (now_time - sta_time) / 10000
    # pid控制
    if ball_x == ball_y == -1: return
    control_signal_x = controller_x.update(ball_x, org_x)
    control_signal_y = controller_y.update(ball_y, org_y)
    changeAngle(control_signal_x, control_signal_y)

"""
PCA9685与舵机的初始化
"""
i2c = board.I2C()  # uses board.SCL and board.SDA
pca = PCA9685(i2c)
pca.frequency = 50
servo7 = servo.Servo(pca.channels[7]) # x轴
servo8 = servo.Servo(pca.channels[8]) # y轴

# 设置舵机中点
x_angle, y_angle = 80, 73
changeAngle(0, 0)


if __name__ == "__main__" :
    sta_time = time.time() # 程序运行时间
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    
    run_time = 1
    # create pid class
    controller_x = PIDController(Kp = 0.009, Ki = 0.0000, Kd = 0.058, run_time = run_time) # 0.009 0.000 0.058
    controller_y = PIDController(Kp = 0.009, Ki = 0, Kd = 0.06, run_time = run_time) # 0.009 0.00 0.06
    
    while True:
        # 读取视频帧
        ret, img = cap.read()
        # 检查是否成功读取帧
        if not ret:
            print("Error: Could not read frame.")
            break
        # change img shape
        img = img[100:-25, 100:-80]
        
        """
        检测小球的位置
        """
        ball_x, ball_y = colorDetect(img)
        # print('ball:', ball_x, ball_y) # 检测到小球的位置
        
        height, width, _ = img.shape
        org_x, org_y = width / 2, height / 2 # 屏幕的中心点坐标
        
        # print(height, width)
        cv2.putText(img, f'ball:({ball_x}, {ball_y})', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(img, f'org:({width // 2}, {height // 2})', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # pid
        pid()

        # 显示当前帧
        cv2.imshow('Camera', img)

        # 按下Esc键退出循环
        if cv2.waitKey(1) == 27:
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()
