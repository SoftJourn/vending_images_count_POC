# vending_images_count_POC
Program to detect the fact that there is something in the vending machine's tray AND count the number of item in the tray

On the common network share you can find an archive with photos /common/POC/pictures-machine.zip
Those are the set of photos "before" and "after" the transaction in the vending machine.

The challenge is:
1. Write a program to detect the fact that there is something in the tray
2. Program should run in the cloud(eg. two images input) or Raspberry Pi
3. Program will be able to tell the number of item in the tray.

LICENSE.txt is a MIT license
***************************************************************************************
RUN (usage):
./compare2im.sh -b before.jpg -a after.jpg

Dependencies:

sudo apt-get install imagemagick python-opencv

pip install scikit-image

pip install imutils

pip install numpy
