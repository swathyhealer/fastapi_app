import models
import json
from database import SessionLocal


def create_admins():

    json_path = "data.json"
    f = open(json_path)
    data = json.load(f)
    f.close()
    admins: list = data["admins"]
    db = SessionLocal()
    for admin in admins:

        admin = models.Admin(**admin)
        if not db.query(models.Admin).filter(models.Admin.admin_id == admin.admin_id).first():

            db.add(admin)
            db.commit()
            db.refresh(admin)

    db.close()
