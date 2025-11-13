from sqlmodel import create_engine
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./dev.db')
engine = create_engine(DATABASE_URL, echo=False)
