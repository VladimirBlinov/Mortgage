import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mortgage import Mortgage

pd.set_option('max_colwidth', 0)
pd.set_option('display.width', 0)
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_rows', None)


def main():
    price_mn = 18  # mln
    initial_payment_mn = 2.5  # mln
    period = 30  # Years
    loan_rate_pct = 7.6  # annual %
    first_month = 24  # Nbr of first month
    frequency = 1  # Every x month
    early_pay_amount = 50000  # RUB
    limit_month_perc = 80000  # RUB
    complex_pct_rate_y = 10  # annual %

    m = Mortgage(price_mn, initial_payment_mn, loan_rate_pct, period,
                 early_payment=True, first_month=first_month, frequency_months=frequency,
                 early_payment_amount=early_pay_amount)
    m.get_payments_calendar()

    df = m.payments_calendar[['Early_ext_percent_part', 'Early_ext_main_part', 'Early_ext_monthly_payment',
                              'Early_ext_residual_loan_amount']].copy()
    df['cum_monthly_payment'] = df.Early_ext_monthly_payment.cumsum()
    df['cum_pct_part'] = df.Early_ext_percent_part.cumsum()
    df['cum_main_part'] = df.Early_ext_main_part.cumsum()
    complex_pct_rate_m = complex_pct_rate_y / m.MONTHS_PER_YEAR
    mort_month_pay = df.loc[1, 'Early_ext_monthly_payment']
    # df['complex_pct'] = [initial_payment_mn * m.MULTIPLIER * (1 + (complex_pct_rate_m/100.0)) ** n for n in df.index]
    for idx in df.index:
        if idx == 1:
            df.loc[idx, 'complex_pct'] = initial_payment_mn * m.MULTIPLIER * (1 + complex_pct_rate_m / 100) + \
                                         (mort_month_pay + early_pay_amount - limit_month_perc)
            df.loc[idx, 'pct_income'] = initial_payment_mn * m.MULTIPLIER * (complex_pct_rate_m / 100)
        else:
            df.loc[idx, 'complex_pct'] = df.loc[idx - 1, 'complex_pct'] * (1 + complex_pct_rate_m / 100) + \
                                         (mort_month_pay + early_pay_amount - limit_month_perc)
            df.loc[idx, 'pct_income'] = df.loc[idx - 1, 'complex_pct'] * (complex_pct_rate_m / 100)
        df.loc[idx, 'month_add_in'] = mort_month_pay + early_pay_amount - limit_month_perc

    df = df[df['Early_ext_percent_part'] >= limit_month_perc]
    print(df)


if __name__ == '__main__':
    main()