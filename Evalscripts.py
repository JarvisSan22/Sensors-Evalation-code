# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 07:53:53 2019

@author: Jarvis
"""
import pandas as pd
from scipy import stats
import matplotlib
import numpy as np
import matplotlib.pylab as plt


def SensorsEvalPlot(dataset,ref,units,refname,Dates,calname,ave,val):
    """
    Evalation code, Perfromes an evations of a sensors set agains a refrece for 
    -Accurcy PCBias, R^2 and MAE, agains the Refrence 
    -Gives the mean values 
    -Provied preceion evaation for CV and ISV
    -Provied mean accuracy PC for each sensors to spot outliers 
    -Performs this for factory and calibrated sensors agains the refrence method
    
    Author:Dainel Jarvis 
    Created 2019/08/13
    Last edit: 2019/08/23
    To do 
    #Add RH effect 
    #Add Mean PC to table 
    """
    
    #Get Factory measurmet average, and PC
    newd,ISV,R2,Bias,MAE,averef=SensorsEval(dataset,ref,units,refname,Dates,ave,val)
    
    #create a figure to have a look at the data 
    figtime,axpm=plt.subplots(1,1,figsize=(15,10))
    axpm.plot(averef[val],label="GRIMM",color="Red")
    for k,item in newd.items():
        axpm.plot(item[val].resample(ave).mean(),color="green")
    
   #calibrate sensors 
    caldataset,caleqn=Calval(newd.copy(),averef,dataset.copy(),refname,val)
    
    
    #plot calibrated data 
    for k,item in caldataset.items():
        item=Timecut(item,Dates)
        axpm.plot(item["cal-"+val].resample(ave).mean(),color="blue")
    
    #generate calibrated PC
    calval="cal-"+val
    calnewd,calISV,calR2,calBias,calMAE,averef2=SensorsEval(caldataset,ref,units,refname,Dates,ave,calval)
    

    #create table for PC 
    cv=pd.DataFrame()   # Coefiction of varation 
    for k, item in newd.items():
        cv[k]=item["CV-"+val]

    #describe the PC, and add thoese vales into a table 
    cvdes=cv.mean(axis=1).describe()
    ISVdes=ISV.describe()
    ISVcaldes=calISV.describe()
    table=pd.DataFrame(index=["CV","ISV(%)","Cal-ISV(%)"],columns=["mean","std","min","max"])
    for c in table.columns:
        table.loc["CV",c]=round(cvdes[c],2)
        table.loc["ISV(%)",c]=round(float(ISVdes.loc[c]),2)
        table.loc["Cal-ISV(%)",c]=round(float(ISVcaldes.loc[c]),2)
    
    
    #create a tbale for the calibration eqns 
    caleqntable=pd.DataFrame(index=["Cal-eqn"],columns=list(caleqn.keys()))
    for k,item in caleqn.items():
        caleqntable.loc["Cal-eqn",k]=item
    #create a table for the accuracy PC 
    valtit=["Bias (%)","MAE ($\mu g/m^3$)","R$^2$"]
    vals={val:newd,"Bias (%)":Bias,"MAE ($\mu g/m^3$)":MAE,"R$^2$":R2}
    calvals={val:calnewd,"Bias (%)":calBias,"MAE ($\mu g/m^3$)":calMAE,"R$^2$":calR2}
    Targets={"Bias (%)":[50,30,10],"MAE ($\mu g/m^3$)":[7,5,2.5],"R$^2$":[0.6,0.7,0.86]} 
    
    i=0
    fig,(axes)=plt.subplots(3,2,figsize=(15,15))
    sens=list(newd.keys())
    for axg in axes:
        #print(axg)
        for ax in axg:
          #  print(i)
            if i==0:
            
              #plot pm2.5 boxplots 
              valdata=pd.DataFrame(columns=[refname,"Fac-"+units,"Cal-"+units],index=ref.index)
              valdata[refname]=averef2[val]
            
              #gen calibrated adata 
              valdata["Cal-"+units]=meandic(calnewd,"cal-"+val)
           #   print(valdata["Cal-"+units].describe())
                #gen Factor data 
              valdata["Fac-"+units]=meandic(newd,val)
            #  print(valdata["Fac-"+units].describe())
            #add them to box plots 
              box=valdata.boxplot(column=list(valdata.keys()),ax=ax,vert=False,patch_artist=True,notch = True,showfliers=False)
              
              #set color 
              colors=["Red","teal","blue"]
              for e, color in enumerate(colors):
                  ax.findobj(matplotlib.patches.Patch)[e].set_facecolor(color)  
              ax.set_title(val+" ($\mu g/m^3$)",fontsize=15)
        

            if i>0 and i<4: #Plot accuract PCS 
                a=i-1
                dval=valtit[a]
          #      print(a)
                Data=vals[dval] #get defult data 
                CalData=calvals[dval] #get calibrated data 
                
                #create data fraome
                data=pd.DataFrame(index=Data.index) #for Preaceion PC data 
                
                #add default data 
                data["Fac-"+units]=Data.mean(axis=1)
                data["std-"+"Fac-"+units]=Data.std(axis=1)
                meand=data["Fac-"+units].mean() #furemean
                #add cal data 
                data["Cal-"+units]=CalData.mean(axis=1)
                data["std-"+"Cal-"+units]=CalData.std(axis=1)
                calmeand=data["Cal-"+units].mean() #furemean
             
                #Plot accurace PC onto boxplots 
                if dval=="R$^2$": #no need to plot calibration for R^2
            
                     data.boxplot(column=["Fac-"+units],ax=ax,vert=False,patch_artist=True,notch = True,showfliers=False,widths=0.4)
                    
                else: #other PC add the calibartion data 

                    data.boxplot(column=["Fac-"+units,"Cal-"+units],ax=ax,vert=False,patch_artist=True,notch = True,showfliers=False,widths=0.3)
                
                
                
                
                
                #box=ax.boxplot(Data.T,patch_artist=True
                title=dval+" \n Fac: (Mean="+str(round(data["Fac-"+units].mean(),2))+"$\pm$"+str(round(data["std-"+"Fac-"+units].std(),2))+")"
                title=title+"\n Cal: (Mean="+str(round(data["Cal-"+units].mean(),2))+"$\pm$"+str(round(data["std-"+"Cal-"+units].std(),2))+")"
                
                

                ax.text(.5,.86,title,horizontalalignment='center',transform=ax.transAxes,fontsize=15)
                
                #add lines for classes target value  
                tar=Targets[dval]
                color=["Blue","Green","Gold"]
                label=["Class-3","Class-2","Class-1"]
                for t,c,l in zip(tar,color,label):
                    ax.axvline(x=t,color=c,linestyle="--",label=l)
                    if "Bias" in dval: #if BAS plot scorse for less than zero as well 
                         ax.axvline(x=-t,color=c,linestyle="--")
                ax.plot([], [], color="Red", label="Fail")    
                ax.legend()
                
                #add color scoure 
                colums=["fac-"+units,"cal-"+units]
                ui=0 #makrer for colums 
                for cl in colums: #colums loop for 
                    if "cal" in cl:
                        mean=calmeand
                    else:
                        mean=meand
                    tar=Targets[dval]
                    tarrange=[2,1,0.5]
                    color=["Blue","Green","Gold"]
            
                  #  f=0 #found marker
                    ci=0
                    col="RED" # if failes target set as red
                  
                    for t,ran in zip(tar,tarrange):
                        if "R" not in dval:
                          #  print("test",meand,t,ci)
                            if mean < t:
                                col=color[ci]
                        else: #R2 good for high vales 
                            if abs(mean) > t: #take abs to accout for negtavie bias 
                                col=color[ci]
                           #     print(mean,t,col)
                        ci=ci+1
                    ax.findobj(matplotlib.patches.Patch)[ui].set_facecolor(col)
                    ui=ui+1
                    
            if i==4:
                #plot preceion PC in a table 
                tab=table
                tabrow=[]
                for row in range(len(tab)):
                    tabrow.append(tab.iloc[row])
               
                
               # header = ax.table(cellText=[['']*2],colLabels=["Precision PC","tes"], loc='center')
               #left. bottom,width,height
                bbox=[0.1, 0.5, 0.7, 0.5]
                plttab=ax.table(cellText=tabrow,colLabels=tab.columns,bbox=bbox,colWidths=[0.25 for x in tab.columns],rowLabels=tab.index,loc="top",cellLoc='center')
                plttab.auto_set_font_size(False)
                plttab.set_fontsize(14)
                plttab.scale(0.8, 1.4) #mae table bigger 
                ax.axis("off")
                ax.set_title("Precision PC",fontsize=15)
                
                #create table for cal eqns 
                tab=caleqntable
                tabrow=[]
                for row in range(len(tab)):
                    tabrow.append(tab.iloc[row])
                    
                bbox=[0, 0.1, 0.9, 0.25]
                plttab=ax.table(cellText=tabrow,colLabels=tab.columns,bbox=bbox,colWidths=[0.4 for x in tab.columns],rowLabels=tab.index,loc="center",cellLoc='center')
                plttab.auto_set_font_size(False)
                plttab.set_fontsize(14)
                plttab.scale(0.8, 1.4) #mae table bigger
                ax.text(.4,.4,"Calibration eqns",horizontalalignment='center',transform=ax.transAxes,fontsize=12)
                
                
                
                
            elif i==5: #plots PC for each sensors 
             #   print(i)
                tablesen=pd.DataFrame(index=[val,calval,"Bias","Cal-Bias","MAE","Cal-MAE","R$^2$","Cal-R$^2$",],columns=list(newd.keys()))
               
                for fac,cal in zip(vals.items(),calvals.items()):
                    if val in fac[0]:
                        for k,item in fac[1].items():
                            tablesen.loc[val,k]=round(item[val].mean(),2)
                        for k,item in cal[1].items():
                             tablesen.loc[calval,k]=round(item[calval].mean(),2)
                    else:
                        for k,item in fac[1].items():
                             VAL=fac[0]
                             if "Bias" in VAL:
                                 FACVAL="Bias"
                             elif "MAE" in VAL:
                                 FACVAL="MAE"
                             elif "R$^2$" in VAL:
                                 FACVAL="R$^2$"
                             CALVAL="Cal"+FACVAL
                             tablesen.loc[FACVAL,k]=round(item.mean(),2)
                        for k,item in cal[1].items():
                             VAL=cal[0]
                             if "Bias" in VAL:
                                 CALVAL="Cal-Bias"
                             elif "MAE" in VAL:
                                 CALVAL="Cal-MAE"
                             elif "R$^2$" in VAL:
                                 CALVAL="Cal-R$^2$"
                             tablesen.loc[CALVAL,k]=round(item.mean(),2)
                
                
                tab=tablesen
                tabrow=[]
                for row in range(len(tab)):
                    tabrow.append(tab.iloc[row])
                plttab=ax.table(cellText=tabrow,colLabels=tab.columns,colWidths=[0.3 for x in tab.columns],rowLabels=tab.index,loc="center",cellLoc='center')
                plttab.auto_set_font_size(False)
                plttab.set_fontsize(14)
                plttab.scale(0.8, 1.4) #mae table bigger 
                ax.axis("off")
                ax.set_title("Accuracy PC for each sensors",fontsize=15)
                
            i=i+1
    title="Evaluation Info; \n  Sensors:"+units+" againsts refrence:"+ refname +" \n From "+Dates[0]+" to "+Dates[1] 
    title=title+ "\n Time average:"+ave
    title=title+", Value:"+val
    fig.suptitle(title,fontsize=15) # or plt.suptitle('Main title')

    fig.show()
    return data,fig


def MulSensorsEvalPlot(datasetdic,ref,refname,Dates,calname,ave,val):
    """
    Evalation code, Perfromes an evations for two low cost sensors accuract set agains a refrece for 
    -Accurcy PC Bias, R^2 and MAE, agains the Refrence 
    -Gives the mean values 
    -Provied mean accuracy PC for each sensors to spot outliers 
    -Performs this for factory and calibrated sensors agains the refrence method
    
    Author:Dainel Jarvis 
    Created 2019/08/22
    Last Edit:2019/08/23
    To do
    #Add preceion PC
    #Add PC time series option
    #Add liner relation option
    #Add RH effect  option
    
    """
    unitnames=[]
    
    evaldic={}
    calevaldic={}
    for unitname,dataset in datasetdic.items():  
        #genrate all the Evlaations for raw data 
        newd,ISV,R2,Bias,MAE,averef=SensorsEval(dataset,ref,unitname,refname,Dates,ave,val)
        
        #calabrate senosrs 
        
        caldataset,caleqn=Calval(newd.copy(),averef,dataset.copy(),refname,val)
       
        
        #Calibrate sensors        
        calval="cal-"+val
        calnewd,calISV,calR2,calBias,calMAE,averef=SensorsEval(caldataset,ref,unitname,refname,Dates,ave,calval)
      
        #create a table for the accuracy PC 
        #add the evalation to a dcitionary
        vals={val:newd,"Bias (%)":Bias,"MAE ($\mu g/m^3$)":MAE,"R$^2$":R2}
        calvals={val:calnewd,"Bias (%)":calBias,"MAE ($\mu g/m^3$)":calMAE,"R$^2$":calR2}
        #add evlation to div
        evaldic[unitname]=vals
        calevaldic[unitname]=calvals
        unitnames.append(unitname)
    
    valtit=["Bias (%)","MAE ($\mu g/m^3$)","R$^2$"]
    Targets={"Bias (%)":[50,30,10],"MAE ($\mu g/m^3$)":[7,5,2.5],"R$^2$":[0.6,0.7,0.86]} 
    
    i=0
    fig,(axes)=plt.subplots(2,2,figsize=(15,12))
    for axg in axes:
        #print(axg)
        for ax in axg:
          #  print(i)
            if i==0: #plot concentration distribtuin through calibration
                
                #creeate a defult data set
                valdata=pd.DataFrame(columns=[refname],index=ref.index)
                valdata[refname]=averef[val] #add refnrece 
                for units in unitnames: #add all data 
                    valdata["Fac-"+units]=meandic(evaldic[units][val],val)
                    valdata["Cal-"+units]=meandic(calevaldic[units][val],"cal-"+val)
              #plot the boxplot o     
                box=valdata.boxplot(column=list(valdata.keys()),ax=ax,vert=False,patch_artist=True,notch = True,showfliers=False)
                colors=["Red","teal","blue","green","lime"]
                for e, color in enumerate(colors):
                    ax.findobj(matplotlib.patches.Patch)[e].set_facecolor(color)  
                ax.set_title(val+" ($\mu g/m^3$)",fontsize=20)
        

            if i>0 and i<4: #Plot accuract PCS 
                
                #get accuracy PC 
                a=i-1
                dval=valtit[a]
                #create data file , with index the days in the reffrence sensors 
                PCdata=pd.DataFrame(index=averef.resample("1D").mean().index) 
                
                #dic for mean values, use for the targets
                facmean={}
                calmean={}
                
                for units in unitnames:
                    Data=evaldic[units][dval] #get defult data 
                    CalData=calevaldic[units][dval] #get calibrated data 
                    #Get mean of all units  for each day
                    PCdata["Fac-"+units]=Data.mean(axis=1)
                    #get mean over all data 
                    facmean[units]=PCdata["Fac-"+units].mean() 
                    #do the same for the calibrated data 
                    PCdata["Cal-"+units]=CalData.mean(axis=1)
                    calmean[units]=PCdata["Cal-"+units].mean() 
                
                #get columens for factory data 
                cols=[] 
                for units in unitnames:
                    cols.append("Fac-"+units)
                if dval=="R$^2$": #no need to plot calibration for R^2
            
                     PCdata.boxplot(column=cols,ax=ax,vert=False,patch_artist=True,notch = True,showfliers=False,widths=0.4)
                    
                else: #other PC add the calibartion data 
                    for units in unitnames:
                        cols.append("Cal-"+units)
                    PCdata.boxplot(column=cols,ax=ax,vert=False,patch_artist=True,notch = True,showfliers=False)
                #plot class targets lines 
                tar=Targets[dval]
                color=["Blue","Green","Gold"]
                label=["Class-3","Class-2","Class-1"]
                for t,c,l in zip(tar,color,label):
                    ax.axvline(x=t,color=c,linestyle="--",label=l)
                    if "Bias" in dval: #if BAS plot scorse for less than zero as well 
                         ax.axvline(x=-t,color=c,linestyle="--")
                ax.plot([], [], color="Red", label="Fail")    
                ax.legend()
                
                
                #add subplot title 
                title=dval #+" \n Fac: (Mean="+str(round(data["fac-"+units].mean(),2))+"$\pm$"+str(round(data["std-"+"fac-"+units].std(),2))+")"
               # title=title+"\n Cal: (Mean="+str(round(data["cal-"+units].mean(),2))+"$\pm$"+str(round(data["std-"+"cal-"+units].std(),2))+")" 
                ax.set_title(title,fontsize=20)
               
              
                #add target scores 
                ui=0 #makrer for colums 
                for cl in cols: #colums loop for
                    units=cl.split("-")
                    units=units[1]
                    if "Cal-" in cl:
                            mean=calmean[units]
                    else:
                            mean=facmean[units]
                    tar=Targets[dval]
                    tarrange=[2,1,0.5] 
                    color=["Blue","Green","Gold"]
            
                  #  f=0 #found marker
                    ci=0
                    col="RED" # if failes target set as red
                  
                    for t,ran in zip(tar,tarrange):
                        if "R" not in dval:
                          #  print("test",meand,t,ci)
                            if mean < t:
                                col=color[ci]
                        else: #R2 good for high vales 
                            if abs(mean) > t: #take abs to accout for negtavie bias 
                                col=color[ci]
                           #     print(mean,t,col)
                        ci=ci+1
                    ax.findobj(matplotlib.patches.Patch)[ui].set_facecolor(col)
                    ui=ui+1
                    
           
            i=i+1 #add to counter, for dval varaible 
    
    #greate a string of the units for the title
    UnitsStr=""
    for units in unitnames:
        UnitsStr=units+","
    UnitsStr=UnitsStr[0:len(UnitsStr)-1] #cut the last commer 
    title="Evaluation Info; \n  Sensors:"+UnitsStr+" againsts refrence:"+ refname +" \n From "+Dates[0]+" to "+Dates[1]
    title=title+ "\n Time average:"+ave
    title=title+", Value:"+val +"\n"
    #fig.suptitle(title,fontsize=15) # or plt.suptitle('Main title')

    fig.show()
  
    
def meandic(sendic,val):
    """
    Mean a group of sensors data from a dictrionary of sensors data 
    """
    df=pd.DataFrame()
    for k,item in sendic.items():
        df2=item[val]
        df=pd.concat([df,df2],axis=1)
    
    data=df.mean(axis=1)

    
    return data   
    
def CombineStat(df1,df2,S1,S2,VAL):
    
    '''
    Statistanca anayslsi fuction to run states.lineregression for diffrent varaibes
    '''
    #Combine the data fram in a easy way, all the non over laps show up as NAN
    #df1 refrence df2 targer sensors
    newdf=pd.concat([df1[VAL],df2[VAL]],axis=1,ignore_index=False)
    newdf.columns=VAL,VAL+"_2"   
    #nana chack
    mask = ~np.isnan(newdf[VAL]) & ~np.isnan(newdf[VAL+"_2"])
    newdf=newdf[mask]
    slope, intercept, r_value, p_value, std_err = stats.linregress(newdf[VAL],newdf[VAL+"_2"])
 #   print("-----"+VAL+"----",S1,'_VS_',S2, ' p=',str(p_value), " r=" , str(r_value), "STD-error",str(std_err),"------")
   # print("y="+str(slope)+"x"+"+"+str(intercept))
    return newdf,  slope, intercept, r_value, p_value, std_err
    
def Calval(dataset,ref,rawdataset,refname,val):
    """
    Function to applys a linear calbration eqn to a data

    """
    caleqn={}
    newdataset={}
    for k,itemave in dataset.items():
        if refname not in k:

            #get calibration eqns of time average 
            df,  slope, intercept, r_value, p_value, std_err=CombineStat(itemave,ref,k,refname,val)
             #apply to raw data 
            print(df)
            item=rawdataset[k]
            item["cal-"+val]=item[val]*slope+intercept
            newdataset[k]=item
            
            #write calibration eqns 
            #account for diffrence signs in intercept
            if intercept < 0:
                sign="-"
            else:
                sign="+"
            #add the call eqn to dic 
            caleqn[k]=str(round(slope,2))+"X"+sign+str(round(abs(intercept),2))
    return newdataset,caleqn



def Timecut(df,Dates):
    '''
    Function to get certain time in dat, account for single day and time intervals 
    
    '''
    if len(Dates)>1:
       
        df=df[(df.index > Dates[0]) & (df.index <= Dates[1])]
    else:
        df=df[Dates[0]]
    return df

def CVandMean(data,vals,ave):
    """
    Function that generates CV and appplied mean over time average 
    """
    Newdata=data.resample(ave).mean()
    for val in vals:
        std=data[val].resample(ave).std()
        mean=data[val].resample(ave).mean()
        CV=std/mean
        Newdata["CV-"+val]=CV
    return Newdata
        
def BiasTrendEval(dataset,ref,dates,refname,val):
    """
    Generate BIAS for ever day of the data
    
    """ #mean bias
   
  #  data=data.dropna()
    ref=Timecut(ref,dates)
    days=ref.index.strftime("%Y/%m/%d")
    days=days[~days.duplicated(keep='first')]
    sens=list(dataset.keys())
    sen=[]
    for s in sens:
        if refname not in s:
            sen.append(s)
    #create R^2 data frame 
    bias=pd.DataFrame(index=days,columns=sen)
    for i in days:
        re=Timecut(ref,[i])
        for k,item in dataset.items():
            if refname not in k:
                if i in item.index:
                    x=Timecut(item,[i])
                    try:
                            df,s,I,r,p,std=CombineStat(x,re,k,refname,val)
                            #print(r)
                            bias.at[i,k]=round(100*((df[val+"_2"]/df[val])-1).mean(),2)
                    except:
                           # print("Error ----",i,"----",k,"------")
                            pass
   # print("Inter sensors variability",ISV," %")
    bias.index=pd.to_datetime(bias.index, yearfirst=True, dayfirst=False)
    for s in sens:
        bias[s]=pd.to_numeric(bias[s], errors='coerce')
    return bias  
def MAETrendEval(dataset,ref,dates,refname,val):
    """
    Generate Mean average Error for ever day of the data
    
    """ #mean bias
   
  #  data=data.dropna()
    ref=Timecut(ref,dates)
    days=ref.index.strftime("%Y/%m/%d")
    days=days[~days.duplicated(keep='first')]
    sens=list(dataset.keys())
    sen=[]
    for s in sens:
        if refname not in s:
            sen.append(s)
    #
    MAE=pd.DataFrame(index=days,columns=sen)
    for i in days:
        re=Timecut(ref,[i])
        for k,item in dataset.items():
            if refname not in k:
                if i in item.index:
                    x=Timecut(item,[i])
                    try:
                            df,s,I,r,p,std=CombineStat(x,re,k,refname,val)
                            #print(r)
                            MAE.at[i,k]=round(1/len(df)*(abs(df[val+"_2"]-df[val])).sum() ,2)
                    except:
                           # print("Error ----",i,"----",k,"------")
                            pass
   # print("Inter sensors variability",ISV," %")
    MAE.index=pd.to_datetime(MAE.index, yearfirst=True, dayfirst=False)
    for s in sens:
        MAE[s]=pd.to_numeric(MAE[s], errors='coerce')
    return MAE 
def R2TrendEval(dataset,ref,dates,refname,val):
    """
    Generate R2 for ever day of the data
    
    """
   
  #  data=data.dropna()
    ref=Timecut(ref,dates)
    days=ref.index.strftime("%Y/%m/%d")
    days=days[~days.duplicated(keep='first')]
    sens=list(dataset.keys())
    sen=[]
    for s in sens:
        if refname not in s:
            sen.append(s)
    #create R^2 data frame 
    R=pd.DataFrame(index=days,columns=sen)
    for i in days:
        re=Timecut(ref,[i])
        for k,item in dataset.items():
            if refname not in k:
                if i in item.index:
                    x=Timecut(item,[i])
                    try:
                            df,s,I,r,p,std=CombineStat(x,re,k,refname,val)
                            #print(r)
                            R.at[i,k]=round(r**2,2)
                    except:
                           # print("Error ----",i,"----",k,"------")
                            pass
   # print("Inter sensors variability",ISV," %")
    R.index=pd.to_datetime(R.index, yearfirst=True, dayfirst=False)
    for s in sens:
        R[s]=pd.to_numeric(R[s], errors='coerce')
    return R 



def ISVTrend(dataset,val):
    data=pd.DataFrame()
    for k,item in dataset.items():
        x=item[val]
        data[k+val]=x
  #  data=data.dropna()
    days=x.index.strftime("%Y/%m/%d")
    days=days[~days.duplicated(keep='first')]
    ISVD=pd.DataFrame(index=days)
    ISVD["ISV"]=0
    
               # for k, item in dic.items():
                #    x=item[val].mean()
                 #   data.at[k,val]=x
               # print(data)
                #des=data.describe()
              # # print(data)
               # ISV=((des.loc["max"][0]-des.loc["min"][0])/des.loc["mean"][0])*100
               # ISVdata.at[g,val]=ISV
    for i in days:
        x=data[i].mean()
       # print(x)
        des=x.describe()
       # print(des)
        ISV=((des.loc["max"]-des.loc["min"])/des.loc["mean"])*100
        ISVD.loc[i,"ISV"]=ISV
        #ISVD.loc[i,"STDEV"]=des.loc["std"]
   # print("Inter sensors variability",ISV," %")
    ISVD.index=pd.to_datetime(ISVD.index)
    ISVD["ISV"]=pd.to_numeric(ISVD["ISV"], errors='coerce')
    
    
    
   # print(data.describe())
   # fig,ax=plt.subplots(1,1,figsize=(8,5))
  #  ax.plot(ISVD["ISV"],label="Mean-ISV:"+str(round(ISVD["ISV"].mean()))+"%",color="Blue")
   # ax.grid(True)
    ##ax.legend()
   # ax.set_ylabel("ISV(%)")
   # ax.set_ylim(0,100)
   # ax.set_xlim(min(ISVD.index),max(ISVD.index))
   # myFmt = mdates.DateFormatter('%d/%m')
  #  ax.xaxis.set_major_formatter(myFmt)
  #  plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
    
    
    
    
    return ISVD

   
def SensorsEval(dataset,ref,sentype,refname,dates,ave,val):
    """
    Function that genrate the PC for the group of sensors (Like Like sensors)
    """

    #Generate CV and average the data
    newdata={}   
    if "SDS" not in sentype:
        for k, item in dataset.items():
            X=Timecut(item,dates) #date in date range
            item=CVandMean(X,[val],ave) #get value with the CV val
            newdata[k]=item
            
    else: #if SDS0011
        newdata=SDSaverage(dataset,3,ave,[val],dates)
   
    #generate the ISV

    ISV=ISVTrend(newdata,val)
     
    if "cal-" in val:
         refval=val[4:]
         ref=Timecut(ref,dates)
         ref=CVandMean(ref,[refval],ave) #get value with the CV val
         ref[val]=ref[refval]
    else:
        #average Ref sensors 
        ref=Timecut(ref,dates)
        ref=CVandMean(ref,[val],ave) #get value with the CV val
    
    #Generate Accuracy PC
    #Genrate daily R2
    R2=R2TrendEval(newdata,ref,dates,refname,val)
    #Generate BIAS
    Bias=BiasTrendEval(newdata,ref,dates,refname,val)
    #Generate MAE
    MAE=MAETrendEval(newdata,ref,dates,refname,val)
  
    return newdata,ISV,R2,Bias,MAE,ref


################Sensors pecefice code 
    
    
    
def SDSaverage(RAWSDS,N,ave,vals,dates):
    """
    SDS011 correaced average, for a set of SDS011. 
    Accounting for sudden Jump in pm2.5 
    
    RAWSDS-RAW data 
    N-Number of sensors 
    ave-time average in the following format "1T","10T","60T","1D"
    vals= array of the values the correaction is appled 
    
    Created:17/07/2019
    Author: Daniel Jarvis
    Contacts: Jarvissan21@gmail.com
    """
    
    RAWSDS=RAWSDS.copy()
    NEWSDS={}
    for k,i in RAWSDS.items():
        NEWSDS[k]=i.resample(ave).mean() #get a dummy data fram of eqaul size 
        
    #loop through values  
    for val in vals:
        #create a new data frame for correaction to be appled 
        SDSfix=pd.DataFrame(columns=list(RAWSDS.keys()))
        SDSfixSTD=pd.DataFrame(columns=list(RAWSDS.keys()))
        for k,item in RAWSDS.items(): 
            if ave=="RAW":
                 SDSfix[k]=item[val].mean() #get the average 
                 SDSfixSTD[k]=item[val].std() #get the STDEV
       
            SDSfix[k]=item[val].resample(ave).mean() #get the average 
            SDSfixSTD[k]=item[val].resample(ave).std() #get the STDEV
       
        SDSfix["N"]=SDSfix[~np.isnan(SDSfix)].count(axis=1)-1 #Get the number of sensors running at any instabce
        
        SDSfix=SDSfix.drop(SDSfix[SDSfix["N"]==0].index) #If non of the sneosrs are running, cut all data 
        
        #Set large STDEV as nan and fill it with the Mean of the other sensors 
        SDSfix2=SDSfix[np.isnan(SDSfix[SDSfixSTD>30])]
        SDSfix2.fillna(SDSfix2[~np.isnan(SDSfix2)].mean()*N/SDSfix["N"], inplace=True) #Fill nan with mean of the other sensors 
        #cheacks
        #SDSfix.plot()
        #SDSfix2.plot()
        #Add the the data to the averaged data set, and generate CV.
        for col in SDSfix.keys():
            if col!="N":
                NEWSDS[col][val]=SDSfix2[col]
                NEWSDS[col]["CV-"+val]=SDSfixSTD[k]/SDSfix2[col]
    #apply the time period 
    for k,item in NEWSDS.items():
        item=Timecut(item,dates)
        #cut bad data period
        badd=Timecut(item,["2019-04-16 12","2019-04-17 18"])
        item=item.drop(badd.index)
    
        NEWSDS[k]=item
        

    return NEWSDS