import os
from conf.local import Config as BaseConfig


class Config(BaseConfig):
    """Clase de conf para tests. Hereda de la conf base (en local.py), y overridea
    los campos necesarios para correr los tests
    """
    MONGO_URI = os.environ.get('DB', "mongodb://localhost:27017/testing")
