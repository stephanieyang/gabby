import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import numpy as np
import cv2
import os
import subprocess
import webbrowser
import pynput
from pynput import mouse
from pynput.mouse import Listener
from pynput.mouse import Button

DEBUG = True
WILL_RECYCLE = False
global WAITING_START
global WAITING_CHOICE
WAITING_START = True
WAITING_CHOICE = False

print "Hi, my name is Gabby!"

if DEBUG:
    print "Setting up click listener..."

def on_click(x,y,button,pressed):
    global WAITING_START
    global WAITING_CHOICE
    if not (WAITING_CHOICE or WAITING_START):
        time.sleep(1)
    if pressed and WAITING_START:
        WAITING_START = False
    elif pressed and WAITING_CHOICE:
        print(button)
        if button == mouse.Button.left:
            WILL_RECYCLE = True
            WAITING_CHOICE = False
        elif button == mouse.Button.right:
            WILL_RECYCLE = True
            WAITING_CHOICE = False


listener = Listener(on_click=on_click)

listener.start()

#with Listener(on_click=on_click) as listener:
#    print "part 2"
#    #listener.join()
#    listener.start()

while True:
    print "Please click the mouse to begin."

    while WAITING_START:
        time.sleep(1)
    WAITING_START = False

    if DEBUG:
        print "Capturing camera image..."

     # get camera content
    cap = cv2.VideoCapture(0)
    captured = False
    time.sleep(1)
    while(not captured):
        # Capture frame-by-frame
        ret, frame = cap.read()


        # Save the resulting frame
        cv2.imwrite('test.png',frame)
        captured = True
        break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    timestamp = time.time()


    if DEBUG:
        print "Identifying item..."

    # run image recognition on saved image
    os.system("python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=./test.png > output.txt")

    # dictionary definitions
    abbreviations = {"aluminum cans":"ALU","cardboard":"CBD","glass bottles":"GLS","paper":"PAP","PTB":"plastic bottles"}
    recLines = {"aluminum cans":0,"cardboard":1,"glass bottles":2,"paper":3,"plastic bottles":4}


    # read in recognition info
    with open('output.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    f.close()

    # check fourth line for item class
    content = [x.strip() for x in content]
    scoredItem = content[3]
    sep = ' ('
    item = scoredItem.split(sep, 1)[0]

    if DEBUG:
        print "Item identified: " + item

    print "I see you have an item that I think fits under the category: " + item

    # read in records for later update
    with open('records.txt') as f:
        content = f.readlines()
    f.close()

    if DEBUG:
        print "content = ", content

    def weekDifference(dt1,dt2):
        week = timedelta(7) # 7 days
        return ((dt2 - dt1) >= week)

    # comparing previously recorded time to current time - want to refresh records every Monday 12 AM
    oldTimestamp = content[5]
    oldDatetime = datetime.fromtimestamp(float(oldTimestamp))
    currentDatetime = datetime.fromtimestamp(timestamp)
    if((currentDatetime.weekday() < oldDatetime.weekday()) or (weekDifference(oldDatetime, currentDatetime))):
        if DEBUG:
            print "Clearing record..."
        content = ['ALU 0\n', 'CBD 0\n', 'GLS 0\n', 'PAP 0\n', 'PTB 0\n', '0']

    # copy of the original content
    newContent = [x for x in content]

    line = newContent[recLines[item]]
    itemCount = int(line[4])
    #itemCount = newContent[abbreviations[item]]
    print "This week you have recycled " + str(itemCount) + " of these items"
    if itemCount == 2:
        print "Video placeholder"
        #webbrowser.open('https://www.youtube.com/embed/eylzazKebD8?autoplay=1', new=0, autoraise=True)
    elif itemCount == 5:
        print "Video placeholder 2"
        #webbrowser.open('https://www.youtube.com/embed/eylzazKebD8?autoplay=1', new=0, autoraise=True)
    elif DEBUG:
        #pass
        print "No video"


    print "Do you want to keep this item instead of recycling it? Left-click for yes, right-click for no."

    WAITING_CHOICE = True
    while WAITING_CHOICE:
        time.sleep(1)

    #answer = raw_input("Do you want to keep this item instead of recycling it? (y/n): ")
    #WAITING_CHOICE = False
    if not WILL_RECYCLE:
        print "Thank you!"
    else:
        # editing item counts
        line = newContent[recLines[item]]
        newCount = itemCount + 1
        line = line[0:4] + str(newCount) + "\n"
        newContent[recLines[item]] = line
        #str(int(count) + 1)

        # update most recent timestamp
        newContent[5] = str(timestamp)
        if DEBUG:
            print "newContent = ", newContent
        print "You have now recycled " + str(newCount) + " items in the " + item + " category."

        # write record info to file
        f = open('records.txt', 'w+')
        for line in newContent:
            f.write(line)
        f.close()
    #webbrowser.open('https://www.youtube.com/embed/eylzazKebD8?autoplay=1', new=0, autoraise=True)

    print "Have a good day!"

    WAITING_START = True
    WAITING_CHOICE = False
