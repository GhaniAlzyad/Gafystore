from App.src.models import Cart, Order, Product, OrderDetail
from App.src.schema import OrderRequestSchema, OrderResponseSchema, ProductOrderSchema, AuthSchema, OrderDetailReport
from datetime import datetime
from fastapi import HTTPException, status

class OrderLogic:
    @staticmethod
    async def add_order(param: OrderRequestSchema):
        carts = await Cart.find_by_customer_id(param.customer_id)
        if carts is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Please add some product first.")

        total_price = 0
        product_schema = []
        order = await Order.create(
                customer_id = param.customer_id,
                date = datetime.now(),
                order_status = 'pending',
                total_price = total_price
            )
        for cart in carts:
            product = await Product.get(cart.product_id)
            total_price += cart.quantity * product.price
            await OrderDetail.create(
                id_order = order.id,
                product_name = product.name,
                qty = cart.quantity,
                price = product.price
            )

            product.stock -= cart.quantity
            await product.commit()

            product_schema.append(
                ProductOrderSchema(
                    name=product.name,
                    qty=cart.quantity,
                    price=cart.quantity * product.price,
                )
            )

        order.total_price = total_price
        await order.commit()

        await Cart.complete(carts)

        return OrderResponseSchema(
            id=order.id,
            customer_id=order.customer_id,
            date=order.date,
            order_status=order.order_status,
            total_price=order.total_price,
            products=product_schema
        )

    @staticmethod
    async def order_details(id: int, auth: AuthSchema):
        # check if order is exist
        order = await Order.get(id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")

        # check if order has order details
        orderDetails = await OrderDetail.get_by_order_id(id)
        if orderDetails is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order details not found.")

        # check if order has delivery address
        delivery = await Delivery.get_by_order_id(id)

        product_name = [detail.product_name for detail in orderDetails]
        qty = [detail.qty for detail in orderDetails]
        price = [detail.price for detail in orderDetails]

        return OrderDetailReport(
            id_order=order.id,
            customer_name=auth.name,
            address=delivery.address,
            phone_number=delivery.phone_number,
            product_name=product_name,
            qty=qty,
            price=price,
            total_price=order.total_price,
        )