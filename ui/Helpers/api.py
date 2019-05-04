import config
import requests


class ChannelsHelper:

    def __init__(self):
        self._chanels_list = []

    def set_channels(self):
        url = f"http://{config.API.host}:{config.API.port}/channel/list"
        print(url)
        resp = requests.get(url=url)
        self._chanels_list = resp.json()

    def create(self,name,chat_id,token):
        url = f"http://{config.API.host}:{config.API.port}/channel/create"
        return requests.post(url, json={"name": name,
                                        "chat_id": chat_id,
                                        "token": token}).json()

    def delete(self,chat_id):
        url = f"http://{config.API.host}:{config.API.port}/channel/del/{chat_id}"
        return requests.get(url=url).json()

    def list(self):
        return self._chanels_list

    def get(self, channel_id):
        for channel in self._chanels_list:
            if int(channel['channel_id']) == int(channel_id):
                return channel


class PublicationHelper:
    def __init__(self):
        self._publications = {}

    def set_publication(self,channel_id):
        url_publications_ids = f"http://{config.API.host}:{config.API.port}/publication/list/{channel_id}"
        url_publications_info = f"http://{config.API.host}:{config.API.port}/publication/get"
        ids = requests.get(url=url_publications_ids).json()
        self._publications = requests.post(url_publications_info, json={"publication_ids": ids}).json()
    def create(self,channel_id,publish_in,publish_data):
        #publish_data = {'album_cover':'text','track_file':'cdn_path','artist_name':'text','track_name':'test'}
        url = f"http://{config.API.host}:{config.API.port}//publication/add"
        return requests.post(url, json={"channel_id": channel_id,
                                 "publish_in":publish_in,
                                 "publish_data":publish_data
                                 }).json()
    def get(self):
        return self._publications
