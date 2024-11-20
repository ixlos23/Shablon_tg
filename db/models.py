from datetime import datetime

from sqlalchemy import BigInteger, VARCHAR, Column, DateTime, Float, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr, relationship


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):  # noqa
        return cls.__name__.lower() + 's'


class CreatedModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)


class User(CreatedModel):
    # class LangEnum(Enum):
    #     EN = "en"
    #     UZ = "uz"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    full_name: Mapped[str] = mapped_column(VARCHAR(255))
    # lang: Mapped[str] = mapped_column(alEnum(LangEnum, values_callable=lambda i: [field.value for field in i]),
    #                                   default=LangEnum.EN)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return self.full_name




class Product(CreatedModel):
    title = mapped_column(VARCHAR(255), nullable=False)
    photo = mapped_column(VARCHAR(255), nullable=True)
    price = mapped_column(Float, nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    description = mapped_column(VARCHAR(255), nullable=True)

    def __repr__(self):
        return self.title

