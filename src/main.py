#Banana Ripeness Detection
#Kevin Pirabaharan (0946212), Ena So (0961375), Muhammad Jaffar (0911910)
#This program creates and segments bananas from images and detects brown spots
# on the banana to determine the ripeness of the bananas.
from imageIO import *
from imthr_lib import*
from PIL import Image
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
import matplotlib.cm as cm 
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt


# Function: Loading Bar
# 
# Loading bar function to print a visual progress of tasks
#
# Parameters:
# (in)    count,total,size     :  progress so far; total tasks to accomplish; size of loading bar pixels
#
def loadingBar(count,total,size):
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + ']')

# Function: Difference
#
# The function finds the absolute difference between two numbers
#
# Parameters:
# (in)    a,b  :  The two numbers being compared
# (out)   diff :  Returns the difference of the two inputted numbers
def difference(a,b):
    diff = abs(a-b)
    return diff

# Function: Color Analysis
#
# The function takes in an image and determines to output the blue-green channel ranges of the image
# this ratio will be used to distinguish between green/blue bananas vs other colors
#
# Parameters:
# (in)    brownImagePath :  file path of the image of the segmented image to be color analyzed
# (out)   avg            :  Returns the average green/blue channel ratio of the image
def colorAnaysis(brownImagePath):
    #Declaring varaiables for image attributes
    r, g ,b = imread_colour(brownImagePath)
    im = Image.open(brownImagePath)
    height, width = im.size

    #Using otsu to find banana vs non-banana pixels 
    thr = otsu(b)
    imgBlueOtsu = im2bw(b,thr)
    
    # Goes through the image pixel by pixel; if the pixel isnt white (background or brownspot)
    # The ratio of the green-blue channls are added a list, appends 0 to avoid divide by 0 errors
    ratio = []
    for i in range(0, width-1):
        for j in range(0, height-1):
            if imgBlueOtsu[i,j] != 255:
                if (b[i,j] > 0):
                    ratio.append(float(g[i,j] / b[i,j]))
                else:
                    ratio.append(0)

    # The average green/blue ratio for the image is calculated and returned
    # Theoretically, the higher the avg; the greener the image is
    avg = float(sum(ratio) / len(ratio))
    
    return avg

# Function: Image Segmentation
#
# The function takes in an image and aims to segment the banana out, exporting a .png with just the bananaand the background turned to black
#
# Parameters:
# (in)    imagePath, imageName, output :  file path of the image; fileName; datafile to print results of the function
# (out)   object[bananaSA, filePath]   :  Returns an object containing the banana's total pixel size and the file path of the processed image
def imageSegment(imagePath, imageName, output):
    
    #start timer for the function
    startDT = datetime.datetime.now()

    #initialize color channels and size variables
    object = []
    im = Image.open(imagePath)
    height, width = im.size
    img = cv2.imread(imagePath)
    r, g ,b = imread_colour(imagePath)
    red, green, blue = imread_colour(imagePath)
    rB = np.zeros((width,height))
    gB = np.zeros((width,height))
    bB = np.zeros((width,height))
    bananaSA = 0

    # The blue channel is binarized since this channel is where the colors of 
    # a banana (green - yellow) should show up most in 
    thr = otsu(b)
    imgBlueOtsu = im2bw(b,thr)

    #the Black and White image is looked at pixel by pixel
    #the black pixels of the the image are saved as the color of the original image, whilst the rest of the image is saved as white pixels
    #this allows the banana to keep it's color while the rest of the image is whiteness
    for i in range(0, width-1):
        for j in range(0, height-1):
            if imgBlueOtsu[i,j] != 255:
                rB[i,j] = red[i,j]
                gB[i,j] = green[i,j]
                bB[i,j] = blue[i,j]
                bananaSA += 1
            else:
                rB[i,j] = 255
                gB[i,j] = 255
                bB[i,j] = 255

    #Image is saved and total time taken, total pixel size are all written to a text file
    imwrite_colour("../images/processed/" + imageName.rsplit('.', 1)[0] + '.png', rB, gB, bB)
    object.append(bananaSA)
    object.append("../images/processed/" + imageName.rsplit('.', 1)[0] + '.png')
    
    endDT = datetime.datetime.now()
    currentDT = endDT - startDT
    output.write(imageName + ": \tTime Taken: " + str(currentDT) + "\tBanana Size: " + str(bananaSA) + "\t")
   
    #Returns the surface area and file path of the banana image as one object for BrownSpot Analysis
    return object

# Function: Brown Spot Analysis
#
# The function takes in the segmented image and aims to check for and segment brown
# spots to determine the ripeness level of the banana
# 
# Parameters:
# (in)    imagePath, imageName, output :  file path of the image; fileName; datafile to print results of the function
# (out)   ripenessLevel                     :  Returns the surface area of the banana in pixels
def brownSpotAnalysis(bananaSize,imagePath, output):
    # Variables delared and ripeness lvl initialized for "Not Banana"
    global tempFile
    ripenessLvl = 5
    im = io.imread(imagePath)
    brownSpots = 0

    # Segmented image is converted to lab color space
    # The B* and A* lab channels are compared to check for the colors yellow, green, and brown
    # a difference of <25 indicates browness. These pixels are set to white so that only the banana pixels remain
    lab_color = color.rgb2lab(im)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if difference(lab_color[i, j][0], lab_color[i, j][1]) < 25 and difference(lab_color[i, j][1], lab_color[i, j][2]) < 25: # it is brown spot
                if im[i, j][0] != 255 and im[i, j][1] != 255 and im[i, j][2] != 255:
                    im[i, j][0] = 255
                    im[i, j][1] = 255
                    im[i, j][2] = 255
                    brownSpots += 1
    
    # Brown spot to banana SA percentage is calculated and calls for color analysis
    brown = ((float(brownSpots) / float(bananaSize)) * 100)
    misc.imsave(tempFile, im)
    avg = colorAnaysis(tempFile)

    # Based on brownspot percentages, the images will be organized into their respective ripeness grades
    if (avg >= 1.10 and avg <= 40.00) and (avg >= 0.300 and avg <= 100.00):
        # Because yellowed and green unripe bananas may have the same number of brownspots,
        # the color analysis average will be used to seperate yellow (< 4 g/b ratio) and green
        if (brown > 0.30 and brown < 14.00):
            if (avg < 4.00):
                misc.imsave("../images/brownSpot/yellowed/brownSpot_" + os.path.basename(imagePath), im)
                ripenessLvl = 1
            else:
                misc.imsave("../images/brownSpot/un_Ripe/brownSpot_" + os.path.basename(imagePath), im)
                ripenessLvl = 0
        elif (brown >= 14.00 and brown < 30.00):
            misc.imsave("../images/brownSpot/ripe/brownSpot_" + os.path.basename(imagePath), im)
            ripenessLvl = 2
        elif (brown >= 30.00 and brown < 70.00):
            misc.imsave("../images/brownSpot/very_Ripe/brownSpot_" + os.path.basename(imagePath), im)
            ripenessLvl = 3
        elif (brown >= 70.00):
            misc.imsave("../images/brownSpot/over_Ripe/brownSpot_" + os.path.basename(imagePath), im)
            ripenessLvl = 4
        else:
            misc.imsave("../images/brownSpot/not_Banana/brownSpot_" + os.path.basename(imagePath), im)
    else:
        misc.imsave("../images/brownSpot/not_Banana/brownSpot_" + os.path.basename(imagePath), im)
    
    # Based on brownspot and color analysis, a ripeness level will be determined and the image will be 
    # saved in the corresponding folder.
    output.write("Brown spot: " + str(((float(brownSpots) / float(bananaSize)) * 100)) + " %" + "\t\t" + str(avg))
    return ripenessLvl

#Program loop to run the program
tempFile = "hsv.jpg"
inputFolder = "../images/raw/"
ripeGrade = ["Unripe", "Yellow", "Ripe", "Very Ripe", "Too Ripe/Going Bad", "Not a Banana"]
progExit = False

# Command loop to take in user input of how they want to process images, will end when user chooses to quit
while (progExit == False):
    fileCount = 0
    obj = []
    if os.path.exists(tempFile):
       os.remove(tempFile)
    inp = raw_input("Execute Algorithm on a single (F)ile, Run (T)est Suite, (Q)uit? ")

    #This option is to only process a single image at a time, returning in command-line feedback with the option to look at a text file
    if (inp == 'f') or (inp == 'F'):
        print("Make sure the image is inside the \'image/raw/\' folder\n")
        fileName = raw_input("Enter File Name: ")
        if os.path.exists(inputFolder + fileName):
            singleData = open("../data/singleResults.txt", 'a+')
            startDT = datetime.datetime.now()
            obj = imageSegment(inputFolder + fileName, fileName, singleData)
            bananaSize = obj[0]
            ripenessLvl = brownSpotAnalysis(bananaSize, obj[1], singleData)
            endDT = datetime.datetime.now()
            currentDT = endDT - startDT

            print ("\nThe image: " + fileName + " is " + ripeGrade[ripenessLvl] + "\nTime Taken: " + str(currentDT) + "\nCheck \'../data/singleResults\' for more details.\n") 
            singleData.close()
        else:
            print("\nThat file/directory does not exist, please import the image into the \'image/raw/\' folder or double check the spelling and try again.\n")

    #This option is to only process every .jpg image inside the ../images/raw directory, returning all the processing information in a text file
    elif (inp == 't') or (inp == 'T'):
        print("Testing Algorithms...")
        data = open("../data/testingResults.txt", 'w+')
        startADT = datetime.datetime.now()
        
        for file in glob.glob(inputFolder + "*.jpg"):
            fileCount += 1
            fname = os.path.basename(file)
            print("")
            obj = imageSegment(inputFolder + fname, fname, data)
            bananaSize = obj[0]
            ripenessLvl = brownSpotAnalysis(bananaSize, obj[1], data)
            data.write("\t\t" + str(ripeGrade[ripenessLvl]) + "\n")
            loadingBar(fileCount,len(glob.glob(inputFolder + "*.jpg")),2)
        
        data.close()
        endADT = datetime.datetime.now()
        currentADT = endADT - startADT
        print ("\nDone!\n Total time taken: " + str(currentADT) + "\nTo look at results check the \"..\data\\testingResults.txt\" file.\n")

    # For users to quit the program
    elif (inp == "q") or (inp == "Q"):
        print("Ending Program...\n")
        progExit = True

    else:
        print("Please check your input\n")
