from sqlalchemy import Column, Integer, DateTime, String, Float
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from App.database import base, db
from fastapi import HTTPException, status


class Order(base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    order_status = Column(String(255), nullable=False)
    total_price = Column(Float, nullable=False)

    def _repr_(self):
        return f"<Order({self.name})>"

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
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        orders = await db.execute(query)
        (order,) = orders.first()
        return order

    @classmethod
    async def get_all_by_customer_id(cls, id):
        query = select(cls).where(cls.customer_id == id)
        orders = await db.execute(query)
        orders = orders.scalars().all()
        return orders

    @classmethod
    async def update(cls, id, **kwargs):
        order = await cls.get(id)
        order.from_dict(kwargs)

        order_dict = order._dict_
        order_dict.pop("_sa_instance_state", None)

        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
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
    async def delete(cls, id):
        query = sqlalchemy_delete (cls).where(cls.id == id)
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