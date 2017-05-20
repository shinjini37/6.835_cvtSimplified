# cvtSimplified

Author: Shinjini Saha

For 6.835 Intellegent Multimodal User Interfaces

## To Run:

### Basics:
You will need:
1. Python 2.7 (2.7.13)
2. OpenCV 3 (3.2.0)
3. Numpy (1.11.3)
4. Scipy (0.19.0)
5. Matplotlib (1.5.3)

The versions used in the project are listed in parenthesis. The latest versions of the libraries should also work. Numpy, scipy and matplotlib can be downloaded using pip, which comes with the latest download of python 2.7.

You can download OpenCV 3 from https://sourceforge.net/projects/opencvlibrary/

For Windows, after downloading: 
1. Extract it
2. Go to opencv\build\python\2.7
3. Go to x64 or x86 based on your Windows type
4. Copy cv2.pyd
5. Go to where your python is downloaded
6. Finally, go to Python27\Lib\site-packages and paste cv2.pyd

### Proper version:
This is the full version of the current application. This has the core fuctionality of detecting lines and circles, but also comes with the added features of easy uploading, and of allowing the user to manually select the corners of the page and run the algorithm again (useful in case the algorithm messed up by itself).

You will need node.js, available from https://nodejs.org/en/download/

After installing, make sure node.js is in your path. For Windows, the path variable is C:\Users\username\AppData\Roaming\npm

Then, from the commandline:
1. Go to the folder containing the downloaded project (the folder with this README)
2. Type "npm install" (without quotes) and press enter (this downloads necessary packages to run the application)
3. Type "npm start" (without quotes) and press enter (this starts the application)
4. Go to localhost:3000 from your browser, where you will see the application running

### Core version:
This is the core of the application, with the line and circle detection. This involves inputting the image manually into the main python script and outputs the results as an image. 


1. Open python/main.py in any editor
2. Comment out "testing = False" (line 21) and
3. Put the pathname of the desired file instead of "path = 'test_lib/crop_6.jpg'" (line 27)
4. Run main.py

(Be sure to close the display window before running the script again, or else the program will pretend to crash.)

## Interpretation:
The yellow/cyan lines are the detected lines and the purple circles are the detected circles.