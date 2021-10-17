""" Набор функций и процедур для работы с данными полученными из VK API """

import numpy as np
import pandas as pd


def friends_list_to_df(friends_list: list) -> pd.DataFrame:
    """ Функция формирует из списка словарей friends_list pd.DataFrame с колонками
        first_name, last_name, country, city, bdate, sex
    """

    friends_df = pd.DataFrame(
        friends_list,
        columns=['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
    )
    return friends_df


def correct_friends_df_values(data_frame: pd.DataFrame) -> None:
    """ Процедура корректирует значения строк pd.DataFrame для удобства чтения """

    data_frame['sex'] = np.vectorize(num_sex_to_str)(data_frame['sex'])
    data_frame['country'] = np.vectorize(get_location_from_dict)(data_frame['country'])
    data_frame['city'] = np.vectorize(get_location_from_dict)(data_frame['city'])
    data_frame['bdate'] = np.vectorize(date_to_iso)(data_frame['bdate'])


def num_sex_to_str(num_sex) -> str:
    """ Функция возвращает строчное представление пола исходя из поданного функции числа
        В случае получения функцией что-то кроме чисел 1 или 2 возвращает 'Unknown'
    """

    if num_sex == 1:
        return 'Female'
    if num_sex == 2:
        return 'Male'

    return 'Unknown'


def get_location_from_dict(location_dict) -> str:
    """ Функция принимает на вход словарь локации и возвращает наименование локации
        В случае если вместо словаря подан иной объект возвращает 'Unknown'
        Пример:
            location_dict: {'id': 71, 'title': 'Greece'} -> 'Greece'
            location_dict: float('nan') -> 'Unknown'
    """

    location_if_not_exist = 'Unknown'
    if isinstance(location_dict, dict):
        return location_dict.get('title', location_if_not_exist)
    return location_if_not_exist


def date_to_iso(date) -> str:
    """ Функция принимает строку 'DD.MM.YYYY' / 'DD.MM' и возвращает строку формата 'YYYY-MM-DD'
        В случае отсутствия года для формирования ISO представления даты берётся год 0001
        В случае если дата не объект типа str, возвращается строка '0001-01-01'
    """

    if not isinstance(date, str):
        return '0001-01-01'

    date_list = date.split('.')

    if len(date_list) < 2 or len(date_list) > 3:
        raise ValueError('Invalid date format, expected "DD.MM.YYYY" or "DD.MM"')

    # Добавляем '0' если в строке число меньше 10
    day = f'{"0" if len(date_list[0]) == 1 else ""}{date_list[0]}'
    month = f'{"0" if len(date_list[1]) == 1 else ""}{date_list[1]}'

    year = date_list[2] if len(date_list) == 3 else '0001'

    day_int = int(day)
    if day_int < 1 or day_int > 31:
        raise ValueError('The day should be in the range 1-31')

    month_int = int(month)
    if month_int < 1 or month_int > 12:
        raise ValueError('The month should be in the range 1-12')

    year_int = int(year)
    if year_int < 1:
        raise ValueError('The year should be greater than 0')

    result_iso = f'{year}-{month}-{day}'

    return result_iso


def save_df_to_file(data_frame: pd.DataFrame, file_path: str, file_format: str) -> None:
    """ Процедура сохраняет pd.DataFrame по указанному пути и формату """

    if file_format == 'json':
        data_frame.to_json(file_path, orient='table', indent=2, index=False)
    elif file_format == 'tsv':
        data_frame.to_csv(file_path, sep='\t', index=False)
    elif file_format == 'csv':
        data_frame.to_csv(file_path, sep=';', index=False)
    else:
        raise ValueError("Unknown report file format")
