# Sensors-Evalation-code
Evaluation, with an with out calibration for low-cost sensors to a reference method for pm2.5. Evaluation based for 5 performance characteristics, 3 for accuracy to refrence method;
Coeffection of determination (R^2), BIAS, Mean average error (MAE), and 2 for sensors preceion, coeffienct of variation (CV) and inter sensors varibility (ISV) 

Download script to your code resperty, get low-cost sensors data into a dictionary and the get the refrence data then.

import Evalscripts as Eval

### Evalation scripts:
 - Eval.SensorsEvalPlot(dataset,ref,units,refname,Dates,calname,ave,val)
 - Eval/MulSensorsEvalPlot(datasetdic,ref,refname,Dates,calname,ave,val)

dataset: low-cost sensors data in a dictionary, ref: refrence sensors data,units: name of the group of low cost sensors, refname: name of refrence sensors, ave: time average (i.e "1T", "10T", "60T")
Dates: date interval of the evalation and calibration performed i.e ["2019-04-01","2019-05-29"] , val: valuse to be evalated (val need to be a column in all sensors including ref). datasetdic: a dictionary for each group of low cost sensors datadiction (i.e a dictionary of dataset) dictionary key names are used as the units.


### SensorsEvalPlot Example plot

 - (Top left) Box plots of the values concentration, with refrence and low-cost sensors before and after calibration
 - (Top right) Boxplots of low-cost sensors BIAS, before and after calibration
 - (Middle left) Boxplots of MAE, befre and after calibration
 - (Middle right) Boxplot of R^2, before calibration 
 - (Bottom left) Preceion PC, for CV and ISV and calibration equation for each sensors in the dataset
 - (Bottom right) Mean concentration and mean Perfroamce charteristic for each sesnors in the dataset 

![SensorsEvalplot](https://github.com/JarvisSan22/Sensors-Evalation-code/blob/master/SensorsEvalplot-EG.png)

### MulSensorsEvalPlot Example plot 
 - (Top left) Box plots of the values concentration, with refrence and low-cost sensors before and after calibration
 - (Top right) Boxplots of low-cost sensors BIAS, before and after calibration
 - (Middle left) Boxplots of MAE, befre and after calibration
 - (Middle right) Boxplot of R^2, before calibration 
 


![MulSensorsEvalplot](https://github.com/JarvisSan22/Sensors-Evalation-code/blob/master/MulSensorsEvalplot-EG.png)


**Evalation method and score method**

The evalation is done be cacaluting the 3 accuracy for each day of the evalation allowing a ditribtuion to be cacualed allowing boxplot to be plotted. 
A 3 class system, is used to assese there results for each PC, with score for each class for pm2.5 are show in the table bellow. 
PC scores for pm2.5 are based of the EPA recomedations (Williams, at al, 2018), and the score take form the Mean of the PC for each group of sensors, that represend as the color of the boxplot.

![ClassScoreTable](https://github.com/JarvisSan22/Sensors-Evalation-code/blob/master/ClassScoreTable.png)

### To DO
- Colors for the tables
- Preceion PC for MulSensors
- PC with Boxplot and time series


**Refrencese**
Williams, R., Nash, H., Benedict, MacGregor, S. L. & T.Dye. (2018), ‘Peer Review and Supporting
Literature Review of Air Sensor Technology Performance Targets’. EPA/600/R-18/324.
