# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 13:41:06 2022

@author: Martin

Make a grid of images from a folder and put the result in the same folder
"""
import os
import re

from PIL import Image


dir_path = r""
out_fname = ""


if not dir_path:
    print("no path has been set to look for the images")
    while True:
        dir_path = input("please enter a path:\n")
        if not os.path.isdir(dir_path):
            print("invalid path")
            continue
        else:
            break
    
if not out_fname:
    print("no output file name has been set")
    while True:
        out_fname = input("please enter a file name:\n> ")
        if not out_fname:
            print("invalid name")
            continue
        else:
            break
        
outfile_addr = os.path.join(dir_path, out_fname)
file_list = os.listdir(dir_path)
img_file_list = [x for x in file_list if\
                 x.endswith(".png") or x.endswith(".jpg")]

#show the image files to choose from
print(f"images located in {dir_path}:")
for i, file in enumerate(img_file_list):
    print(f"{i}: {file}")
    
#ask user to select the files for the new image
selected_files = input("write the file index to be added to the grid, \
                         separated by a coma (ex: '0,2,5,8')\n> ")
while True:                  
    selected_indices = [int(x) for x in selected_files.split(",")]
    
    max_index = max(selected_indices)
    min_index = min(selected_indices)
    
    if min_index < 0: 
        print(f"problem with index: {min_index} below 0")
        selected_files = input("please enter the index list again\n> ")
        continue
    if max_index > len(img_file_list):
        print(f"problem with index: {max_index} out of range")
        selected_files = input("please enter the index list again\n> ")
        continue   
    else:
        break 

#ask the user for the arrangement of the images
print(f"valid list \n{len(selected_files.split(','))} files selected")
input_dims = input("write the number of rows and columns of the final image, \
             separated by a coma (ex: '5,6')\n> ")

while True:
    n_rows = int(input_dims.split(',')[0])
    n_cols = int(input_dims.split(',')[1])
    
    if n_rows <= 0 or n_cols <= 0:
        print("problem with input: dimensions cannot be smaller than 1")
        input_dims = input("please write another couple of dimensions\n> ")
        continue
    elif n_rows * n_cols < len(selected_indices):
        print("size error: there are not enough spaces on the grid for the"+\
              "given file list.")
        input_dims = input("please write another couple of dimensions\n> ")
        continue
    else:
        break

#calculate the dimensions of the new image
max_block_width = 0
max_block_height = 0
img_list = [Image.open(os.path.join(dir_path, img_file_list[x]),'r')\
            for x in selected_indices]

for im in img_list:
    max_block_width = max(max_block_width, im.width)
    max_block_height = max(max_block_height, im.height)

new_width = max_block_width * n_cols
new_height = max_block_height * n_rows

print(f"the new image will be {new_width}x{new_height}\n"+\
       "do you want to scale the image down?")
scale_prompt = input("write one (1) integer to scale down by that number or\n"+\
              "write two (2) integers separated by a coma to set the new "+\
              "dimensions of the image or\n"+\
              "press enter (enter) to continue without scaling\n> ")

if scale_prompt:
    while True:
        patt = re.compile(r"\d{1,5},\d{1,5}|\d{1,2}") 
        # 2 ints of 1 to 5 digits OR 1 integer of 1 or 2 digits
        match = re.search(patt, scale_prompt)
        if match is None:
            print("invalid input")
            scale_prompt = input("enter either one integer or two integers\
                                 separated by a coma")
            continue
        else:
            break

#optional scaling
resize_dim = ()
scale_dim = ()
if scale_prompt:
    if ',' in scale_prompt:
        resize_dim = tuple([int(x) for x in scale_prompt.split(',')])
    else: #scale_prompt is therefore a single integer
        scale = int(scale_prompt)
        maxsize = int(max(new_width/scale, new_height/scale))
        scale_dim = (maxsize,maxsize)

#make the new  image
with Image.new("RGB", (new_width, new_height)) as new_im:
    x = 0
    y = 0
    for i,im in enumerate(img_list, start = 1):
        new_im.paste(im, (x,y))
        x = x + max_block_width
        if i % n_cols == 0:
            x = 0
            y = y + max_block_height
    if len(scale_dim) > 0:
        new_im.thumbnail(scale_dim)
        print(f"new image rescaled to: {new_im.size}")
    elif len(resize_dim) > 0:
        new_im = new_im.resize(resize_dim)
        print(f"new image resized to: {resize_dim}")
    new_im.save(outfile_addr)
    print(f"new image saved as '{out_fname}' in {dir_path}")
#close the used images 
for im in img_list:
    im.close()