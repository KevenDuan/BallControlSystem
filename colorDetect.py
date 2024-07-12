# 轮廓提取
import cv2
import numpy as np

def colorDetect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    # 颜色二值化筛选处理
    inRange_hsv_green = cv2.inRange(hsv, np.array([35, 170, 46]), np.array([77, 255, 255]))
    # cv2.imshow('inrange_hsv_green', inRange_hsv_green)

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
    return cX1, cY1
    
    # 打开摄像头
cap = cv2.VideoCapture(0)
# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
 
while True:
    # 读取视频帧
    ret, img = cap.read()
    # 检查是否成功读取帧
    if not ret:
        print("Error: Could not read frame.")
        break
    
    img = img[100:-25, 100:-80]
    
    ball_x, ball_y = colorDetect(img)
    print(ball_x, ball_y) # 检测到小球的位置

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # 显示当前帧
    cv2.imshow('Camera', img)

    # 按下Esc键退出循环
    if cv2.waitKey(1) == 27:
        break
# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()
