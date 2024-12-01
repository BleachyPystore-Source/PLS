# -*- coding: UTF-8 -*-
import time
import RPi.GPIO as GPIO


#车轮马达代码
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 

########电机驱动接口定义#################
ENA = 13    # L298使能A
ENB = 15    # L298使能B
IN1 = 31    # 电机接口1
IN2 = 33    # 电机接口2
IN3 = 35    # 电机接口3
IN4 = 37    # 电机接口4

frequency = 30 # 电机频率
dc = 50 # 占空比，即电机工作时间占比

#########电机初始化为LOW#################
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
ENA_pwm = GPIO.PWM(ENA, frequency)
ENA_pwm.start(0)
# ENA_pwm.ChangeFrequency(frequency)
ENA_pwm.ChangeDutyCycle(dc)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
ENB_pwm = GPIO.PWM(ENB, frequency)
ENB_pwm.start(0)
# ENB_pwm.ChangeFrequency(frequency)
ENB_pwm.ChangeDutyCycle(dc)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

def Motor_Forward():
    print( 'motor forward' )
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    
def Motor_Backward():
    print( 'motor_backward' )
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    
def Motor_TurnLeft():
    print( 'motor_turnleft' )
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    
def Motor_TurnRight():
    print( 'motor_turnright' )
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    
def Motor_Stop():
    print( 'motor_stop' )
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)




#超声波定义初始化
#设置 GPIO 模式为 BCM
GPIO.setmode(GPIO.BCM)
  
#定义 GPIO 引脚
GPIO_TRIGGER = 15
GPIO_ECHO = 14
  
#设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
  
def distance():
    # 发送高电平信号到 Trig 引脚
    GPIO.output(GPIO_TRIGGER, True)
  
    # 持续 10 us 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
  
    start_time = time.time()
    stop_time = time.time()
  
    # 记录发送超声波的时刻1
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
  
    # 记录接收到返回超声波的时刻2
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
  
    # 计算超声波的往返时间 = 时刻2 - 时刻1
    time_elapsed = stop_time - start_time
    # 声波的速度为 343m/s， 转化为 34300cm/s。
    distance = (time_elapsed * 34300) / 2
  
    return distance




#舵机定义初始化
def tonum(num):  # 用于处理角度转换的函数
    fm = 10.0 / 180.0
    num = num * fm + 2.5
    num = int(num * 10) / 10.0
    return num

servopin1 = 18   #舵机1,方向为左右转
servopin2 = 23   #舵机2,方向为上下转

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin1, GPIO.OUT, initial=False)
GPIO.setup(servopin2, GPIO.OUT, initial=False)
p1 = GPIO.PWM(servopin1,50) #50HZ
p2 = GPIO.PWM(servopin2,50) #50HZ

p1.start(tonum(85)) #初始化角度
p2.start(tonum(40)) #初始化角度
time.sleep(0.5)
p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
time.sleep(0.1)

a = 0  #云台舵机1的执行次数
c = 9  #云台舵机1初始化角度：90度

b = 0  #云台舵机2的执行次数
d = 4  #云台舵机2初始化角度：40度

q = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
 100, 110, 120, 130, 140, 150, 160, 170, 180]  #旋转角度列表

def left():
    global a, c   #引入全局变量
    a += 1
    if c > 2:  #判断角度是否大于20度
        c = c-4
        g = q[c]  #调用q列表中的第c位元素
        print('当前角度为',g)
        p1.ChangeDutyCycle(tonum(g))  #执行角度变化，跳转到q列表中对应第c位元素的角度
        time.sleep(0.1)
        p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)
    else:
        print('\n**超出范围**\n')
        c = 9
        g = 85  #调用q列表中的第c位元素
        p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        time.sleep(0.1)
        p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)
       
def right():
    global a, c    #引入全局变量
    if c < 16:
        c = c+4
        g = q[c]  #调用q列表中的第c位元素
        print('当前角度为',g)
        p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        time.sleep(0.1)
        p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)
    else:
        print('\n****超出范围****\n')
        c = 9
        g = 85  #调用q列表中的第c位元素
        p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        time.sleep(0.1)
        p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)

def up():
    global b, d    #引入全局变量
    b += 1
    if d > 2:
        d = d-1
        g = q[d]  #调用q列表中的第d位元素
        print('当前角度为',g)
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        time.sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)
    else:
        print('\n**超出范围**\n')
        d = 4
        g = q[d]  #调用q列表中的第d位元素
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        time.sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)

def down():
    global b, d    #引入全局变量
    if d < 11:
        d = d+1
        g = q[d]  #调用q列表中的第d位元素
        print('当前角度为',g)
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        time.sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)
    else:
        print('\n****超出范围****\n')
        d = 4
        g = q[d]  #调用q列表中的第d位元素
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        time.sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        time.sleep(0.01)




#进步电机定义初始化

IN1 = 12   #树莓派的引脚与驱动连接
IN2 = 16   
IN3 = 20
IN4 = 21
 
GPIO.setmode(GPIO.BCM)       # 使用BCM编码
GPIO.setwarnings(False)
 
GPIO.setup(IN1, GPIO.OUT)      # 设置为输出模式
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
 
def setStep(h1, h2, h3, h4):
    GPIO.output(IN1, h1)
    GPIO.output(IN2, h2)
    GPIO.output(IN3, h3)
    GPIO.output(IN4, h4)
 
delay = 0.003 #控制转速，增大则转速变慢  最快稳定转速大概为0.0017（这个速度想要转的话需要预热，不然转不起来）
steps =200   #控制转动时长


def leftStep():
    for i in range(0, steps):   #这是顺时针转动，如果要反向转动则将下面四行setStep反过来就行了
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)

def rightStep():

    for j in range(0, steps):   #这是逆时针转动，如果要反向转动则将下面四行setStep反过来就行了
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        
def connectCamera():
    print("Loading camera...")
    time.sleep(5)
    print("Camera Load Successful")


#Camera 定义和初始化
import socket
import cv2
import numpy as np

# 绑定地址和端口
host = '192.168.1.68'
port = 8000

# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Listening on {host}:{port}")

# 接受连接
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

try:
    while True:
        # 接收图像大小
        data = client_socket.recv(4)
        if not data:
            break
        img_size = int.from_bytes(data, 'big')

        # 接收图像数据
        img_data = bytearray()
        while len(img_data) < img_size:
            packet = client_socket.recv(img_size - len(img_data))
            if not packet:
                break
            img_data.extend(packet)

        # 将字节数据转换为 numpy 数组
        img_array = np.frombuffer(img_data, dtype=np.uint8)

        # 解码图像
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # 显示图像
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("接收中断")

finally:
    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()

#Defines a function to spray the anti-pest solution.
def sprayWater():
    print("Spraying...")
    time.sleep(60)
#Defines a function to identify the pests.
def pestID():
    health = True
    if health == False:
        sprayWater()
        return "Infected"
    else:
        return "Healthy" 
#This is where the code starts

print("Welcome to PIs Software v1.1.5, software initializing...")
time.sleep(10)
print("Initialization Successful! Connecting Camera...")
connectCamera()

while True: 
        
    a = input("Enter WASD to control the robot: ")
    
    if a == "w":
        if distance() > 5:
            Motor_Forward()
            pestID()
        else:
            print("Danger! You are crashing!")
    elif a == "s":
        Motor_Backward()
    elif a == "a":
        Motor_TurnLeft()
    elif a == "d":
        Motor_TurnRight()
     
    elif a == "q":
        b = input("Quit? Y/n ")
        if b == "Y":
            break
            print("Thank you for using the PIs software!")
    else:
        print("Error! please enter a value of either 'w', 'a', 's', 'd'. ")




