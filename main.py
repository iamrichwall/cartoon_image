from email import message
import sys
import os
import cv2 as cv
from cv2 import cvtColor
import easygui 
import imageio
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import datetime

top = tk.Tk()
top.geometry('400x400')
top.title('Cartnoon')
top.configure(background ='white')
label = Label(top, background='#cdcdcd', font = ('calibri', 20, 'bold'))



""" fileopenbox opens the box to choose file and help us store file path as string"""
def upload():
    image_path = easygui.fileopenbox()
    cartoonify(image_path)
    
    
def cartoonify(image_path):
    original_image = cv.imread(image_path)
    original_image = cv.cvtColor(original_image, cv.COLOR_BGR2RGB)
    
    if original_image is None:
        print('Can not find any image. Choose appropriate file')
        sys.exit()
        
    resize_1 = cv.resize(original_image, (960, 540))
    
    #converting an image to grayscale
    gray_scale_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
    resize_2 = cv.resize(gray_scale_image, (960, 540))
    
    #applying median blur to smoothen an image
    smooth_gray_scale = cv.medianBlur(gray_scale_image, 5)
    resize_3 = cv.resize(smooth_gray_scale, (960, 540))
    
    #retrieving the edges for cartoon effect
    get_edge = cv.adaptiveThreshold(smooth_gray_scale, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9)
    resize_4 = cv.resize(get_edge, (960, 540))
    
    #appling bilateral filter to remove noise
    #and keep edge sharp as required
    color_image = cv.bilateralFilter(original_image, 9, 300, 300)
    resize_5 = cv.resize(color_image, (960, 540))
    
    
    #giving a cartoon effect
    cartoon_image = cv.bitwise_and(color_image, color_image, mask=get_edge)
    resize_6 = cv.resize(cartoon_image, (960, 540))
    
    #ploting the whole trainsition 
    image = [resize_1, resize_2, resize_3, resize_4, resize_5, resize_6]
    fig, axes = plt.subplots(3,2,figsize=(8,8), subplot_kw={'xticks':[], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    
    for i, ax in enumerate(axes.flat):
        ax.imshow(image[i], cmap='gray')
    
    save1=Button(top,text="Save cartoon image",command=lambda: save(resize_6, image_path),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
        
    # plt.show()
    
def save(resize, image_path):
    new_name = 'cartoonified_image' + datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    print(new_name)
    path_1 = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    path = os.path.join(path_1, new_name + extension)
    cv.imwrite(path, cv.cvtColor(resize, cv.COLOR_RGB2BGR))
    I = "image save by name " + new_name +" at " + path
    
    tk.messagebox.showinfo(title=None, message=I)
    
upload = Button(top, text = 'Cartoonify an image', command=upload, padx=10, pady=5)
upload.configure(background = '#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady = 50)

top.mainloop()