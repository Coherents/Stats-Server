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

def validate_data(read:bool):
        def inner(f:Function):
                if read:
                     return f
                else:
                    raise('First data has to be read')
        return inner

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
        print(self.data)
        self.__read=True
        self.__managing_cat
        self.__managing_null
    @property
    def __managing_cat(self):
            L=[]
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
        plt.plot(self.data.iloc[:,1:])
        plt.savefig('Server/dataFiles/simple.png')
        plt.hist(self.data.iloc[:,1:])
        plt.savefig('Server/dataFiles/Hist.png')
        sns.pairplot(self.data)
        plt.savefig('Server/dataFiles/PairPLot_main.png')
        for i in self.data.columns:
                try:
                    sns.pairplot(self.data,hue=i)
                    plt.savefig(f'{Path}/PairPlot_on_{i}.png')
                except:
                    continue;
        sns.heatmap(self.data.iloc[:,1:],fmt=".2f")
        plt.savefig(f'{Path}/Heatmap.png')
    
        
    
    @property
    def distribution(self):
        for i in self.data.columns:
                print(i,self.data[i].dtype)
            
    @property
    def Ouliers(self):
        pass

        
        
        
        
if __name__=='__main__':
    G=Stats('class.csv')
    G.Load_data()
    G.Getting_plots
    
                 
            