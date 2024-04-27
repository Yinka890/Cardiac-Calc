import nibabel as nb
import os
import re
import matplotlib.pyplot as plt
import numpy as np

#this is to combine different segmentation files of the same image into one file

#this path is a folder of folders
#Each folder here contains an original image and all segmentation files belonging to that image
p = "/mnt/c/Users/anifo/OneDrive/Desktop/merge/Resampled_all_scans_and_masks"
input = os.listdir(p)

#compile the pattern matching the name of the segmentation files
pattern = re.compile(r'^Seg\d+[_]ZL[_]label[_]\d[.]nii.gz')

#compile the pattern matching the name of the original image
pattern_original = re.compile(r'^LRAD\d+[_]CT')

#path to folder where your new combined segmentations will go
output = "your output folder here"


#loops through all folders in the list of folders
for dir in input:
    if dir == "nondistinct":
        try:
            next
        except:
            break
    print(dir)
    dir_path = os.path.join(p,dir)
    
   #for each folder inside the main folder, loop through the documents inside it
    for doc in os.listdir(dir_path):
        
        #this is the original image file so save the header and affine matrix as not affine or header as that will affect bottom condition
        if pattern_original.match(doc):
            print(doc)
            
            #load image
            doc_path = os.path.join(dir_path, doc)
            original_img = nb.load(doc_path)
            #always use header and affine of original images for the new combined segmentation file that will be produced
            header= original_img.header
            affine= original_img.affine
            shape = original_img.get_fdata().shape
            new_label_arr=np.zeros(shape)
            
        #this finds the segmentation files and loads them 
        if pattern.match(doc):
            print(doc)
            #get segmentation arrray here and get where the label value is not zero
            doc_path = os.path.join(dir_path, doc)
            seg_img = nb.load(doc_path)
            img_arr = seg_img.get_fdata()
        
            #change img_arr == <label value of your segmentation>
            x,y,z = np.where(img_arr == 1)
            print(f"the number of ones in {doc} is {len(x)}")
            
            
            #this creates an array which has ones in the same index as the different segmentation files
            for i,j,k in zip(x,y,z):
                new_label_arr[i,j,k] = 1
            height, width,depth = np.where(new_label_arr == 1)
            print(f" there are {len(height)} ones in the new array now")
        #when we get to end of the files in a directory
        if doc == os.listdir(dir_path)[-1]:
            #save the new label a a nifti segmentation
            #use nibabel to create new nifti using old affine matrix and header: 
            #affine and header should be correct here because we have processed the last element
            #print(np.where(new_label_arr == 1))
            new_label = nb.Nifti1Image(new_label_arr, affine=affine, header=header)
            
            height, width, depth = np.where(new_label.get_fdata() == 1)
            #work out the name for the new label
            print(f"the number of ones in the saved image is {len(height)}")
            
            new_name = f"{dir.split("_")[0].split("LRAD")[1]}.nii.gz"
            new_label_filepath = os.path.join(output, new_name)
            nb.save(new_label, new_label_filepath)
            print("done")
            