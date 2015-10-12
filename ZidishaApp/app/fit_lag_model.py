import numpy as np
import pandas as pd
import scipy.signal as sps
import statsmodels.api as sm
import matplotlib.pyplot as plt
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


def causal_rect_window_filter(data: np.array, window_length: int) -> np.array:
    window_length = np.round(window_length)
    if window_length > 0:
        front_pad = window_length - 1
        end_pad = 0
        norm_window = np.repeat(1.0, window_length) / window_length
        data_long = np.pad(data, ((front_pad, end_pad),), mode='edge')
        # avoid fftconvolve as it distributes one input NaN to entire output
        data_filtered = sps.convolve(data_long, norm_window, 'valid')
    else:
        data_filtered = data.copy()
    return data_filtered


def causal_hann_window_filter(data: np.array, window_length: int) -> np.array:
    window_length = np.round(window_length)
    if window_length > 0:
        front_pad = window_length
        end_pad = 1
        norm_window = sps.hann(window_length + 2)
        norm_window /= np.sum(norm_window)
        data_long = np.pad(data, ((front_pad, end_pad),), mode='edge')
        # avoid fftconvolve as it distributes one input NaN to entire output
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
                  ) -> sm.regression:
    pass


class LaggedParameter(object):

    def __init__(self, data: np.array,
                 label: str,
                 transition_length: int,
                 shift_size: int=0,
                 filter_type: str='hann'):
        """
        Process data to be lagged with a smooth transition determined by the filter type and shift.
        :param data: Data to be lagged.
        :param label: Label for data.
        :param transition_length: Number of points over which the lag transition occurs.
        :param shift_size: Number of points to shift the data.
        :param filter_type: Type of filter to use to generate the transition.
        :raise ValueError: Error if the filter_type is not valid.
        """
        self.data = data.copy()
        self.label = label
        self.transition_length = transition_length
        self.window_size = self.transition_length + 1
        self.shift_size = np.round(shift_size)

        dict_filter_type_func = {'none': None,
                                'rect': causal_rect_window_filter,
                                'hann': causal_hann_window_filter
                                }

        try:
            filter_func = dict_filter_type_func[filter_type]
        except KeyError:
            type_str = ', '.join(dict_filter_type_func.keys())
            raise ValueError(filter_type+' is not a valid type of binning. Valid types: '+type_str)

        self.use_shift = self.shift_size > 0
        if filter_func is not None:
            self.data = filter_func(self.data, self.window_size)

        if self.use_shift:
            self.data = self.data[:-self.shift_size]


class LagModel(object):

    def __init__(self, list_lagged_parameters: list,
                 response_array: np.array,
                 time_array: pd.DatetimeIndex,
                 use_constant: bool=True,
                 data_variance: np.array=None):
        self.list_lagged_parameters = list_lagged_parameters.copy()
        self.response_array = response_array.copy()
        self.time_array = time_array.values.copy()
        self.use_constant = use_constant
        self.use_weights = data_variance is not None

        self.num_params = len(self.list_lagged_parameters)
        self.list_labels = []
        self.max_shift = 0

        if self.use_constant:
            self.num_params += 1
            self.list_labels.append('Constant')

        # Find max shift, necessary to clip all data to the same size
        for param in self.list_lagged_parameters:
            self.list_labels.append(param.label)
            if param.shift_size > self.max_shift:
                self.max_shift = param.shift_size

        # Clip initial points in the un-shifted response and time data
        self.response_array = self.response_array[self.max_shift:]
        self.time_array = self.time_array[self.max_shift:]
        self.clipped_data_length = len(self.response_array)
        if self.use_weights:
            self.weights = 1.0 / data_variance[self.max_shift:]

        self.list_lagged_arrays = []
        if self.use_constant:
            self.constant_array = np.ones(self.clipped_data_length)
            self.list_lagged_arrays.append(self.constant_array)

        # Extract clipped views of the lagged parameters
        for param in self.list_lagged_parameters:
            shift = self.max_shift - param.shift_size
            self.list_lagged_arrays.append(param.data[shift:])

        # Range of data to use in fit
        self.start_index = 0
        self.end_index = self.clipped_data_length - 1

        self.has_results = False
        self.fit_matrix = None
        self.model = None
        self.results = None
        self.auto_correlation_matrix = None
        self.time_axis = None
        self.response_cut = None

    def fit(self, start_time: np.datetime64=None, end_time: np.datetime64=None):

        # Find cut indices
        if start_time:
            self.start_index = np.searchsorted(self.time_array, start_time)
        if end_time:
            self.end_index = np.searchsorted(self.time_array, end_time)

        self.time_axis = self.time_array[self.start_index: self.end_index]
        self.response_cut = self.response_array[self.start_index: self.end_index]

        # List of cut views of parameters
        list_cut_arrays = []
        for param in self.list_lagged_arrays:
            list_cut_arrays.append(param[self.start_index: self.end_index])

        self.fit_matrix = np.transpose(np.array(list_cut_arrays))
        if self.use_weights:  # Solve WLS
            weights_array = self.weights[self.start_index: self.end_index]
            self.model = sm.WLS(self.response_cut, self.fit_matrix, weights=weights_array)
        else:  # Solve OLS
            self.model = sm.OLS(self.response_cut, self.fit_matrix)

        self.results = self.model.fit()

        self.auto_correlation_matrix = self.results.cov_params()
        v_sdev = np.sqrt(np.diag(self.auto_correlation_matrix))
        self.auto_correlation_matrix /= np.outer(v_sdev, v_sdev)
        self.has_results = True

    def print_summary(self):
        if self.has_results:
            print(self.results.summary())
            list_param_labels = []
            for i in range(1, self.num_params):
                list_param_labels.append('x'+str(i)+': '+self.list_labels[i])
            print('\n'.join(list_param_labels)+'\n')
            df_acm = pd.DataFrame(self.auto_correlation_matrix, columns=self.list_labels, index=self.list_labels)
            print(df_acm)
        else:
            print('Fit first.')

    def display_fit(self, data_label: str, fit_label: str='Model', y_label: str='', x_label: str=''):
        if self.has_results:
            df_fit = pd.DataFrame({data_label: self.response_cut,
                                   fit_label: self.results.predict()},
                                  columns=[data_label, fit_label],
                                  index=self.time_axis)
            df_fit.plot(style=['o', '-'])
            if y_label:
                plt.ylabel(y_label)
            if x_label:
                plt.xlabel(x_label)

            df_dict = {'Model': self.results.predict()}
            for index, param in enumerate(self.results.params):
                df_dict[self.list_labels[index]] = self.fit_matrix[:, index] * param
            df_parts = pd.DataFrame(df_dict, index=self.time_axis)
            df_parts.plot()
            if y_label:
                plt.ylabel(y_label)
            if x_label:
                plt.xlabel(x_label)

            pd.DataFrame({'Residuals': self.results.resid}, index=self.time_axis).plot()

            return df_fit
        else:
            print('Fit first.')
            return None

    def get_normalized_results(self, start_time: np.datetime64=None, end_time: np.datetime64=None):
        if self.has_results:

            peak_times = np.array([start_time, end_time])
            peak_range = np.searchsorted(self.time_axis, peak_times)
            norm_scale = 1 / np.amax(self.results.predict()[peak_range[0]:peak_range[1]])

            return self.results.predict() * norm_scale
        else:
            print('Fit first.')
            return None






