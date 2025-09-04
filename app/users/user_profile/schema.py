from pydantic import BaseModel


class UserCreateBasicSchema(BaseModel):
    username: str
    password: str
    work_duration: int = 25
    short_break_duration: int = 5
    long_break_duration: int = 15


class UserSettingsSchema(BaseModel):
    username: str
    work_duration: int
    short_break_duration: int
    long_break_duration: int


class UserCreateSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    name: str | None = None
    google_access_token: str | None = None
    yandex_access_token: str | None = None
    work_duration: int = 25
    short_break_duration: int = 5
    long_break_duration: int = 15


class UserLoginProcessSchema(BaseModel):
    username: str
    password: str
