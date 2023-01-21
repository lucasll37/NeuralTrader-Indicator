from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential
from keras.losses import MeanSquaredError
from variable import *
from optimizers import opt_Adagrad
import os


def create_model(checkpoint=None,
                 optimizer=opt_Adagrad,
                 layers=layers,
                 n_lstm=n_lstm,
                 dropoutFoward=dropoutFoward,
                 stepsBack=stepsBack,
                 stepsFoward=stepsFoward,
                 ):

    model = Sequential()
    model.add(LSTM(n_lstm,
                   activation='tanh',
                   recurrent_activation='sigmoid',
                   return_sequences=True,
                   input_shape=(stepsBack, 1)))
    #################################################################
    for _ in range(layers):
        model.add(Dropout(dropoutFoward))
        model.add(LSTM(n_lstm,
                       activation='tanh',
                       recurrent_activation='sigmoid',
                       return_sequences=True))
    ##################################################################
    model.add(LSTM(n_lstm,
                   activation='tanh',
                   recurrent_activation='sigmoid',
                   return_sequences=False))

    model.add(Dense(stepsFoward, activation='linear'))
    Lmse = MeanSquaredError()

    if (checkpoint != None) and (os.path.exists(checkpoint)):
        model.load_weights(checkpoint)

    model.compile(loss=Lmse, optimizer=optimizer)

    return model
