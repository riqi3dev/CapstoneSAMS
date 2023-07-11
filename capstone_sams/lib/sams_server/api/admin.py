from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from api.models import Account, Patient, Data_Log, Prescription, Medicine, Symptom, Health_Record, Comment, Prescribed_Medicine, Patient_Symptom

COMMON_PASSWORDS = ['password', '12345678', 'qwerty', 'abc123']


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('accountID', 'username', 'firstName', 'lastName', 'accountRole',
                  'is_active', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        # Check for password length
        if len(password1) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long")

        # Check that the password is not entirely numeric
        if password1.isdigit():
            raise forms.ValidationError("Password cannot be entirely numeric")

        # Check that the password is not common
        if password1.lower() in COMMON_PASSWORDS:
            raise forms.ValidationError("Password is too common")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = Account
        fields = ('username', 'password', 'firstName', 'lastName', 'accountRole',
                  'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'firstName', 'lastName', 'accountRole',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ('accountRole', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
         'fields': ('firstName', 'lastName', 'accountRole',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('accountID', 'username', 'firstName', 'lastName', 'accountRole',
                       'is_active', 'is_staff', 'is_superuser', 'password1', 'password2')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientAdmin(admin.ModelAdmin):
    form = PatientAdminForm
    list_display = ('patientID', 'firstName', 'middleName', 'lastName', 'gender', 'birthDate', 'phone', 'email')
    list_filter = ('patientID', 'gender')
    search_fields = ('patientID', 'firstName', 'middleName', 'lastName', 'birthDate', 'email')

class DataLogsAdminForm(forms.ModelForm):
    class Meta:
        model = Data_Log
        fields = '__all__'

class DataLogsAdmin(admin.ModelAdmin):
    form = DataLogsAdminForm
    list_display = ('logNum', 'event', 'date', 'account')
    list_filter = ('event', 'date', 'account')
    search_fields = ('event', 'date', 'account')

class MedicineAdminForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

class MedicineAdmin(admin.ModelAdmin):
    form = MedicineAdminForm
    list_display = ('drugId', 'drugCode', 'drugName')
    search_fields = ('drugId', 'drugCode', 'drugName')

class HealthRecordAdminForm(forms.ModelForm):
    class Meta:
        model = Health_Record
        fields = '__all__' 

class HealthRecordAdmin(admin.ModelAdmin):
    form = HealthRecordAdminForm
    list_display = ('recordNum', 'patient')
    search_fields = ('recordNum',)
    autocomplete_fields = ['patient']


class PrescriptionAdminForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'

class PrescriptionAdmin(admin.ModelAdmin):
    form = PrescriptionAdminForm
    autocomplete_fields = ['health_record']
    list_display = ('presNum', 'dosage', 'timeFrame', 'amount', 'account', 'health_record')
    list_filter = ('timeFrame', 'account', 'health_record')
    search_fields = ('presNum',)
    autocomplete_fields = ['account', 'health_record']

class SymptomsAdminForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = '__all__'

class SymptomsAdmin(admin.ModelAdmin):
    form = SymptomsAdminForm
    list_display = ('sympNum', 'symptom')
    search_fields = ('sympNum','symptom') 


# Now register the new UserAdmin...
admin.site.register(Account, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Data_Log, DataLogsAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Health_Record, HealthRecordAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Symptom, SymptomsAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)