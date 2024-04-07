from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Jewelry, Feeding, Toy
from .serializers import JewelrySerializer, FeedingSerializer, ToySerializer

class JewelryList(generics.ListCreateAPIView):
  queryset = Jewelry.objects.all()
  serializer_class = JewelrySerializer

class JewelryDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Jewelry.objects.all()
  serializer_class = JewelrySerializer
  lookup_field = 'id'


# Create your views here.
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the jewelry-collector api home route!'}
    return Response(content)

class FeedingListCreate(generics.ListCreateAPIView):
  serializer_class = FeedingSerializer

  def get_queryset(self):
    jewelry_id = self.kwargs['jewelry_id']
    return Feeding.objects.filter(jewelry_id=jewelry_id)

  def perform_create(self, serializer):
    jewelry_id = self.kwargs['jewelry_id']
    jewelry = Jewelry.objects.get(id=jewelry_id)
    serializer.save(jewelry=jewelry)

class FeedingDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FeedingSerializer
  lookup_field = 'id'

  def get_queryset(self):
    jewelry_id = self.kwargs['jewelry_id']
    return Feeding.objects.filter(jewelry_id=jewelry_id)
  
class ToyList(generics.ListCreateAPIView):
  queryset = Toy.objects.all()
  serializer_class = ToySerializer

class ToyDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Toy.objects.all()
  serializer_class = ToySerializer
  lookup_field = 'id'  
   
   

