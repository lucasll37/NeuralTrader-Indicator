from keras.optimizers import *
from variable import learning_rate


opt_SGD = SGD(
    learning_rate = learning_rate,
    momentum = 0.0,
    nesterov = False)

opt_RMSprop = RMSprop(
    learning_rate = learning_rate,
    rho = 0.9,
    momentum = 0.0,
    epsilon = 1e-07,
    centered = False)

opt_Adam = Adam(
    learning_rate = learning_rate,
    beta_1 = 0.9,
    beta_2 = 0.999,
    epsilon = 1e-07,
    amsgrad = False)

opt_Adadelta = Adadelta(
    learning_rate = learning_rate,
    rho = 0.95,
    epsilon = 1e-07)

opt_Adagrad = Adagrad(
    learning_rate = learning_rate,
    initial_accumulator_value = 0.1,
    epsilon = 1e-07)

opt_Adamax = Adamax(
    learning_rate = learning_rate,
    beta_1 = 0.9,
    beta_2 = 0.999,
    epsilon = 1e-07)

opt_Nadam = Nadam(
    learning_rate = learning_rate,
    beta_1 = 0.9,
    beta_2 = 0.999,
    epsilon = 1e-07)

opt_Ftrl = Ftrl(
    learning_rate = learning_rate,
    learning_rate_power = -0.5,
    initial_accumulator_value = 0.1,
    l1_regularization_strength = 0.0,
    l2_regularization_strength = 0.0,
    l2_shrinkage_regularization_strength = 0.0,
    beta = 0.0)