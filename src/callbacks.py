from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TerminateOnNaN
from datetime import datetime
from variable import *

tensorboard = TensorBoard(
    log_dir="logs/{}".format(datetime.now().strftime('%d-%B-%Ih%Mmin')))

checkpoint = ModelCheckpoint(checkpoint,
                             monitor="val_loss",
                             verbose=1,
                             save_best_only=True,
                             save_weights_only=False,
                             mode="min",
                             save_freq="epoch")

earlystop = EarlyStopping(monitor='val_loss',
                          min_delta=0,
                          patience=20,
                          verbose=verbose,
                          restore_best_weights=True)

reduceLr = ReduceLROnPlateau(monitor='loss',
                             factor=0.2,
                             patience=3,
                             mode="min",
                             verbose=verbose,
                             min_delta=0.0001,
                             min_lr=0)

callbacksGrid = [tensorboard, earlystop, reduceLr, TerminateOnNaN()]
callbacksTrain = [tensorboard, checkpoint,
                  earlystop, reduceLr, TerminateOnNaN()]
