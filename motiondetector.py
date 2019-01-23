#importing required packages
from imutils.video import VideoStream
import argparse
import datetime
import time
import timeit
import cv2
import imutils



#constructing argument parser and parsing arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help ="path to video file")
ap.add_argument("-a", "--min-area", type=int, default = 700, help = "minimum area size or change in pxiels to be detecting for motion")
args = vars(ap.parse_args())

#if video argument is none, then we take webcam live stream source
if args.get('video', None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

#otherwise, read in actual video file or ip source
else:
    vs = cv2.VideoCapture(args["video"])
    fps = vs.get(cv2.CAP_PROP_FPS)
    print(fps)

#initialize first video frame
firstFrame = None
occupy_frame = 0


#start basic motion detection
#first loop over all frames of video

while True:
    #grab current frame, and check whether occupied or unoccupied

    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "unoccupied"

    #ie: read current frame of video stream. Default state of frame is unoccupied, assumption is that the first frame is background.

    if frame is None:
          break
    #if current read frame does not exist, means we are at the end of our vide file, thus exit operation

    frame = imutils.resize(frame,width = 720)
    #resizing file, convert to grayscale and blur it
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #take current frame, and convert to grayscale
    grayscale = cv2.GaussianBlur(grayscale, (21,21),0 ) # we apply gaussian blur to remove noise, number denotes extent of blur

    # we assume that the first frame is the base state, and unchanging. Thus we will store this first frame as reference and continue to
    #process the next frame

    #requires that first frame be representative of background, and there is no ongoing motion
    if firstFrame is None:
        firstFrame = grayscale
        continue

    #compute difference between current analysed frame and first frame. We are measuring differences in pixel intensities here.
    frameDelta = cv2.absdiff(firstFrame,grayscale)
    threshold = cv2.threshold(frameDelta, 80, 255, cv2.THRESH_BINARY)[1]
    #here we set thresholds for what is a SIGNIFICANT CHANGE IN PIXEL INTENSITY, if delta < 25, we discard the pixel and set to background,
    #otherwise, we set as a the foerground in white.

    #dilate thresholded image, fill in holes and draw around contours
    threshold = cv2.dilate(threshold, None, iterations = 2)
    contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #grabbing contours and drawing
    contours = imutils.grab_contours(contours)

    #looping over contours and drawing box
    for c in contours:

        #if the present contour is smaller than our set minimum area threshold for motion detection, ignore, text stays unoccupied. otherwise draw box.
        if cv2.contourArea(c) < args["min_area"]:
            continue
        #x coord, y coord, width and height
        (x,y,w,h) = cv2.boundingRect(c)
        #draw rectange direct on frame, from bottom left corner. with w = width, h = height
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        #update text to occupied
        text = "Occupied"

    if text == "Occupied":
        occupy_frame = occupy_frame + 1
        print(occupy_frame)
    #drawing text and timestamp on video
    cv2.putText(frame,"Cage status:{}".format(text), (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
    cv2.putText(frame, datetime.datetime.now().strftime("%d-%m-%y %H:%M%p"), (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255),1)

    #show frame and record if user presses a key
    cv2.imshow("Marmobox feed",frame)
    cv2.imshow("thresh", threshold)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

print('Total occupied frames: ', occupy_frame)
print('Total time interaction with test(s): ', occupy_frame / fps)
vs.stop() if args.get("video",None) is None else vs.release()
cv2.destroyAllWindows()


