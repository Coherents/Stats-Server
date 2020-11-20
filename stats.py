# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys
#import optparse
import argparse
import seaborn as sns
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.utils import shuffle
from scipy.stats import norm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import adfuller, acf, pacf,arma_order_select_ic
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs



# validating Read data

def validate_data(read:bool):
        def inner(f:Function):
                if read:
                     return f
                else:
                    raise('First data has to be read')
        return inner

# main stat class
class Stats(object):
    def __init__(self,name,type="csv",req_sep=False):
        self.name=name
        self.type1=type
        self.sep=req_sep
        self.__data=None
        self.__read:bool=False
    
    
    def Load_data(self,head_included=False):
        if 'dataFiles' not in os.listdir(os.getcwd()):
            os.mkdir('dataFiles')
        if not head_included:
            if not self.sep:
                self.data=pd.read_csv(self.name,engine="python")
            else:
               self.data=pd.read_csv(self.name,engine="python",header=None)
        else:
            if not self.sep:
                self.data=pd.read_csv(self.name,engine="python")
            else:
                self.data=pd.read_csv(self.name,engine="python")
        
        self.__read=True
        self.__managing_cat
        self.__managing_null
    @property
    def __managing_cat(self):
            L=[]
            
            
            self.data.set_index('Date',inplace=True)
            print(self.data)
            for i in self.data.columns:
                    if self.data[i].dtype=='object':
                            L.append(i)
            
            for j in L:
                lb=LabelEncoder()
                self.data[j]=lb.fit_transform(self.data[j])
    
    @property
    def __managing_null(self):
            M={}
            for k in self.data.columns:
                    M[k]=[self.data[k].isnull().sum()]
            print(M)
            self.data.dropna(inplace=True)
            temp=pd.DataFrame(M)
            temp.to_csv('dataFiles/Null.csv') 
            print(self.data)
    @property
    def Getting_description(self):
        if not self.__read:
                print('You first have to read the data')
                sys.exit(1)
        self.temp=self.data.describe()
        try:
            self.temp.to_csv('dataFiles/Desc.csv')
        except:
            raise('First you have to read a data')
    
                
                    
    @property
    def Getting_plots(self,roll_av_value=100):
        if not self.__read:
                    print('You first have to read the data')
                    sys.exit(1)
        Path='dataFiles'
        if 'Analysis' not in os.listdir('dataFiles'):
                os.mkdir('dataFiles/Analysis')
        c=0
        for l in self.data.columns:
                fig=plt.figure(figsize=(12,12))
                ax1 = plt.subplot2grid((7,1), (0,0), rowspan=5, colspan=1)
                ax2 = plt.subplot2grid((7,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
                ax3=plt.subplot2grid((7,1),(6,0),rowspan=1,colspan=1,sharex=ax2)
                self.data[l].plot(ax=ax1,use_index=True,figsize=(12,12))
                self.data[l].rolling(window=roll_av_value).mean().plot(ax=ax1,use_index=True,figsize=(12,12),label='Mean')
                self.data[l].rolling(window=roll_av_value).std().plot(ax=ax1,use_index=True,figsize=(12,12),label='STdev')
                self.data['Volume'].rolling(window=roll_av_value).mean().plot(ax=ax2,use_index=True,figsize=(12,12),label='Volume_mean')
                self.data['Volume'].rolling(window=roll_av_value).mean().plot(ax=ax3,use_index=True,figsize=(12,12),label='Volume_std')
                plt.title(f'Moving Average analysis on {l}',size=18,loc='right')
                ax1.legend(loc='best')
                ax2.legend(loc='best')
                ax3.legend(loc='best')
                plt.savefig(f'dataFiles/Analysis/ID{c}.png')
                c+=1
        
                
        print(self.data.iloc[:,1:])
        for i in self.data.columns:
                fig=plt.figure(figsize=(12,12))
                self.data[i].plot()
                plt.savefig(f'dataFiles/{i}.png')
        plt.savefig('dataFiles/simple.jpg')
        if  "Histograms" not in os.listdir('dataFiles'):
                    os.mkdir('dataFiles/Histograms')
        
        c=0
        for i in self.data.columns[1:]:
                fig=plt.figure(figsize=(12,12))
                plt.hist(self.data[i])
                plt.title(i,size=14)
                plt.savefig(f'dataFiles/Histograms/Histograms_{c}.jpg')
                c+=1
        sns.pairplot(self.data[1:])
        plt.savefig('dataFiles/PairPLot_main.png')
        
        
        
    
        
    
    @property
    def distribution(self,histo=True,rug=False):
        # distplots
        
        if 'Distribution' not in os.listdir('dataFiles'):
            os.mkdir('dataFiles/Distribution')
        c=0
        for k in self.data.columns[1:]:
                fig=plt.figure(figsize=(12,12))
                sns.distplot(self.data[k].values,hist=histo,rug=rug)
                plt.title(k,size=17)
                plt.savefig(f'dataFiles/Distribution/Distributionplot_{str(c)}.png')
                c+=1
        self.corr=self.data[1:].corr()
        sns.heatmap(self.corr)
        plt.savefig('dataFiles/Heatmap.png')
            
    @property
    def Outliers(self):
        if 'Outliers' not in os.listdir('dataFiles'):
            os.mkdir('dataFiles/Outliers')
        c=0
        for k in self.data.columns[1:]:
                fig=plt.figure(c+1,figsize=(12,12))
                sns.boxplot(self.data[k])
                plt.savefig(f'dataFiles/Outliers/box_{str(c)}.png')
                c+=1
    
    def Laura(self):
            plt.plot(self.data['Adj Close'])
            plt.show()

        
        
        
        
if __name__=='__main__':
    G=Stats('tsla.csv')
    G.Load_data()
    G.Getting_plots
    
                 
#Date,Open,High,Low,Close,Adj Close,Volume