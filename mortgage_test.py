from mortgage import Mortgage
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


pd.set_option('max_colwidth', 0)
pd.set_option('display.width', 0)
pd.options.display.float_format = '{:,.2f}'.format


class MortTest:
    def __init__(self, price_mn=22, initial_payment_mn=2.5, period=30, loan_rate_pct=6.5, first_month=1, frequency=1,
                 early_payment_amount=50000, limit_month_perc=50000):
        self.price_mn = price_mn
        self.initial_payment_mn = initial_payment_mn
        self.period = period
        self.loan_rate_pct = loan_rate_pct
        self.first_month = first_month
        self.frequency = frequency
        self.early_payment_amount = early_payment_amount
        self.limit_month_perc = limit_month_perc
        self.price_test_result = pd.DataFrame(columns=['price', 'month_pay', 'avg_perc_part', 'overpayment', 'months',
                                                       'total_month_pay', 'early_month_pay', 'early_avg_perc_part',
                                                       'early_overpayment', 'early_months', 'early_total_month_pay',
                                                       'reduce_month_pay', 'reduce_avg_perc_part', 'reduce_overpayment',
                                                       'reduce_months', 'reduce_total_pay'])
        self.initial_payment_test_result = pd.DataFrame(columns=['init_payment', 'month_pay', 'avg_perc_part',
                                                                 'overpayment', 'months', 'total_month_pay',
                                                                 'early_month_pay', 'early_avg_perc_part',
                                                                 'early_overpayment', 'early_months',
                                                                 'early_total_month_pay', 'reduce_month_pay',
                                                                 'reduce_avg_perc_part', 'reduce_overpayment',
                                                                 'reduce_months', 'reduce_total_pay'])
        self.price_result = {}
        self.equity_income_rate = 0
        self.income_rate_df = pd.DataFrame()

    def price_test(self, start_price=10, end_price=23):
        for _price_mn in range(start_price, end_price, 1):
            m = Mortgage(price_mln=_price_mn, initial_payment_mln=self.initial_payment_mn, loan_rate=self.loan_rate_pct,
                         period_years=self.period,
                         early_payment=True, first_month=self.first_month,
                         frequency_months=self.frequency,
                         early_payment_amount=self.early_payment_amount)
            m.get_payments_calendar()
            _test_dict = {'price': _price_mn,
                          'month_pay': round(m.avg_monthly_payment, 2),
                          'avg_perc_part': round(m.average_percent_part, 0),
                          'overpayment': round(m.overpayment / m.MULTIPLIER, 2),
                          'months': m.total_period,
                          'total_month_pay': round(m.avg_monthly_payment + self.early_payment_amount, 2),
                          'early_month_pay': round(m.avg_early_monthly_payment, 2),
                          'early_avg_perc_part': round(m.average_early_percent_part, 0),
                          'early_overpayment': round(m.early_overpayment / m.MULTIPLIER, 2),
                          'early_months': m.early_total_period,
                          'early_total_month_pay': round(m.avg_early_monthly_payment + self.early_payment_amount, 2),
                          'reduce_month_pay': round(m.avg_reduce_period_monthly_payment, 2),
                          'reduce_avg_perc_part': round(m.average_reduce_period_percent_part, 0),
                          'reduce_overpayment': round(m.reduce_period_overpayment / m.MULTIPLIER, 2),
                          'reduce_months': m.reduce_total_period,
                          'reduce_total_pay': round(m.avg_reduce_period_monthly_payment + self.early_payment_amount, 2)}
            if m.average_reduce_period_percent_part <= self.limit_month_perc:
                self.price_result = {'price': _price_mn,
                                     'month_pay': m.avg_monthly_payment,
                                     'month_percent': m.average_percent_part,
                                     'overpayment': m.overpayment / m.MULTIPLIER,
                                     'reduce_percent': m.average_reduce_period_percent_part,
                                     'reduce_overpayment': m.reduce_period_overpayment / m.MULTIPLIER}

            _test_ser = pd.Series(_test_dict, name=_price_mn)
            self.price_test_result = self.price_test_result.append(_test_ser)
        return self.price_result, self.price_test_result

    def initial_payment_test(self, start_init_pay=2.5, end_init_pay=15, steps_nb=20):
        for _initial_payment_mn in np.linspace(start_init_pay, end_init_pay, steps_nb):
            m = Mortgage(self.price_mn, _initial_payment_mn, self.loan_rate_pct, self.period,
                         early_payment=True, first_month=self.first_month,
                         frequency_months=self.frequency,
                         early_payment_amount=self.early_payment_amount)
            m.get_payments_calendar()
            _test_dict = {'init_payment': _initial_payment_mn,
                          'month_pay': round(m.avg_monthly_payment, 2),
                          'avg_perc_part': round(m.average_percent_part, 0),
                          'overpayment': round(m.overpayment / m.MULTIPLIER, 2),
                          'months': m.total_period,
                          'total_month_pay': round(m.avg_monthly_payment + self.early_payment_amount, 2),
                          'early_month_pay': round(m.avg_early_monthly_payment, 2),
                          'early_avg_perc_part': round(m.average_early_percent_part, 0),
                          'early_overpayment': round(m.early_overpayment / m.MULTIPLIER, 2),
                          'early_months': m.early_total_period,
                          'early_total_month_pay': round(m.avg_early_monthly_payment + self.early_payment_amount, 2),
                          'reduce_month_pay': round(m.avg_reduce_period_monthly_payment, 2),
                          'reduce_avg_perc_part': round(m.average_reduce_period_percent_part, 0),
                          'reduce_overpayment': round(m.reduce_period_overpayment / m.MULTIPLIER, 2),
                          'reduce_months': m.reduce_total_period,
                          'reduce_total_pay': round(m.avg_reduce_period_monthly_payment + self.early_payment_amount, 2)}
            _test_ser = pd.Series(_test_dict, name=_initial_payment_mn)
            self.initial_payment_test_result = self.initial_payment_test_result.append(_test_ser)
        return self.initial_payment_test_result

    def draw_test(self, _df, save_img=False):
        plt.figure(figsize=(15, 10))
        sns.set_theme(style="darkgrid")
        sns.lineplot(data=_df[['month_pay', 'early_month_pay', 'reduce_month_pay',
                               'avg_perc_part', 'early_avg_perc_part', 'reduce_avg_perc_part',
                               'total_month_pay', 'early_total_month_pay', 'reduce_total_pay']])
        plt.axhline(y=self.limit_month_perc, c='red', linestyle='dashed', label="horizontal")
        plt.title(f'{_df.columns[0]}')
        if save_img:
            plt.savefig(f'D:\\pyprojects\\pyprojects\\mortgage_img\\{_df.columns[0]}.jpg')
        plt.show()

    def income_rate(self, start_income_rate=1, end_income_rate=5, step_income_rate=1):
        self.equity_income_rate = 0
        _price_test_res, _ = self.price_test()
        _income_rate = start_income_rate
        self.price_mn = _price_test_res['price']
        best_price_m = Mortgage(self.price_mn, self.initial_payment_mn, self.loan_rate_pct, self.period,
                                early_payment=True, first_month=self.first_month,
                                frequency_months=self.frequency,
                                early_payment_amount=self.early_payment_amount)
        _calendar = best_price_m.get_payments_calendar()
        for _income_rate in range(start_income_rate, end_income_rate, step_income_rate):
            self.income_rate_df = pd.DataFrame(
                columns=['eq_month', 'eq_cum', 'total_loan', 'reduce_total_loan', 'overpayment', 'reduce_overpayment'])
            _income_rate /= 100
            _month_rate = _income_rate / 12
            _last_eq_month = 0
            _last_eq_month_compl = 0
            _overpayment = 0
            _reduce_overpayment = 0
            _month = 1
            for _month in range(1, self.period * 12 + 1):
                _last_eq_month += self.early_payment_amount
                _last_eq_month_compl = _last_eq_month_compl * (
                            1 + _month_rate) + self.early_payment_amount
                _overpayment += _calendar['Percent_part'][_month]
                _reduce_overpayment += _calendar['Reduce_period_Percent_part'][_month]
                _data = {'eq_month': _last_eq_month,
                         'eq_cum': _last_eq_month_compl,
                         'total_loan': _calendar['Residual_loan_amount'][_month],
                         'reduce_total_loan': _calendar['Reduce_period_Residual_loan_amount'][_month],
                         'overpayment': _overpayment,
                         'reduce_overpayment': _reduce_overpayment
                         }
                _row = pd.Series(data=_data, name=_month)
                self.income_rate_df = self.income_rate_df.append(_row)
                if (_data['eq_cum'] >= _data['total_loan']) &\
                        (self.income_rate_df.overpayment.max() <= self.income_rate_df.reduce_overpayment.max()):
                    self.equity_income_rate = _income_rate
            if self.equity_income_rate > 0:
                return self.equity_income_rate, self.income_rate_df

        return self.equity_income_rate, self.income_rate_df


def main():
    price = 22
    initial_payment = 2.5
    period = 30
    loan_rate_pct = 6.5
    first_month = 24
    frequency = 1
    early_payment_amount = 50000
    limit_month_perc = 50000

    mt = MortTest(price_mn=price, initial_payment_mn=initial_payment, period=period, loan_rate_pct=loan_rate_pct,
                  early_payment_amount=early_payment_amount, first_month=first_month, frequency=frequency,
                  limit_month_perc=limit_month_perc)
    price_test_res, test_res = mt.price_test()
    mt.draw_test(test_res)
    print(price_test_res)
    print(test_res)

    init_pay_test = mt.initial_payment_test()
    print(init_pay_test)
    mt.draw_test(init_pay_test)

    equity_income_rate, df = mt.income_rate()
    print(df)

    fig, ax = plt.subplots(figsize=(15, 10))
    lp = sns.lineplot(ax=ax, data=df)
    ax.set_xlim(left=0, right=mt.period*12)
    ax.set_ylim(bottom=0, top=int(df.overpayment.max()))
    yticks = lp.get_yticks()
    ylabels = ['{:,.2f}'.format(y).replace(",", " ") for y in yticks]
    lp.set(yticks=yticks, yticklabels=ylabels)
    plt.show()


if __name__ == '__main__':
    main()
