from django.shortcuts import render

from models import Crime
from serializers import CrimeSerializer

# Create your views here.
class CrimeDetail(generics.RetrieveAPIView):
	queryset = Crime.objects.all()
	serializer_class = CrimeSerializer