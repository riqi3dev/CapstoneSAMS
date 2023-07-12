import pandas as pd
import json
from rest_framework import status

from django.shortcuts import render, redirect
from api.serializers import AccountSerializer, PatientSerializer, MedicineSerializer, HealthRecordSerializer, SymptomSerializer, CommentSerializer, PrescriptionSerializer, MedicineSerializer, PersonalNoteSerializer
from tabula.io import read_pdf
import csv
from django.contrib import messages
from django.http import JsonResponse

from api.models import DrugModel, UploadDrugFile, Patient, Medicine, Health_Record, Patient_Symptom, Medical_History, Comment, Account, Symptom, Prescription, Prescribed_Medicine, Personal_Note, UploadLabResult 
# from somewhere import handle_uploaded_file
from django.http import HttpResponseRedirect, HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from disease_prediction.prediction_model import predict_disease
# def process_pdf(request):
#     # file_path = "\Users\nulltest\ocr\cbc.pdf"
#     df = read_pdf(file_path, pages='all', encoding='cp1252')
#     df = df[2].to_json(orient='records')
#     return JsonResponse(df, safe=False)

def decode_utf8(line_iterator):
    for line in line_iterator:
        yield line.decode('utf-8')

# def handle_uploaded_file(f):
#     with open('C:\Users\nulltest\ocr\upload', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# def upload_pdf(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})


def ViewLabResult(request):
    if request.method == 'POST':
        form = UploadLabResult(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('The file is saved')
    else:
        form = UploadLabResult()
    return render(request, 'ocr.html', {'form': form})

def ViewUploadCSV(request):
    if request.method == 'GET':
        form = UploadDrugFile()
        return render(request, 'addDrug.html', {'form': form})
    form = UploadDrugFile(request.POST, request.FILES)
    if form.is_valid():
        drugs_file = csv.reader(decode_utf8(request.FILES['sent_file']))
        next(drugs_file)

def process_pdf(request):
    pdf_path = "cbc.pdf"
    dfs = read_pdf(pdf_path, pages='all', encoding='cp1252',
                   pandas_options={'header': True})
    json_data = dfs[1].to_json(orient='columns')
    print(json_data)
    dfs[0].to_json('output.json', orient='columns')


class PatientView(viewsets.ModelViewSet):

    @api_view(['POST'])
    def create_patient(request):
        try:
            patient_data = json.loads(request.body)
            patient = Patient.objects.create(
                patientID=patient_data['patientID'],
                firstName=patient_data['firstName'],
                middleName=patient_data['middleName'],
                lastName=patient_data['lastName'],
                gender=patient_data['gender'],
                birthDate=patient_data['birthDate'],
                phone=patient_data['phone'],
                email=patient_data['email']
            )
            patient.save()
            return Response({"message": "Patient created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Failed to create patient.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def fetch_patients(request):
        try:
            queryset = Patient.objects.all()
            serializer = PatientSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch patients.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def fetch_patient_by_id(request, patientID):
        try:
            queryset = Patient.objects.filter(pk=patientID)
            serializer = PatientSerializer(queryset.first())
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch patients.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['PUT'])
    def update_patient(request):
        try:
            patient_data = json.loads(request.body)
            patient_id = patient_data['patientID']
            patient = Patient.objects.get(pk=patient_id)
            patient.firstName = patient_data['firstName']
            patient.middleName = patient_data['middleName']
            patient.lastName = patient_data['lastName']
            patient.gender = patient_data['gender']
            patient.birthDate = patient_data['birthDate']
            patient.phone = patient_data['phone']
            patient.email = patient_data['email']
            patient.save()
            return Response({"message": "Patient updated successfully."}, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"message": "Patient does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Failed to update patient.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MedicineView(viewsets.ModelViewSet):

    @api_view(['GET'])
    def fetch_medicine(request):
        try:
            queryset = Medicine.objects.all()
            serializer = MedicineSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch medicines.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['GET'])
    def fetch_medicine_by_id(request, drugID):
        try:
            queryset = Medicine.objects.filter(pk=drugID)
            serializer = MedicineSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch medicine.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class HealthRecordView(viewsets.ViewSet):

    @api_view(['GET'])
    def fetch_records(request):
        try:
            records = Health_Record.objects.all()
            response_data = []
            for record in records:
                history = Medical_History.objects.filter(histNum__in=record)
                patient = Patient.objects.filter(patientID__in=history)
                patient_symptoms = Patient_Symptom.objects.filter(medical_history__in=history)
                symptoms = Symptom.objects.filter(patient_symptoms__in=patient_symptoms)
                comments = Comment.objects.filter(health_record=record)
                physician = Account.objects.filter(comment__in=comments)
                prescription = Prescription.objects.filter(health_record=record)
                prescribed_medicines = Prescribed_Medicine.objects.filter(prescription__in=prescription)
                medicines = Medicine.objects.filter(prescribed_medicine__in=prescribed_medicines)
                # Serialize the data
                history_data = HealthRecordSerializer(record).data
                patient_data = PatientSerializer(patient, many=True).data
                symptoms_data = SymptomSerializer(symptoms, many=True).data
                comments_data = CommentSerializer(comments, many=True).data
                physician_data = AccountSerializer(physician, many=True).data
                prescription_data = PrescriptionSerializer(prescription, many=True).data
                medicines_data = MedicineSerializer(medicines, many=True).data

                record_data = {
                    'history': history_data,
                    'physicians': physician_data,
                    'patients': patient_data,
                    'symptoms': symptoms_data,
                    'comments': comments_data,
                    'prescription': prescription_data,
                    'medicines': medicines_data,
                }

                response_data.append(record_data)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch health records", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['GET'])
    def fetch_record_by_num(request):
        try:
            data = json.loads(request.body)
            recordNum = data['recordNum']
            record = Health_Record.objects.get(pk=recordNum)
            history = Medical_History.objects.filter(health_record=record)
            patient_symptoms = Patient_Symptom.objects.filter(
                medical_history__in=history)
            symptoms = Symptom.objects.filter(
                patient_symptoms__in=patient_symptoms)
            comments = Comment.objects.filter(health_record=record)
            physician = Account.objects.filter(comment__in=comments)
            prescription = Prescription.objects.filter(health_record=record)
            prescribed_medicines = Prescribed_Medicine.objects.filter(
                prescription__in=prescription)
            medicines = Medicine.objects.filter(
                prescribed_medicine__in=prescribed_medicines)

            history_data = HealthRecordSerializer(record)
            physician_data = AccountSerializer(physician, many=True)
            symptoms_data = SymptomSerializer(symptoms, many=True)
            comments_data = CommentSerializer(comments, many=True)
            prescription_data = PrescriptionSerializer(prescription, many=True)
            medicines_data = MedicineSerializer(medicines, many=True)

            response_data = {
                'history': history_data.data,
                'physicians': physician_data.data,
                'symptoms': symptoms_data.data,
                'comments': comments_data.data,
                'presription': prescription_data.data,
                'medicines': medicines_data.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": "Failed to fetch health record", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SymptomsView(viewsets.ModelViewSet):
    
    @api_view(['GET'])
    def fetch_symptoms(request):
        try:
            symptoms = Symptom.objects.all()
            serializer = SymptomSerializer(symptoms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch symptoms", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    def fetch_symptoms_by_num(request, sympNum):
        try:
            symptoms = Symptom.objects.get(pk=sympNum)
            serializer = SymptomSerializer(symptoms)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch symptoms", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PersonalNotesView(viewsets.ModelViewSet):
    
    @api_view(['GET'])
    def fetch_personal_notes(request, accountID):
        try:
            personal_notes = Personal_Note.objects.filter(account__accountID=accountID)
            serializer = PersonalNoteSerializer(personal_notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OKs)
        except Exception as e:
            return Response({"message": "Failed to fetch personal notes"}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST']) 
    def create_personal_note(request):
        try:
            notes_data = json.load(request.body)
            note = Personal_Note.objects.create(
                title = notes_data['title'],
                content = notes_data['content'],
                account = notes_data['account']
            )
            note.save()
            return Response({"message": "Note successfully created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Failed to create note"}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['PUT'])
    def update_personal_note(request, noteNum):
        try:
            notes_data = json.load(request.body)
            note = Personal_Note.objects.get(pk=noteNum)
            note.title = notes_data['title']
            note.content = notes_data['content']
            note.account = notes_data['account']
            note.save()
            return Response({"message": "Note successfully update"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": "Failed to update note", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['DELETE'])
    def delete_personal_note(request, noteNum):
        try:
            note = Personal_Note.objects.get(pk=noteNum)
            note.delete()
            return Response({"message": "Note successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
             return Response({"message": "Failed to delete note", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# def predict(request):
#     # Get symptoms from GET parameters
#     symptoms = request.GET.getlist('symptoms')

#     # Predict the disease
#     prediction = predict_disease(symptoms)

#     # Return prediction as JSON
#     return JsonResponse({'prediction': prediction})