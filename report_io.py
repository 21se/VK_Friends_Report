""" Набор функций и процедур для ввода/вывода данных отчета """

import os
from math import ceil

import pyinputplus as pyip
from pandas import DataFrame


def output(friends_df: DataFrame) -> None:
    """ Вывод pd.DataFrame в консоль с пагинацией """

    friends_count = len(friends_df)
    friends_per_page = 10
    total_pages = ceil(friends_count / friends_per_page)
    current_page = 1

    while current_page != 0:
        df_page = friends_df[
                  (current_page - 1) * friends_per_page:
                  (current_page - 1) * friends_per_page + friends_per_page]
        print(f'\n\tPage {current_page} of {total_pages}')
        print(f'{df_page.to_string()}\n')
        current_page = pyip.inputInt(f'Select the report page (1-{total_pages}) [0 to exit]: ',
                                     min=0, max=total_pages)


def get_settings() -> dict:
    """ Чтение консольного ввода пользователя в словарь, содержащий настройки отчета """

    print('\nPlease fill in the report settings: ')

    report_formats = [
        'csv',
        'tsv',
        'json'
    ]

    default_report_format = 'csv'

    access_token = pyip.inputStr('Enter the access token: ')
    user_id = pyip.inputInt('Enter the user id: ', greaterThan=0)

    report_format = pyip.inputMenu(
        report_formats,
        f'Select one of the following report formats (default: {default_report_format}):\n',
        blank=True,
        numbered=True) or default_report_format

    default_report_path = os.path.join(os.getcwd(), f'report.{report_format}')
    report_path = pyip.inputStr('Enter the output report path (optional): ',
                                blank=True) or default_report_path

    print()

    report_settings = {
        'path': report_path,
        'format': report_format,
        'access_token': access_token,
        'user_id': user_id
    }

    return report_settings
