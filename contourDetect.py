# 轮廓提取
import cv2

def ToBinray():
    """
    转二进制图像
    """
    global imgray, binary
    # 1、灰度图
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('imgray', imgray)
    
    # 2、二进制图像
    ret, binary = cv2.threshold(imgray, 80, 255, 0)
    cv2.imshow('binary', binary)
 
# 提取轮廓
def GetGontours():
    """
    检测小球的位置返回(x, y), 如果没有找到返回(-1, -1)
    """
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 获取轮廓面积
    for i in contours:
        area = cv2.contourArea(i)
        # 筛选轮廓面积
        if area < 800 or area > 2000: continue
        x, y, w, h = cv2.boundingRect(i)
        if w - 10 < h < w + 10:
            # print("轮廓面积：", area)
            cv2.rectangle(img,  (x, y + h), (x + w, y), (0, 0, 255))
            # 画出中心点
            cv2.circle(img, (x + w // 2, y + h // 2), 1, (0, 0, 255), 2)
            cv2.putText(img, f'org:({x + w//2}, {y + h//2})', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            return x + w // 2, y + h // 2
    return -1, -1
    
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
    
    ToBinray()
    org_x, org_y = GetGontours()
    print(org_x, org_y) # 检测到小球的位置

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