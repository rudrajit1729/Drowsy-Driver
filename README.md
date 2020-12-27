# Drowsiness & Yawn detection

Drowsiness and Yawn detection to alert drivers.

## Dependencies

1. Python 3
2. opencv
3. dlib
4. imutils
5. scipy
6. numpy
7. argparse
8. pyttsx3



## Setup

Create a virtual environment using 

`conda create -n virenv`

Anaconda installation: [Click Here](https://docs.anaconda.com/anaconda/install/)

Activate virtual environment:

`conda activate virenv`

Install dependencies

`pip install -r requirements.txt`

Install dlib(CPP package) --> `conda install -c conda-forge dlib`

## Run 

```
python main.py --webcam 0	//For external webcam, use the webcam number accordingly
```

## Settings

Change the threshold values according to distance from camera
```
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 30
YAWN_THRESH = 10`	//change this according to the distance from the camera
```

## Authors

**Rudrajit Choudhuri** 







