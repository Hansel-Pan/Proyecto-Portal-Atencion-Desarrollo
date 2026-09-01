from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase

BigIntPK = BigInteger().with_variant(Integer(), "sqlite")


class Base(DeclarativeBase):
    pass
