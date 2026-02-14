from datetime import datetime
from uuid import uuid4, UUID
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import mapped_column


# ----------- Basic Columns -----------

int_id = Annotated[int, mapped_column(primary_key=True)]
_uuid = Annotated[UUID, mapped_column(default=uuid4, unique=True)]
created_at = Annotated[datetime, mapped_column(default=func.now())]
updated_at = Annotated[datetime, mapped_column(default=func.now(),
                                               onupdate=func.now())]
_bool_f = Annotated[bool, mapped_column(default=False)]
_bool_t = Annotated[bool, mapped_column(default=True)]
url = Annotated[str, mapped_column(default='', comment='Path to the file')]
