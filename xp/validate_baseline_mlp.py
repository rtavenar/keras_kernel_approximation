import numpy

from utils.model_utils import print_train_valid
from utils.prepare_data import load_tiselac
from keras_models.model_zoo import model_mlp

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'

# Params
d = 10
sz = 23
n_classes = 9

n_units_hidden_layers = [256, 128, 64]

validation_split = .05

# Load training data
X, X_coord, y = load_tiselac(training_set=True, shuffle=True, random_state=0)

# Load model
fname_model = "output/models_baseline/mlp.256-128-64.00055-0.2315.weights.hdf5"

# Model definition
model = model_mlp(input_shape=(sz * d + 2, ), hidden_layers=n_units_hidden_layers, n_classes=n_classes)
model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])
model.load_weights(fname_model)

print_train_valid(model=model, X=numpy.hstack((X, X_coord)), y=y, validation_split=validation_split)
