from .forms import OrderForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
import json
from django.http import HttpResponse
from django.shortcuts import render
from customers.models import Customer


def html_post_form(request):
    return render(request, 'orders/order_template.html')


def post_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Заказ оформлен")
        else:
            # Обработка невалидной формы
            return render(request, 'orders/order_template.html', {'form': form})
    else:
        # Обработка GET-запроса, если это не POST
        form = OrderForm()
        return render(request, 'orders/order_template.html', {'form': form})


@csrf_exempt
def create_order_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Разбираем JSON-данные из запроса

            # Получаем объект Customer по email
            customer_email = data.get('customer')
            customer = Customer.objects.get(email=customer_email)

            # Создаем объект Order, используя данные из JSON
            order = Order(
                customer=customer,
                model=data.get('model'),
                version=data.get('version'),
            )

            # Сохраняем Order в базе данных
            order.save()

            return JsonResponse({'message': 'order created', 'id': order.id}, status=201)
        except json.JSONDecodeError:
            # Возвращаем JSON с сообщением об ошибке, если данные не могут быть разобраны как JSON
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Customer.DoesNotExist:
            # Обработка ситуации, когда нет соответствующего Customer
            return JsonResponse({'message': 'Customer not found'}, status=404)

    return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)


