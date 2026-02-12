from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión: usuario:contraseña@servidor:puerto/base_de_datos
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:206083Rr.@localhost:3306/empresa_clientes"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    echo=True  # Muestra las consultas SQL en la terminal
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()