import os
from src.config import *
from src.apps.zohopeople.adapter import ZohoPeople

app = ZohoPeople(
    client_id=ZP_CLIENT_ID,
    client_secret=ZP_CLIENT_SECRET,
    authorization_code=ZP_CODE,
    redirect_uri=ZP_REDIRECT_URI,
    base_uri=ZP_BASE_URI,
    api_version=ZP_OAUTH_VERSION
    )


# response = app.handle_requests("people/api/forms/employee/getRecords")
# print(response)

resp = app.handle_requests("/people/api/forms/employee/getRecords")
print(resp)