from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions # modify these imports to match
from .models import Jewelry, Feeding, Toy
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, JewelrySerializer, FeedingSerializer, ToySerializer
from rest_framework.exceptions import PermissionDenied # include this additional import

# Create your views here.
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the jewelry-collector api home route!'}
    return Response(content)

# include the registration, login, and verification views below
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })


class JewelryList(generics.ListCreateAPIView):
  queryset = Jewelry.objects.all()
  serializer_class = JewelrySerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      # This ensures we only return jewelrys belonging to the logged-in user
      user = self.request.user
      return Jewelry.objects.filter(user=user)

  def perform_create(self, serializer):
      # This associates the newly created jewelry with the logged-in user
      serializer.save(user=self.request.user)


class JewelryDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Jewelry.objects.all()
  serializer_class = JewelrySerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Jewelry.objects.filter(user=user)


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
  
  def perform_update(self, serializer):
    jewelry = self.get_object()
    if jewelry.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this jewelry."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this jewelry."})
    instance.delete()


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

 
   
   

