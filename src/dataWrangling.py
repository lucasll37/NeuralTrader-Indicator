import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from variable import *


def auxCreateColumns():
    nameColumns = []
    for i in range(-stepsBack, stepsFoward+1, 1):
        if i == 0:
            continue

        elif i > 0:
            nameColumns.append('Close(+{})'.format(i))

        else:
            nameColumns.append('Close({})'.format(i))

    return nameColumns


def generatorTimeframeTable(table):
    nameColumns = auxCreateColumns()
    totalSteps = stepsBack + stepsFoward
    TimeframeTable = pd.DataFrame(np.zeros((len(table) - totalSteps, totalSteps)),
                                  index=table.index[stepsBack: len(
                                      table) - stepsFoward],
                                  columns=nameColumns)

    for index, close in enumerate(table['Close']):
        tempA = index
        tempB = 0
        for i in range(totalSteps):
            if tempA < len(table['Close'])-totalSteps and tempA >= 0:
                TimeframeTable.iloc[tempA, tempB] = close

            tempA -= 1
            tempB += 1

    return TimeframeTable


def scalerTimeframeTable(timeframeTable):
    mean = timeframeTable.sum(axis=1)/(stepsBack + stepsFoward)
    sd = timeframeTable.iloc[:, :stepsBack].std(axis=1)
    for column in timeframeTable.columns:
        timeframeTable.loc[:, column] = (
            timeframeTable.loc[:, column] - mean)/sd


def Preprocessingdata(timeframeTable, validationSize=0.000001):
    # ------Divisão de dados entre Treino, Teste e Validação-----------------------------------------------
    X = timeframeTable.iloc[:, :stepsBack].to_numpy()
    y = timeframeTable.iloc[:, -stepsFoward:].to_numpy()
    X, X_validation, y, y_validation = train_test_split(X, y, test_size=validationSize, shuffle=False)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize, shuffle=False)

    X_train = X_train.reshape((-1, stepsBack, 1))
    X_test = X_test.reshape((-1, stepsBack, 1))
    y_train = y_train.reshape((-1, stepsFoward))
    y_test = y_test.reshape((-1, stepsFoward))

    # PROBLEMAS PARA O GRIDSEARCH?
    X_validation = X_validation.reshape((-1, stepsBack, 1))
    y_validation = y_validation.reshape((-1, stepsFoward))

    print("Preprocessing data done")
    print("X_train shape: {}".format(X_train.shape))
    print("X_test shape: {}".format(X_test.shape))
    print("X_validation shape: {}".format(X_validation.shape))
    # -----------------------------------------------------------------------------------------------

    return [X_train, X_test, X_validation, y_train, y_test, y_validation]
