"""
patients/views.py  —  Patient CRUD views (owner-scoped).
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Patient
from .serializers import PatientSerializer, PatientReadSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/patients/   — list own patients
    POST /api/patients/   — create a patient
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return PatientSerializer if self.request.method == "POST" else PatientReadSerializer

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        response_serializer = PatientReadSerializer(patient, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/patients/<id>/  — retrieve own patient
    PUT    /api/patients/<id>/  — full update
    PATCH  /api/patients/<id>/  — partial update
    DELETE /api/patients/<id>/  — delete
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PatientReadSerializer
    http_method_names = ["get", "put", "patch", "delete"]

    def get_object(self) -> Patient:
        return get_object_or_404(Patient, pk=self.kwargs["pk"], created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        patient = self.get_object()
        serializer = PatientSerializer(
            patient, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PatientReadSerializer(patient, context={"request": request}).data)
