import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys
import argparse
import seaborn as sns


class Stats(object):
    def __init__(self,name,type="csv",req_sep=False):
        self.name=name
        self.type1=type
        self.sep=req_sep
        self.__data=None
    def Load_data(self,head_included=False):
        if not head_included:
            if not self.sep:
                self.data=pd.read_csv(self.name,engine="python",header=None)
            else:
               self.data=pd.read_csv(self.name,engine="python",header=None)
        else:
            if not self.sep:
                self.data=pd.read_csv(self.name,engine="python")
            else:
                self.data=pd.read_csv(self.name,engine="python")
        print(self.data)
    @property
    def Getting_info(self):
        self.temp=self.data.describe()
        self.temp.to_csv('Desc.csv')
        
    
    @property
    def Getting_plots(self):
        pass
    
    @property
    def distribution(self):
        pass
    @property
    def Ouliers(self):
        pass

        
        
        
        
if __name__=='__main__':
    pass

    
                 
            