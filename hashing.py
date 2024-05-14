from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def verify_password(plain_password: str, hashed_password :str):
        return pwd_context.verify(plain_password, hashed_password) 
    

    def get_password_hash(password:str):
        return pwd_context.hash(password)
