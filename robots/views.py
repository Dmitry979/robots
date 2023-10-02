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


def get_unique_models(start_date, end_date):
    return (
        Robot.objects
        .filter(created__gte=start_date, created__lte=end_date)
        .values('model')
        .distinct()
    )


def get_versions_for_model(model, start_date, end_date):
    return (
        Robot.objects
        .filter(model=model, created__gte=start_date, created__lte=end_date)
        .values('version')
        .annotate(total_count=Count('id'))
    )


def create_excel_sheet(wb, model, versions):
    ws = wb.create_sheet(title=f"Модель {model}")
    headers = ["Модель", "Версия", "Количество"]
    ws.append(headers)

    for version_info in versions:
        version = version_info['version']
        total_count = version_info['total_count']
        ws.append([model, version, total_count])


def export_to_excel(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    unique_models = get_unique_models(start_date, end_date)

    if not unique_models:
        return HttpResponse("Новых роботов нет")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Robot.xlsx"'
    wb = Workbook()

    for model_info in unique_models:
        model = model_info['model']
        versions = get_versions_for_model(model, start_date, end_date)
        create_excel_sheet(wb, model, versions)

    del wb['Sheet']
    wb.save(response)
    return response

