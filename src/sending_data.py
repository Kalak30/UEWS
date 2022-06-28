from multiprocessing.connection import Client
import time

def sendMessage(total_message):
    c.send(total_message)
    time.sleep(2)





c = Client(('localhost', 5000))




#read in from file
#read line by line, cat each line to total string
#stop once you reach <rsdf >
 #send the total string to logic-reciving-data
 #wait 2 seconds???
 #start reading again, repeat
 
             

with open('../Test Data/projection_test.txt') as f:
    total_message = ""
    #for i in range(0,35):
    while True:
        line = f.readline()
        if not line: 
            break
        #print(line)  \
        #try parsing by checksum
        #print("\n", line[0:2], "\n")
        total_message = total_message + line
        #print("message so far: ", total_message)
        if (line[0:2] == "CS"):
            print("end of message, sending")
            sendMessage(total_message)
            total_message = ""
            

