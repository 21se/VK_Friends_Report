""" Набор функций для работы с VK API """

import requests

GET_FRIENDS_METHOD_URL = 'https://api.vk.com/method/friends.get'
API_VERSION = '5.131'


def get_user_friends_list(access_token: str, user_id: int, fields: list,
                          api_version: str = API_VERSION,
                          verbose: bool = False) -> list:
    """ Функция возвращает список друзей пользователя используя метод VK API friends.get
        Метод VK API: https://vk.com/dev/friends.get
    """

    user_friends_list = []

    offset_count = 5000
    result_count = offset_count
    request_num = 0

    # При вызове метода friends.get с аргументом fields возможно получить не более 5000 друзей,
    # поэтому в цикле используем friends.get с аргументом offset = offset_count * request_num.
    while result_count >= offset_count:
        if verbose:
            print('Trying to get the user\'s friends...')

        offset = offset_count * request_num
        get_friends_response = requests.get(GET_FRIENDS_METHOD_URL,
                                            {'access_token': access_token,
                                             'user_id': user_id,
                                             'fields': ','.join(fields),
                                             'offset': offset,
                                             'v': api_version})
        get_friends_response_json = get_friends_response.json()

        error_response = get_friends_response_json.get('error', {})
        if error_response:
            error_code = error_response.get('error_code', 'Unknown error')
            error_msg = error_response.get('error_msg', '-1')
            raise ValueError(f'{error_msg} [Error code: {error_code}]')

        get_friends_response = get_friends_response_json.get('response', {})
        friends_list = get_friends_response.get('items', [])

        result_count = len(friends_list)
        user_friends_list += friends_list
        request_num += 1

        if verbose:
            print(f'\tReceived {result_count} friend{"s" if result_count > 1 else ""}')

    return user_friends_list
