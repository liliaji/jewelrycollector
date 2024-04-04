from django.urls import path
from .views import Home, JewelryList, JewelryDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('jewelrys/', JewelryList.as_view(), name='jewelry-list'),
  path('jewelrys/<int:id>/', JewelryDetail.as_view(), name='jewelry-detail'),
]