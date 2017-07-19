from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ports = Table('ports', pre_meta,
    Column('Id', INTEGER, primary_key=True, nullable=False),
    Column('SwitchId', INTEGER),
    Column('Name', VARCHAR(length=64)),
    Column('Speed', VARCHAR(length=8)),
    Column('Duplex', VARCHAR(length=8)),
    Column('Status', VARCHAR(length=8)),
)

ports = Table('ports', post_meta,
    Column('Id', Integer, primary_key=True, nullable=False),
    Column('Switch_Id', Integer),
    Column('Name', String(length=64)),
    Column('Speed', String(length=8)),
    Column('Duplex', String(length=8)),
    Column('Status', String(length=8)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ports'].columns['SwitchId'].drop()
    post_meta.tables['ports'].columns['Switch_Id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ports'].columns['SwitchId'].create()
    post_meta.tables['ports'].columns['Switch_Id'].drop()
