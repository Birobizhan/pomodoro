from dataclasses import dataclass
import requests
from settings import Settings
from schemas import GoogleUserData


@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> GoogleUserData:
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                 headers={"Authorization": f"Bearer {access_token}"})
        print(user_info)
        return GoogleUserData(**user_info.json(), access_token=access_token)

    def _get_user_access_token(self, code: str):
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        print(response.json()['access_token'])
        return response.json()['access_token']
