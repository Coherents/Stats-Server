# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys
import optparse
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
        if 'dataFiles' not in os.listdir(os.path.join(os.getcwd(),'Server')):
            os.mkdir('Server/dataFiles')
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
            temp=pd.DataFrame(M)
            temp.to_csv('Server/dataFiles/Null.csv') 
            print(self.data)
    @property
    def Getting_description(self):
        if not self.__read:
                print('You first have to read the data')
                sys.exit(1)
        self.temp=self.data.describe()
        try:
            self.temp.to_csv('Server/dataFiles/Desc.csv')
        except:
            raise('First you have to read a data')
    
                
                    
    @property
    def Getting_plots(self):
        if not self.__read:
                    print('You first have to read the data')
                    sys.exit(1)
        Path='Server/dataFiles'
        
        print(self.data.iloc[:,1:])
        for i in self.data.columns:
                fig=plt.figure(figsize=(12,12))
                self.data[i].plot()
                plt.savefig(f'Server/dataFiles/{i}.png')
        plt.savefig('Server/dataFiles/simple.jpg')
        if  "Histograms" not in os.listdir('Server/dataFiles'):
                    os.mkdir('Server/dataFiles/Histograms')
        
        c=0
        for i in self.data.columns[1:]:
                fig=plt.figure(figsize=(12,12))
                plt.hist(self.data[i])
                plt.title(i,size=14)
                plt.savefig(f'Server/dataFiles/Histograms/Histograms_{c}.jpg')
                c+=1
        sns.pairplot(self.data[1:])
        plt.savefig('Server/dataFiles/PairPLot_main.png')
        
        
        
    
        
    
    @property
    def distribution(self,histo=True,rug=False):
        # distplots
        
        if 'Distribution' not in os.listdir('Server/dataFiles'):
            os.mkdir('Server/dataFiles/Distribution')
        c=0
        for k in self.data.columns[1:]:
                fig=plt.figure(figsize=(12,12))
                sns.distplot(self.data[k].values,hist=histo,rug=rug)
                plt.title(k,size=17)
                plt.savefig(f'Server/dataFiles/Distribution/Distributionplot_{str(c)}.png')
                c+=1
        self.corr=self.data[1:].corr()
        sns.heatmap(self.corr)
        plt.savefig('Server/dataFiles/Heatmap.png')
            
    @property
    def Outliers(self):
        if 'Outliers' not in os.listdir('Server/dataFiles'):
            os.mkdir('Server/dataFiles/Outliers')
        c=0
        for k in self.data.columns[1:]:
                fig=plt.figure(c+1,figsize=(12,12))
                sns.boxplot(self.data[k])
                plt.savefig(f'Server/dataFiles/Outliers/box_{str(c)}.png')
                c+=1
    
    def Laura(self):
            plt.plot(self.data['Adj Close'])
            plt.show()

        
        
        
        
if __name__=='__main__':
    G=Stats('tsla.csv')
    G.Load_data()
    G.Getting_plots
    
                 
#Date,Open,High,Low,Close,Adj Close,Volume