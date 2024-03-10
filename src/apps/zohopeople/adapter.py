from ast import Dict
from ftplib import error_proto
from typing import Any
from src.base import App
import time
from datetime import datetime
import os
import json
import requests
import coloredlogs
import logging
from utils.logger import Logger
from utils.decorators import handle_log
from utils.helpers import print_request_object_helper, status_code_parse_helper
requests.packages.urllib3.add_stderr_logger()

urliblog = logging.getLogger('requests.packages.urllib3')
coloredlogs.install(level='DEBUG', logger=urliblog)

urliblog.setLevel(logging.INFO)

console_logger = Logger(__file__, "stream", "warning")
file_logger = Logger(__file__, handler_type="file",
                     log_level="debug", filename=f"{datetime.now()}-ZohoPeople_app.log")


class ZohoPeople(App):
    def __init__(
            self,
            client_id,
            client_secret,
            authorization_code,
            base_uri,
            redirect_uri,
            api_version) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_code = authorization_code
        self.base_uri = base_uri
        self.redirect_uri = redirect_uri
        self.api_version = api_version
        self.authorization_link = "/token"
        console_logger.set_class_name(self.__class__.__name__)
        file_logger.set_class_name(self.__class__.__name__)

        

    def build_uri(self, action_link, type_="auth") -> str:
        #  builds endpoint uri
        console_logger.set_func_name(self.build_uri.__name__)
        file_logger.set_func_name(self.build_uri.__name__)
        if type_ == "auth":
            console_logger.log(1, "Building URI")
            return self.base_uri + self.api_version + action_link
        if type_ is None:
            console_logger.log(1, "Building URI")
            return self.base_uri + action_link

    def save_credentials(
            self, json_response_data: Any | Dict)->None:
        #  saves generated tokens
        console_logger.set_func_name(self.save_credentials.__name__)
        file_logger.set_func_name(self.save_credentials.__name__)
        access_token = json_response_data['access_token']
        refresh_token = json_response_data['refresh_token']
        expires_in = time.time() + json_response_data['expires_in']
        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in" : expires_in
            }
        filepath = os.path.abspath("src/access/credentials.json")

        try:
            with open(filepath, 'w') as file:
                json.dump(data, file)
                console_logger.log(1, "Saved credentials.")
        except FileNotFoundError:
            console_logger.log(3, f"`{filepath}` does not exist.")

        except Exception as e:
            console_logger.log(3, f"Exception Occured while saving credential.")
            console_logger.log(3, f"Exception Detail: {e}")
    

    def __generate_access_token(self) -> None:
        #  get refresh token
        console_logger.set_func_name(self.__generate_access_token.__name__)
        file_logger.set_func_name(self.__generate_access_token.__name__)

        filename = os.path.abspath("src/access/credentials.json")
        parameters = {}
        with open(filename, 'r') as file:
            data = json.load(file)
            parameters["refresh_token"] = data["refresh_token"]
        parameters["client_id"] = self.client_id
        parameters["client_secret"] = self.client_secret
        parameters["grant_type"] = "refresh_token"
        action_link = "/token"
        uri = self.build_uri(action_link)

        try:
            response = requests.post(uri, params=parameters)
            if response.status_code != 200:
                console_logger.log(3, f"Error Occured while generating access token")
                print(f"Response Status: {response.status_code}")
                print(f"Response Text : {response.content}")
                return
            else:
                data = response.json()
                if data["error"]:
                    console_logger.log(3,  f"OAuth Error: {data['error']}")
                    return
                console_logger(1, f"Access token generated: {data}")
                self.save_credentials(data)
        except Exception as e:
            console_logger.log(3, f"Exception Occurred: {e}")

  
    def get_token(self) -> str:
        console_logger.set_func_name(__name__)
        file_logger.set_func_name(self.get_token.__name__)

        filepath = os.path.abspath("src/access/credentials.json")
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                if time.time() < data['expires_in']:
                    return data['access_token']
                else:
                    return self.__generate_access_token()
        except Exception as e:
            console_logger.log(3, f"Exception Occured: {e}")

    
    def authenticate(self) -> None:
        console_logger.set_func_name(self.authenticate.__name__)
        file_logger.set_func_name(self.authenticate.__name__)

        uri = self.build_uri(self.authorization_link)
        console_logger.log(0, f"Received URI - {uri}")
        parameters = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,    
            'code': self.authorization_code,
            'redirect_uri': self.redirect_uri
        }
        try:
            response = requests.post(uri, params=parameters)
            if response.status_code == 200:
                response_data_packet = response.json()
                console_logger.log(1, "Authorization Successful!")
                console_logger.log(0, f"Response Packet: {response_data_packet}")

                if 'error' in response_data_packet.keys():
                    console_logger.log(3, f"Error Occured: ", response_data_packet['error'])
                if 'refresh_token' not in response_data_packet.keys():
                    console_logger.log(3, f"Refresh token is missing. Might be some problem related to code authorization. Try using prompt=conset in the uri.")
                    return
                else:
                    self.save_credentials(response_data_packet)
            else:
                console_logger.log(3, f"Error in requests: {response.status_code}")
                console_logger.log(3, f"Detail: {response.content}")
        except Exception as e:
            console_logger.log(3, f"Exception Occurred: {e}")
    

    def handle_requests(self, action, parameters={}, headers={}, data=None, method='GET'):
        file_logger.set_func_name(self.handle_requests.__name__)
        console_logger.set_func_name(self.handle_requests.__name__)

        uri = self.build_uri(action_link=action, type_=None)
        access_token = self.get_token()
        headers['Authorization'] = f"Zoho-oauthtoken {access_token}"
        response: Any | Dict = {}

        if method.upper() == "GET":
            # handle get requests
            console_logger.log(1, f"GET operation initiated.")
            try:
                response = requests.get(uri, headers=headers, params=parameters)
                if response.request.body:
                    console_logger.log(1, f"ResponseURL: {response.request.url}\nResponseHeaders: {response.request.headers}\nRequestBody: {response.request.body}")
                else:
                    console_logger.log(1, f"ResponseURL: {response.request.url}\nResponseHeaders: {response.request.headers}")

                if response.status_code != 200:
                    status_code_parse_helper(response, console_logger)
                    return response
                else:
                    return response.json()
            except Exception as e:
                console_logger.log(3, f"Exception Occurred: {e}")
                console_logger.log(3, f"ResponseDetails: {response}")
                return response

        if method.upper() == "POST":
            # handle post requests
            console_logger.log(2, f"POST operation initiated.")
            pass

        if method.upper() == "PUT":
            # hanle put requests
            console_logger.log(2, f"PUT operation initiated.")
            pass

        if method.upper() == "DELETE":
            # handle delete requests
            console_logger.log(2, f"DELETE operation initiated.")
            pass

        
if __name__ == "__main__":
    print(os.path.dirname())