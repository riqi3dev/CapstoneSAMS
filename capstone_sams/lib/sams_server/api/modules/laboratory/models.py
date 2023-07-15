from django.db import models
from django import forms



# import os
# import datetime
# from django import forms
# Create your models here.



# def filepath(request, filename):
#     old_filename  =filename
#     timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
#     filename = '%%' % (timeNow, old_filename)
#     return os.path.join('uploads/', filename)

# class LabResult(models.Model):
#     name = models.TextField(max_length=128)
#     comment = models.TextField(max_length=512)
#     pdf = models.

# class UploadFileForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     comments = forms.TimeField()
#     file = forms.FileField(upload_to=filepath, null=True, blank=True)





class LabResult(models.Model):
    title = models.CharField(max_length=128)
    comment = models.TextField(max_length=512)
    pdf = models.FileField(upload_to='upload/')
 
    class Meta:
        ordering = ['title']
     
    def __str__(self):
        return f"{self.title}"

class UploadLabResult(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ('title', 'comment','pdf')

class pdfJson(models.Model):
    text = models.TextField()