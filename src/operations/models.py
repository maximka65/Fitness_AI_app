from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

operation = Table(
    "info_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("Name", String, nullable=False),
    Column("Surname", String),
    Column("Birthday", String, nullable=False),
    Column("Gender", String),
    Column("Height", Integer, nullable=False),
    Column("Weight", Integer, nullable=False),
)


