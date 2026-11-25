"""
doctors/views.py  —  Doctor CRUD views.
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Doctor
from .serializers import DoctorSerializer, DoctorReadSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/doctors/  — list all doctors
    POST /api/doctors/  — create a doctor
    """
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()

    def get_serializer_class(self):
        return DoctorSerializer if self.request.method == "POST" else DoctorReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = DoctorSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save()
        return Response(DoctorReadSerializer(doctor, context={"request": request}).data, status=status.HTTP_201_CREATED)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/doctors/<id>/
    PUT    /api/doctors/<id>/
    PATCH  /api/doctors/<id>/
    DELETE /api/doctors/<id>/
    """
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorReadSerializer
    http_method_names = ["get", "put", "patch", "delete"]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        doctor = self.get_object()
        serializer = DoctorSerializer(
            doctor, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(DoctorReadSerializer(doctor, context={"request": request}).data)
