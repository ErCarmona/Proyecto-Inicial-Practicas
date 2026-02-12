from sqlalchemy.orm import Session
import modelo
import esquemas
from autor import get_password_hash

# --- OPERACIONES DE USUARIO (Autenticación) ---

def create_user(db: Session, user: esquemas.UsuarioCreate):
    """Registra un nuevo usuario encriptando su contraseña"""
    hashed_password = get_password_hash(user.password)
    db_user = modelo.Usuario(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    """Busca un usuario por su correo electrónico"""
    return db.query(modelo.Usuario).filter(modelo.Usuario.email == email).first()

def get_user_by_username(db: Session, username: str):
    """Busca un usuario por su nombre de usuario para el login"""
    return db.query(modelo.Usuario).filter(modelo.Usuario.username == username).first()


# --- OPERACIONES DE CLIENTE (Gestión) ---

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos los clientes con paginación"""
    return db.query(modelo.Cliente).offset(skip).limit(limit).all()

def get_cliente(db: Session, cliente_id: int):
    """Busca un cliente específico por su ID único"""
    return db.query(modelo.Cliente).filter(modelo.Cliente.id == cliente_id).first()

def get_cliente_by_telefono(db: Session, telefono: str):
    """Busca un cliente por su teléfono para evitar duplicados"""
    return db.query(modelo.Cliente).filter(modelo.Cliente.telefono == telefono).first()

def create_cliente(db: Session, cliente: esquemas.ClienteCreate):
    """Guarda un cliente con todos sus campos"""
    db_cliente = modelo.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, cliente_id: int, cliente: esquemas.ClienteUpdate):
    """Actualiza solo los campos que el usuario modifique en el frontend"""
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None
    
    update_data = cliente.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    """Elimina permanentemente un cliente por su ID"""
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None
    
    db.delete(db_cliente)
    db.commit()
    return db_cliente