from .base import Module
from bs4 import BeautifulSoup
import requests

class Twitter(Module):
    DESCRIPTION = 'Creates Twitter DM button'
    ARGC = 1
    def response(self, query, message):
        msg = ''
        if ',' in query:
            qlist = query.split(',', 1)
            query = qlist[0].strip()
            msg = qlist[1].strip()
        url = f'http://gettwitterid.com/?user_name={query}&submit=GET+USER+ID'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        try:
            id = str(soup.find_all('p')[2])
            id = id[3:id.__len__()-4]
        except IndexError:
            return 'Twitter handle does not exist'

        if msg is not '':
            msg = msg.replace(' ', '%20')
            return f'https://twitter.com/messages/compose?recipient_id={id}&text={msg}'
        else:
            return 'https://twitter.com/messages/compose?recipient_id='+id
