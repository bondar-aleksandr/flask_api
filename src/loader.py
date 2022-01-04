from utils import Database
from config import ROOT_DIR
import os

db = Database(os.path.join(ROOT_DIR, 'flask_api.db'))
db.create_tables()