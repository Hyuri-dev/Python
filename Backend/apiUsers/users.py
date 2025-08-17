from fastapi import FastAPI, Depends , HTTPException, status
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import bcrypt

#Configuracion basica para el token
SECRET_KEY = "mandarino"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "admin": {
        "username": "Admin",
        "email": "Admin@example.com",
        "full_name": "Administrador",
        "hashed_password": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt().decode('utf-8')),
        "role": "admin",
        "disabled": False,
    },
    
    "user": {
        "username": "Mandarin",
        "email": "Admin@example.com",
        "full_name": "usuario regular",
        "hashed_password": bcrypt.hashpw("user123".encode('utf-8'), bcrypt.gensalt().decode('utf-8')),
        "role": "user",
        "disabled": False,
    },
}

#--- Modelos ---

class User(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    disabld: bool

class UserInDB (User):
    hashed_password : str

class Token (BaseModel):
    access_token: str
    token_type: str #token de tipo bearer

#--- funciones bcrypt --- 
def hash_password (password: str) -> str:
    salt = bcrypt.gensalt() # Salt se encarga de variar nuestra contraseña hasheada, lo cual lo hace mas segura y permite de paso poder hacer 
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str , hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# --- Funciones autenticacion --- 
def get_user(db, username: str):
        user_dict = db.get(username)
        if user_dict:
            return UserInDB(**user_dict)

def authenticate_user (username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_token_access(data: dict , expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithms=ALGORITHM)

def decode_token (token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code= 401, detail="Token invalido o expirado")

#--- Dependencias --- 

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User :
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code= 401, detail= "Credenciales Invalidas")
    user = get_user(fake_users_db, username)
    if user is None:
        raise HTTPException(status_code= 401 , detail="Usuario no encontrado")
    return user

def check_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="No tienes permisos suficiente")
    return user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username , form_data.password)
    if not user:
        raise HTTPException(status_code= 401 , detail= "Usuario o contraseña incorrecto")
    access_token = create_token_access(data = {"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/admin/")
async def admin_route(current_user: User = Depends(check_admin)):
    return {"msg": f"Hola {current_user} Bienvenido al Panel de Administradores"}