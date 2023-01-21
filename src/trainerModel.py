from datetime import datetime
from model import create_model
from dataWrangling import generatorTimeframeTable, scalerTimeframeTable, Preprocessingdata
from variable import *
from callbacks import callbacksTrain


def trainer(rates_frame, checkpoint = None):
    timeframeTable = generatorTimeframeTable(rates_frame)
    scalerTimeframeTable(timeframeTable)
    X_train, X_test, X_validation, y_train, y_test, y_validation = Preprocessingdata(timeframeTable, validationSize)


    model = create_model(checkpoint)

    model.fit(x = X_train,
              y = y_train,
              batch_size = batchSize,
              epochs = epochs,
              verbose = verbose,
              validation_data = (X_test, y_test),
              callbacks = callbacksTrain)

    nameFolder = datetime.now().strftime('%d-%B-%Ih%Mmin')
    outdir = '{}/{}'.format(pathModel, nameFolder)
    outdirCompatible = '{}/{}-compatible.h5'.format(pathModel, nameFolder)

    #---------Save Model---------------------------
    model.save(outdir,
               overwrite = False,
               include_optimizer = True,
               save_format = 'tf')

    model.save(outdirCompatible,
               overwrite = False,
               include_optimizer = True,
               save_format = 'h5')
    #----------------------------------------------

    scoreTrain = model.evaluate(X_train, y_train)
    scoreTest = model.evaluate(X_test, y_test)
    scoreValidation = model.evaluate(X_validation, y_validation)

    print('\nErro quadrático médio em dados de treinamento: {:.5f} \
           \nErro quadrático médio em dados de teste: {:.5f} \
           \nErro quadrático médio em dados de validação: {:.5f}\n' \
          .format(scoreTrain, scoreTest, scoreValidation))

    return model