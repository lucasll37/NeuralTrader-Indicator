from datetime import datetime

_PIP = 0.0001

# ---- MetaTrader5 --------------
# //////////////////////////////////////
account = 'Demo'  # 'Real' or 'Demo' ///
# //////////////////////////////////////

###################
pathModel = './saveModel'
pathModelTrain = pathModel + '/20-January-06h53min/'
symbol = "EURUSD"
###################
tpDelta = 1
slDelta = 1
deviation = 20
trailStopSpeed = 1
fee = 2 * _PIP
lot = 0.01
startDate = datetime(2022, 11, 3)
###################
CoefAngInf = -0.20
CoefAngSup = 0.20
maxIndLucas = 1.5
minModDelta = 20 * _PIP
###################
graphic = True
###################
stepsBack = 90
stepsFoward = 15
stepsShow = 90

# ---- Train ---------------
trainCandles = 100000
useSaveModel = True
selection = False
downloadData = False
epochs = 1000
testSize = 0.2
validationSize = 0.1
verbose = 2
seed = 25
batchSize = 64
nKFold = 5
layers = 1
n_lstm = 180
dropoutFoward = 0
learning_rate = 0.01
stdParamGrid = 2
checkpoint = './saveModel/tmp/best_model_checkpoint.hdf5'
# --------------------------
