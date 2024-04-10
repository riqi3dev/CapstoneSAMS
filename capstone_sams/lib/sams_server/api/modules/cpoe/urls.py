from .views import CommentView, MedicineView, PrescriptionView
from django.urls import path

urlpatterns = [
    path('comments/create/<str:accountId>/<str:recordNum>/', CommentView.create_comment, name='create_comment'),
    path('comments/get/', CommentView.fetch_comments, name='fetch_comments'),
    path('comments/get/<str:accountId>', CommentView.fetch_comments_by_account_id, name='fetch_comments_by_account_id'),
    path('comments/update/<int:comNum>', CommentView.update_comment, name='update_comment'),
    path('comments/delete/<int:comNum>', CommentView.delete_comment, name='delete_comment'),
    path('medicines/', MedicineView.fetch_medicine, name='fetch_medicines'),
    path('medicines/<str:drugID>', MedicineView.fetch_medicine_by_id, name='fetch_medicine'),
    path('medicines/<str:presID>', MedicineView.fetch_medicine_through_prescription, name='fetch_medicine_through_prescription'),
    path('prescription/save/', PrescriptionView.save_prescription, name='save_prescription'),
    path('prescription/get-patient/<str:patientID>/', PrescriptionView.fetch_prescription_by_patientIds, name='fetch_prescription'),
    path('prescription/get-prescription/update-amount/<str:presID>', PrescriptionView.update_prescription_amount, name='update_prescription_amount'),
    path('prescription/get-prescription/<str:presID>', PrescriptionView.fetch_prescription_by_id, name='fetch_prescription_by_id'), 
    path('prescription/get-illness-prescription/<str:illnessID>/', PrescriptionView.fetch_prescription_by_illness_id, name='fetch_prescription_by_illness_id'), 
    path('prescription/get-prescription/update/<str:presID>/<str:accountID>/<str:patientID>/<str:illnessID>', PrescriptionView.update_prescription, name='update_prescription'), 
    path('prescription/get-prescription/delete/<str:presID>', PrescriptionView.delete_prescription, name='delete_prescription'), #API Endpoint for note deletion
    path('prescription/get-prescription-<str:presID>/delete-medicine/<str:drugId>', PrescriptionView.delete_medicine, name='delete_medicine'), #API Endpoint for note deletion
]
