from imageIO import *
from imthr_lib import*
from PIL import Image
import cv2
import datetime
import glob
import os
import sys
import cv2
from skimage import io, color
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import color
from skimage import io
from scipy import ndimage, misc
import matplotlib.cm as cm #
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt # import


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def dummyFunc ():
    inputFolder = "../data/"
    fileCount = 0

    data = open("results_of_Comp_Medium.txt", 'w')
    Davg = 0
    DMAX = 0
    DMIN = 0
    avg = 0
    MAX = 0
    MIN = 0
    Dlists = []
    lists = []
    diff = []

    f = open("../data/dumdum5.txt", "r")
    for x in f:
        if (len(x) > 80): 
            if (is_number(x[69:82])):
                it = float(x[69:82])
                lists.append(it)
    if(len(lists) > 0):
        avg = sum(lists) / float(len(lists))
        MAX = max(lists)
        MIN = min(lists)
        print("../data/dumdum5.txt" + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))
        data.write("../data/dumdum5.txt" + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN) + "\n")
    
    print(str(lists) + "\n size is: " + str(len(lists)))
    
    f = open("../data/segmentationResultsM.txt", "r")
    for x in f:
        if (len(x) > 80): 
            if (is_number(x[69:82])):
                io = float(x[69:82])
                Dlists.append(io)
    if(len(Dlists) > 0):
        Davg = sum(Dlists) / float(len(Dlists))
        DMAX = max(Dlists)
        DMIN = min(Dlists)
        print("../data/segmentationResultsM.txt" + ": \t avg = " + str(Davg) + "\t Max: " + str(DMAX) + "\t Min: " + str(DMIN))
        data.write("../data/segmentationResultsM.txt" + ": \t avg = " + str(Davg) + "\t Max: " + str(DMAX) + "\t Min: " + str(DMIN) + "\n")
    
    print(str(Dlists) + "\n size is: " + str(len(Dlists)))

    for i in range(len(Dlists)):
        diff.append(Dlists[i] - lists[i])

    if(len(diff) > 0):
        print("diff" + ": \t avg = " + str( sum(diff) / float(len(diff))) + "\t Max: " + str(max(diff)) + "\t Min: " + str(min(diff)))
        data.write("diff" + ": \t avg = " + str( sum(diff) / float(len(diff))) + "\t Max: " + str(max(diff)) + "\t Min: " + str(min(diff)) + "\n")

        
    data.close()

def brownSportResults ():
    inputFolder = "../data/"
    fileCount = 0

    data = open("results_of_Results.txt", 'w')
    for file in glob.glob(inputFolder + "*.txt"):
        lists = []
        fileCount += 1
        fname = os.path.basename(file)
        print("")
        avg = 0
        MAX = 0
        MIN = 0
        f = open(file, "r")

        for x in f:
            if (len(x) > 80):
                offset = 87 - len(x)
                # print(x[70-offset:81-offset])
                if (is_number(x[70-offset:81-offset])):
                    it = float(x[70-offset:81-offset])
                    lists.append(it)
        # print(str(lists) + "\n size is: " + str(len(lists)))
        if(len(lists) > 0):
            avg = sum(lists) / float(len(lists))
            MAX = max(lists)
            MIN = min(lists)
            print(file + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))
            data.write(file + ": \t avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))
                    
    data.close()


def colorAvg():
    fileCount = 0
    lists = []
    data = open("results_of_ColorsVR.txt", 'w')
    avg = 0
    MAX = 0
    MIN = 0
    f = open("../data/green_Blue_RatioVERYRIPEFOLDER.txt", "r")

    for x in f:
            if (is_number(x[0:4])):
                it = float(x[0:4])
                lists.append(it)
    # print(str(lists) + "\n size is: " + str(len(lists)))
            if (it > 15):
                print(it)

    if(len(lists) > 0):
        avg = sum(lists) / float(len(lists))
        MAX = max(lists)
        MIN = min(lists)
        print("avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))
        data.write("avg = " + str(avg) + "\t Max: " + str(MAX) + "\t Min: " + str(MIN))
    data.close()


op = raw_input("Enter a thing:")

if (op == '1'):
    # colorAvg()
    dummyFunc()

elif (op == '2'):
    brownSportResults()

else: 
    print("You dun screwed up")