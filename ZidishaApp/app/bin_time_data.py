import numpy as np
import pandas as pd
__author__ = 'alexglenday'


def bin_centers_from_edges_time(bin_edges: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """
    Calculate bin center positions based on the edge positions of each bin.
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :return: Center positions of the bins as DatetimeIndex. Length is one less than edge positions.
    """
    if bin_edges.freq is None:
        bin_edge_values = bin_edges.values
        return pd.to_datetime(bin_edge_values[:-1] + (bin_edge_values[1:] - bin_edge_values[:-1]) / 2)
    else:
        return (bin_edges + (bin_edges[1]-bin_edges[0]) / 2)[:-1]


def bin_general_time(bin_function, bin_edges: pd.DatetimeIndex, data: pd.DataFrame,
                     col_to_bin: int=0, empty_bin_value: np.float64=np.nan) -> pd.DataFrame:
    """
    Applies a summary function (e.g. sum, mean, median, len) to segments of the data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_function: Summary function (e.g. sum, mean, median, length).
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a DataFrame.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :param empty_bin_value: Value to use in the case that there is no data in a bin. Default is NaN.
    :return: DataFrame where the first column is the binned data indexed by the centers of the bins.
    """
    bin_centers = bin_centers_from_edges_time(bin_edges)
    bin_length = len(bin_centers)
    data_ordered = data.sort_index()
    data_time_series = data_ordered.index
    data_array = data_ordered.iloc[:, col_to_bin].values
    data_bin_array = np.zeros(bin_length)

    data_bin_edges = np.searchsorted(data_time_series.values, bin_edges.values)
    data_bin_starts = data_bin_edges[:-1]
    data_bin_ends = data_bin_edges[1:]
    for index in range(bin_length):
        slice_start = data_bin_starts[index]
        slice_end = data_bin_ends[index]
        if slice_end > slice_start:
            data_bin_array[index] = bin_function(data_array[slice_start: slice_end])
        else:
            data_bin_array[index] = empty_bin_value

    binned_data = pd.DataFrame({'data_binned': data_bin_array}, index=bin_centers)

    return binned_data


def bin_sum_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame, col_to_bin: int=0) -> pd.DataFrame:
    """
    Sums data into the bins given by bin_edges and returns a DataFrame with the index centered on the bins.
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a DataFrame.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :return: Binned data in a DataFrame.
    """
    return bin_general_time(np.sum, bin_edges, data, col_to_bin=col_to_bin, empty_bin_value=0.0)


def bin_count_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame, col_to_bin: int=0) -> pd.DataFrame:
    """
    Counts the number of elements in data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a DataFrame.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :return: Binned data in a DataFrame.
    """
    return bin_general_time(len, bin_edges, data, col_to_bin=col_to_bin, empty_bin_value=0.0)


def bin_mean_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame, col_to_bin: int=0) -> pd.DataFrame:
    """
    Calculates the mean of the data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a DataFrame.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :return: Binned data in a DataFrame.
    """
    return bin_general_time(np.mean, bin_edges, data, col_to_bin=col_to_bin, empty_bin_value=np.nan)


def bin_median_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame, col_to_bin: int=0) -> pd.DataFrame:
    """
    Calculates the median of the data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a DataFrame.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :return: Binned data in a DataFrame.
    """
    return bin_general_time(np.median, bin_edges, data, col_to_bin=col_to_bin, empty_bin_value=np.nan)


def bin_max_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame, col_to_bin: int=0) -> pd.DataFrame:
    """
    Calculates the max of the data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a DataFrame.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :return: Binned data in a DataFrame.
    """
    return bin_general_time(np.amax, bin_edges, data, col_to_bin=col_to_bin, empty_bin_value=np.nan)


def bin_min_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame, col_to_bin: int=0) -> pd.DataFrame:
    """
    Calculates the min of the data in the bins given by bin_edges and returns a DataFrame with the index centered on the bins
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a DataFrame.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :return: Binned data in a DataFrame.
    """
    return bin_general_time(np.amin, bin_edges, data, col_to_bin=col_to_bin, empty_bin_value=np.nan)


dict_bin_type_func = {'sum': bin_sum_time,
                      'count': bin_count_time,
                      'mean': bin_mean_time,
                      'median': bin_median_time,
                      'max': bin_max_time,
                      'min': bin_min_time
                      }


def bin_time(bin_edges: pd.DatetimeIndex, data: pd.DataFrame,
             bin_type: str='count', col_to_bin: int=0, binned_col_label: str=None):
    """
    Calculates the indicated binning operation into the bins given by bin_edges for all DataFrames in the input list
    and returns a list of DataFrames with the indices centered on the bins.
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param data: Data to be binned as a list of DataFrames.
    :param bin_type: Type of binning. Default is a count. Valid inputs are: 'sum', 'count', 'median', 'mean', 'min', 'max'.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :param binned_col_label: String to use as label for the binned data column.
    :return: Binned data in a list of DataFrames.
    """
    try:
        bin_func = dict_bin_type_func[bin_type]
    except KeyError:
        type_str = ', '.join(dict_bin_type_func.keys())
        raise ValueError(bin_type+' is not a valid type of binning. Valid types: '+type_str)

    df_binned = bin_func(bin_edges, data, col_to_bin)
    if binned_col_label:
        binned_label = df_binned.columns[0]
        df_binned.rename(columns={binned_label: binned_col_label}, inplace=True)

    return df_binned


def bin_list_time(bin_edges: pd.DatetimeIndex, list_df_data: list,
                  bin_type: str='count', col_to_bin: int=0, binned_col_labels: list=None):
    """
    Calculates the indicated binning operation into the bins given by bin_edges for all DataFrames in the input list
    and returns a list of DataFrames with the indices centered on the bins.
    :param bin_edges: Edge positions of the bins as DatetimeIndex.
    :param list_df_data: Data to be binned as a list of DataFrames.
    :param bin_type: Type of binning. Default is a count. Valid inputs are: 'sum', 'count', 'median', 'mean'.
    :param col_to_bin: Column of the DataFrame to bin. Default is 0.
    :param binned_col_labels: List of strings to use as labels for the binned data column.
    :return: Binned data in a list of DataFrames.
    """
    # Match list lengths
    num_data = len(list_df_data)
    if binned_col_labels:
        num_labels = len(binned_col_labels)
        if num_data > num_labels:
            binned_col_labels += [None] * (num_data-num_labels)
        elif num_data < num_labels:
            binned_col_labels = binned_col_labels[: num_data]
    else:
        binned_col_labels = [None] * num_data

    list_df_binned = []
    for df, label in zip(list_df_data, binned_col_labels):
        list_df_binned.append(bin_time(bin_edges, df, bin_type=bin_type, col_to_bin=col_to_bin, binned_col_label=label))

    return list_df_binned


def bin_list_to_data_frame(list_df_binned: list) -> pd.DataFrame:
    """
    Takes a list of DataFrames from a bin_list_time operation and combines them into one DataFrame.
    :param list_df_binned: List of DataFrames from a bin_list_time operation.
    :return: DataFrame combined from the input list.
    """
    df_labels = []
    for df in list_df_binned:
        df_labels.append(df.columns[0])
    df_all = pd.DataFrame({label: df.iloc[:, 0] for df, label in zip(list_df_binned, df_labels)})
    return df_all


def bin_data_frame_to_list(df_binned: pd.DataFrame) -> list:
    """
    Takes a DataFrames combined by bin_list_to_data_frame and converts it back into a list.
    :param df_binned: DataFrames from a bin_list_to_data_frame operation.
    :return: List of DataFrames extracted from the input.
    """
    df_col_labels = df_binned.columns
    list_df = []
    for col_label in df_col_labels:
        list_df.append(df_binned[col_label].copy(deep=True))
    return list_df


