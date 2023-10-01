"""R4C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from robots.views import create_robot, export_to_excel, html_index
from orders.views import post_form, html_post_form, create_order_json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_robot/', create_robot, name='create_robot'),
    path('export/', export_to_excel, name='export_to_excel'),
    path('', html_index, name='html_index'),
    path('order/', html_post_form, name='html_post_form'),
    path('create_order/', post_form, name='create_order'),
    path('create_order_json/', create_order_json, name='create_order_json'),
]
