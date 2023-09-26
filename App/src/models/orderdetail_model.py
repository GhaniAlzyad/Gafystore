from sqlalchemy import Column, Integer, DateTime, String, Float
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from App.database import base, db
from fastapi import HTTPException, status


class Orderdetail(base):
    __tablename__ = 'orderdetail'
    orderdetail_id = Column(Integer,primary_key=True)
    order_id = Column(Integer, nullable=False)
    user_id = Column(String, nullable=False, index=True)
    id_jumlah= Column(String, nullable=False, index=True)
    account_id = Column(Integer,nullable=False)
    Quantity = Column(Integer,default=1)
    UnitPrice = Column(Integer)
    total_price = Column(Float, nullable=False)

    def _repr_(self):
        return f"<orderdetail({self.name})>"

    @classmethod
    async def create(cls, **kwargs):
        order = cls(**kwargs)
        db.add(order)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return order

    @classmethod
    async def get(cls, orderdetail_id):
        query = select(cls).where(cls.orderdetail_id == orderdetail_id)
        orders = await db.execute(query)
        (order,) = orders.first()
        return order

    @classmethod
    async def get_all_by_user_id(cls, orderdetail_id):
        query = select(cls).where(cls.user_id == orderdetail_id)
        orders = await db.execute(query)
        orders = orders.scalars().all()
        return orders

    @classmethod
    async def update(cls, orderdetail_id, **kwargs):
        order = await cls.get(orderdetail_id)
        order.from_dict(kwargs)

        order_dict = order._dict_
        order_dict.pop("_sa_instance_state", None)

        query = (
            sqlalchemy_update(cls)
            .where(cls.orderdetail_id == orderdetail_id)
            .values(**order_dict)
            .execution_options(synchronize_session=False)
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return order_dict

    @classmethod
    async def delete(cls, orderdetail_id):
        query = sqlalchemy_delete (cls).where(cls.orderdetail_id == orderdetail_id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

    def from_dict(self, data):
        fields = [
            'user_id', 'date', 'order_status', 'total_price',
        ]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(self, field, value)

    @staticmethod
    async def commit():
        try:
            await db.commit()
        except:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")