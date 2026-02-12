from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

import modelo
import esquemas
import crud
from BBDD import engine, get_db
import autor  # Importamos el módulo completo para evitar líos de nombres

# Crear las tablas automáticamente al arrancar el servidor
modelo.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Clientes Pro",
    description="Sistema CRUD completo con autenticación JWT y validación de duplicados",
    version="1.2.0"
)

# --- CONFIGURACIÓN DE CORS (Conexión con Vue) ---
# Permite la comunicación entre el frontend (5173) y el backend (8005)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RUTAS DE AUTENTICACIÓN ---

@app.post("/register", response_model=esquemas.Usuario, tags=["Autenticación"])
def register(user: esquemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo administrador en el sistema"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    
    db_email = crud.get_user_by_email(db, email=user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=esquemas.Token, tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Genera el token JWT para entrar al Panel"""
    user = autor.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=autor.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = autor.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- RUTAS DE CLIENTES (CRUD con Validación) ---

@app.post("/clientes/", response_model=esquemas.Cliente, tags=["Clientes"])
def crear_cliente(
    cliente: esquemas.ClienteCreate, 
    db: Session = Depends(get_db), 
    current_user: modelo.Usuario = Depends(autor.get_current_active_user)
):
    """Guarda un cliente nuevo y verifica que el teléfono no esté duplicado"""
    # Verificamos si el teléfono ya existe en la base de datos
    db_cliente = crud.get_cliente_by_telefono(db, telefono=cliente.telefono)
    if db_cliente:
        raise HTTPException(
            status_code=400, 
            detail=f"El teléfono {cliente.telefono} ya está registrado a nombre de {db_cliente.nombre}"
        )
    
    return crud.create_cliente(db=db, cliente=cliente)

@app.get("/clientes/", response_model=List[esquemas.Cliente], tags=["Clientes"])
def listar_clientes(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: modelo.Usuario = Depends(autor.get_current_active_user)
):
    """Obtiene la lista completa para la tabla de Vue"""
    return crud.get_clientes(db, skip=skip, limit=limit)

@app.get("/clientes/{cliente_id}", response_model=esquemas.Cliente, tags=["Clientes"])
def obtener_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db), 
    current_user: modelo.Usuario = Depends(autor.get_current_active_user)
):
    """Obtiene un cliente específico por ID"""
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@app.put("/clientes/{cliente_id}", response_model=esquemas.Cliente, tags=["Clientes"])
def actualizar_cliente(
    cliente_id: int, 
    cliente: esquemas.ClienteUpdate, 
    db: Session = Depends(get_db), 
    current_user: modelo.Usuario = Depends(autor.get_current_active_user)
):
    """Actualiza los datos desde el Modal de edición"""
    db_cliente = crud.update_cliente(db, cliente_id=cliente_id, cliente=cliente)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@app.delete("/clientes/{cliente_id}", tags=["Clientes"])
def eliminar_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db), 
    current_user: modelo.Usuario = Depends(autor.get_current_active_user)
):
    """Borra un cliente de la base de datos"""
    db_cliente = crud.delete_cliente(db, cliente_id=cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"status": "success", "message": f"Cliente {cliente_id} eliminado"}

@app.get("/", tags=["General"])
def root():
    return {"mensaje": "Backend Online", "docs": "/docs"}