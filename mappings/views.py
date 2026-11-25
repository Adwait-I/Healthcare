"""
mappings/views.py  —  Patient-Doctor Mapping views.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from patients.models import Patient
from .models import PatientDoctorMapping
from .serializers import MappingCreateSerializer, MappingReadSerializer


class MappingListCreateView(APIView):
    """
    GET  /api/mappings/  — list all mappings
    POST /api/mappings/  — assign a doctor to a patient
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        mappings = PatientDoctorMapping.objects.select_related("patient", "doctor", "assigned_by").all()
        serializer = MappingReadSerializer(mappings, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MappingCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save()
        return Response(
            MappingReadSerializer(mapping).data,
            status=status.HTTP_201_CREATED,
        )


class MappingByPatientView(APIView):
    """
    GET /api/mappings/<patient_id>/  — get all doctors assigned to a patient
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, patient_id: int) -> Response:
        # Verify the patient exists
        patient = get_object_or_404(Patient, pk=patient_id)
        mappings = (
            PatientDoctorMapping.objects
            .filter(patient=patient)
            .select_related("patient", "doctor", "assigned_by")
        )
        serializer = MappingReadSerializer(mappings, many=True)
        return Response(
            {
                "patient_id": patient.pk,
                "patient_name": patient.full_name,
                "mappings": serializer.data,
            }
        )


class MappingDeleteView(APIView):
    """
    DELETE /api/mappings/<id>/  — remove a mapping by its ID
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, pk: int) -> Response:
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        mapping.delete()
        return Response(
            {"detail": "Mapping deleted successfully."},
            status=status.HTTP_200_OK,
        )
