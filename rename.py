import os

target = "folder path here"
target_list= os.listdir(target)
#end= " Segmentation.nii.gz"
for i in target_list:
    #change this to fit your name type
    number = i.split(".")[0].split(" ")[0]
    new_name =  number + ".nii.gz"
    ##
    print(new_name)
    new_name = os.path.join(target, new_name)
    img_path = os.path.join(target, i)
    os.rename(img_path, new_name)
    