from fastapi.security import OAuth2PasswordBearer

auth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
