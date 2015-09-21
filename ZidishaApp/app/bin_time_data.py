import numpy as np
import pandas as pd
__author__ = 'alexglenday'


def bin_centers_from_edges_time(bin_edges: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """
    Calculate bin center positions based on the edge positions of each bin
    :param bin_edges: DatetimeIndex
    :return: DatetimeIndex
    """
    if bin_edges.freq == None:
        bin_edge_values = bin_edges.values
        return pd.to_datetime(bin_edge_values[:-1] + (bin_edge_values[1:] - bin_edge_values[:-1]) / 2)
    else:
        return (bin_edges + (bin_edges[1]-bin_edges[0]) / 2)[:-1]


def bin_sum_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame) -> pd.DataFrame:
    """
    Sums data into the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex
    :param data: Data to be binned as a DataFrame
    :return: Binned data in a DataFrame
    """
    bin_centers = bin_centers_from_edges_time(bin_edges)
    data_ordered = data.sort_index()
    data_time_series = data_ordered.index
    data_array = data_ordered.iloc[:, 0].values
    data_sum_array = np.zeros(len(bin_centers))
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


def bin_count_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame) -> pd.DataFrame:
    """
    Counts the number of elements in data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex
    :param data: Data to be binned as a DataFrame
    :return: Binned data in a DataFrame
    """
    data_time_series = data.index
    data_unit = pd.DataFrame({'data': 1}, index=data_time_series)
    data_count = bin_sum_time(bin_edges, data_unit)
    data_count.rename(columns={'data_sum': 'data_counts'}, inplace=True)
    return data_count


def bin_mean_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the mean of the data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex
    :param data: Data to be binned as a DataFrame
    :return: Binned data in a DataFrame
    """
    bin_centers = bin_centers_from_edges_time(bin_edges)
    data_ordered = data.sort_index()
    data_time_series = data_ordered.index
    data_array = data_ordered.iloc[:, 0].values
    data_avg_array = np.zeros(len(bin_centers))
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
                else:
                    data_avg_array[i] = np.nan
                break
            data_index += 1
    binned_data = pd.DataFrame({'data_mean': data_avg_array}, index=bin_centers)

    return binned_data


def bin_median_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the median of the data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex
    :param data: Data to be binned as a DataFrame
    :return: Binned data in a DataFrame
    """
    bin_centers = bin_centers_from_edges_time(bin_edges)
    data_ordered = data.sort_index()
    data_time_series = data_ordered.index
    data_array = data_ordered.iloc[:, 0].values
    data_median_array = np.zeros(len(bin_centers))
    data_index = 0
    bin_size = 0
    data_bin_start = 0
    data_length = len(data)
    for i in range(len(bin_centers)):
        bin_start = bin_edges[i]
        bin_end = bin_edges[i+1]
        while data_index < data_length:
            data_time = data_time_series[data_index]
            if bin_start < data_time <= bin_end:
                bin_size += 1
            elif data_time > bin_end:
                if bin_size > 0:
                    data_bin_end = data_index + 1
                    data_median_array[i] = np.median(data_array[data_bin_start: data_bin_end])
                    data_bin_start = data_bin_end
                    bin_size = 0
                else:
                    data_median_array[i] = np.nan
                break
            data_index += 1
    binned_data = pd.DataFrame({'data_median': data_median_array}, index=bin_centers)

    return binned_data


dict_bin_type_func = {'sum': bin_sum_time, 'count': bin_count_time, 'mean': bin_mean_time, 'median': bin_median_time}

def bin_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame, bin_type: str='sum'):
    """
    Calculates the indicated binning operation into the bins given by bin_edges for all DataFrames in the input list
    and returns a list of DataFrames with the indices centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex
    :param data_list: Data to be binned as a list of DataFrames
    :param bin_type: Type of binning. Default is a sum. Valid inputs are: 'sum', 'count', 'median', 'mean'
    :return: Binned data in a list of DataFrames
    """
    try:
        bin_func = dict_bin_type_func[bin_type]
    except KeyError:
        type_str = ', '.join(dict_bin_type_func.keys())
        raise ValueError(bin_type+' is not a valid type of binning. Valid types: '+type_str)

    return bin_func(bin_edges, data)


def bin_list_time(bin_edges: pd.DatetimeIndex, data_list: list, bin_type: str='sum'):
    """
    Calculates the indicated binning operation into the bins given by bin_edges for all DataFrames in the input list
    and returns a list of DataFrames with the indices centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex
    :param data_list: Data to be binned as a list of DataFrames
    :param bin_type: Type of binning. Default is a sum. Valid inputs are: 'sum', 'count', 'median', 'mean'
    :return: Binned data in a list of DataFrames
    """

