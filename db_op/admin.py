from typing import Union

from sqlalchemy.orm import Session

from models import admin as admin_model
from schemas import common as common_schema


def get_admin(
    db: Session, tokendata: common_schema.TokenData
) -> Union[admin_model.Admin, None]:
    admin: Union[admin_model.Admin, None] = (
        db.query(admin_model.Admin)
        .filter(admin_model.Admin.email == tokendata.username)
        .first()
    )

    if admin:
        return admin
    else:
        return None
