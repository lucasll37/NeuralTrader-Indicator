from datetime import datetime

_PIP = 0.0001

# ---- Trader --------------
# //////////////////////////////////////
account = 'Real'  # 'Real' or 'Demo' ///
# //////////////////////////////////////

# operation = True
###################
pathModel = './saveModel'
pathModelTrain = pathModel + '/20-January-06h53min/'
symbol = "EURUSD"

# startDate = datetime(2022, 11, 3)
# lot = 0.01
# deviation = 20
###################
# tpDelta = 1
# slDelta = 1
###################
# maxLoss24h = 50
# maxLoss = 100
###################
CoefAngInf = -0.20
CoefAngSup = 0.20
maxIndLucas = 1.5
minModDelta = 20 * _PIP
###################
# restrictWeekday = False
# restrictHour = False
# fixedDelta = False
# decreaseDelta = False
#trailStop = False
graphic = True
###################
stepsBack = 90
stepsFoward = 15
stepsShow = 90
###################
# RESTRICT WEEKDAY 0: Monday ... 6: Sunday
# intervalOper = 25
# startWeekday = 0  # inclusive
# stopWeekday = 6  # inclusive
###################
# RESTRICT HOUR
# local + 6
# startHour = 0  # inclusive
# stopHour = 23  # inclusive
###################
# FIXED DELTA
# estaticDelta = 20 * _PIP
###################
# DECREASE DELTA
# maxModDelta = 30 * _PIP
###################
# TRAIL STOP
# trailStopSpeed = 1
# fee = 2 * _PIP


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
