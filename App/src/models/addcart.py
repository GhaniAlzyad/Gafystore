from sqlalchemy import  Column, Integer, String
from sqlalchemy import false, true 
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy.orm import relationship
from sqlalchemy import select
from ...database import base, db
from datetime import datetime



class CartItem(base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    game_id = Column(Integer)
    account_id =Column(Integer)
    quantity = Column(Integer, default=1)
    token = Column(String(255), nullable=True)
    status = Column(String, nullable=False) #paid / unpaid