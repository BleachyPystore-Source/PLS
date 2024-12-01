#Developer Team: Tom L, ...

#Welcome to the PIs editing interface! This is where you can access our code. 
#Explanations like this will guide you through our software and provide details on our team-crafted world class software.

#The functions to control the APSIS. In later stages a GUI for iOS will be available so you can control your APSIS via your phone!
import random 
import time
#Defines a function to turn left.
def left():
    print("Turning left")

#Defines a function to turn right.
def right():
    print("Turning right")
#Defines a function to reverse.
def backward():
    while True:
        print("Backing up")
        if radarDistance() <= 5:
            print("Danger! Obstacle behind!")
            stop()
        break
#Defines a function to move forward
def forward():
    while True:
        print("Moving forward")
        if radarDistance() <= 5:
            print("Danger! Obstacle ahead!")
            stop()
        break
#Defines a function to get a random value of the distance between cart and obstacle.
def radarDistance():
    distanceMeter = random.randint(0,10)
    return distanceMeter
#Defines a function to brake in case the APSIS gets too close to an object
def stop():
    print("Stopping")
#Defines a function to connect to the mounted camera.
def connectCamera():
    print("Loading camera...")
    time.sleep(5)
    print("Camera Load Successful")
#Defines a function to turn the eyes to a random position
def servoTurn():
    s = random.randint(0,180)
    print("Turning...")
    time.sleep(1)
    print("Turned Servo " + s + " degrees.")

print("Welcome to PIs Software v0.0.1, software initializing...")
#time.sleep(10)
print("Initialization Successful! Connecting Camera...")
connectCamera()

while True: 
        
    a = input("Enter WASD to control the robot: ")
    
    if a == "w":
        forward()
        continue
    elif a == "s":
        backward()
        continue 
    elif a == "a":
        left()
    elif a == "d":
        right()
    elif a == "q":
        b = input("Quit? Y/n ")
        if b == "Y":
            break
            print("Thank you for using the PIs software! The price is $500.00, pay via Bitcoin")
    else:
        print("Error! please enter a value of either 'w', 'a', 's', 'd'. ")
