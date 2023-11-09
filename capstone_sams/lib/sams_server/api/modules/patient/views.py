
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework import status
from api.modules.user.models import Account, Data_Log
from api.modules.patient.models import Patient, Health_Record
from api.modules.patient.serializers import PatientSerializer, HealthRecordSerializer

'''
This view represent all the functions necessary to conduct
operations related to Patient objects.
'''
class PatientView(viewsets.ModelViewSet):


    '''
    This view allow the user to create a new patient and store it into the 
    database.
    In addition, it creates a health record link to the new patient and also
    create data log for reference.
    Certain to exception handlers were coded to ensure continued operations.
    '''
    @api_view(['POST'])
    def create_patient(request):
        try:
            patient_data = json.loads(request.body)
            patient = Patient.objects.create(
                patientID=patient_data['patientID'],
                firstName=patient_data['firstName'],
                middleName=patient_data['middleName'],
                lastName=patient_data['lastName'],
                age=patient_data['age'],
                gender=patient_data['gender'],
                birthDate=patient_data['birthDate'],
                registration=patient_data['registration'],
                phone=patient_data['phone'],
                email=patient_data['email']
            )
            patient_instance = get_object_or_404(Patient, pk=patient_data['patientID'])
            record = Health_Record.objects.create(
                symptoms = {"symptoms": "None"},
                diseases = {"diseases": "None"},
                patient = patient_instance
            )
            data = json.loads(request.body)
            accountID = data['account']
            account = get_object_or_404(Account, pk=accountID)
            data_log = Data_Log.objects.create(
                event = f"{account.username} created patient",
                type = "User Created Patient",
                account = account
            )
            return Response({"message": "Patient created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Failed to create patient.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    '''
    This view allow the user to fetch all patients currently stored into the system.
    Certain to exception handlers were coded to ensure continued operations.
    '''
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def fetch_patients(request):
        try:
            queryset = Patient.objects.all()
            serializer = PatientSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch patients.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    '''
    This view allow the user to fetch a certain patient base on the patient's id.
    Certain to exception handlers were coded to ensure continued operations.
    '''
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def fetch_patient_by_id(request, patientID):
        try:
            queryset = Patient.objects.filter(pk=patientID)
            serializer = PatientSerializer(queryset.first())
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch patients.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    '''
    This view allow the user to update a patient based on the patient's id.
    A data log will be automatically generated for reference.
    Certain to exception handlers were coded to ensure continued operations.
    '''
    @api_view(['PUT'])
    def update_patient(request):
        try:
            patient_data = json.loads(request.body)
            patient_id = patient_data['patientID']
            patient = Patient.objects.get(pk=patient_id)
            patient.firstName = patient_data['firstName']
            patient.middleName = patient_data['middleName']
            patient.lastName = patient_data['lastName']
            patient.age = patient_data['age']
            patient.gender = patient_data['gender']
            patient.birthDate = patient_data['birthDate']
            patient.phone = patient_data['phone']
            patient.email = patient_data['email']
            patient.save()
            accountID = patient_data['account']
            account = get_object_or_404(Account, pk=accountID)
            data_log = Data_Log.objects.create(
                event = f"{account.username} updated patient id {patient_id}",
                type = "User Update Patient Data",
                account = account
            )
            return Response({"message": "Patient updated successfully."}, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"message": "Patient does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Failed to update patient.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

'''
This view represent all the functions necessary to conduct
operations related to Health_Record objects.
'''
class HealthRecordView(viewsets.ViewSet):

    '''
    This view allow the user to fetch a certain patient's record base on the patient's id.
    Certain to exception handlers were coded to ensure continued operations.
    '''
    @api_view(['GET'])
    def fetch_record_by_id(request, patientID):
        try:
            patient = Patient.objects.get(pk=patientID)
            record = Health_Record.objects.get(patient=patient)
            serializer = HealthRecordSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Health_Record.DoesNotExist:
            return Response({"message": "Health Record does not exist."}, status=status.HTTP_404_NOT_FOUND)