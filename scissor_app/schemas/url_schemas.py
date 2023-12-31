from pydantic import BaseModel


class URLBase(BaseModel):
    target_url: str


class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class URLInfo(URL):
    url: str
    admin_url: str


class CustomURLBase(URLBase):
    custom_name: str


class URLInfoResponse():
    status: str
    detail: object
