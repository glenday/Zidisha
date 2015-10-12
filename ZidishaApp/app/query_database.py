import os
import pandas as pd
import sqlalchemy as sql
import pymysql
__author__ = 'alexglenday'


class QueryDatabase(object):

    def __init__(self, database: str, user: str='root', password: str='', address: str='localhost'):
        self.database = database
        self.user = user
        self.password = password
        self.address = address

        connect_str = 'mysql+pymysql://'+self.user+':'+self.password+'@'+self.address+'/'+self.database
        self.engine = sql.create_engine(connect_str)

    def string_query(self, query_str: str) -> pd.DataFrame:
        df = pd.read_sql_query(query_str, self.engine)
        return df

    def source_query(self, query_dir: str, query_file: str,
                     index_col_position: int=0, where_filter_col: str=None, where_filter_list: iter= None) -> list:
        """
        Query the database using a file containing the SQL query.

        :rtype : list
        :param query_dir: Base directory containing SQL files
        :param query_file: SQL file with a single query
        :param index_col_position: Numeric position of the column to use as the DataFrame index. Default is 0.
        Use None for row number indexing.
        :param where_filter_col: String specifying the column to use for the filter. Default is None.
        :param where_filter_list: List of objects that will be matched by the where filter.
        :return: List of DataFrames where the first element is the result of the full query and subsequent elements are
        the output of the where filter.
        """
        query_path = os.path.join(query_dir, query_file)
        with open(query_path, 'r') as f:
            sql_str = f.read()

        df = pd.read_sql_query(sql_str, self.engine)
        if index_col_position is not None:
            index_col = df.columns.tolist()[index_col_position]
            df.set_index(index_col, inplace=True)

        df_list = [df]
        if where_filter_col is not None and where_filter_list is not None:
            for where_filter in where_filter_list:
                df_list.append(df[df[where_filter_col] == where_filter])

        return df_list

