
import json
from database import SessionLocal

from models import admin as admin_model


def create_admins():

    json_path = "data.json"
    f = open(json_path)
    data = json.load(f)
    f.close()
    admins: list = data["admins"]
    db = SessionLocal()
    for admin in admins:

        admin = admin_model.Admin(**admin)
        if not db.query(admin_model.Admin).filter(admin_model.Admin.admin_id == admin.admin_id).first():

            db.add(admin)
            db.commit()
            db.refresh(admin)

    db.close()
