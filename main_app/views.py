from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Jewelry
from .serializers import JewelrySerializer

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

