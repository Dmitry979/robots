from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot
import json
from openpyxl import Workbook
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime, timedelta


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Разбираем JSON-данные из запроса

            # Создаем объект робота, используя данные из JSON
            robot = Robot(
                model=data.get('model'),
                version=data.get('version'),
                created=data.get('created')
            )
            # Сохраняем робота в базе данных
            robot.save()

            return JsonResponse({'message': 'Robot created successfully', 'id': robot.id}, status=201)
        except json.JSONDecodeError:
            # Возвращаем JSON с сообщением об ошибке, если данные не могут быть разобраны как JSON
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)


def html_index(request):
    return render(request, 'robots/index.html')


def export_to_excel(request):
    # Определяем дату начала недели (7 дней назад от текущей даты)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Получаем уникальные модели роботов из базы данных, учитывая только записи за последнюю неделю
    unique_models = (
        Robot.objects
        .filter(created__gte=start_date, created__lte=end_date)
        .values('model')
        .distinct()
    )

    # Если нет уникальных моделей, значит, за последнюю неделю нет новых записей
    if not unique_models:
        return HttpResponse("Новых роботов нет")

    # Создаем HTTP-ответ с типом контента "application/ms-excel" для Excel-файла
    response = HttpResponse(content_type='application/ms-excel')

    # Устанавливаем имя файла, который будет использоваться при скачивании
    response['Content-Disposition'] = 'attachment; filename="Robot.xlsx"'

    # Создаем новую рабочую книгу Excel
    wb = Workbook()

    # Проходим по уникальным моделям
    for model_info in unique_models:
        model = model_info['model']

        # Создаем новый лист Excel для каждой модели
        ws = wb.create_sheet(title=f"Модель {model}")

        # Заголовок на листе
        headers = ["Модель", "Версия", "Количество"]
        ws.append(headers)

        # Получаем данные о версиях роботов для данной модели с учетом количества, учитывая только записи за последнюю неделю
        versions = (
            Robot.objects
            .filter(model=model, created__gte=start_date, created__lte=end_date)
            .values('version')
            .annotate(total_count=Count('id'))
        )

        # Цикл по версиям роботов данной модели
        for version_info in versions:
            version = version_info['version']
            total_count = version_info['total_count']

            # Добавляем данные о версии и общем количестве на лист
            ws.append([model, version, total_count])

    # Удаляем первый лист (по умолчанию) и сохраняем рабочую книгу в HTTP-ответ
    del wb['Sheet']
    wb.save(response)

    # Возвращаем HTTP-ответ, содержащий Excel-файл
    return response

