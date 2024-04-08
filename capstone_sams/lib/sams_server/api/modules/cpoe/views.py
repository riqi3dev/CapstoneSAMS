from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework import status
from api.modules.user.models import Account, Data_Log
from api.modules.user.serializers import AccountSerializer
from api.modules.patient.models import Health_Record, Patient,Present_Illness
from api.modules.cpoe.models import Comment, Medicine, Prescription
from api.modules.cpoe.serializers import CommentSerializer, MedicineSerializer, PrescriptionSerializer
from api.modules.disease_prediction.cdssModel.models import HealthSymptom


class CommentView(viewsets.ModelViewSet):

    @api_view(['POST'])
    def create_comment(request, accountId, recordNum):
        try:
            comment_data = json.loads(request.body)
            account = Account.objects.get(pk=accountId)
            record = Health_Record.objects.get(pk=recordNum)
            comment = Comment.objects.create(
                content = comment_data['content'],
                account = account,
                health_record = record
            )
            data_log = Data_Log.objects.create(
                event = f"{account.username} created comment",
                type = "User Created Comment",
                account = account
            )
            return Response({"message": "Comment successfully created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Failed to create comment"}, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    def fetch_comments(request):
        try:
            queryset = Comment.objects.all()
            serializer = CommentSerializer(queryset, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch comments.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    def fetch_comments_by_account_id(request, accountId):
        try:
            account = Account.objects.get(pk=accountId)
            queryset = Comment.objects.filter(account=account)

            account_serializer = AccountSerializer(account)
            serializer = CommentSerializer(queryset, many = True)
            response_data = {
                'comments' : serializer.data,
                'account': account_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch comments.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    @api_view(['PUT'])
    def update_comment(request, comNum):
        try:
            comments_data = json.loads(request.body)
            comment = Comment.objects.get(pk = comNum)
            comment.content = comments_data['content']
            comment.save()
            accountID = comments_data['account']
            account = get_object_or_404(Account, pk=accountID)
            data_log = Data_Log.objects.create(
                event = f"{account.username} updated comment code {comNum}",
                type = "User Update Comment",
                account = account
            )
            return Response({"message": "Comment successfully update"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": "Failed to update comment", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['DELETE'])
    def delete_comment(request, comNum):
        try:
            comment = Comment.objects.get(pk = comNum)
            comment.delete()
            data_log = Data_Log.objects.create(
                event = f"{comment.account.username} deleted comment code {comNum}",
                type = "User Deleted Personal Prescription",
                account = comment.account 
            )
            return Response({"message": "Comment successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
             return Response({"message": "Failed to delete comment", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class MedicineView(viewsets.ModelViewSet):
    
    @api_view(['GET'])
    # @permission_classes([IsAuthenticated])
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
    
    @api_view(['GET'])
    def fetch_medicine_through_prescription(request, presID):
        try:
            prescription = Prescription.objects.get(pk=presID)
            prescribed_medicines = Prescribed_Medicine.objects.filter(prescription=prescription)
            medicines = [prescribed_medicine.medicine for prescribed_medicine in prescribed_medicines]
            serializer = MedicineSerializer(medicines, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({"message": "Failed to fetch medicine.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

class PrescriptionView(viewsets.ViewSet):
    @api_view(['POST'])
    # @permission_classes([IsAuthenticated])
    def save_prescription(request):
        try:
            prescription_data = json.loads(request.body)
            accountID = prescription_data['account']
            patientID = prescription_data['patient']             
            illnessID = prescription_data['illness'] 
            account = Account.objects.get(pk=accountID)
            # record = Health_Record.objects.get(patient=patientID)
            patient = Patient.objects.get(pk=patientID) 
            illness = Present_Illness.objects.get(pk=illnessID)
            # disease = prescription_data.get('disease')
            prescription = Prescription.objects.create(
                medicines=prescription_data['medicines'],
                account=account,
                # health_record = record,
                patient = patient,
                illness = illness,
                # disease=disease
            )
            data_log = Data_Log.objects.create(
                event = f"{account.username} created prescription",
                type = "User Created Prescription",
                account = account
            )
            return Response({"message": "Prescription saved successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Failed to save prescription", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['PUT'])
    # @permission_classes([IsAuthenticated])
    def update_prescription_amount(request, presID):
        try:
            prescription_data = json.loads(request.body)
            prescription = Prescription.objects.get(pk=presID)
            if 'medicines' in prescription_data:
                prescription.medicines = prescription_data['medicines']
            if 'account' in prescription_data:
                account_id = prescription_data['account']
                account = get_object_or_404(Account, pk=account_id)
            if 'health_record' in prescription_data:
                prescription.health_record_id = prescription_data['health_record']
            if 'patient' in prescription_data:
                prescription.patient_id = prescription_data['patient']
            prescription.save()
            data_log = Data_Log.objects.create(
                event=f"{account.username} updated prescription amount",
                type="User Updated Prescription Amount",
                account=account
                )
            return Response({"message": "Prescription amount updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Failed to update prescription amount", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


   
    @api_view(['GET'])
    def fetch_prescription_by_id(request, presID):
        try:
            presriptID = Prescription.objects.get(pk=presID) 
            serializer = PrescriptionSerializer(presriptID)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Present_Illness.DoesNotExist:
            return Response({"message": "Prescription does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    @api_view(['PUT'])
    def update_prescription(request, presID, accountID, patientID, illnessID):
        try:
        # Retrieve necessary objects from IDs
            account = Account.objects.get(pk=accountID)
            patient = Patient.objects.get(pk=patientID)
            present_illness = Present_Illness.objects.get(pk=illnessID)
 
            prescription = Prescription.objects.get(pk=presID)
 
            prescription_data = json.loads(request.body)
 
            prescription.medicines = prescription_data.get('medicines')   
            prescription.patient = patient
            prescription.account = account
            prescription.illness = present_illness
 
            prescription.save()
 
            data_log = Data_Log.objects.create(
                event=f"{account.username} updated prescription",
                type="User Updated Prescription",
                account=account
            )

            return Response({"message": "Prescription updated successfully"}, status=status.HTTP_200_OK)

        except Prescription.DoesNotExist:
            return Response({"message": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": "Failed to update prescription", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # @api_view(['PUT'])
    # # @permission_classes([IsAuthenticated])
    # def update_prescription(request, presID, accountID, patientID, illnessID):
    #     try:
    #         present_illness = Present_Illness.objects.get(pk=illnessID)
    #         account = Account.objects.get(pk=accountID) 
    #         patient = Patient.objects.get(pk=patientID) 
    #         prescription = Prescription.objects.get(pk=presID)
    #         prescription_data = json.loads(request.body)
    #         prescription.presID = prescription
    #         prescription.medicines = prescription_data['medicines']
    #         prescription.patient = patient
    #         prescription.account = account
    #         prescription.illness = present_illness
            
    #         # if 'medicines' in prescription_data:
    #         #     prescription.medicines = prescription_data['medicines']
    #         # if 'account' in prescription_data:
    #         #     account_id = prescription_data['account']
    #         #     account = get_object_or_404(Account, pk=account_id)
    #         # # if 'health_record' in prescription_data:
    #         # #     prescription.health_record_id = prescription_data['health_record']
    #         # if 'patient' in prescription_data:
    #         #     prescription.patient_id = prescription_data['patient']
    #         # if 'illness' in prescription_data:
    #         #     prescription.illness = prescription_data['illness']
    #         prescription.save()
    #         data_log = Data_Log.objects.create(
    #             event=f"{account.username} updated prescription",
    #             type="User Updated Prescription",
    #             account=account
    #             )
    #         return Response({"message": "Prescription updated successfully"}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         print(e)
    #         return Response({"message": "Failed to update prescription", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['POST'])
    # @permission_classes([IsAuthenticated])
    def delete_prescription(request, presID):
        try:
            prescription = Prescription.objects.get(presID = presID)
            data_log = Data_Log.objects.create(
                event = f"{prescription.account.username} deleted prescription code {prescription}",
                type = "User Deleted Prescription",
                account = prescription.account 
            )
            # prescription.delete()
            prescription.isDeleted = True
            prescription.save()
            return Response({"message": "Prescription successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
             return Response({"message": "Failed to delete prescription", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    # @permission_classes([IsAuthenticated])
    def delete_medicine(request, presID, drugId):
        try:
            prescription = Prescription.objects.get(presID = presID)
            medicines = prescription.medicines
            for medicine in medicines:
                if medicine['drugId'] == drugId:
                    medicines.remove(medicine)
                    prescription.save()
                    return Response({"message": "Medicine successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
            data_log = Data_Log.objects.create(
                event = f"{prescription.account.username} deleted medicine code {prescription}",
                type = "User Deleted Medicine",
                account = prescription.account 
            ) 
            return Response({"message": "Medicine with given drugId not found"}, status=status.HTTP_404_NOT_FOUND)

        except Prescription.DoesNotExist:
            return Response({"message": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Failed to delete medicine", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    # @permission_classes([IsAuthenticated])
    def fetch_prescription_by_patientIds(request, patientID ):
        try: 
            patient = Patient.objects.get(pk=patientID)    
            prescriptions = Prescription.objects.filter(patient=patient )  
            prescriptionData = PrescriptionSerializer(prescriptions, many=True)  
            return Response(prescriptionData.data, status=status.HTTP_200_OK)
            # return Response(data_clean, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to fetch prescriptioddns", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)