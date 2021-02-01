from django.urls import path
from .views import EquipmentView, DownloadCpView


urlpatterns = [
    path('equipments/', EquipmentView.as_view()),
    path('downloadcp/', DownloadCpView.as_view()),
]
