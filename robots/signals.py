from django.db.models.signals import post_save
from django.dispatch import receiver
from robots.models import Robot
import logging
from orders.models import Order
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Robot)
def robot_create(sender, instance, created, **kwargs):
    if created:
        logger.info("Robot created successfully.")
        orders = Order.objects.filter(
            model=instance.model,
            version=instance.version
        )[:1]

        # Проверяем, есть ли заказы, соответствующие условиям
        if orders.exists():
            order = orders.first()

            # Получаем объект Customer из заказа
            customer = order.customer

            send_mail(
                'Subject',
                f'Добрый день!Недавно вы интересовались нашим роботом модели {order.model}, '
                f'версии {order.version}. Этот робот теперь в наличии.Если вам подходит этот вариант - пожалуйста,свяжитесь с нами',
                'from@example.com',
                [customer.email],
                fail_silently=False,
            )
        else:
            logger.info("No matching orders found.")
    else:
        logger.info("Robot was not created.")




