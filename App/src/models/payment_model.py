from sqlalchemy import Column, Integer, String
from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select
from ...database import base, db


class Payment(base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    id_order = Column(Integer, nullable=False)
    method = Column(String(255), nullable=False)
    payment_status = Column(String(255), nullable=False)

    def _repr_(self):
        return f"<Payment({self})>"

    @classmethod
    async def create(cls, **kwargs):
        payment = cls(**kwargs)
        db.add(payment)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return payment

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        payments = await db.execute(query)
        (payment,) = payments.first()
        return payment

    @classmethod
    async def get_all(cls):
        query = select(cls)
        payments = await db.execute(query)
        payments = payments.scalars().all()
        return payments

    @classmethod
    async def update(cls, id, **kwargs):
        payment = await cls.get(id)
        payment.from_dict(kwargs)

        payment_dict = payment._dict_
        payment_dict.pop("_sa_instance_state", None)

        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**payment_dict)
            .execution_options(synchronize_session=False)
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return payment_dict

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

    def from_dict(self, data):
        fields = [
            'id_order', 'method', 'payment_status',
        ]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(self,field,value)