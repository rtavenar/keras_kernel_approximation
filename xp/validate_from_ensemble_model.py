import numpy
import os

from utils.prepare_data import load_tiselac
from utils.model_utils import print_train_valid_test, load_model

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'

# Params
d = 10
sz = 23
n_classes = 9

validation_split = .1
test_split = .05

# Load training data
X, X_coord, y = load_tiselac(training_set=True, shuffle=True, random_state=0)

fname_ensemble = "output/models_ensemble/mlp_rnn_rff.64-32.rnn.256.128-64.00409-0.9404.mlp.256-128-64.00258-0.9440." + \
                 "mlp_rff.256-128-64.00316-0.9456.00080-0.9514.weights.hdf5"

splitted_fname = os.path.basename(fname_ensemble).split(".")
n_units_hidden_layers_ensemble = [int(s) for s in splitted_fname[1].split("-")]

# =========
# RFF stuff
# =========
fname_model_rff = os.path.join("output/models_baseline/",
                               "mlp_rff.256-128-64.00316-0.9456.weights.hdf5")
rff_model = load_model(fname_model_rff, sz=sz, d=d, d_side_info=2)
rff_features = rff_model.predict(numpy.hstack((X, X_coord)))

# =========
# RNN stuff
# =========
X_rnn = X.reshape((-1, sz, d))
fname_model_rnn = os.path.join("output/models_baseline/",
                               fname_ensemble[fname_ensemble.rfind("rnn."):fname_ensemble.rfind(".mlp.")]
                               + ".weights.hdf5")
rnn_model = load_model(fname_model_rnn, sz=sz, d=d, d_side_info=2)
rnn_features = rnn_model.predict([X_rnn, X_coord])

# =========
# MLP stuff
# =========
fname_model_mlp = os.path.join("output/models_baseline/",
                               fname_ensemble[fname_ensemble.rfind("mlp."):fname_ensemble.rfind(".mlp_rff.")]
                               + ".weights.hdf5")
mlp_model = load_model(fname_model_mlp, sz=sz, d=d, d_side_info=2)
mlp_features = mlp_model.predict(numpy.hstack((X, X_coord)))

# ==============
# Ensemble stuff
# ==============
ensemble_features = numpy.hstack((mlp_features, rnn_features, rff_features))
ensemble_model = load_model(fname_ensemble, sz=ensemble_features.shape[1], d=1, n_classes=n_classes)

print_train_valid_test(model=ensemble_model, X=ensemble_features, y=y, validation_split=validation_split,
                       test_split=test_split)
