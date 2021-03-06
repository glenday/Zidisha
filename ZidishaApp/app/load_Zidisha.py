import pandas as pd
__author__ = 'alexglenday'


def max_invites(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Maximum number of invitees allowed at once.
    :param time_bins_center: Center time value for each bin.
    :return: DataFrame containing maximum number of invitees indexed by time_bins_center.
    """
    # maximum number of invitees
    df_max_invite = pd.DataFrame({'max_invites': 0.0}, index=time_bins_center)
    df_max_invite[('2014-04-01' <= df_max_invite.index) & (df_max_invite.index < '2014-06-01')] = 4
    #df_max_invite[('2014-04-01' <= df_max_invite.index) & (df_max_invite.index < '2014-06-01')] = 25
    df_max_invite[('2014-06-01' <= df_max_invite.index) & (df_max_invite.index < '2014-10-01')] = 3
    df_max_invite[('2014-10-01' <= df_max_invite.index) & (df_max_invite.index < '2014-12-01')] = 4
    df_max_invite[('2014-12-01' <= df_max_invite.index) & (df_max_invite.index < '2015-02-01')] = 4
    #df_max_invite[('2014-12-01' <= df_max_invite.index) & (df_max_invite.index < '2015-02-01')] = 8
    df_max_invite[('2015-02-01' <= df_max_invite.index) & (df_max_invite.index < '2015-04-07')] = 4
    df_max_invite[('2015-04-07' <= df_max_invite.index) & (df_max_invite.index < '2015-08-01')] = 10
    df_max_invite[('2015-08-01' <= df_max_invite.index) & (df_max_invite.index < '2015-09-01')] = 4

    return df_max_invite


def max_new_loan_size(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Maximum new loan size in USD.
    :param time_bins_center: Center time value for each bin.
    :return: DataFrame containing maximum loan size in USD indexed by time_bins_center.
    """
    # maximum new loan
    df_max_new_loan = pd.DataFrame({'max_loan': 0.0}, index=time_bins_center)
    df_max_new_loan[('2012-02-1' <= df_max_new_loan.index) & (df_max_new_loan.index < '2012-08-01')] = 1000
    df_max_new_loan[('2012-08-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2013-04-01')] = 500
    df_max_new_loan[('2013-04-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2013-12-01')] = 100
    df_max_new_loan[('2013-12-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2014-01-01')] = 100
    #df_max_new_loan[('2013-12-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2014-01-01')] = 250
    df_max_new_loan[('2014-01-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2014-02-01')] = 150
    #df_max_new_loan[('2014-01-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2014-02-01')] = 450
    df_max_new_loan[('2014-02-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2014-11-01')] = 150
    df_max_new_loan[('2014-11-01' <= df_max_new_loan.index) & (df_max_new_loan.index < '2015-08-06')] = 100
    df_max_new_loan[('2015-08-06' <= df_max_new_loan.index) & (df_max_new_loan.index < '2015-08-11')] = 125
    df_max_new_loan[('2015-08-11' <= df_max_new_loan.index) & (df_max_new_loan.index < '2015-10-01')] = 150

    return df_max_new_loan


def loan_loss_reserve_fee_Kenya(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Loan loss reserve fee in USD for Kenya.
    :param time_bins_center: Center time value for each bin.
    :return: DataFrame containing the loan loss reserve fee in USD indexed by time_bins_center.
    """
    # fee level for Kenya
    df_fee_level = pd.DataFrame({'fee_level': 0.0}, index=time_bins_center)
    df_fee_level[('2015-02-21' <= df_fee_level.index) & (df_fee_level.index < '2015-04-22')] = 20
    df_fee_level[('2015-04-22' <= df_fee_level.index) & (df_fee_level.index < '2015-08-11')] = 30
    df_fee_level[('2015-08-11' <= df_fee_level.index) & (df_fee_level.index < '2015-08-18')] = 50
    df_fee_level[('2015-08-18' <= df_fee_level.index) & (df_fee_level.index < '2015-11-01')] = 70

    return df_fee_level


def loan_loss_reserve_fee_Other(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    # fee level for Kenya
    df_fee_level = pd.DataFrame({'fee_level': 0.0}, index=time_bins_center)
    df_fee_level[('2015-02-21' <= df_fee_level.index) & (df_fee_level.index < '2015-04-22')] = 10
    df_fee_level[('2015-04-22' <= df_fee_level.index) & (df_fee_level.index < '2015-08-11')] = 10
    df_fee_level[('2015-08-11' <= df_fee_level.index) & (df_fee_level.index < '2015-08-18')] = 10
    df_fee_level[('2015-08-18' <= df_fee_level.index) & (df_fee_level.index < '2015-11-01')] = 10

    return df_fee_level


def loan_loss_reserve_fee_indonesia(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Loan loss reserve fee (and membership fee) in USD for Indonesia.
    :param time_bins_center: Center time value for each bin.
    :return: DataFrame containing the loan loss reserve fee in USD indexed by time_bins_center.
    """
    # fee level for Indonesia
    df_fee_level = pd.DataFrame({'fee_level': 0.0}, index=time_bins_center)
    df_fee_level[('2015-02-10' <= df_fee_level.index) & (df_fee_level.index < '2015-03-06')] = 18
    df_fee_level[('2015-03-06' <= df_fee_level.index) & (df_fee_level.index < '2015-04-24')] = 7
    df_fee_level[('2015-04-24' <= df_fee_level.index) & (df_fee_level.index < '2015-11-01')] = 15

    return df_fee_level


def loan_loss_reserve_fee_ghana(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Loan loss reserve fee (and membership fee) in USD for Ghana.
    :param time_bins_center: Center time value for each bin.
    :return: DataFrame containing the loan loss reserve fee in USD indexed by time_bins_center.
    """
    # fee level for Ghana
    df_fee_level = pd.DataFrame({'fee_level': 0.0}, index=time_bins_center)
    df_fee_level[('2015-02-08' <= df_fee_level.index) & (df_fee_level.index < '2015-03-06')] = 27
    df_fee_level[('2015-03-06' <= df_fee_level.index) & (df_fee_level.index < '2015-04-24')] = 27
    df_fee_level[('2015-04-24' <= df_fee_level.index) & (df_fee_level.index < '2015-11-01')] = 27

    return df_fee_level


def website_change(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Dummy variable indicating the website change.
    :param time_bins_center: Center time value for each bin.
    :return: DataFrame containing the dummy variable indexed by time_bins_center.
    """

    df_web_change = pd.DataFrame({'web_change': 0.0}, index=time_bins_center)
    df_web_change[('2015-01-01' <= df_web_change.index) & (df_web_change.index < '2015-10-01')] = 1

    return df_web_change


def upfront_fee(time_bins_center: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Dummy variable indicating the use of an upfront fee.
    :param time_bins_center: Center time value for each bin.
    :return: DataFrame containing the dummy variable indexed by time_bins_center.
    """

    df_upfront_fee = pd.DataFrame({'upfront_fee': 0.0}, index=time_bins_center)
    df_upfront_fee[('2015-02-21' <= df_upfront_fee.index) & (df_upfront_fee.index < '2015-04-08')] = 1

    return df_upfront_fee

