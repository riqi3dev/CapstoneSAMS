from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin 

class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
class Account(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_ROLE_CHOICES = [
        ('physician', 'Physician'),
        ('medtech', 'MedTech'),
        ('nurse', 'Nurse'),
        ('admin', 'Admin'),
    ]
    accountID = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank = False)
    firstName = models.CharField(max_length=100, blank = False)
    middleName = models.CharField(max_length=100, blank = False)
    lastName = models.CharField(max_length=100, blank = False)
    accountRole = models.CharField(max_length=100, choices=ACCOUNT_ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['accountID','accountRole']

    objects = AccountManager()

    class Meta:
        db_table = "account"
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True

class Personal_Note(models.Model):
    noteNum = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 20)
    content = models.CharField(max_length = 3000)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)

class Data_Log(models.Model):
    #Log Attributes
    logNum = models.AutoField(primary_key = True) #Auto incrementing field
    event = models.CharField(max_length = 500)
    date = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)