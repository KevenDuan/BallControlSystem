## Equipment 器材说明

The main control board uses a Raspberry Pi 4B.

主控板使用的是树莓派4B。

USB camera, servo, connecting rod bearing, universal joint, acrylic plate.

USB摄像头、舵机、连杆轴承、万向节、亚克力板。

## Description 描述

The position of the ball is detected by the camera using `OpenCv`, and the slope of the board is controlled by the `PID` algorithm so that the ball stays on the board.

球的位置通过摄像头，使用“OpenCv”对其进行检测，板的坡度由“PID”算法控制从而使得球一直停留在板上。

The program can give an arbitrary position and make the ball reach that position.

该程序可以给出任意位置并使球到达该位置。

<img src=".\show.jpg" style="zoom: 33%;" />



## Precautions 注意事项

Depending on each servo, the program cannot be used directly, and it is necessary to set the midpoint and adjust the PID algorithm according to its own mechanical mechanism.

根据每个舵机的不同，该程序并不能直接运行使用，需要根据自己的机械机构设置中点以及调节pid算法。

The integral effect in the PID algorithm is relatively small and can be debugged at the end.

PID算法中的积分影响比较小，可以放到最后调试。

The steering gear is controlled using the adafruit-circuitpython-pca9685 library, please refer to the blog for details: [树莓派4B-PCA9685驱动舵机 - KevenDuan](https://www.cnblogs.com/kevenduan/p/18289747)

舵机的控制用了adafruit-circuitpython-pca9685库，具体细节参考博客。

If the Raspberry Pi doesn't download OpenCV refer to this blog: [树莓派安装OpenCv - KevenDuan](https://www.cnblogs.com/kevenduan/p/17355146.html)

如果树莓派没有下载opencv参考这篇博客

## File Description 文件说明

- colorDetect.py: Pellets are detected using a color-detection method.

- contourDetect.py: The method of contour detection is used.
- main_greenBall.py: Main program.

- PidControl.py: PID control algorithm library.
- servo.py: This procedure is a procedure for testing servos.