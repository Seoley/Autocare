from django.db import models

# Create your models here.

class CR_USER_INFO(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_age = models.IntegerField()
    user_sex = models.CharField(max_length=1)
    user_disease = models.CharField(max_length=200)

class CR_BIOFILE_INFO(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    file_user_id = models.ForeignKey("CR_USER_INFO", related_name="CR_USER_INFO", on_delete=models.CASCADE, db_column="file_user_id")
    file_path = models.CharField(max_length=200)
    file_name = models.CharField(max_length=300)
    file_rname = models.CharField(max_length=300)
    file_ext = models.CharField(max_length=10)
    file_size = models.CharField(max_length=30)
    file_savetime = models.DateTimeField(auto_now_add=True)
    
