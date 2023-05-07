from django.shortcuts import render

# Create your views here.
from rest_framework import api_view
from rest_framework.response import Response

@api_view(['POST'])
def move_piece(request) -> Response:
    pass