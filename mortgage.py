import pandas as pd
import matplotlib.pyplot as plt


class Mortgage:
    MONTHS_PER_YEAR = 12
    MULTIPLIER = 1000000
    PLOT_MONTH_TICKS = 6
    PLOT_PAYMENTS_TICKS = 5000

    def __init__(self, price_mln, initial_payment_mln, loan_rate, period_years=30,
                 early_payment=True, first_month=24, frequency_months=1, early_payment_amount=50000):
        self._early_payment_flag = False
        self.price = price_mln * self.MULTIPLIER
        self.initial_payment = initial_payment_mln * self.MULTIPLIER
        self.loan_rate = loan_rate
        self.period = period_years
        self.period_months = self.period * self.MONTHS_PER_YEAR
        self.reduce_period_month = self.period * self.MONTHS_PER_YEAR
        self.month_loan_rate = self.loan_rate / self.MONTHS_PER_YEAR / 100
        # ОБЩАЯ_СТАВКА = (1 + ЕЖЕМЕСЯЧНАЯ_СТАВКА) ^ СРОК_ИПОТЕКИ_МЕСЯЦЕВ
        self.common_rate = (1 + self.month_loan_rate) ** self.period_months
        self.early_common_rate = (1 + self.month_loan_rate) ** self.period_months
        self.reduce_period_common_rate = (1 + self.month_loan_rate) ** self.reduce_period_month
        self.total_loan_amount = self.price - self.initial_payment
        # ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ = СУММА_КРЕДИТА * ЕЖЕМЕСЯЧНАЯ_СТАВКА * ОБЩАЯ_СТАВКА / (ОБЩАЯ_СТАВКА - 1)
        self.monthly_payment = self.total_loan_amount * self.month_loan_rate * self.common_rate / (self.common_rate - 1)
        self.early_monthly_payment = \
            self.total_loan_amount * self.month_loan_rate * self.early_common_rate / (self.early_common_rate - 1)
        self.reduce_period_monthly_payment = self.total_loan_amount * self.month_loan_rate * \
            self.reduce_period_common_rate / (self.reduce_period_common_rate - 1)
        # ОСТАТОК ДОЛГА
        self.residual_loan = self.total_loan_amount
        self.early_residual_loan = self.total_loan_amount
        self._reduce_period_residual_loan = self.total_loan_amount
        # ПРОЦЕНТНАЯ_ЧАСТЬ = ОСТАТОК_ДОЛГА * ЕЖЕМЕСЯЧНАЯ_СТАВКА
        self.monthly_percent_part = self.residual_loan * self.month_loan_rate
        self.early_monthly_percent_part = self.early_residual_loan * self.month_loan_rate
        self.reduce_period_monthly_percent_part = self._reduce_period_residual_loan * self.month_loan_rate
        # ОСНОВНАЯ_ЧАСТЬ = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ - ПРОЦЕНТНАЯ_ЧАСТЬ
        self.monthly_main_part = self.monthly_payment - self.monthly_percent_part
        self.early_monthly_main_part = self.early_monthly_payment - self.early_monthly_percent_part
        self.reduce_period_monthly_main_part = self.reduce_period_monthly_payment - \
            self.reduce_period_monthly_percent_part
        # ПЕРЕПЛАТА = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ * СРОК_ИПОТЕКИ_МЕСЯЦЕВ - СУММА_КРЕДИТА
        self.overpayment = self.monthly_payment * self.period_months - self.total_loan_amount
        self.residual_loan = self.residual_loan - self.monthly_main_part
        self.early_residual_loan = self.early_residual_loan - self.early_monthly_main_part
        self._reduce_period_residual_loan = self._reduce_period_residual_loan - self.reduce_period_monthly_main_part
        self._data_dict = {'Percent_part': self.monthly_percent_part,
                           'Main_part': self.monthly_main_part,
                           'Monthly_payment': self.monthly_payment,
                           'Residual_loan_amount': self.residual_loan,
                           'Early_percent_part': self.early_monthly_percent_part,
                           'Early_main_part': self.early_monthly_main_part,
                           'Early_monthly_payment': self.early_monthly_payment,
                           'Early_residual_loan_amount': self.early_residual_loan,
                           'Reduce_period_Percent_part': self.reduce_period_monthly_percent_part,
                           'Reduce_period_Main_part': self.reduce_period_monthly_main_part,
                           'Reduce_period_Monthly_payment': self.reduce_period_monthly_payment,
                           'Reduce_period_Residual_loan_amount': self._reduce_period_residual_loan,
                           }
        self.payments_calendar = pd.DataFrame(data=self._data_dict, index=[1])
        self.average_percent_part = 0
        self.average_early_percent_part = 0
        self.average_reduce_period_percent_part = 0
        self.total_payment = 0
        self.early_total_payment = 0
        self.early_overpayment = 0
        self.reduce_period_total_payment = 0
        self.reduce_period_overpayment = 0
        self.avg_monthly_payment = 0
        self.avg_early_monthly_payment = 0
        self.avg_reduce_period_monthly_payment = 0
        self._early_payment_flag = early_payment
        self._early_payment_amount = early_payment_amount
        self._frequency_months = frequency_months
        self._first_month = first_month
        self._early_additional_payments = 0
        self._reduce_period_additional_payment = 0
        self.total_period = 0
        self.early_total_period = 0
        self.reduce_total_period = 0

    def get_payments_calendar(self):
        for _month in range(2, self.period_months + 1):
            self.monthly_percent_part = self.residual_loan * self.month_loan_rate
            self.early_monthly_percent_part = self.early_residual_loan * self.month_loan_rate
            self.reduce_period_monthly_percent_part = self._reduce_period_residual_loan * self.month_loan_rate

            self.monthly_main_part = self.monthly_payment - self.monthly_percent_part
            if self.early_residual_loan == 0:
                self.early_monthly_payment = 0
            self.early_monthly_main_part = self.early_monthly_payment - self.early_monthly_percent_part
            if self._reduce_period_residual_loan == 0:
                self.reduce_period_monthly_payment = 0
            self.reduce_period_monthly_main_part = self.reduce_period_monthly_payment -\
                self.reduce_period_monthly_percent_part

            self.residual_loan = self.residual_loan - self.monthly_main_part
            self.early_residual_loan = self.early_residual_loan - self.early_monthly_main_part
            self._reduce_period_residual_loan = self._reduce_period_residual_loan - self.reduce_period_monthly_main_part

            if self._early_payment_flag and _month >= self._first_month and _month % self._frequency_months == 0:
                if self.early_residual_loan - self._early_payment_amount > 0:
                    self._early_additional_payments += self._early_payment_amount
                    self.early_residual_loan = self.early_residual_loan - self._early_payment_amount
                    if self.period_months > _month:
                        self.early_common_rate = (1 + self.month_loan_rate) ** (self.period_months - _month)
                        self.early_monthly_payment = self.early_residual_loan * self.month_loan_rate * \
                            self.early_common_rate / (self.early_common_rate - 1)
                else:
                    self._early_additional_payments += self.early_residual_loan
                    self.early_residual_loan = self.early_residual_loan - self.early_residual_loan

                if self._reduce_period_residual_loan - self._early_payment_amount > 0:
                    self._reduce_period_additional_payment += self._early_payment_amount
                    self._reduce_period_residual_loan = self._reduce_period_residual_loan - self._early_payment_amount
                else:
                    self._reduce_period_additional_payment += self._reduce_period_residual_loan
                    self._reduce_period_residual_loan = self._reduce_period_residual_loan - \
                        self._reduce_period_residual_loan

            _data_dict = {'Percent_part': self.monthly_percent_part,
                          'Main_part': self.monthly_main_part,
                          'Monthly_payment': self.monthly_payment,
                          'Residual_loan_amount': self.residual_loan,
                          'Early_percent_part': self.early_monthly_percent_part,
                          'Early_main_part': self.early_monthly_main_part,
                          'Early_monthly_payment': self.early_monthly_payment,
                          'Early_residual_loan_amount': self.early_residual_loan,
                          'Reduce_period_Percent_part': self.reduce_period_monthly_percent_part,
                          'Reduce_period_Main_part': self.reduce_period_monthly_main_part,
                          'Reduce_period_Monthly_payment': self.reduce_period_monthly_payment,
                          'Reduce_period_Residual_loan_amount': self._reduce_period_residual_loan,
                          }

            _row = pd.Series(_data_dict, name=_month)
            self.payments_calendar = self.payments_calendar.append(_row)

        self.avg_monthly_payment = \
            self.payments_calendar.Monthly_payment[self.payments_calendar.Monthly_payment != 0].mean()
        self.avg_early_monthly_payment = \
            self.payments_calendar.Early_monthly_payment[self.payments_calendar.Early_monthly_payment != 0].mean()
        self.avg_reduce_period_monthly_payment = \
            self.payments_calendar.Reduce_period_Monthly_payment[self.payments_calendar.Reduce_period_Monthly_payment 
                                                                 != 0].mean()

        self.total_period = \
            self.payments_calendar.Monthly_payment[self.payments_calendar.Monthly_payment != 0].count()
        self.early_total_period = \
            self.payments_calendar.Early_monthly_payment[self.payments_calendar.Early_monthly_payment != 0].count()
        self.reduce_total_period = \
            self.payments_calendar.Reduce_period_Monthly_payment[self.payments_calendar.Reduce_period_Monthly_payment 
                                                                 != 0].count()

        self.average_percent_part = \
            self.payments_calendar.Percent_part[self.payments_calendar.Percent_part != 0].mean()
        self.average_early_percent_part = \
            self.payments_calendar.Early_percent_part[self.payments_calendar.Early_percent_part != 0].mean()
        self.average_reduce_period_percent_part = \
            self.payments_calendar.Reduce_period_Percent_part[self.payments_calendar.Reduce_period_Percent_part 
                                                              != 0].mean()

        self.total_payment = self.payments_calendar.Monthly_payment.sum()
        self.overpayment = self.payments_calendar.Monthly_payment.sum() - self.total_loan_amount
        self.early_total_payment = self.payments_calendar.Early_monthly_payment.sum() + self._early_additional_payments
        self.early_overpayment = self.early_total_payment - self.total_loan_amount
        self.reduce_period_total_payment = self.payments_calendar.Reduce_period_Monthly_payment.sum() +\
            self._reduce_period_additional_payment
        self.reduce_period_overpayment = self.reduce_period_total_payment - self.total_loan_amount
        return self.payments_calendar

    def draw_background(self):
        _xticks = [x for x in range(0, self.period_months + 1, self.PLOT_MONTH_TICKS)]
        _yticks = [y for y in range(0, int(round(self.payments_calendar.Monthly_payment[1], 0)) +
                                    self.PLOT_PAYMENTS_TICKS, self.PLOT_PAYMENTS_TICKS)]
        plt.figure(figsize=(15, 10))
        plt.xticks(ticks=_xticks)
        plt.yticks(ticks=_yticks)
        plt.xlabel(f'Month')
        plt.ylabel(f'Payment, RUB')
        plt.grid()

    def draw(self, show=True):
        self.draw_background()
        plt.plot(self.payments_calendar.Percent_part, label='Percent part', color='r')
        plt.plot(self.payments_calendar.Main_part, label='Main part', color='g')
        plt.hlines(self.average_percent_part, xmin=self.payments_calendar.index[0],
                   xmax=self.payments_calendar.index[-1],
                   label=f'Average percent payment {round(self.average_percent_part, 2)} RUB', color='y')
        plt.hlines(self.monthly_payment, xmin=self.payments_calendar.index[0],
                   xmax=self.payments_calendar.index[-1],
                   label=f'Monthly payment {int(self.avg_monthly_payment)} RUB', color='b')
        plt.title(f'Average monthly payment: {int(self.monthly_payment)} RUB; Period: {self.period} years; '
                  f'Price: {self.price} RUB; Initial payment: {int(self.initial_payment)} RUB;\n'
                  f'Total payment: {int(self.total_payment)} RUB; '
                  f'Total loan amount: {int(self.total_loan_amount)} RUB; '
                  f'Overpayment: {int(self.overpayment)} RUB')
        plt.legend()
        if show:
            plt.show()

    def draw_early_payment(self, show=True):
        self.draw_background()
        plt.plot(self.payments_calendar.Early_percent_part, label='Early Percent part', color='r')
        plt.plot(self.payments_calendar.Early_main_part, label='Early Main part', color='g')
        plt.hlines(self.average_early_percent_part, xmin=self.payments_calendar.index[0],
                   xmax=self.payments_calendar.index[-1],
                   label=f'Average percent payment {int(self.average_early_percent_part)} RUB', color='y')
        plt.plot(self.payments_calendar.Early_monthly_payment,
                 label=f'Monthly payment {int(self.avg_early_monthly_payment)} RUB', color='b')
        plt.title(f'Average monthly payment: {int(self.avg_early_monthly_payment)} RUB;'
                  f'Period: {self.period} years; Price: {self.price} RUB; '
                  f'Initial payment: {int(self.initial_payment)} RUB;\n'
                  f'Total payment: {int(self.early_total_payment)} RUB; '
                  f'Total loan amount: {int(self.total_loan_amount)} RUB; '
                  f'Overpayment: {int(self.early_overpayment)} RUB;\n'
                  f'Early payment: {self._early_payment_amount} RUB every'
                  f' {self._frequency_months} month starting from {self._first_month} month')
        plt.legend()
        if show:
            plt.show()

    def draw_reduce_period(self, show=True):
        self.draw_background()
        plt.plot(self.payments_calendar.Reduce_period_Percent_part, label='Reduce_period_Percent_part', color='r')
        plt.plot(self.payments_calendar.Reduce_period_Main_part, label='Reduce_period_Main_part', color='g')
        plt.hlines(self.average_reduce_period_percent_part, xmin=self.payments_calendar.index[0],
                   xmax=self.payments_calendar.index[-1],
                   label=f'Average percent payment {int(self.average_reduce_period_percent_part)} RUB', color='y')
        plt.plot(self.payments_calendar.Reduce_period_Monthly_payment,
                 label=f'Monthly payment {int(self.avg_reduce_period_monthly_payment)} RUB', color='b')
        plt.title(f'Average monthly payment: {int(self.avg_reduce_period_monthly_payment)} RUB;'
                  f'Period: {self.period} years; Price: {self.price} RUB; '
                  f'Initial payment: {int(self.initial_payment)} RUB;\n'
                  f'Total payment: {int(self.reduce_period_total_payment)} RUB; '
                  f'Total loan amount: {int(self.total_loan_amount)} RUB; '
                  f'Overpayment: {int(self.reduce_period_overpayment)} RUB;\n'
                  f'Early payment: {self._early_payment_amount} RUB every'
                  f' {self._frequency_months} month starting from {self._first_month} month')
        plt.legend()
        if show:
            plt.show()


if __name__ == '__main__':
    price_mn = 17
    initial_payment_mn = 2.5
    period = 30
    loan_rate_pct = 6.5
    first_month_pay = 24
    frequency_pay = 1
    early_pay_amount = 50000

    m = Mortgage(price_mn, initial_payment_mn, loan_rate_pct, period,
                 early_payment=True, first_month=first_month_pay, frequency_months=frequency_pay,
                 early_payment_amount=early_pay_amount)
    calendar = m.get_payments_calendar()

    # m.draw()
    # m.draw_early_payment()
    # m.draw_reduce_period()
    print('месячный платеж  {:,.0f}'.format(m.avg_monthly_payment).replace(',', ' '))
    print('процентная часть  {:,.0f}'.format(m.average_percent_part).replace(',', ' '))
    print('остаток на жизнь {:,.0f}'.format(260000 - m.avg_monthly_payment - 50000).replace(',', ' '))
    print('переплата {:,.0f}'.format(m.overpayment).replace(',', ' '))
    print('стоимость 1 руб  {:,.2f}'.format(m.total_payment / (m.price - m.initial_payment)).replace(',', ' '))
    print('--------------')
    print('месячный платеж (срок) {:,.0f}'.format(m.avg_reduce_period_monthly_payment).replace(',', ' '))
    print('процентная часть (срок) {:,.0f}'.format(m.average_reduce_period_percent_part).replace(',', ' '))
    print('остаток на жизнь {:,.0f}'.format(260000 - m.avg_reduce_period_monthly_payment - 50000).replace(',', ' '))
    print('переплата {:,.0f}'.format(m.reduce_period_overpayment).replace(',', ' '))
    print('стоимость 1 руб  {:,.2f}'.format(m.reduce_period_total_payment / (m.price - m.initial_payment)).replace(',',
                                                                                                                   ' '))
    print('--------------')
    print('месячный платеж (платеж) {:,.0f}'.format(m.avg_early_monthly_payment).replace(',', ' '))
    print('процентная часть (платеж) {:,.0f}'.format(m.average_early_percent_part).replace(',', ' '))
    print('остаток на жизнь {:,.0f}'.format(260000 - m.avg_early_monthly_payment - 50000).replace(',', ' '))
    print('переплата {:,.0f}'.format(m.early_overpayment).replace(',', ' '))
    print('стоимость 1 руб  {:,.2f}'.format(m.early_total_payment / (m.price - m.initial_payment)).replace(',', ' '))
    print('--------------')

    pd.options.display.float_format = '{:,.0f}'.format
    pd.set_option('max_colwidth', 0)
    pd.set_option('display.width', 0)


