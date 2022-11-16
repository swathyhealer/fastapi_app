import json
from typing import Union
from datetime import timedelta, datetime
from jose import jwt

from schemas import common as common_schema


class CommonFunction:

    @staticmethod
    def read_json(path: str) -> dict:
        f = open(path)
        data = json.load(f)
        f.close()
        return data

    @staticmethod
    def get_jwt_config() -> common_schema.JwtConfig:
        config_json_path="config.json"
        config: dict = CommonFunction.read_json(config_json_path
            )
        jwt_config = config["jwt_token"]
        return common_schema.JwtConfig(**jwt_config)

    @staticmethod
    def create_access_token(secret_key: str, algorithm: str, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt
        
    @staticmethod
    def decode_token(token: str):
        jwt_config = CommonFunction.get_jwt_config()
        payload = jwt.decode(token, jwt_config.secret_key,
                             algorithms=[jwt_config.algorithm])
        return payload
