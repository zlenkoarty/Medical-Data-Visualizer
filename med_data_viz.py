import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Read data from CSV file
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
#Add an overweight column to the data. To determine if a person is overweight, 
#first calculate their BMI by dividing their weight in kilograms by the square of their height in meters. 
#If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.

df['overweight'] = (df['weight'] / (df['height']/100)**2).apply(lambda x: 1 if x > 25 else 0)

#Normalize the data by making 0 always good and 1 always bad. 
#If the value of cholesterol or gluc is 1, make the value 0. 
#If the value is more than 1, make the value 1.

df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x==1 else 1)
df['gluc'] =df['gluc'].apply(lambda x:0 if x==1 else 1)

#Convert the data into long format and create a chart that shows the value counts of the categorical features using seaborn's catplot().
#The dataset should be split by 'Cardio' so there is one chart for each cardio value. 
#The chart should look like examples/Figure_1.png.


df_cat = pd.melt(df, id_vars = 'cardio',value_vars = ['alco', 'active','cholesterol', 'gluc', 'overweight','smoke'])
df_cat["total"] = 1
df_cat = df_cat.groupby(["cardio", "variable", "value"], as_index = False).count()
fig = sns.catplot(x = "variable", y = "total", data = df_cat, hue = "value", kind = "bar", col = "cardio").fig
fig.savefig('catplot.png')



#clean the data to gather the desired range of height and weight.

df_heat = df[
     (df['ap_lo'] <= df['ap_hi']) &
     (df['height'] >= df ['height'].quantile(0.025)) &
     (df['height'] <= df ['height'].quantile(0.975)) &
     (df['weight'] >= df ['weight'].quantile(0.025)) &
     (df['weight'] <= df ['weight'].quantile(0.975))]

#Correlation matrix
corr = df_heat.corr(method="pearson")

#Generating the mask for the upper triangle:
mask = np.triu(corr)

#Setting up the matplotlib figure:
fig, ax = plt.subplots(figsize = (12,12))  

#Seaborn heat map:
sns.heatmap(corr, 
            linewidths=1, 
            annot = True, 
            square = True, 
            mask = mask, 
            fmt = ".1f", 
            center = 0.08, 
            cbar_kws = {"shrink": 0.5})
                        
fig.savefig('heatmap.png')
