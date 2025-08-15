import datetime
from dataclasses import dataclass
from models import UserProfile
from repository import UserRepository
from settings import Settings
from schemas import UserLoginSchema, UserCreateSchema
import datetime as dt
from datetime import timedelta
from exception import UserNotFoundException, UserIncorrectPasswordException, TokenExpiredException, \
    TokenINCorrectException
from jose import jwt, JWTError, ExpiredSignatureError
from client import GoogleClient, YandexClient


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    def get_yandex_auth(self, code: str):
        user_data = self.yandex_client.get_user_info(code=code)

        if user := self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(yandex_access_token=user_data.access_token, email=user_data.default_email,
                                            name=user_data.name)
        created_user = self.user_repository.create_user(user_data=create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user_create')
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def google_auth(self, code: str) -> UserLoginSchema:
        user_data = self.google_client.get_user_info(code)

        if user := self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print('user login')
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(google_access_token=user_data.access_token, email=user_data.email, name=user_data.name)

        created_user = self.user_repository.create_user(user_data=create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user_create')
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserIncorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (dt.datetime.now(datetime.UTC) + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'exp': expire_date_unix},
                           self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, key=self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except ExpiredSignatureError:
            raise TokenExpiredException
        except JWTError:
            raise TokenINCorrectException
        return payload['user_id']
