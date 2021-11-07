import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mortgage import Mortgage
from mortgage_test import MortTest

pd.options.display.float_format = '{:,.0f}'.format
pd.set_option('max_colwidth', 0)
pd.set_option('display.width', 0)


def main():
    price_mn = 17
    initial_payment_mn = 2.5
    period = 30
    loan_rate_pct = 6.5
    first_month = 24
    frequency = 1
    early_pay_amount = 50000
    limit_month_perc = 50000

    m = Mortgage(price_mn, initial_payment_mn, loan_rate_pct, period,
                 early_payment=True, first_month=first_month, frequency_months=frequency,
                 early_payment_amount=early_pay_amount)
    m.get_payments_calendar()


    print('ежемесячный платеж  {:,.0f}'.format(m.avg_monthly_payment).replace(',', ' '))
    print('процентная часть  {:,.0f}'.format(m.average_percent_part).replace(',', ' '))
    print('остаток на жизнь {:,.0f}'.format(260000 - m.avg_monthly_payment - 50000).replace(',', ' '))
    print('переплата {:,.0f}'.format(m.overpayment).replace(',', ' '))
    print('стоимость 1 руб  {:,.2f}'.format(m.total_payment / (m.price - m.initial_payment)).replace(',', ' '))
    print('--------------')
    print('ежемесячный платеж (срок) {:,.0f}'.format(m.avg_reduce_period_monthly_payment).replace(',', ' '))
    print('процентная часть (срок) {:,.0f}'.format(m.average_reduce_period_percent_part).replace(',', ' '))
    print('остаток на жизнь {:,.0f}'.format(260000 - m.avg_reduce_period_monthly_payment - 50000).replace(',', ' '))
    print('переплата {:,.0f}'.format(m.reduce_period_overpayment).replace(',', ' '))
    print('стоимость 1 руб  {:,.2f}'.format(m.reduce_period_total_payment / (m.price - m.initial_payment)).replace(',',
                                                                                                                   ' '))
    print('--------------')
    print('ежемесячный платеж (платеж) {:,.0f}'.format(m.avg_early_monthly_payment).replace(',', ' '))
    print('процентная часть (платеж) {:,.0f}'.format(m.average_early_percent_part).replace(',', ' '))
    print('остаток на жизнь {:,.0f}'.format(260000 - m.avg_early_monthly_payment - 50000).replace(',', ' '))
    print('переплата {:,.0f}'.format(m.early_overpayment).replace(',', ' '))
    print('стоимость 1 руб  {:,.2f}'.format(m.early_total_payment / (m.price - m.initial_payment)).replace(',', ' '))
    print('--------------')


if __name__ == '__main__':
    main()
