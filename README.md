# CIS-4720-Banana Ripeness Detection
CIS*4720 Final Project Submission (README)

Program Description
======================
The assignment submission outlines the design and implementation of an algorithm in python, to isolate and recognize a banana and it's ripeness amongst regular environments.

4 different techniques: Image Segmentation, BrownSpot Analysis, and Color Analys; were used on ~350 images. The images were processed with the algorithm then a determined ripeness grade will be returned between: Not A Banana, Unripe, Yellow, Ripe, Very Ripe, Too Ripe.

Images
=========
Source Images 			        ->    "images/raw/"
Segmented Images 			   	->    "images/processed/"
Processed Images 	            -> 	  "images/brownSpot/<ripenessGrade>/"

Data
=======
The image names, banana pixel size, brownSpot% level, ripeness grade, and how long the algorithm took to run on that specific image in a text file ("testingResults.txt" when testing all images: 't' option or "singleResults.txt" when testing a single image: 'f' option).


Submission Contents
=======================
Included in this folder are:
- This README
- Final Project Report - FinalReport.pdf
- data folder
    - singleResults.txt (Results of single image are appeneded)
    - testingResults.txt (Results of all images are printed to file)
- images folder
    - Raw Images
    - Processed Segmented Images
    - BrownSpot + Color Analyzed Image
- src folder
    - Python code used:
        - main.py (algorithms to process images in addition to function that compares images to ground truth)
        - imthr_lib.py (binarizing functions) and imageIO.py (opening and closing images)
            - provided inside python toolbox given to us by Dr. Denis Nikitenko


Limitations
================
The amount of testing shows that we need to integrate shape analysis into our code so that results become more perfect. We found in our testing that images with stark backgrounds don't get segmented correctly. Images with similar foregrounds also get analyzed as bananas when they shouldn't be. 

Running Code
================
Make sure you have PIL(pillow), time, division, numpy, matplotlib, pylab, tkinter, scipy, opencv2, sys, and skimage
python packages installed to run the code.

Running Code using Makefile:
1. run 'make all' to initialize files
2. cd into the src folder as the working directory
3. 'python ./main.py' to run the program
4. Use the corresponding options for the algorithm you want to run
5. a) Enter 'f' if you want to test a single image  and enter the name of the file
   b) Enter 't' if you want to test all the included test Images
   c) Enter 'q' if you want to exit the program

Running Code through compile lines:
1. cd into the src folder as the working directory
2. 'chmod u+x main.py' & 'chmod u+x lmthr_lib.py' & 'chmod u+x imageIO.py' to initialize the python files
3. 'python ./main.py' to run the program
4. Use the corresponding options for the algorithm you want to run
5. a) Enter 'f' if you want to test a single image  and enter the name of the file
   b) Enter 't' if you want to test all the included test Images
   c) Enter 'q' if you want to exit the program
