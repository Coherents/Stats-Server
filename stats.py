import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys
import argparse
import seaborn as sns
from sklearn.preprocessing import LabelEncoder,OneHotEncoder



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
        print(self.data)
        self.__read=True
    @property
    def Getting_description(self):
        if not self.__read:
                raise('You First have to read the data before analysis')
        self.temp=self.data.describe()
        try:
            self.temp.to_csv('dataFiles/Desc.csv')
        except:
            raise('First you have to read a data')
    @property
    def Getting_plots(self):
        
        print(self.data.iloc[:,2:])
        plt.plot(self.data.iloc[:,2:])
        plt.savefig('dataFiles/simple.png')
    
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
    
                 
            