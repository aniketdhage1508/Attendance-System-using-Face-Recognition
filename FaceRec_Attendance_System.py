import cv2                                      #importing the opencv module used to take input from input devices like camera
import numpy as np                              #importing numpy module used later in program
import face_recognition as fc                   #face recognition module on which the core of the program is based
import os                                       #OS module is used to make changes in any file directory of the system
from datetime import datetime                   #basic date time function used to check the time of attendance
import mysql.connector as mycon
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from Studentdetails import Studentdetails


class Recognise:
    def __init__(self,root):
        self.root = root
        path = 'ImagesAttendance'                       #defining the path for the database directory
        images = []                                     # making empty lists for further use
        classNames = []                                 # as above
        myList = os.listdir(path)                       # assigning the path to a variable myList and appending all the names of the images
                                                        # stored in ImagesAttendance folder
        # print(myList)
        for cl in myList :                           # Now here myList contains all the names of files
            curImg = cv2.imread(f'{path}/{cl}')     # this statement reads the image name as 'img.jpg' so to remove the '.jpg' part we use this line
            images.append(curImg)                   # appending the new names in the images list we use this
            classNames.append(os.path.splitext(cl)[0]) # this line does the same process of removing the '.jpg' from filename

        # print(classNames)

        def findEncodings(images) :         # here a function is defined as findEncodings👎
            encodeList = []             # defining an empty list
            for img in images:          # for each element in the list images this iteration will run
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      # it will convert the BGR format of images to RGB format
                encode = fc.face_encodings(img)[0]             # it will convert the RGB converted images to encodings in an array
                encodeList.append(encode)               # appending the encodings to encodeList
            return encodeList                   # returns the encoded list to the variable where it is called

        def markAttendance(name) :                  # function used to mark attendance
            with open('Attendance.csv','r+') as f :         # will open the file names 'Attendance.csv' with reading and writing right as 'r+' is given
                myDataList = f.readlines()          # readlines() is used to read each line in the csv file and give resultant output as list
                nameList = []           # creates an empty list named nameList
                for line in myDataList:        # as myDataList contains each line from the csv file in string type inside a list it will iterate through it
                    entry = line.split(',')     # here the variable entry will contain all the words from the csv file which also includes the names
                                                # of the students whose attendance is already marked
                    nameList.append(entry[0])  # all the names of students are appended in this list named nameList

                if name not in nameList:       # here we will check if the name identified by matching the face is present prior in our register if
                                                # not then its name will be registered
                    now = datetime.now()        # this uses the datetime function which we have imported earlier to enter current time in the variable
                    dtString = now.strftime('%H:%M:%S')     # the format how the time will be entered in the register as hour minute second
                    f.writelines(f'\n{name},{dtString}')       # writelines is used to write the variable value inside the csv file


        encodeListKnown = findEncodings(images)     # calling the function and then assigning the returned value to encodeListKnown
        print("Encoding Complete")                  # now this list contains all the encodings of the images in our database
        print("Starting camera")                    # inshort we can use this to match the input image if its present in database
        cap = cv2.VideoCapture(0)              # VideoCapture is used to open camera and take input

        while True :            # while true written because to make it infinite
            success, img = cap.read()           # read function from cv2 used to take input from camera
            imgs = cv2.resize(img,(0,0),None,0.25,0.25)     # resizing the input image to 25% of its original size
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)    # changing the BGR colours of input image to RGB

            facesCurFrame = fc.face_locations(imgs)     # face_locations used to find all the faces in the input image and create a box around it
            encodesCurFrame = fc.face_encodings(imgs,facesCurFrame)     # converting the image inside the face box to encodings (simply arrays)

            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):       # iteration of both encodeFace and faceLoc together
                matches = fc.compare_faces(encodeListKnown,encodeFace)      # compares the input encodings with the database and returns a True/False list
                faceDis = fc.face_distance(encodeListKnown,encodeFace)      # compares the input encodings with the database to find the best match
                # print(faceDis)
                matchIndex = np.argmin(faceDis)             # returns the index of the best match encodings from the database list

                if matches[matchIndex]:         # if the matchIndex index of the list has True value in matches list then the condition will be True
                    name = classNames[matchIndex].upper()       # classNames list contains all the names of files in database(which have the same name
                                                                # as that of students

                    y1,x2,y2,x1 = faceLoc       # as the faceLoc is list of four values which are the vertices of the square formed around the face while
                                                # camera is on it is given to variables
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4    # we multiply the values by 4 to get the original frame which we have resized to 25% earlier
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)  # it forms a rectangle at the four points which is basically around the face
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)  # these lines are just to adjust the box around face and show name
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)        # in it
                    markAttendance(name)        # calling the markAttendance function to insert name inside the csv file

                else :
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0),cv2.FILLED)
                    cv2.putText(img, "UKNOWN FACE", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


            cv2.imshow('Webcam',img)    # command to show what input is being taken
            key = cv2.waitKey(1)      # to make the camera frame static
            if key == ord('x'):
                # cv2.quit('Webcam')
                # cap.release()
                # cv2.destroyALlWindows()
                break


if __name__ =="__main__":
    root=Tk()
    obj = Recognise(root)
    root.mainloop()
