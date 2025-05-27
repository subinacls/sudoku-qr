import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# our metadata
from app.database import Base
target_metadata = Base.metadata

# Use the Railway DATABASE_URL at runtime
def get_url():
    return os.getenv("DATABASE_URL")

config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", get_url())
