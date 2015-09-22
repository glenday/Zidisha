import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
__author__ = 'alexglenday'


def group(list_df: list, df_col_index: int=0, seaborn_context: str='poster'):
    sns.set_context(seaborn_context)
    df_labels = []
    for df in list_df:
        df_labels.append(df.columns[df_col_index])
    df_all = pd.DataFrame({label: df.iloc[:, df_col_index] for df, label in zip(list_df, df_labels)})
    df_all.plot()


def individual(list_df: list, seaborn_context: str='poster'):
    sns.set_context(seaborn_context)
    for df in list_df:
        df.plot()

