import pytest
import json
import os
from apps.zohopeople import ZohoPeople



class TestZohoPeopleApp:
    def test_save_credential(self):
        access_token = "access"
        refresh_token = "refresh_token"
        client_id = "ID"
        client_secret = "Secret"
        code = "Code"
        base_uri = "base_uri"
        redirect_uri = "redirect_uri"
        app = ZohoPeople(
            client_id=client_id,
            client_secret=client_secret,
            authorization_code=code,
            base_uri=base_uri,
            redirect_uri=redirect_uri
        )
        app.save_tokens(access_token=access_token, refresh_token=refresh_token)

        filepath = os.path.abspath("access/credentials.json")
        with open(filepath, 'r') as file:
            data = json.load(file)
            assert data['access_token'] == access_token
            assert data['refresh_token'] == refresh_token