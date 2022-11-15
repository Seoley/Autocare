# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CrCompany(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    company_ip = models.CharField(max_length=15)
    company_token = models.CharField(max_length=300)
    company_operation = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'CR_COMPANY'


class CrConfig(models.Model):
    config_id = models.BigAutoField(primary_key=True)
    model = models.ForeignKey('CrModelInfo', models.DO_NOTHING)
    collection_oper = models.CharField(max_length=3)
    labeling_oper = models.CharField(max_length=3)
    learning_oper = models.CharField(max_length=3)
    learning_cycle = models.CharField(max_length=8)
    learning_start = models.CharField(max_length=9)
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CR_CONFIG'


class CrModelHistory(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(CrCompany, models.DO_NOTHING)
    model = models.ForeignKey('CrModelInfo', models.DO_NOTHING)
    using_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'CR_MODEL_HISTORY'


class CrModelInfo(models.Model):
    model_id = models.BigAutoField(primary_key=True)
    model_name = models.CharField(max_length=200)
    model_rname = models.CharField(max_length=200)
    model_path = models.CharField(max_length=200)
    model_api = models.CharField(max_length=200, blank=True, null=True)
    data_path = models.CharField(max_length=200, blank=True, null=True)
    model_file = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CR_MODEL_INFO'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
