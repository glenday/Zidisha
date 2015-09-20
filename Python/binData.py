import numpy as np
import pandas as pd
__author__ = 'alexglenday'


def bin_sum_time(bin_edges: pd.DatetimeIndex, bin_centers: pd.DatetimeIndex, data: pd.DataFrame) -> pd.DataFrame:
    """
    Sums data into the bins given by bin_edges and returns a DataFrame with bin_centers as the index
    :param bin_edges: DatetimeIndex
    :param bin_centers: DatetimeIndex
    :param data: DataFrame
    :return: DataFrame
    """
    data_ordered = data.sort_index()
    data_time_series = data_ordered.index
    data_array = data_ordered.iloc[:, 0].values
    data_sum_array = np.array(range(len(bin_centers)))
    data_index = 0
    data_length = len(data)
    for i in range(len(bin_centers)):
        bin_start = bin_edges[i]
        bin_end = bin_edges[i + 1]
        while data_index < data_length:
            data_time = data_time_series[data_index]
            if bin_start < data_time <= bin_end:
                data_sum_array[i] += data_array[data_index]
            elif data_time > bin_end:
                break
            data_index += 1
    binned_data = pd.DataFrame({'data_sum': data_sum_array}, index=bin_centers)
    return binned_data


def bin_count_time(bin_edges: pd.DatetimeIndex, bin_centers: pd.DatetimeIndex, data: pd.DataFrame) -> pd.DataFrame:
    data_time_series = data.index
    data_unit = pd.DataFrame({'data': 1}, index=data_time_series)
    data_count = bin_sum_time(bin_edges, bin_centers, data_unit)
    data_count.rename(columns={'data_sum': 'data_counts'}, inplace=True)
    return data_count


def bin_avg_time(bin_edges: pd.DatetimeIndex, bin_centers: pd.DatetimeIndex, data: pd.DataFrame) -> pd.DataFrame:
    data_ordered = data.sort_index()
    data_time_series = data_ordered.index
    data_array = data_ordered.iloc[:, 0].values
    data_avg_array = np.array(range(len(bin_centers)))
    data_index = 0
    bin_size = 0.0
    data_length = len(data)
    for i in range(len(bin_centers)):
        bin_start = bin_edges[i]
        bin_end = bin_edges[i+1]
        while data_index < data_length:
            data_time = data_time_series[data_index]
            if bin_start < data_time <= bin_end:
                data_avg_array[i] += data_array[data_index]
                bin_size += 1.0
            elif data_time > bin_end:
                if bin_size > 0:
                    data_avg_array[i] /= bin_size
                    bin_size = 0.0
                break
            data_index += 1
    binned_data = pd.DataFrame({'data_avg': data_avg_array}, index=bin_centers)

    return binned_data


'''
def bin_fill_time(bin_edges, bin_centers, data):
    data_ordered = data.sort_index()
    data_time_series = data_ordered.index
    data_array = data_ordered.iloc[:, 0]
    binned_data = pd.DataFrame({'data_filled': 0}, index=bin_centers)
    data_index = 0
    bin_size = 0
    data_length = len(data)
    for i in range(len(bin_centers)):
        bin_start = bin_edges[i]
        bin_end = bin_edges[i+1]
        while data_index < data_length:
            data_time = data_time_series[data_index]
            if bin_start < data_time <= bin_end:
                binned_data.data_sum[i] += data_array[data_index]
                bin_size += 1
            elif data_time > bin_end:
                if bin_size > 0 :
                    binned_data.data_sum[i] /= bin_size
                    bin_size = 0
                break
            data_index += 1

    return binned_data
'''

