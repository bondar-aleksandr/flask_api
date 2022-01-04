from utils import Database
from config import ROOT_DIR
import os

db = Database(os.path.join(ROOT_DIR, 'flask_api.db'))
db.add_user(login='user01', password='pass01')
db.add_user(login='user02', password='pass02')