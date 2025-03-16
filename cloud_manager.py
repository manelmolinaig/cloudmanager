import requests
import json
import os
import datetime

class CloudManager:
    def __init__(self, domain, username, password):
        self.domain = domain
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.base_url = f'https://{self.domain}/'
        self.validationkey = self.login()
    
    def login(self):
        login_url = self.base_url + "sapi/login"
        params = {'action': 'login'}
        data = {'login': self.username, 'password': self.password}
        headers = {'referer': self.base_url}
        
        response = self.session.post(login_url, params=params, data=data, headers=headers)
        user_info = response.json()
        return user_info['data']['validationkey']
    
    def get_folders(self):
        get_folders_url = self.base_url + 'sapi/media/folder'
        params = {'action': 'get', 'validationkey': self.validationkey}
        response = self.session.post(get_folders_url, params=params)
        folders_info = json.loads(response.text)
        return folders_info
    
    def list_folder_files(self, folderid):
        list_folder_files_url = self.base_url + 'sapi/media'
        params = {
            'action': 'get',
            'folderid': folderid,
            'limit': 2000,
            'validationkey': self.validationkey
        }
        response = self.session.post(list_folder_files_url, params=params)
        folder_files = json.loads(response.text)
        files = folder_files['data']['media']
        return files
    
    def upload_file(self, file_path, folder_id):
        upload_url = self.base_url + 'sapi/upload'
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        mod_time = os.path.getmtime(file_path)
        mod_date = datetime.datetime.fromtimestamp(mod_time)
        formatted_date = mod_date.strftime("%Y%m%dT%H%M%SZ")
        
        metadata = {
            "data": {
                "name": file_name,
                "size": file_size,
                "modificationdate": formatted_date,
                "contenttype": "application/pdf",
                "folderid": folder_id
            }
        }
        
        params = {
            'action': 'save',
            'acceptasynchronous': 'true',
            'validationkey': self.validationkey,
        }
        
        with open(file_path, 'rb') as file:
            files = {
                'data': (None, json.dumps(metadata), 'application/json'),
                'file': (file_name, file, 'application/pdf')
            }
            response = self.session.post(upload_url, params=params, files=files)
        
        return response.json()
    
    def download_file(self, fileid, save_path=None):
        if save_path is None:
            save_path = os.getcwd()
        file_info_url = self.base_url + 'sapi/media'
        params = {'action': 'get', 'origin': 'omh,dropbox', 'validationkey': self.validationkey}
        json_data = {"data": {"ids": [fileid], "fields": ["url", "name"]}}
        response = self.session.post(file_info_url, params=params, json=json_data)
        file_info = response.json()
        download_url = file_info['data']['media'][0]['url']
        name = file_info['data']['media'][0]['name']
        file_path = os.path.join(save_path, name)
        
        response = self.session.get(download_url, stream=True)
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        return file_path
