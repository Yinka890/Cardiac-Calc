import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lifelines import CoxPHFitter

#cox regression for single variables and multivariable as well
data = pd.read_csv("Latest_clinical_csv.csv", usecols=range(1,16))

#print(data.isnull().sum())
data.drop([101], axis = 0, inplace=True)
data.drop(['Height', 'Weight'], axis =1, inplace = True)

#put average into overaall survival days
data.fillna({"Overall.survival..days.": data["Overall.survival..days."].mean()}, inplace = True)

#data['N'] = data["N"].replace('X'
#Stage ['1b' '2a' '3' '2b' '4' '2' '1a' '1c' 'IS']
data['N'] = data["N"].replace('X', np.nan)
data['M'] = data['M'].replace('X', np.nan)
data['Numeral'] = data['Numeral'].replace('I', '1')
#N ['0' '2' '3' '1' 'X']
#M ['0':0, '1b':2 '1a':1 'X' '1c':3]
#Numeral ['I' '2' '5' '4' '8' '6' '1' '7' '3' '9' '0']

#change the alphanumeric scoring systems to strictly numeric
Stage_dic = {'1b': "3", '2a':"6", '3':"8", '2b':"7", '4':"9", '2':"5",'1a':"2", '1c':"4", 'IS':"1"}
comp_dic = {'Ia':"1", 'Ib':"2", 'IIIa':"5", 'IIb':"4", 'IVa':"8", 'IIIb':"6", 'IIIc':"7", 'IIa':"3", 'IVb':"9", '0':"0"}
m_dic= {'0':"0", '1b':"2" ,'1a':"1",'1c':"3"}
for key in m_dic:
    data["M"] = data["M"].replace(key, m_dic[key])
for key in comp_dic:
    data["CompositeStage"] =data["CompositeStage"].replace(key, comp_dic[key])
for key in Stage_dic:
    data["Stage"] =  data["Stage"].replace(key, Stage_dic[key])

#remove all other rows missing important data
data.dropna(inplace = True)

#data =  data.where(data["Gender"] !=0)
#data.dropna(inplace =True)

#Add all the features into one dataframe called variables
variables = pd.DataFrame([])

for col in data.columns:
    #print(col, data[col].unique())
    #os.event and sruvival days are dependent variables
    if col != "ID" and col!= "OS.event" and col!= "Overall.survival..days." and variables.empty:
        try:
           variables= pd.to_numeric(data[col])
        except:
            print(f"column {col} was not parsable, so we skipped it")
    elif not variables.empty:
        try:
            variables = pd.concat([variables, pd.to_numeric(data[col])], axis=1)
        except:
            print(f"column {col} was not parsable, so we skipped it")
            
#Add the depenent variables to the a datafram
dependent_var = data[["Overall.survival..days.", "OS.event"]]
print(variables.dtypes)
#print(variables.head)

#carry out univariable COX analysis and produces a plot and csv for each variable to find which ones are significant
count=0
data_single = pd.DataFrame([])
for col in variables.columns:
    #if col == "Age":
    data_single = pd.concat([dependent_var,pd.to_numeric(variables[col])], axis=1)
    cph_single = CoxPHFitter()
    cph_single.fit(data_single, duration_col="Overall.survival..days.", event_col="OS.event")
    cph_single.summary.to_csv(col+".csv", index=False)
    cph_single.print_summary()
    plt.figure(count)
    cph_single.plot()
    plt.savefig(col + ".png")
    data_single.drop([col], axis=1)
    count+=1
        #break
    
#This is the code to leave only the significant variables from the univariate analysis
#significant->N, M, Numerical, dummy->(histology is good?), 
for col in variables.columns:
    if col != "N" and col!= "M" and col!= "Numeral" and col!="Performance":
        variables.drop(col, axis=1, inplace=True)
#print(variables.head)

data_multiple = pd.concat([variables, dependent_var], axis = 1)
#print(data_multiple.head)
data_multiple.dropna(inplace=True)

#print(data_multiple.head)
#data_multiple.to_csv("multiple.csv")
cph_multi = CoxPHFitter(penalizer=0.001)
cph_multi.fit(data_multiple, duration_col="Overall.survival..days.", event_col="OS.event")
cph_multi.plot()
plt.savefig("cox" + ".png")
cph_multi.summary.to_csv("cox.csv", index= False)
cph_multi.print_summary()
plt.show()
