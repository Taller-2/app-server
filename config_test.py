import os
from config import Config as BaseConfig


class Config(BaseConfig):
    """Clase de config para tests. Hereda de la config base (en config.py), y overridea
    los campos necesarios para correr los tests
    """
    MONGO_URI = os.environ.get('DB', "mongodb://localhost:27017/testing")
    SKIP_AUTH = os.environ.get('SKIP_AUTH', 'YES')
