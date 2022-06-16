import datetime
import math
import numpy as np
from shapely.geometry import Point, Polygon
from multiprocessing.connection import Client
from multiprocessing.connection import Listener

#border boundies - in yards
chordsInner = [(2500,-1200),(2500,1000),(3100,1500),(5900,1500),(8500,1500),(10000,1200),(12100,870), (14050,600), (15560,1100),(15560,-1530),(9000,-1530),(6800,-830), (5800,-680),(5200,-720),(2500, -1200)]
chordsCenter =[(2500,-1230),(2500,1220),(3100,1680),(5900,1530),(8500,1590),(10000,1220),(12100,930), (14050,1250),(15560,1500),(15560,-1680),(9000,-1680),(6800,-900), (5800,-800),(5200,-810),(2500, -1230)]
chordsOuter = [(2500,-1400),(2500,1900),(3100,1900),(5900,1600),(8500,1740),(10000,1300),(12100,1150),(14050,1350),(15560,1500),(15560,-1900),(9000,-1900),(6800,-1020),(5800,-970),(5200,-933),(2500, -1400)]

innerPoly = Polygon(chordsInner)


#old function, don't use
def recived_data(conn):
        
    alertCount1 = 0
    alertCount2 = 0
    alertCount3 = 0
    alertCount4 = 0
    predictCounter = [0,0,0,0,0]

    inputPosition = [0,0,0]
    inputKnotHead = [0,0]
    inputTime = datetime.datetime(1,1,1,1,1,1)
    lastTime = datetime.datetime(1,1,1,1,1,1)

    Proj_Position = [0,0,0]

    avg_x_dif = 0
    avg_y_dif = 0
    avg_knot_diff = 0
    total = 0
    
    
    #make these different functions
    try: 
        while True:
            msg = str(conn.recv())
            
            
      
            lines = msg.split('\n')
            #read data in from file
            #this will have to change when input data every 2 seconds

            first_pp = 1
            for line in lines:

                print(line)
                

                words = line.split(' ')
                print(words)

                if len(words)<2:
                    continue
                elif(words[0] == "HS"):
                    for i in range(len(words)):
                        try:
                            words[i] = int(words[i])
                        except ValueError as verr:
                            pass
                    #store and get the next line
                    lastTime = inputTime
                    inputTime = datetime.datetime(words[1],words[2],words[3],words[4],words[5],words[6])
                    
                    print("input time", inputTime)
                    print("last time :", lastTime) 
                    continue
                    
                elif(words[0] == 'PP' and words[4]=='11' and first_pp ==1):
                    lastPosition = inputPosition
                    inputPosition = list(map(float, [words[1],words[2],words[3]]))
                    inputKnotHead = list(map(float, [words[10],words[11]]))
                    first_pp = 0
                    print("found pp")
                    continue
                    
                elif(words[0] == 'PP' and words[4] == '11' and first_pp == 0):
                    newPosition = list(map(float, [words[1],words[2],words[3]]))
                    newKnotHead = list(map(float, [words[10],words[11]]))
                    
                    #combind the new position numbers to get theaverage
                    for i in range(len(inputPosition)):
                        inputPosition[i] = (inputPosition[i] + newPosition[i])/2
                    for i in range(len(inputKnotHead)):
                        inputKnotHead[i] = (inputKnotHead[i] + newKnotHead[i])/2
                    continue
                elif(words[0] =="CS"):
                    print("\nend of message")
                    #if there was never a PP ------ADD CODE TO START COUNDOWN-----
                    if(first_pp == 1):
                        print("\n\n no pp")
                        print("input time", inputTime)
                        print("last time :", lastTime)   
                        inputTime = lastTime
                        print("input time", inputTime)
                        print("\n")
                        continue
                    else:
                        first_pp = 1
                else:
                    continue
                
                
                


                #alertResult = alertDetector(currentPosition, lastPosition, currentTime, lastTime, currentknothead);
                testheading = inputKnotHead[0]
                given_knots = inputKnotHead[1]

                currentPosition = inputPosition
                currentTime = inputTime

                time_diff = inputTime - lastTime
                seconds = abs(time_diff.total_seconds())
                if(seconds == 0):
                    seconds = 100000
                print("time difference: ", seconds)

                my_speed = [0,0,0]
                getSpeed(my_speed,currentPosition,lastPosition, seconds)
                my_knots = getKnots(my_speed)
                given_speed = [0,0]
                getSpeedFromKnots(given_speed, given_knots, testheading)
                
                print("my_knots: ", my_knots)
                print("given knots", given_knots)
                print("my_speed: ",my_speed)
                print("given_speed: ",given_speed)
                
                print("x-diff: ", my_speed[0] - given_speed[0])
                print("y-diff: ", my_speed[1] - given_speed[1])
                
                avg_knot_diff = avg_knot_diff + (my_knots - given_knots)
                avg_x_dif = avg_x_dif + (my_speed[0] - given_speed[0])
                avg_y_dif = avg_y_dif + (my_speed[1] - given_speed[1])
                total = total +  1
                continue
                #alert caes:
                
                #1: basic outliers:
                #x,y,x, and my_speed outliers (these boundrays are in yards, need to adjjust for feeeeet)
                if not 2500<=(currentPosition[0])<=15560:
                    alertCount1 += 1
                elif not -2200<=(currentPosition[1])<=2200:
                    alertCount1 += 1
                elif not -600<=currentPosition[2]<=25:
                    alertCount1 += 1
                elif not 0<=my_knots<=40:
                    alertCount1 += 1
                    
                #add projected position tests
                
                
                
                #2: loss of track (PP)
                
                
                
                #2: depth according to boarder level (need to calculate which level we are in)
                p1 = Point(currentPosition[0],currentPosition[1])
                if (p1.within(innerPoly)):
                    print("inside inner boundry")
                    #inner boundry is at most 220 feet (yards?) deep
                    #if(currentPosition[2] > -220)
                    
                #add projected position tests
                

                
                
                
                
                
                

                """
                if alertResult == 1:
                    alertCounter += 1
                #if there is no alert, reset the counter
                elif alertResult == 0:
                    alertCounter = 0
                    
                match alertResult:
                    case 0:
                        alertCounter = 0
                        print("in case 0")
                    case 1:
                        print("in case 1")
                        alertCounter += 1
                    case 2:
                        print("in case 2")
                        #need to claculate R (before?) and alarm after that many seconds
                    case 3:
                        print("in case 3")
                        
                    case 4:
                        print("in case 4")
                        predictCounter.append(1)
                        predictCounter.pop()
                    

                """
                #alarm enable if 5 consecutive alert ons
                if alertCounter >= 5:
                    print("alarm enable")
                    
                # alram enable if 2 out of 5 predictions 
                if sum(predictCounter) >=2:
                    print("alarm enable")
    
                    
        print("\navg x dif: ", avg_x_dif/total)
        print("avg y dif: ", avg_y_dif/total)
        print("avg knot dif: ", avg_knot_diff/total)
    except EOFError as e:
        print("end of file")


    return 0


#takes entire message and exstracts + updates input position and time
def parse_data(message, inputPosition, inputTime, lastTime):
    lines = message.split('\n')
    first_pp = 1
    for line in lines:

        print(line)
        words = line.split(' ')
        
        #if blank, go to next line
        if len(words)<2:
            continue
        
        #if HS line, get the times, then go to next line
        elif(words[0] == "HS"):
            for i in range(len(words)):
                try:
                    words[i] = int(words[i])
                except ValueError as verr:
                    pass
            #store and get the next line
            lastTime = inputTime
            inputTime = datetime.datetime(words[1],words[2],words[3],words[4],words[5],words[6])
            
            print("input time", inputTime)
            print("last time :", lastTime) 
            continue
        
        #if the first instance of PP data, set the input positions
        elif(words[0] == 'PP' and words[4]=='11' and first_pp ==1):
            lastPosition = inputPosition
            inputPosition = list(map(float, [words[1],words[2],words[3], words[10], words[11]]))
            first_pp = 0
            print("found pp")
            continue
            
        #if second or more instance of PP, take average of positions and new PP
        elif(words[0] == 'PP' and words[4] == '11' and first_pp == 0):
            newPosition = list(map(float, [words[1],words[2],words[3], words[10], words[11]]))
            
            #combind the new position numbers to get theaverage
            for i in range(len(inputPosition)):
                inputPosition[i] = (inputPosition[i] + newPosition[i])/2

            continue
            
        #if CS line, then it is th end of message
        elif(words[0] =="CS"):
            print("\nend of message")
            
            #if there was never a PP ------ADD CODE TO START COUNDOWN-----
            if(first_pp == 1):
                print("no pp")
                
                #set the time back to last time PP was sent
                inputTime = lastTime

                #return 3 to show no PP
                return 3
            else:
                return 0
        else:
            continue



#needs updating
def alertDetector(currentPosition, lastPosition, currentTime, lastTime):
    
    
    return 0;


#get my_speed in yards per second
def getSpeed(my_speed, currentPosition, lastPosition, seconds):
    #alternitivly this can be done by using the given my_speed and heading.
    print(currentPosition[0])
    print(lastPosition[0])
    #calculated my_speed in each direction with current and last positions (each position is in yards)
    print("seconds: ", seconds)
    my_speed[0] = (currentPosition[0]-lastPosition[0])/(seconds);
    my_speed[1] = (currentPosition[1]-lastPosition[1])/(seconds);
    my_speed[2] = (currentPosition[2]-lastPosition[2])/(seconds);
    
#calculate speed in x and y direction from the given knots and heading values
def getSpeedFromKnots(given_speed, my_knots, heading):

    #rotate 90 so that head is degrees off of x axis (instead of y axis) ((or y instead of x, not sure))
    heading = heading-90
    #print("incomming knots : ",my_knots,"incomming heading: ",heading)
    given_speed[0] = (1.68781* (my_knots * math.sin((math.radians(heading)))))
    given_speed[1] = (1.68781* (my_knots * math.cos((math.radians(heading)))))

#calculate knots from calculated speed from given positioning
def getKnots(my_speed):
    #1 yard/second = 1.77745 my_knots
    #totalSpeed = math.sqrt(my_speed[0]**2 + my_speed[1]**2 + my_speed[2]**2)
    xySpeed = math.sqrt((my_speed[0])**2 + (my_speed[1]**2))
    totalSpeed = math.sqrt(xySpeed**2 + (my_speed[2])**2)
    
    print("xySpeed:     ", xySpeed)
    print("total speed: ", totalSpeed) 
    
    #totalKnots = totalSpeed * 0.592484
    totalKnots = xySpeed  *0.592484
    
    #note: incomming knots only account for xy directions
    return totalKnots


#config file variables
alertType = 'consecutive' #or 'cumulative'
alertType = 'cumulative'
alertNum = 3
alertNumTotal = 5 #only used for cumlulative (i.e. 3 out of past 5)

#def setProjPosition(proj_pos, my_speed):
def main():

    #read in settings from config file?
    
    #alerts for current position (XYZ positions, depth violation).  Proj is same alerts but for porjected position
    if(alertType == 'consecutive'):
        alerts = [np.zeros((alertNum), dtype = int)]
    elif(alertType == 'cumulative'):
        alerts = [np.zeros(alertNum, alertNumTotal)]
        
    print("alerts: ", alerts)
    
    proj_alerts = [0,0]

    #input data (x,y,z,knot,head)
    inputPosition = [0,0,0,0,0]
    
    #input time
    inputTime = datetime.datetime(1,1,1,1,1,1)
    
    #last input time
    lastTime = datetime.datetime(1,1,1,1,1,1)

    #server
    address = ('',5000)


    
    serv = Listener(address)
    while True:
        client = serv.accept()
        try:
            while True:
                #recived_data(client)
                msg = str(client.recv())
                print(msg)
                
                
                #parse data
                R = parse_data(msg, inputPosition, inputTime, lastTime) #if return 3 (no pp) reset last position?
                
                
        except EOFError as e:
            print("end of file")
            break


    
    
    

if __name__ == "__main__":
    main()


