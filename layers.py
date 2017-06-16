from keras.layers import Dense
import keras.backend as K

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


class CosineActivatedDenseLayer(Dense):
    """Layer that mimics the behaviour or a Random Fourier Feature extractor.

    This is nothing more than a densely connected layer with cosine activation."""
    def __init__(self, units,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(CosineActivatedDenseLayer, self).__init__(units,
                                                        use_bias=use_bias,
                                                        kernel_initializer=kernel_initializer,
                                                        bias_initializer=bias_initializer,
                                                        kernel_regularizer=kernel_regularizer,
                                                        bias_regularizer=bias_regularizer,
                                                        activity_regularizer=activity_regularizer,
                                                        kernel_constraint=kernel_constraint,
                                                        bias_constraint=bias_constraint,
                                                        **kwargs)
        self.activation = K.cos