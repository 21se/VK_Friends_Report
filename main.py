""" Просмотр/выгрузка списка друзей пользователя ВКонтакте в отчет выбранного формата """

import pyinputplus as pyip
import requests.exceptions

import report_data
import report_io
import vk_api


def vk_user_friends_report() -> None:
    """ Просмотр/выгрузка списка друзей пользователя ВКонтакте в отчет выбранного формата """

    while True:
        report_settings = report_io.get_settings()

        friends_list = None

        try:
            friends_list = vk_api.get_user_friends_list(
                access_token=report_settings['access_token'],
                user_id=report_settings['user_id'],
                fields=['nickname', 'country', 'city', 'bdate', 'sex'],
                verbose=True
            )
        except ValueError as value_error:
            print(f'The report cannot be received for the following reason: {value_error}')
        except requests.exceptions.ConnectionError:
            print('Failed to connect to VK API, check your connection and try again')
        except requests.exceptions.Timeout:
            print('Request timeout to VK API, try again')

        friends_list_received = isinstance(friends_list, list)
        friends_count = len(friends_list) if friends_list_received else 0

        if friends_count == 0 and friends_list_received:
            friends_list_received = False
            print('The user has no friends :(')

        if not friends_list_received:
            if pyip.inputBool(
                    '\nDo you want to make changes to the report settings? [(T)rue / (F)alse] '):
                # Вернуться к началу ввода данных
                continue
            # В случае отказа прекратить работу
            raise SystemExit(0)

        print(f'The user has {friends_count} friend{"s" if friends_count > 1 else ""}')

        friends_df = report_data.friends_list_to_df(friends_list)
        friends_df = friends_df.sort_values(by='first_name', axis=0, ignore_index=True)
        # Инкрементирует индексы friends_df для того чтобы в stdout-отчете
        # индексы друзей отображались начиная с единицы.
        friends_df.index = range(1, friends_count + 1)

        report_data.correct_friends_df_values(friends_df)

        responses = [
            'View the report',
            'Save the report to a file',
            'Make changes to the report settings',
            'Exit'
        ]

        while True:
            response = pyip.inputMenu(
                responses,
                prompt='\nPlease select one of the following:\n',
                numbered=True)
            if response == responses[0]:
                report_io.output(friends_df)
            elif response == responses[1]:
                try:
                    report_data.save_df_to_file(friends_df,
                                                report_settings['path'],
                                                report_settings['format'])
                    print(f'The report was saved at "{report_settings["path"]}"'
                          f' in "{report_settings["format"]}" format')
                except ValueError as value_error:
                    print(f'The report cannot be saved for the following reason: {value_error}')
                except PermissionError:
                    print('You don\'t have rights to save the file'
                          ' (maybe someone is already using the file)')
            elif response == responses[2]:
                # Вернуться к началу ввода данных
                break
            else:
                raise SystemExit(0)


if __name__ == '__main__':
    vk_user_friends_report()
