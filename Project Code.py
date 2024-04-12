import RPi.GPIO as GPIO         
import time

# GPIOs used

GPIO_M1 = 27  #for Motors
GPIO_M2 = 22
GPIO_M3 = 5  
GPIO_M4 = 6  
en = 25
GPIO_TRIGGER = 18 #for Ultrasonic
GPIO_ECHO = 24
GPIO_LED_RED = 15 #for LED

temp1=1

#initialize the GPIOs

GPIO.setmode(GPIO.BCM) # for Motors
GPIO.setup(GPIO_M1,GPIO.OUT)
GPIO.setup(GPIO_M2,GPIO.OUT)
GPIO.setup(GPIO_M3,GPIO.OUT)
GPIO.setup(GPIO_M4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #for Ultrasonic
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED_RED, GPIO.OUT) #for LED 

GPIO.setwarnings(False)

GPIO.output(GPIO_M1,GPIO.LOW)
GPIO.output(GPIO_M2,GPIO.LOW)
GPIO.output(GPIO_M3,GPIO.LOW)
GPIO.output(GPIO_M4,GPIO.LOW) 

GPIO.setup(en,GPIO.OUT)
p=GPIO.PWM(en,10000)

p.start(25)
print("\n")
print("r-run s-stop")
print("\n")

##########ultrasonic
        
def distance():  # Ultrasonic code for distance
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

def empty_obs(): #Empty/obstacle time
    if __name__ == '__main__':
        time1 = 0
        time2 = 0
        stop = 0
        GPIO.output(GPIO_LED_RED, GPIO.LOW)
        try:
            while True:
                depth = distance() #distance
                if depth > 35: 
                    time1 = float(time.perf_counter());
                    print("Empty ",time1)
                    GPIO.output(GPIO_LED_RED, GPIO.LOW)
                else:    
                    time2 = float(time.perf_counter());
                    print("Obstacle",time2)
                    GPIO.output(GPIO_LED_RED, GPIO.HIGH)
                
                empty_time = time1 - time2
                print("The Empty time is ", empty_time)
                time.sleep(1)
                
                if empty_time > 0.3 and stop==0 :
                    parking()
                    stop = 1
                    
            # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
            
def parking(): # code for parking
    clock = 3

    GPIO.output(GPIO_M1,GPIO.LOW)
    GPIO.output(GPIO_M2,GPIO.LOW)
    GPIO.output(GPIO_M3,GPIO.LOW)
    GPIO.output(GPIO_M4,GPIO.LOW)
    time.sleep(1)

    while clock>0:  #code for rotating 90 degrees   
        GPIO.output(GPIO_M1,GPIO.HIGH)
        GPIO.output(GPIO_M2,GPIO.LOW)
        GPIO.output(GPIO_M3,GPIO.LOW)
        GPIO.output(GPIO_M4,GPIO.HIGH)
        time.sleep(1)
        clock-= 1
            
    GPIO.output(GPIO_M1,GPIO.LOW)
    GPIO.output(GPIO_M2,GPIO.LOW)
    GPIO.output(GPIO_M3,GPIO.LOW)
    GPIO.output(GPIO_M4,GPIO.LOW)

    time.sleep(2)
    clock=3

    while clock>0:  #code for reverse parking   
        GPIO.output(GPIO_M1,GPIO.LOW)
        GPIO.output(GPIO_M2,GPIO.HIGH)
        GPIO.output(GPIO_M3,GPIO.LOW)
        GPIO.output(GPIO_M4,GPIO.HIGH)
        time.sleep(1)
        clock-= 1  
        
    GPIO.output(GPIO_M1,GPIO.LOW)
    GPIO.output(GPIO_M2,GPIO.LOW)
    GPIO.output(GPIO_M3,GPIO.LOW)
    GPIO.output(GPIO_M4,GPIO.LOW)

while(1):  #code for going run/stop 
    x=input()
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(GPIO_M1,GPIO.HIGH)
         GPIO.output(GPIO_M2,GPIO.LOW)
         GPIO.output(GPIO_M3,GPIO.HIGH)
         GPIO.output(GPIO_M4,GPIO.LOW)   
         print("forward")
         empty_obs()
         x='z'
         
    elif x=='s':
        print("stop")
        GPIO.output(GPIO_M1,GPIO.LOW)
        GPIO.output(GPIO_M2,GPIO.LOW)
        GPIO.output(GPIO_M3,GPIO.LOW)
        GPIO.output(GPIO_M4,GPIO.LOW) 
        x='z'
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
        

        

