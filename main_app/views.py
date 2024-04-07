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

  # add (override) the retrieve method below
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance) 

    # Get the list of toys not associated with this jewelry
    toys_not_associated = Toy.objects.exclude(id__in=instance.toys.all())
    toys_serializer = ToySerializer(toys_not_associated, many=True)

    return Response({
      'jewelry': serializer.data,
      'toys_not_associated': toys_serializer.data
    })

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

class AddToyToJewelry(APIView):
  def post(self, request, jewelry_id, toy_id):
    jewelry = Jewelry.objects.get(id=jewelry_id)
    toy = Toy.objects.get(id=toy_id)
    jewelry.toys.add(toy)
    return Response({'message': f'Toy {toy.name} added to Jewelry {jewelry.name}'})
  
class RemoveToyFromJewelry(APIView):
  def post(self, request, jewelry_id, toy_id):
    jewelry = Jewelry.objects.get(id=jewelry_id)
    toy = Toy.objects.get(id=toy_id)
    jewelry.toys.remove(toy)
    return Response({'message': f'Toy {toy.name} removed from Jewelry {jewelry.name}'})

 
   
   

