import requests
import misc
from yobit import get_btc
from time import sleep

token = misc.token
URL = 'https://api.telegram.org/bot' + token + '/'

# sendMessage?chat_id=276871710&text=Hi
global last_update_id
last_update_id = 0


def getUpdates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    return r.json()


def getMessage():

    data = getUpdates()

    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id

        type_of_message = data['result'][-1]

        if 'message' in type_of_message:
            chat_id = last_object['message']['chat']['id']
            message_text = last_object['message']['text']

        if 'edited_message' in type_of_message:
            chat_id = last_object['edited_message']['chat']['id']
            message_text = last_object['edited_message']['text']

        message = {'chat_id': chat_id,
                   'text': message_text}
        return message
    return None



def sendMessage(chat_id, text='Wait a second, please...'):
    url = URL + 'sendMessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)



def main():

    while True:
        answer = getMessage()
        if answer != None:
            chat_id = answer['chat_id']
            text = answer['text']

            if text == '/btc':
                sendMessage(chat_id, get_btc())
        else:
            continue

        sleep(2)


if __name__ == '__main__':
    main()


































