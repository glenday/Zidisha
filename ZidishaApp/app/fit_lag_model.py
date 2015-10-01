import numpy as np
import scipy.signal as sps
import statsmodels.api as sm
__author__ = 'alexglenday'


def rect_window_filter(data: np.array, window_length: int) -> np.array:
    window_length = np.round(window_length)
    if window_length:
        if window_length % 2 == 0:  # even length window
            front_pad = window_length/2
            end_pad = window_length/2
            norm_window = np.repeat(1.0, window_length + 1)
            norm_window[0] = 0.5
            norm_window[-1] = 0.5
            norm_window /= window_length
        else:  # odd length window
            front_pad = (window_length - 1)/2
            end_pad = front_pad
            norm_window = np.repeat(1.0, window_length) / window_length
        data_long = np.pad(data, ((front_pad, end_pad),), mode='edge')
        data_filtered = sps.convolve(data_long, norm_window, 'valid')
    else:
        data_filtered = data.copy()
    return data_filtered


def fit_lag_model(list_indep_vars: list,
                  dep_var: np.array,
                  list_indep_labels: list,
                  list_indep_max_lag: list,
                  list_indep_link_slopes_to_lag: list,
                  list_indep_max_slope: list
                  ) -> :

class FitLagModel(object):

    def __init__(self, list_indep_vars: list, response_vector):
        self.fit_matrix = fit_matrix
        self.response_vector = response_vector
        self.num_params = 0
        self.labels = [""]
