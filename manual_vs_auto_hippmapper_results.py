
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluating hippmapper automatic segmentation against manual labels

@author: Sabrina Sghirripa
"""

import seg_metrics.seg_metrics as sg
import pandas as pd

#Metrics .csv
csv_file = '/path/to/placeholder/results/sheet.csv'

#Create subjects array
subjects=["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "s11", "s12", "s13", "s14",
          "s15", "s16", "s17", "s18", "s19", "s20", "s21", "s22", "s23", "s24", "s25"]
          
#Create hemispheres array
hemisphere=['L', 'R']

#Create list to store all metrics and dictionaries to save the individual metrics
segmentation_metrics = []

for subj in subjects:
    
    for h in hemisphere:

        #Denote label for use in mastching (1 for binarised masks)
        labels = [1]
        
        #Path to ground truth (manual segmentation)
        gdth_file = 'path/to/manual/label.nii.gz'
        
        #Path to automated segmentation result (binarised left and right hemisphere as separate files)
        pred_file = 'path/to/hippmapper/label.nii.gz'
        
        #Calculate metrics of interest 
        metrics = sg.write_metrics(labels, gdth_file, pred_file, metrics=['dice', 'hd', 'hd95','vs'])
        
        #Store metrics along with subject and hemisphere
        segmentation_metrics.append({
            'Subject': subj,
            'Hemisphere': h,
            'Metrics': metrics})

#Convoluted routine to get the values out of the segmentation metrics list/dictionary/list/dictionary 
all_metrics = []

# Loop through the segmentation_metrics list
for entry in segmentation_metrics:
    subject = entry['Subject']
    hemisphere = entry['Hemisphere']
    metrics_list = entry['Metrics']  
    
    # Loop through the metrics_list, which is a list containing a dictionary
    for metrics in metrics_list:
        dice_coefficient = metrics['dice']
        hausdorff_distance = metrics['hd']
        hd95 = metrics['hd95']
        volume_similarity = metrics['vs']
        
        # Create a list to represent the data for each metric entry
        metric_data = [subject, hemisphere, dice_coefficient, hausdorff_distance, hd95, volume_similarity]
        
        # Append the metric data to the all_metrics list
        all_metrics.append(metric_data)
        
# Create a DataFrame from the list of metrics
df = pd.DataFrame(all_metrics, columns=['Subject', 'Hemisphere', 'Dice Coefficient', 'Hausdorff Distance', 'HD95', 'Volume Similarity'])
        
# Save the DataFrame to a CSV file
df.to_csv(csv_file, index=False)
