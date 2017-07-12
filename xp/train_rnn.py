from utils.prepare_data import load_tiselac
from utils.model_utils import model_fit_and_save, print_eval
from keras_models.model_zoo import model_rnn

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'

# Params
d = 10
sz = 23
n_classes = 9

dim_rnn = 256
n_units_hidden_layers = [128, 64]

# Load training data
X, X_coord, y, X_test, X_coord_test, y_test = load_tiselac(training_set=True, test_split=.05, shuffle=True,
                                                           random_state=0)
X = X.reshape((-1, sz, d))
X_test = X_test.reshape((-1, sz, d))

# Model definition
model = model_rnn(input_shape=(sz, d), hidden_layers=n_units_hidden_layers, rnn_layer_dim=dim_rnn,
                  input_shape_side_info=(2, ), n_classes=n_classes, use_lstm=True)
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Just check that weights are shared, not repeated as many times as the number of features in the sets
print("Weights:", [w.shape for w in model.get_weights()])
print("Total number of parameters:", model.count_params())

# Fit
basename = "output/models_baseline/rnn.%d." % dim_rnn
for n_units in n_units_hidden_layers:
    basename += "%d-" % n_units
basename = basename[:-1]
fname_weights = model_fit_and_save(model, basename, X=[X, X_coord], y=y, patience_early_stopping=100, save_acc=True,
                                   validation_split=0.1)
model.load_weights(fname_weights)

# Go!
print_eval(model, [X_test, X_coord_test], y_test)
