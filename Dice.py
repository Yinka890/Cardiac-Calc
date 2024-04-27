import os
import numpy as np
import nibabel as nb

#loop through all predicted and true seg files
prediction = "/path to your inference folder"
true = "path to the original combined segmentations"

temp = 0
count =0
count_zero=0
negative = False
for seg in os.listdir(prediction):
    count+=1
    prediction_path = os.path.join(prediction, seg)
    number = seg.split(".")[0]
    end = " Segmentation.nii.gz"
    new = number + end
    true_path = os.path.join(true, new)
    print(seg)
    #load arrays
    predict_data = nb.load(prediction_path).get_fdata()
    true_data = nb.load(true_path).get_fdata()
    #print(f"prediciton is {prediction_path} and true is {true_path}")
    


    #get indices of all one's in predicted segmentation and true segmentation
    
    h_p, w_p, d_p = np.where(np.round(predict_data) == 1)
    h_true, w_true, d_true = np.where(np.round(true_data) ==1)
    #print("the predicted is",h_p, w_p, d_p,"the true is ", h_true, w_true, d_true)
    #print(len(h_p),"and", len(h_true))
    
    #gives the total number of voxels in the predicted and true segmentations
    pred_index = zip(h_true, w_true, d_true)
    print("number of voxels in prediction seg", len(h_p))
    print("number of voxels in true seg", len(h_true))
    voxel_set_size = len(h_p) + len(h_true)
    print("total number of voxels",voxel_set_size)
    
    #initialize set
    set_union = set()
    #add all the predicted voxels
    overlap_count = 0
    total_count = 0
    '''
    dim_x,dim_y,dim_z = predict_data.shape

    for i in range(dim_x):
        for j in range(dim_y):
            for k in range(dim_z):
                if (predict_data[i,j,k]== 1):
                    total_count +=1
                if (true_data[i,j,k] == 1):
                    total_count +=1
                if (predict_data[i,j,k] == 1) and (true_data[i,j,k] == 1):
                    overlap_count +=1
        
                

    score = (2*overlap_count)/(total_count)
    print(f"score is {score}, total is {total_count} and overlap is {overlap_count}")
            
    '''      
    #add both inference and true array data to a set to count the number of overlapped voxels
    for i, j, k in zip(h_true, w_true, d_true):
        #add all true voxels
        #all overlapping voxels will not be repeated
        set_union.add((i, j, k))
    for m,n,o in zip(h_p, w_p, d_p):
        set_union.add((m, n, o))
            

    #get number of overlapped voxels
    overlap = voxel_set_size - len(set_union)
    print("the number of voxels that overlap is: ",overlap)
    #calculate dice score
    top = 2* overlap
    bottom = (voxel_set_size)
    
    #this excludes images with negative findings and prevents dividing by zero
    if bottom == 0:
        bottom = 1
        negative =True
        #negative calcification
    dice = top / bottom
    
    #write dice to results file and
    with open("dice_score.txt", "a") as out_file:
        if dice !=0:
            count_zero+=1
        if len(h_true) == 0 and not negative:
            out_file.write(seg + "True segmentation is negative. Dice is " + str(dice))
        if negative:
            out_file.write("Prediction path is" + prediction_path+ "True path is " + true_path + "This segmentation was negative for both" + "\n")
            count-=1
        if len(h_true) != 0:
            out_file.write(seg + " dice score is " + str(dice) + "\n")
        out_file.close()
        negative = False
        
    #average the dice scores
    temp +=dice
    print(f" Set method: dice score is {dice}, overlap is {overlap}, and total is {bottom}")
    #write 

#writes the average to a file, calculates the average for all segmentations and also for only ones where dice is 0
average = temp/count
average_nozeros = temp/count_zero
f = open("dice_score.txt", "a")
f.write("average: " + str(average))
f.write("average no zeros: "+str(average_nozeros))
f.close()