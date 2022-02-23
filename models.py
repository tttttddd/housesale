# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Agent(db.Model):
    __tablename__ = 'agent'

    agent_name = db.Column(db.String(255), nullable=False)
    agent_id = db.Column(db.Numeric(20, 0), primary_key=True)
    agent_account = db.Column(db.Numeric(15, 0), nullable=False, unique=True)
    agent_password = db.Column(db.String(25), nullable=False)



class Deal(db.Model):
    __tablename__ = 'deal'

    deal_id = db.Column(db.Numeric(20, 0), primary_key=True)
    house_id = db.Column(db.ForeignKey('house.house_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    agent_id = db.Column(db.ForeignKey('agent.agent_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    deal_prices = db.Column(db.Numeric(15, 2), nullable=False)
    id = db.Column(db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    agent = db.relationship('Agent', primaryjoin='Deal.agent_id == Agent.agent_id', backref='deals')
    house = db.relationship('House', primaryjoin='Deal.house_id == House.house_id', backref='deals')
    user = db.relationship('User', primaryjoin='Deal.id == User.id', backref='reserves')


class House(db.Model):
    __tablename__ = 'house'

    house_name = db.Column(db.String(255), nullable=False, unique=True)
    house_id = db.Column(db.Numeric(20, 0), primary_key=True)
    deal_id = db.Column(db.ForeignKey('deal.deal_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    house_owner_id = db.Column(db.ForeignKey('house_owner.house_owner_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    add_date = db.Column(db.Date, nullable=False)
    sold_date = db.Column(db.Date)
    province = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    acreage = db.Column(db.Numeric(15, 2), nullable=False)
    prices = db.Column(db.Numeric(15, 2), nullable=False)
    price_per_square = db.Column(db.Numeric(15, 2), nullable=False)

    deal = db.relationship('Deal', primaryjoin='House.deal_id == Deal.deal_id', backref='houses')
    house_owner = db.relationship('HouseOwner', primaryjoin='House.house_owner_id == HouseOwner.house_owner_id', backref='houses')



class HouseOwner(db.Model):
    __tablename__ = 'house_owner'

    house_owner_name = db.Column(db.String(255), nullable=False)
    house_owner_id = db.Column(db.Numeric(20, 0), primary_key=True)
    house_owner_account = db.Column(db.Numeric(15, 0), nullable=False, unique=True)
    house_owner_password = db.Column(db.String(25), nullable=False)



class NormalUser(db.Model):
    __tablename__ = 'normal_user'

    user_id = db.Column(db.Numeric(20, 0), primary_key=True)
    id = db.Column(db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='NormalUser.id == User.id', backref='normal_users')



class Reserve(db.Model):
    __tablename__ = 'reserve'

    resever_id = db.Column(db.Numeric(20, 0), primary_key=True)
    house_id = db.Column(db.ForeignKey('house.house_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    agent_id = db.Column(db.ForeignKey('agent.agent_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    watch_time = db.Column(db.Date, nullable=False)
    id = db.Column(db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    agent = db.relationship('Agent', primaryjoin='Reserve.agent_id == Agent.agent_id', backref='reserves')
    house = db.relationship('House', primaryjoin='Reserve.house_id == House.house_id', backref='reserves')



class User(db.Model):
    __tablename__ = 'user'

    name = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Numeric(20, 0), primary_key=True)
    user_id = db.Column(db.Numeric(20, 0))
    vip_id = db.Column(db.Numeric(20, 0))
    account = db.Column(db.Numeric(15, 0), nullable=False, unique=True)
    regist_date = db.Column(db.Date, nullable=False)
    property_level = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    age = db.Column(db.Integer)
    user_password = db.Column(db.String(25), nullable=False)
    user_phone = db.Column(db.Numeric(11, 0))



class VipUser(db.Model):
    __tablename__ = 'vip_user'

    vip_level = db.Column(db.Integer)
    money_num = db.Column(db.Numeric(15, 2), nullable=False)
    vip_id = db.Column(db.Numeric(20, 0), primary_key=True)
    id = db.Column(db.ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='VipUser.id == User.id', backref='vip_users')
