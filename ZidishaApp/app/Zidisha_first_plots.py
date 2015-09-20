import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy as sql
import pymysql
import sklearn.linear_model as skllm
import statsmodels.api as sm
import bin_time_data as bd
#get_ipython().magic('matplotlib inline')


def zidisha_regress(first_date_str):

    # connect to db
    engine = sql.create_engine('mysql+pymysql://root:@localhost/zidisha')

    # new accepted borrower account creation dates
    df_new_borrowers = pd.read_sql_query('SELECT created_at FROM borrowers WHERE activation_status != 4 ORDER BY created_at', engine)
    df_new_borrowers = pd.DataFrame({'number': range(len(df_new_borrowers))}, index=df_new_borrowers.created_at.values)

    # all borrower account creation dates
    df_borrowers = pd.read_sql_query('SELECT created_at FROM borrowers', engine)
    df_borrowers = pd.DataFrame({'number': 1}, index=df_borrowers.created_at.values)

    # all loans
    df_loans = pd.read_sql_query('SELECT created_at FROM loans', engine)
    df_loans = pd.DataFrame({'number': 1}, index=df_loans.created_at.values)

    # all loans fully funded
    df_loans_funded = pd.read_sql_query('SELECT created_at FROM loans WHERE raised_percentage = 100', engine)
    df_loans_funded = pd.DataFrame({'number': 1}, index=df_loans_funded.created_at.values)

    # time to funding
    df_time_to_fund = pd.read_sql_query('SELECT applied_at, TIMESTAMPDIFF(MINUTE, applied_at, accepted_at) AS time_to FROM loans WHERE disbursed_at IS NOT NULL', engine)
    df_time_to_fund = pd.DataFrame({'time_to': df_time_to_fund.time_to.values/(24.*60.)}, index=df_time_to_fund.applied_at.values)

    # time to disbursement
    df_time_to_disperse = pd.read_sql_query('SELECT accepted_at, TIMESTAMPDIFF(MINUTE, accepted_at, disbursed_at) AS time_to FROM loans WHERE disbursed_at IS NOT NULL', engine)
    df_time_to_disperse = pd.DataFrame({'time_to': df_time_to_disperse.time_to.values/(24.*60.)}, index=df_time_to_disperse.accepted_at.values)

    #time_bins_edge = pd.date_range('2014-04-01','2015-09-01', None, 'W')
    time_bins_edge = pd.date_range(first_date_str, '2015-09-01', None, '3W')
#    time_bins_edge = pd.date_range('2012-02-01','2015-09-01', None, '3W')
    #time_bins_edge = pd.date_range('2013-04-01','2015-09-01', None, '3W')
    time_bins_center = (time_bins_edge + (time_bins_edge[1] - time_bins_edge[0])/2)[:-1]

    # maximum number of invitees
    df_max_invite = pd.DataFrame({'max_invites': 0}, index=time_bins_center)
    df_max_invite[('2014-04-01'<=df_max_invite.index) & (df_max_invite.index<'2014-06-01')] = 4
    #df_max_invite[('2014-04-01'<=df_max_invite.index) & (df_max_invite.index<'2014-06-01')] = 25
    df_max_invite[('2014-06-01'<=df_max_invite.index) & (df_max_invite.index<'2014-10-01')] = 3
    df_max_invite[('2014-10-01'<=df_max_invite.index) & (df_max_invite.index<'2014-12-01')] = 4
    df_max_invite[('2014-12-01'<=df_max_invite.index) & (df_max_invite.index<'2015-02-01')] = 4
    #df_max_invite[('2014-12-01'<=df_max_invite.index) & (df_max_invite.index<'2015-02-01')] = 8
    df_max_invite[('2015-02-01'<=df_max_invite.index) & (df_max_invite.index<'2015-03-01')] = 4
    df_max_invite[('2015-03-01'<=df_max_invite.index) & (df_max_invite.index<'2015-08-01')] = 10
    df_max_invite[('2015-08-01'<=df_max_invite.index) & (df_max_invite.index<'2015-09-01')] = 4

    # maximum new loan
    df_max_new_loan = pd.DataFrame({'max_loan': 1}, index=time_bins_center)
    df_max_new_loan[('2012-02-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2012-08-01')] = 1000
    df_max_new_loan[('2012-08-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2013-04-01')] = 500
    df_max_new_loan[('2013-04-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2013-12-01')] = 100
    df_max_new_loan[('2013-12-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2014-01-01')] = 100
    #df_max_new_loan[('2013-12-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2014-01-01')] = 250
    df_max_new_loan[('2014-01-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2014-02-01')] = 150
    #df_max_new_loan[('2014-01-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2014-02-01')] = 450
    df_max_new_loan[('2014-02-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2014-11-01')] = 150
    df_max_new_loan[('2014-11-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2015-08-01')] = 100
    df_max_new_loan[('2015-08-01'<=df_max_new_loan.index) & (df_max_new_loan.index<'2015-10-01')] = 150

    # fee level
    df_fee_level = pd.DataFrame({'fee_level': 1}, index=time_bins_center)

    df_avg_total_borrowers = bd.bin_avg_time(time_bins_edge, time_bins_center, df_new_borrowers)
    df_new_borrowers_counts = bd.bin_count_time(time_bins_edge, time_bins_center, df_new_borrowers)
    df_borrowers_counts = bd.bin_count_time(time_bins_edge, time_bins_center, df_borrowers)
    df_new_app_accept_rate = df_new_borrowers_counts / df_borrowers_counts
    df_avg_total_borrowers.rename(columns={'data_avg': 'avg_total_borrowers'}, inplace=True)
    df_new_borrowers_counts.rename(columns={'data_counts': 'new_borrowers_per_period'}, inplace=True)
    df_new_app_accept_rate.rename(columns={'data_counts': 'new_app_accept_frac'}, inplace=True)

    df_avg_time_to_fund = bd.bin_avg_time(time_bins_edge, time_bins_center, df_time_to_fund)
    df_avg_time_to_disperse = bd.bin_avg_time(time_bins_edge, time_bins_center, df_time_to_disperse)
    df_avg_time_to_fund.rename(columns={'data_avg': 'avg_time_to_fund'}, inplace=True)
    df_avg_time_to_disperse.rename(columns={'data_avg': 'avg_time_to_disperse'}, inplace=True)

    df_loans_count = bd.bin_count_time(time_bins_edge, time_bins_center, df_loans)
    df_loans_funded_count = bd.bin_count_time(time_bins_edge, time_bins_center, df_loans_funded)
    df_loans_fund_rate = df_loans_funded_count / df_loans_count
    df_loans_fund_rate.rename(columns={'data_counts': 'loan_fund_rate'}, inplace=True)

    # Fit matrix, n_samples x n_features
    disperse_feature = df_avg_time_to_disperse.avg_time_to_disperse.values
    fund_time_feature = df_avg_time_to_fund.avg_time_to_fund.values
    invite_feature = df_avg_total_borrowers.avg_total_borrowers * df_max_invite.max_invites.values
    fund_rate_feature = df_loans_fund_rate.loan_fund_rate.values
    app_accept_feature = df_new_app_accept_rate.new_app_accept_frac.values
    max_loan_feature = df_max_new_loan.max_loan.values

    label_array = df_new_borrowers_counts.new_borrowers_per_period.values
    #feature_mat = np.transpose(np.array([disperse_feature, fund_time_feature, invite_feature, fund_rate_feature, app_accept_feature, max_loan_feature]))

    const_array = np.empty(len(time_bins_center))
    const_array.fill(1)
    feature_mat2 = np.transpose(np.array([const_array, disperse_feature, fund_time_feature, invite_feature, fund_rate_feature, app_accept_feature, max_loan_feature]))
    model = sm.OLS(label_array, feature_mat2)
    results = model.fit()
    table_str = results.summary()
    labels = ['x1: Time to dispersal','x2: Time to fund','x3: Max invites * total borrowers','x4: Fraction funded','x5: Fraction applicants accepted','x6: Maximum loan limit']
    label_str = '\n'+'\n'.join(labels)+'\n'


# In[ ]:
"""
plt.scatter(time_bins_center, label_array)
plt.plot(time_bins_center, fit_array)


# In[ ]:

df_fit = pd.DataFrame({'Fit': fit_array, 'Data':df_new_borrowers_counts.new_borrowers_per_period},index=time_bins_center)

df_fit.plot()
plt.ylabel('Number of new borrowers')
plt.xlabel('Date')


# In[ ]:

df_fit = pd.DataFrame({'Fit': fit_array},index=time_bins_center)
plt.plot(time_bins_center, label_array)
plt.plot(time_bins_center, fit_array)
plt.legend()


# In[ ]:

sns.set_context('poster')
#plt.figure(figsize=(8, 6))
df_avg_time_to_fund.plot()
#plt.ylim([0, 11])
plt.ylabel('Days')
plt.xlabel('Date')


# In[ ]:

df_avg_time_to_disperse.plot()
plt.ylabel('Days')
plt.xlabel('Date')


# In[ ]:

df_max_new_loan.plot()
plt.ylabel('Dollars')
plt.xlabel('Date')


# In[ ]:

df_new_app_accept_rate.plot()
plt.ylabel('Fraction accepted')
plt.xlabel('Date')


# In[ ]:

df_loans_fund_rate.plot()
plt.ylabel('Fraction funded')
plt.xlabel('Date')


# In[ ]:

df_new_borrowers_counts.plot()
plt.ylabel('New borrowers per period')
plt.xlabel('Date')


# In[ ]:

df_avg_total_borrowers.plot()
plt.ylabel('Average total borrowers')
plt.xlabel('Date')


# In[ ]:

df_new_borrowers.plot()
plt.ylabel('Total borrowers')
plt.xlabel('Date')


# In[ ]:

df_borrowers.dtypes


# In[ ]:

df_loans.dtypes


# In[ ]:

df_exchange.dtypes


# In[ ]:

df_countries.dtypes


# In[ ]:

df_countries[df_countries.name=='Kenya']


# In[ ]:

#merge tables (this is not particularly efficient, as we do not need all the columns)
df_loans_borrowers = pd.merge(df_borrowers, df_loans, left_on='id', right_on='borrower_id')
df_loans_borrowers_countries = pd.merge(df_loans_borrowers, df_countries, left_on='country_id',right_on='id')


# In[ ]:

df_borrowers_time = df_borrowers.set_index('created_at')
df_borrowers_time = df_borrowers_time[df_borrowers_time.activation_status != 4]
#s_new_rates = df_borrowers_time.groupby([lambda x: pd.datetime(x.year, x.month, 0, 0)])['id'].count()
s_new_rates = df_borrowers_time.groupby([lambda x: x.year, lambda x: x.month, ])['id'].count()
#s_new_rates = pd.DataFrame({s_new_rates})


# In[ ]:

df_borrowers_simp = pd.DataFrame({'year' : df_borrowers.created_at.dt.year,
                                 'month' : df_borrowers.created_at.dt.month,
                                 'id' : df_borrowers.id})
s_new_rates = df_borrowers_simp.groupby(['year','month'])['id'].count()
s_new_rates = pd.DataFrame({'date' : dateTime(s_new_rates})

"""