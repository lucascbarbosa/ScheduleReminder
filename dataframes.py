import pandas as pd
import time
import datetime
from math import isnan


def Nao(x):
    try:
        if isnan(x):
            return 'Nao'
        else:
            return x
    except TypeError:
        return x

def extractData():

    cons = pd.read_excel('Excel/Consultas.xlsx')
    cons.set_index('Nome',inplace = True)
    hist = pd.read_excel('Excel/Histórico.xlsx')
    hist.set_index('Nome',inplace = True)
    hist['Enviado'] = hist['Enviado'].apply(lambda x: Nao(x))

    return cons,hist




