from django.urls import path
from .views import Home, JewelryList, JewelryDetail, FeedingListCreate, FeedingDetail, ToyList, ToyDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('jewelrys/', JewelryList.as_view(), name='jewelry-list'),
  path('jewelrys/<int:id>/', JewelryDetail.as_view(), name='jewelry-detail'),
  path('jewelrys/<int:jewelry_id>/feedings/', FeedingListCreate.as_view(), name='feeding-list-create'),
	path('jewelrys/<int:jewelry_id>/feedings/<int:id>/', FeedingDetail.as_view(), name='feeding-detail'),
  path('toys/', ToyList.as_view(), name='toy-list'),
  path('toys/<int:id>/', ToyDetail.as_view(), name='toy-detail'), 
]