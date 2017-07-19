from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
authorizationrules = Table('authorizationrules', post_meta,
    Column('Id', Integer, primary_key=True, nullable=False),
    Column('Uuid', Integer),
    Column('Method', String(length=64)),
    Column('Role', Integer),
)

defaultrules = Table('defaultrules', post_meta,
    Column('Id', Integer, primary_key=True, nullable=False),
    Column('Name', String(length=64)),
    Column('Method', String(length=64)),
    Column('Role', Integer),
)

objects = Table('objects', post_meta,
    Column('Uuid', Integer, primary_key=True, nullable=False),
    Column('Name', String(length=64)),
    Column('Id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['authorizationrules'].create()
    post_meta.tables['defaultrules'].create()
    post_meta.tables['objects'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['authorizationrules'].drop()
    post_meta.tables['defaultrules'].drop()
    post_meta.tables['objects'].drop()
