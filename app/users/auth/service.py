import datetime
from dataclasses import dataclass
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.settings import Settings
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.schema import UserLoginSchema
import datetime as dt
from datetime import timedelta
from app.exception import UserNotFoundException, UserIncorrectPasswordException, TokenExpiredException, \
    TokenINCorrectException
from jose import jwt, JWTError, ExpiredSignatureError
from app.users.auth.client import GoogleClient, YandexClient, MailClient


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient
    mail_client: MailClient

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def get_yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(yandex_access_token=user_data.access_token, email=user_data.default_email,
                                            name=user_data.name)
        created_user = await self.user_repository.create_user(user_data=create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user_create')
        # self.mail_client.send_welcome_email(to=user_data.email)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    async def google_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.google_client.get_user_info(code)
        print(user_data)
        print('тут еще не сломался')
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print('user login')
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(google_access_token=user_data.access_token, email=user_data.email, name=user_data.name)

        created_user = await self.user_repository.create_user(user_data=create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user_create')
        # self.mail_client.send_welcome_email(to=user_data.email)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
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
        expire_date_unix = (dt.datetime.now(tz=dt.UTC) + timedelta(days=7)).timestamp()
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
