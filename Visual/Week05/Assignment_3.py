#!/usr/bin/env python
# coding: utf-8

# ## Assignment 3 - Edge detection

# __Finding text using edge detection__
# 
# The purpose of this assignment is to use computer vision to extract specific features from images. In particular, we're going to see if we can find text. We are not interested in finding whole words right now; we'll look at how to find whole words in a coming class. For now, we only want to find language-like objects, such as letters and punctuation.
# 
# Download and save the image at the link below:
# 
# https://upload.wikimedia.org/wikipedia/commons/f/f4/%22We_Hold_These_Truths%22_at_Jefferson_Memorial_IMG_4729.JPG
# 
# Using the skills you have learned up to now, do the following tasks:
# 
# - Draw a green rectangular box to show a region of interest (ROI) around the main body of text in the middle of the image. Save this as image_with_ROI.jpg.
# - Crop the original image to create a new image containing only the ROI in the rectangle. Save this as image_cropped.jpg.
# - Using this cropped image, use Canny edge detection to 'find' every letter in the image
# - Draw a green contour around each letter in the cropped image. Save this as image_letters.jpg
# 
# __TIPS__
# - Remember all of the skills you've learned so far and think about how they might be useful
# - This means: colour models; cropping; masking; simple and adaptive thresholds; binerization; mean, median, and Gaussian blur.
# - Experiment with different approaches until you are able to find as many of the letters and punctuation as possible with the least amount of noise. You might not be able to remove all artifacts - that's okay!

# __Libraries__

# In[1]:


import os
import sys
import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


# __Used functions__

# I have had some issues importing jimshow and jimshow_channel from utils as i keep getting error messages. Therefore, I have copied the functions so that they can be used anyway.

# In[4]:


def jimshow(image, title=False):
    """imshow with matplotlib dependencies 
    """
    # Acquire default dots per inch value of matplotlib
    dpi = mpl.rcParams['figure.dpi']

    height, width, depth = image.shape
    figsize = width / float(dpi), height / float(dpi)
    
    plt.figure(figsize=figsize)
    
    if depth == 1:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      
    if title:
        plt.title(title)
    plt.axis('off')
    
    plt.show()

def jimshow_channel(image, title=False):
    """
    Modified jimshow() to plot individual channels
    """
    # Acquire default dots per inch value of matplotlib
    dpi = mpl.rcParams['figure.dpi']

    height, width = image.shape
    figsize = width / float(dpi), height / float(dpi)
    
    plt.figure(figsize=figsize)
    
    plt.imshow(image, cmap='gray')
      
    if title:
        plt.title(title)
    plt.axis('off')
    
    plt.show()


# __Image path__

# In[5]:


# Define the path were the image is located
image_path = os.path.join("..", "data", "We_Hold_These_Truths_at_Jefferson_Memorial.JPG")


# In[68]:


# image is now defined by reading the path
image = cv2.imread(image_path)


# In[7]:


# Checking the image
jimshow(image, "original image")


# ## Region of interest

# To do:
# - Draw a green rectangular box to show a region of interest (ROI) around the main body of text in the middle of the image. 
# - Save this as image_with_ROI.jpg.

# In[51]:


# I check the image shape. This is not nessecary but I like to have an idea about the dimensions
image.shape


# In[52]:


# I now find the centers of the x and y axes. 
# The centers are defined by dividing the width(x) and height(y) by two.
(centre_x, centre_y) = (image.shape[1]//2, image.shape[0]//2)


# In[69]:


# I find the region of interest by by having the two centers as a starting point. 
# From here, the distance from the center and out to the frame of the ROI is subtracted or added depending on whether it is on the right or left side of the ROI.
ROI = cv2.rectangle(image, (centre_x-1000, centre_y-1000), (centre_x+1000, centre_y+1500), (0,255,0), 3)
#The last two elements refer to the color, namely green, and the thickness of the line that makes up the ROI, namely 3 pixels.


# In[70]:


jimshow(ROI)


# __Save ROI__

# In[71]:


# I define the path were the image is going to be stored. 
outfile_ROI = os.path.join("..", "data", "image_with_ROI.jpg")
# Save the image 
cv2.imwrite(outfile_ROI, ROI)


# ## Crop the image

# To do:
# - Crop the original image to create a new image containing only the ROI in the rectangle. 
# - Save this as image_cropped.jpg

# In[49]:


# Read the image with the region of interest as ROI
ROI = cv2.imread(outfile_ROI)


# In[76]:


# I have tried some different approaches but ended up cropping the image by using a feature from np.array
# NB: the order of values is different from when I found the ROI. This time I had to combine it as: start_y:end_y and start_x:end_x
cropped = ROI[centre_y-1000:centre_y+1500, centre_x-1000:centre_x+1000]


# In[77]:


# Checking the cropped image
jimshow(cropped)


# __Save cropped__

# In[78]:


# Define the path were the cropped image will be saved
outfile_cropped = os.path.join("..", "data", "image_cropped.jpg")
# Save the cropped image
cv2.imwrite(outfile_cropped, cropped)


# ## Canny edge detection

# To do:
# - Using this cropped image, use Canny edge detection to 'find' every letter in the image

# In[81]:


# Read the cropped image
cropped = cv2.imread(outfile_cropped)


# __Making image greyscale__

# In[82]:


# Making the cropped image grey scale.
grey_image = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)


# In[83]:


# Check the grey image
jimshow_channel(grey_image)


# __Blur the image__

# In[84]:


# I use the Gaussian blur to blur the cropped, grey image
blurred = cv2.GaussianBlur(grey_image, (5,5), 0)


# In[85]:


# Show the blurred image
jimshow_channel(blurred)


# __Canny edge detection__ 

# In[123]:


# I use canny edge detection to detect the letters 
canny = cv2.Canny(blurred, 115, 150) 
# I tried some differnt min and max values. 
# If the values are lower, the outlines of the bricks are clearer
# If the values are higher, some of the letters was ignorred 


# In[124]:


# Show the detected edges 
jimshow_channel(canny)


# ## Contours

# To do:
# - Draw a green contour around each letter in the cropped image. 
# - Save this as image_letters.jpg

# In[125]:


# I find the contours on the canny edge detected image 
(contours, _) = cv2.findContours(canny.copy(),
                 cv2.RETR_EXTERNAL,
                 cv2.CHAIN_APPROX_SIMPLE)


# In[128]:


# I apply the contours
cropped_contour = cv2.drawContours(cropped.copy(), # The contours are applied on the cropped image
                         contours,
                         -1,       # We want all the "letters" to be marked, so we choose the value -1, where a possitive value are refering to an 'index'/an individual letter 
                        (0,255,0), # The contours will be green
                         2)        # the thickness of the markings will be two pixels


# In[129]:


# Check the contours on the cropped image
jimshow(cropped_contour)


# __Save contoured image__

# In[130]:


# Define the path were the contoured image will be saved
outfile_contoured = os.path.join("..", "data", "image_letters.jpg")
# Save the contoured image
cv2.imwrite(outfile_contoured, cropped_contour)

