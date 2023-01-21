# Bibliotecas e Frameworks
import numpy as np
from variable import *
from sklearn.linear_model import LinearRegression


def indicatorLucas(frameCurrent, mean, std):
    closeStd = (frameCurrent['Close'][:stepsBack] - mean)/std
    openStd = (frameCurrent['Open'][:stepsBack] - mean)/std
    highStd = (frameCurrent['High'][:stepsBack] - mean)/std
    lowStd = (frameCurrent['Low'][:stepsBack] - mean)/std

    openCloseStd = np.abs(openStd - closeStd)
    highLowStd = np.abs(highStd - lowStd)
    weights = np.linspace(0, 1, stepsBack)  ** 10
    highLowStdWighted = ((highLowStd * weights)/weights.sum()).sum()
    openCloseStdWighted = ((openCloseStd * weights)/weights.sum()).sum()
    indLucas = ((highLowStdWighted / openCloseStdWighted) - 1)

    return indLucas


def LinRegression(rates_frameStd, std, mean, yStd, trainMode = False):
    x = np.array([i for i in range(1, stepsFoward+1)]).reshape(-1, 1)
    regr = LinearRegression().fit(x, yStd)
    CoefAng = regr.coef_[0, 0]
    RScore = regr.score(x, yStd)
    predictionStd = regr.predict(x)
    prediction = predictionStd * std + mean
    if trainMode:
        priceTraderStd = rates_frameStd['Close'][-stepsFoward]
        priceTrader = priceTraderStd * std + mean

    else:
        priceTraderStd = rates_frameStd['Close'][-1]
        priceTrader = priceTraderStd * std + mean

    y = yStd * std + mean
    deltaStd = predictionStd[-1, 0]-predictionStd[0, 0]
    takeProfitStd = priceTraderStd + tpDelta * deltaStd
    stopLossStd = priceTraderStd - slDelta * deltaStd
    delta = deltaStd * std
    takeProfit = takeProfitStd * std + mean
    stopLoss = stopLossStd * std + mean

    return [CoefAng, RScore, prediction, priceTrader, delta, takeProfit, stopLoss, y]