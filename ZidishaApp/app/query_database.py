__author__ = 'alexglenday'
import os
import numpy as np
import pandas as pd
import sqlalchemy as sql
import pymysql


class QueryDatabase(object):

    def __init__(self, database: str, user='root', password='', address='localhost'):
        self.database = database
        self.user = user
        self.password = password
        self.address = address

        connect_str = 'mysql+pymysql://'+self.user+':'+self.password+'@'+self.address+'/'+self.database
        self.engine = sql.create_engine(connect_str)

    def source_query(self, query_dir: str, query_file: str, index_col_position=0) -> pd.DataFrame:
        query_path = os.path.join(query_dir, query_file)
        with open(query_path, 'r') as f:
            sql_str = f.read()

        df = pd.read_sql_query(sql_str, self.engine)
        if index_col_position is not None:
            index_col = df.columns.tolist()[index_col_position]
            df.set_index(index_col, inplace=True)

        return df
