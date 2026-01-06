from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class ShortURL(Base):
    __tablename__ = "short_urls"

    slug: Mapped[str] = mapped_column(primary_key=True, index=True, unique=True)
    long_url: Mapped[str]