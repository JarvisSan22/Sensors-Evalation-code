# Sensors-Evaluation-code
Evaluation, with an without calibration for low-cost sensors to a reference method for pm2.5. Evaluation based for five performance characteristics, 3 for accuracy to reference method;
coefficient of determination (R^2), BIAS, Mean average error (MAE), and 2 for sensors precision, coefficient of variation (CV) and inter sensors variability (ISV) 

Download script to your code folder, get low-cost sensors data into a dictionary, and the get the reference data then.

import Evalscripts as Eval

### Evalation scripts:
 - Eval.SensorsEvalPlot(dataset,ref,units,refname,Dates,calname,ave,val)
 - Eval/MulSensorsEvalPlot(datasetdic,ref,refname,Dates,calname,ave,val)

dataset: low-cost sensors data in a dictionary

ref: reference sensors data, units: name of the group of low-cost sensors

refname: name of refrence sensors

ave: time average (i.e "1T", "10T", "60T")

Dates: date interval of the evalation and calibration performed i.e ["2019-04-01","2019-05-29"] 

val: value to be evaluated (val need to be a column in all sensors including ref)( note: Grade system based off pm2.5)

datasetdic: a dictionary for each group of low-cost sensors data dictionary (i.e. a dictionary of dataset) dictionary key names are used as the units.


### SensorsEvalPlot Example plot

 - (Top left) Box plots of the concentration of the values, with reference and low-cost sensors before and after calibration
 - (Top right) Boxplots of low-cost sensors BIAS, before and after calibration
 - (Middle left) Boxplots of MAE, before and after calibration
 - (Middle right) Boxplot of R^2, before calibration 
 - (Bottom left) Precision PC, for CV and ISV and calibration equation for each sensor in the dataset
 - (Bottom right) Mean concentration and mean Perfroamce characteristic for each sensor in the dataset 

![SensorsEvalplot](https://github.com/JarvisSan22/Sensors-Evalation-code/blob/master/SensorsEvalplot-EG.png)

### MulSensorsEvalPlot Example plot 
 - (Top left) Box plots of the concentration of the values, with reference and low-cost sensors before and after calibration
 - (Top right) Boxplots of low-cost sensors BIAS, before and after calibration
 - (Middle left) Boxplots of MAE, before and after calibration
 - (Middle right) Boxplot of R^2, before calibration 
 


![MulSensorsEvalplot](https://github.com/JarvisSan22/Sensors-Evalation-code/blob/master/MulSensorsEvalplot-EG.png)


**Evalation method and score method**

The evaluation is performed by calculating the three accuracy PC for each day of the assessment allowing distribution to be calculated, allowing boxplot to be plotted. 
A 3 class system, is used to assese there results for each PC, with a score for each class for pm2.5 is shown in the table below. 
PC scores for pm2.5 are based on the EPA recommendations (Williams, at al, 2018), and the score is taken from the Mean of the PC for each group of sensors, that represented as the colour of the boxplot.

![ClassScoreTable](https://github.com/JarvisSan22/Sensors-Evalation-code/blob/master/ClassScoreTable.png)

### To DO
- Colours for the tables
- Precision PC for MulSensors
- PC with Boxplot and time series


**References**
Williams, R., Nash, H., Benedict, MacGregor, S. L. & T.Dye. (2018), ‘Peer Review and Supporting
Literature Review of Air Sensor Technology Performance Targets’. EPA/600/R-18/324.

