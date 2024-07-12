class PIDController:
    def __init__(self, Kp, Ki, Kd, run_time):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        # 程序的运行时间
        self.run_time = run_time
        # 误差
        self.error = 0
        # 上一次误差
        self.last_error = 0
        # 累计误差
        self.integral = 0
        
    def update(self, feedback_value, set_point):
        """
        feedback_value: 摄像头捕获点的坐标
        set_point: 目标点的坐标
        """
        self.error = set_point - feedback_value
        # 将误差累加起来
        self.integral += self.error * self.run_time
        # 误差的变化量
        derivative = (self.error - self.last_error) / self.run_time
        
        output = self.Kp * self.error + self.Ki * self.integral + self.Kd * derivative
        
        self.last_error = self.error
        
        return output