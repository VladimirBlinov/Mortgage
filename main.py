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
    loan_rate_pct = 7.6
    first_month = 24
    frequency = 1
    early_pay_amount = 50000
    limit_month_perc = 50000

    mt = MortTest(price_mn=price_mn, initial_payment_mn=initial_payment_mn, loan_rate_pct=loan_rate_pct,
                  period=period, first_month=first_month, frequency=frequency,
                  early_payment_amount=early_pay_amount, limit_month_perc=limit_month_perc)

    price_real, test_result = mt.price_test()
    print(price_real)
    mt.draw_test(test_result)


if __name__ == '__main__':
    main()
