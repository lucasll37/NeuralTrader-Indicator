#!/usr/bin/env python
# coding: utf-8

# Bibliotecas e Frameworks
import numpy as np
import pandas as pd
from keras.models import load_model
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import os
from pandas.plotting import register_matplotlib_converters
from downloadData import getData
from variable import *
from trainerModel import trainer
from graphicTrain import graphicTrain
from checkGPU import checkGPU
from utils import indicatorLucas, LinRegression

sns.set_style('whitegrid')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
plt.rcParams['figure.figsize'] = (15, 10)
register_matplotlib_converters()
np.random.seed(seed)

# Confirma se o TensorFlow pode acessar a GPU
checkGPU()

# Download dos Dados
rates_frame = getData()

# Model
if useSaveModel:
    model = load_model(pathModelTrain)

else:
    model = trainer(rates_frame, checkpoint)

info = pd.DataFrame(
    columns=['Coef. Ang.(std)', 'RScore', 'Ind. Lucas', 'Delta', 'Std Deviation'])
infoSelected = pd.DataFrame(
    columns=['Coef. Ang.(std)', 'RScore', 'Ind. Lucas', 'Delta', 'Std Deviation'])
outdir = './graphics/train/{}/'.format(
    datetime.now().strftime('%d-%B-%Ih%Mmin'))

if not os.path.exists(outdir):
    os.mkdir(outdir)

stepsTotal = stepsBack + stepsFoward
rates_frameTest = rates_frame[-int(validationSize * trainCandles):]

for i in range(0, len(rates_frameTest)-stepsTotal, 1):
    frameCurrent = rates_frameTest.iloc[i: i + stepsTotal, :]
    std = frameCurrent['Close'].std()
    mean = frameCurrent['Close'].mean()
    rates_frameStd = (
        frameCurrent[["Open", "High", "Low", "Close"]] - mean)/std
    rates_frameStd['Volume'] = frameCurrent['Volume']

    # ----------Indice de Lucas ------------------------------------------
    indLucas = indicatorLucas(frameCurrent, mean, std)
    # --------------------------------------------------------------------

    # -------Prediction---------------------------------------------------
    X = rates_frameStd['Close'][:stepsBack].to_numpy().reshape(1, stepsBack, 1)
    yStd = model.predict(X, verbose=0).reshape(stepsFoward, 1)

    epsilon = yStd[0, 0] - rates_frameStd['Close'][-stepsFoward]
    yStd = yStd - epsilon
    # --------------------------------------------------------------------

    # -----Regressão Linear-----------------------------------------------
    CoefAng, RScore, prediction, priceTrader, delta, takeProfit, stopLoss, y \
        = LinRegression(rates_frameStd, std, mean, yStd, trainMode=True)
    # --------------------------------------------------------------------

    # ------Popula tabela info--------------------------------------------
    newLine = {'Coef. Ang.(std)': CoefAng,
               'RScore': RScore,
               'Ind. Lucas': indLucas,
               'Delta': delta,
               'Std Deviation': std}

    info = info.append(pd.DataFrame([newLine]), ignore_index=True)
    # --------------------------------------------------------------------

    if delta > 0:
        action = 'BUY'

    else:
        action = 'SELL'

    # -----Seleção--------------------------------------------------------
    if selection:
        boolCoefAngInf = not(CoefAng < CoefAngInf)
        boolCoefAngSup = not(CoefAng > CoefAngSup)
        boolIndLucas = not(indLucas < maxIndLucas)
        boolDelta = not(np.abs(delta) > minModDelta)

        if((boolCoefAngInf & boolCoefAngSup) | boolIndLucas | boolDelta):
            continue

        infoSelected = infoSelected.append(
            pd.DataFrame([newLine]), ignore_index=True)
    # --------------------------------------------------------------------

    # -----------Grafhic--------------------------------------------------
    if graphic:
        graphicTrain(frameCurrent,
                     RScore,
                     prediction,
                     indLucas,
                     priceTrader,
                     CoefAng,
                     delta,
                     stopLoss,
                     takeProfit,
                     std,
                     outdir,
                     action,
                     y)

info.to_excel(
    './data/resultTrain {}.xlsx'.format(frameCurrent.index[-1].strftime('%Y-%m-%d %Hh%Mm%Ss')))

if selection:
    print('Oportunidade de Operação: {}'.format(infoSelected.shape[0]))
    infoSelected.to_excel('./data/resultTrainSelected {}.xlsx'
                          .format(frameCurrent.index[-1].strftime('%Y-%m-%d %Hh%Mm%Ss')))
