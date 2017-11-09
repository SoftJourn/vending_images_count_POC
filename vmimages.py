from skimage import measure
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the cropped input diff file")
ap.add_argument("-a", "--originAfter", required=True, help="path to the original image_after output file")
ap.add_argument("-b", "--originBefore", required=True, help="path to the original image_before output file")
args = vars(ap.parse_args())

##### crop,  top-left: x=340, y=210
dx_origin=340
dy_origin=210

# crop bottom-right: x=740, y=360
##### new cropped size 400 x 150

image = cv2.imread(args["image"])
origin_after = cv2.imread(args["originAfter"])
origin_before = cv2.imread(args["originBefore"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

##### threshold the image to reveal light regions in the blurred image
thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

##### removing small blobs of noise from the thresholded image (erode x2, dilate x4)
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)


# perform a connected component analysis on the thresholded image,
labels = measure.label(thresh, neighbors=8, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")

# loop over the unique components
for label in np.unique(labels):
    # if this is the background label, then ignore it
    if label == 0:
        continue

    # otherwise, construct the label mask and count the number of pixels
    labelMask = np.zeros(thresh.shape, dtype="uint8")
    labelMask[labels == label] = 255
    numPixels = cv2.countNonZero(labelMask)

    # Initialize a mask to store only the "large enough" objects.
    # If the number of pixels in the object is sufficiently large, then add it to the mask of "large blobs"
    if numPixels > 300:
        mask = cv2.add(mask, labelMask)

# find the contours in the mask, then sort them from left to right
cntrs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cntrs = cntrs[0] if imutils.is_cv2() else cntrs[1]
count = len(cntrs)
sys.stdout.write("Items count:"+str(count)+"\n")

if count > 0:
    cntrs = contours.sort_contours(cntrs)[0]
    for (i, c) in enumerate(cntrs):
        # draw the bright spot on the image
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 255, 0), 1)
        cv2.circle(origin_after, (int(cX + dx_origin), int(cY + dy_origin)), int(radius), (0, 255, 0), 1)
        cv2.putText(image, "{}".format(i + 1), (x + 25, y + 25), cv2.FONT_HERSHEY_DUPLEX, 0.45, (0, 255, 0), 1)
        cv2.putText(origin_after, "{}".format(i + 1), (x + dx_origin + 25, y + dy_origin + 25), cv2.FONT_HERSHEY_DUPLEX, 0.45, (0, 255, 0), 1)

cv2.imshow("Input diff image", image)
cv2.imshow("Processed diff image", thresh)
cv2.imshow("Original image_before output file", origin_before)
cv2.imshow("Original image_after output file", origin_after)
cv2.waitKey(0)

sys.exit(0)
