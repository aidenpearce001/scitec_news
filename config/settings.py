import os
from typing import Union
from loguru import logger
from typing import Tuple

from pydantic import BaseSettings, Field
class Base(BaseSettings):
    
    config_file: str = "config.yaml"
    

class Dev(Base):
    
    enviroment: str = "Dev"

class Prod(Base):
    
    enviroment: str = "Prod"

config = dict(
    dev=Dev,
    prod=Prod
)

settings: Union[Dev, Prod] = config[os.environ.get('ENV', 'dev').lower()]()
