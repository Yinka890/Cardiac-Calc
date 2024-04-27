import os
import re
import nibabel as nb
import numpy as np
#
img_path = "/mnt/c/Users/anifo/OneDrive/Desktop/merge/Resampled_all_scans_and_masks/LRAD89_CT/LRAD89_CT.nii.gz"
seg_path = "/mnt/c/Users/anifo/OneDrive/Desktop/merge/Resampled_all_scans_and_masks/LRAD89_CT/Seg89_ZL_label_5.nii.gz"
img = nb.load(img_path)
seg = nb.load(seg_path)
img_data = img.get_fdata()
seg_data = seg.get_fdata()
voxel_dims = img.header
#tells us the voxel dimensions in mm ->multiply these and multiply by the number of voxels

x,y,z = voxel_dims.get_zooms()
print("volume dimension", x,y,z)
volume =  x * y * z

print(f"calculated volume of voxel is {volume}")

#density is scored 1 for 130–199 HU, 2 for 200–299 HU, 3 for 300–399 HU, and 4 for 400 HU and greater
count_1 = count_2 =count_3 =count_4 = 0
height, width, depth = np.where(seg_data == 1)
for x,y,z in zip(height, width, depth):
    #calc.append(img_data[x,y,z])
    if 200> img_data[x,y,z] >= 130:
        count_1 += 1
    elif 300> img_data[x,y,z] >= 200:
        count_2 +=1
    elif 400> img_data[x,y,z] >= 300:
        count_3 +=1
    elif img_data[x,y,z] >= 400:
        count_4 += 1
    #print(img_data[x,y,z])
print(f'number of voxels in segmentation with score 1 is {count_1}, score 2:{count_2}, score 3: {count_3}, score 4: {count_4}')

#calculate agatston score
score = (1* count_1 + 2 *count_2 +  3 * count_3 + 4 * count_4) * volume
print(score)