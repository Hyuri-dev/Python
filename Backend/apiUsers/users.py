from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import bcrypt

# Configuración básica para el token
SECRET_KEY = "mandarino"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Base de datos de usuarios de ejemplo ---
# NOTA: En la práctica, esto debería estar en una base de datos real.
# El password hasheado se guarda como bytes, NO como string.
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "Admin@example.com",
        "full_name": "Administrador",
        # CORRECCIÓN: Eliminamos .decode() del salt y guardamos el hash como bytes
        "hashed_password": bcrypt.hashpw("aquiles".encode('utf-8'), bcrypt.gensalt()),
        "role": "admin",
        "disabled": False,
    },
    
    "mandarino": {
        "username": "mandarino",
        "email": "Admin@example.com",
        "full_name": "usuario regular",
        # CORRECCIÓN: Eliminamos .decode() del salt y guardamos el hash como bytes
        "hashed_password": bcrypt.hashpw("mandarino2206".encode('utf-8'), bcrypt.gensalt()),
        "role": "user",
        "disabled": False,
    },
}

# --- Modelos Pydantic ---

class User(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    disabled: bool

class UserInDB (User):
    # La contraseña hasheada se almacena como bytes
    hashed_password: bytes 

class Token(BaseModel):
    access_token: str
    token_type: str # Token de tipo bearer

# --- Funciones bcrypt --- 
def hash_password(password: str) -> bytes:
    # bcrypt.gensalt() ya devuelve bytes, no necesitas decodificar.
    salt = bcrypt.gensalt()
    # bcrypt.hashpw() devuelve bytes.
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    # La función checkpw recibe la contraseña en texto plano codificada
    # y el hash que está en bytes. No necesitas decodificar el hash aquí.
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# --- Funciones de autenticación --- 
def get_user(db, username: str):
    user_dict = db.get(username)
    if user_dict:
        # Aquí el UserInDB debe manejar el campo de bytes
        # Nota: La validación de Pydantic lo acepta sin problemas
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_token_access(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

# --- Dependencias --- 

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    user_data = fake_users_db.get(username)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    
    # Se crea un objeto UserInDB para poder usarlo en las validaciones
    user = User(**user_data)
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    
    return user

def check_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos suficientes")
    return user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrecto")
    access_token = create_token_access(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/admin/")
async def admin_route(current_user: User = Depends(check_admin)):
    return {"msg": f"Hola {current_user.full_name}, bienvenido al Panel de Administradores"}