# -*- coding: UTF-8 -*-
import time
import RPi.GPIO as GPIO
from time import sleep
import socket
import io
import time
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder



#车轮马达代码
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True) 

########电机驱动接口定义#################
ENA = 27    # L298使能A
ENB = 22    # L298使能B
IN1 = 6     # 电机接口1
IN2 = 13    # 电机接口2
IN3 = 19    # 电机接口3
IN4 = 26    # 电机接口4

frequency = 30 # 电机频率
dc = 30 # 占空比，即电机工作时间占比

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


#超声波定义初始化
#设置 GPIO 模式为 BCM
# GPIO.setmode(GPIO.BCM)
    
#定义 GPIO 引脚
GPIO_TRIGGER = 15
GPIO_ECHO = 14
    
#设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#舵机定义初始化

def tonum(num):  # 用于处理角度转换的函数
    fm = 10.0 / 180.0
    num = num * fm + 2.5
    num = int(num * 10) / 10.0
    return num

servopin1 = 18   #舵机1,方向为左右转
servopin2 = 24   #舵机2,方向为上下转

# GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin1, GPIO.OUT, initial=False)
GPIO.setup(servopin2, GPIO.OUT, initial=False)
p1 = GPIO.PWM(servopin1,50) #50HZ
p2 = GPIO.PWM(servopin2,50) #50HZ

p1.start(tonum(85)) #初始化角度
p2.start(tonum(85)) #初始化角度
time.sleep(0.5)
p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
time.sleep(0.1)

a = 0  #云台舵机1的执行次数
c = 9  #云台舵机1初始化角度：90度

b = 0  #云台舵机2的执行次数
d = 9  #云台舵机2初始化角度：90度

q = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
 100, 110, 120, 130, 140, 150, 160, 170, 180]  #旋转角度列表



#电机函数
def Motor_Forward():
    print( 'motor forward' )
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    print( 'motor forward end' )

    
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
#电机函数结束

#超声波函数
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
#超声波函数结束

#舵机函数
def left():
    global a, c   #引入全局变量
    a += 1
    if c > 2:  #判断角度是否大于20度
        c = c-4
        g = q[c]  #调用q列表中的第c位元素
        print('当前角度为',g)
        p1.ChangeDutyCycle(tonum(g))  #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.1)
        p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动
        sleep(0.01)
    else:
        print('\n**超出范围**\n')
        c = 9
        g = 85  #调用q列表中的第c位元素
        p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.1)
        p1.ChangeDutyCycle(0)  #清除当前占空比，使舵机停止抖动
        sleep(0.01)
       
def right():
    global a, c    #引入全局变量
    if c < 16:
        c = c+4
        g = q[c]  #调用q列表中的第c位元素
        print('当前角度为',g)
        p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.1)
        p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        sleep(0.01)
    else:
        print('\n****超出范围****\n')
        c = 9
        g = 85  #调用q列表中的第c位元素
        p1.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第c位元素的角度
        sleep(0.1)
        p1.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        sleep(0.01)

def up():
    global b, d    #引入全局变量
    b += 1
    if d > 2:
        d = d-4
        g = q[d]  #调用q列表中的第d位元素
        print('当前角度为',g)
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        sleep(0.01)
    else:
        print('\n**超出范围**\n')
        d = 4
        g = q[d]  #调用q列表中的第d位元素
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        sleep(0.01)

def down():
    global b, d    #引入全局变量
    if d < 16:
        d = d+4
        g = q[d]  #调用q列表中的第d位元素
        print('当前角度为',g)
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        sleep(0.01)
    else:
        print('\n****超出范围****\n')
        d = 4
        g = q[d]  #调用q列表中的第d位元素
        p2.ChangeDutyCycle(tonum(g)) #执行角度变化，跳转到q列表中对应第d位元素的角度
        sleep(0.1)
        p2.ChangeDutyCycle(0) #清除当前占空比，使舵机停止抖动
        sleep(0.01)
#舵机函数结束
        


#Camera 定义和初始化
def cameraSetup():
    # 初始化摄像头
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)

    # 目标主机 IP 和端口
    host = '192.168.1.68'  # 替换为你的目标主机 IP
    port = 8000  # 替换为你的目标主机端口

    # 创建 socket 对象
    def connect_to_server(host, port, retries=50, delay=10):
        for attempt in range(retries):
            try:
                # 创建 socket 对象
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))
                print("Connected to server on attempt", attempt + 1)
                return client_socket
            except socket.error as e:
                print(f"Connection failed on attempt {attempt + 1}/{retries}: {e}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("Failed to connect to server after multiple attempts.")
                    return None

    # 尝试连接服务器
    client_socket = connect_to_server(host, port)

    if client_socket:
        # 连接成功后可以在这里继续进行通信处理
        print("Connection established. You can now communicate with the server.")
    else:
        # 连接失败的处理
        print("Unable to connect to the server.")


    # 连续捕获视频流帧
    try:
        picam2.start()
        while True:
            # 捕获图像到字节流
            stream = io.BytesIO()
            picam2.capture_file(stream, format='jpeg')
            
            # 将字节流位置设置为开头
            stream.seek(0)

            # 读取图像数据
            img_bytes = stream.read()

            # 发送图像大小
            client_socket.sendall(len(img_bytes).to_bytes(4, 'big'))

            # 发送图像数据
            client_socket.sendall(img_bytes)

            # 延迟一段时间（可调节发送频率）
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("捕获中断")

    finally:
        picam2.stop()
        client_socket.close()
#Camera 定义和初始化结束

def connectCamera():
    print("Loading camera...")
    cameraSetup()
    time.sleep(3)
    print("Camera Load Successful")



#Defines a function to spray the anti-pest solution.
def sprayWater():
    print("Spraying...")
    up()
    time.sleep(3)
    up()

#Defines a function to identify the pests.
def pestID():
    if True == True:#Replace with the actual pest detection code
        health = False
    if health == False:
        return "Infected"
    else:
        return "Healthy" 



############################################################################################################
#This is where the code starts

print("Welcome to PIs Software v1.1.5, software initializing...")
time.sleep(1)
print("Initialization Successful! Connecting Camera...")
# connectCamera()

while True:    
    command = input("Please enter the key 'w,s,a,d,x' to control the robot,press q to quit: ")    
    if command == "w":
        safe_distance = int(distance())
        print("Distance: ", safe_distance)
        if int(safe_distance) > 30:
            Motor_Forward()
            if pestID()=="Infected":
                time.sleep(2)
                print("Danger! Pests detected!")
                Motor_Stop()
                sprayWater()
                continue

            else:
                print("Safe! No pests detected!")
                Motor_Forward()
                continue
        else:
            print("Danger! You are crashing!")
            Motor_Stop()
            right()
            sleep(5)
            if distance() > 30:
                Motor_TurnLeft()
                left()

            else:
                Motor_Stop()
                left()
                sleep(5)
                if distance() > 30:
                    Motor_TurnRight()
                    right()
                else:
                    Motor_Stop()    
    elif command == "s":
        Motor_Backward()
    elif command == "a":
        Motor_TurnLeft()
    elif command == "d":
        Motor_TurnRight()
    elif command == "x":
        Motor_Stop()
    elif command == "q":
        quit = input("Quit? Y/N ")
        if quit == "Y":
            print("Thank you for using the PIs software!")
            break
        else:
            continue
    else:
        print("Error! please enter a value of either 'w', 'a', 's', 'd'. ")




