from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import date


class TimezoneDict(models.Model):
    id = models.SmallAutoField(primary_key=True)
    timezone_name = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.TimeField()

    class Meta:
        db_table = "timezone_dict"
        verbose_name = "Справочник таймзон"
        verbose_name_plural = "Справочник таймзон"

    def __str__(self):
        return self.timezone_name


class CustomUserManager(BaseUserManager):
    def create_user(self, username, company, group, timezone, password, **extra_fields):
        if not username:
            raise ValueError('Имя пользователя обязательно')
        if not company or not group or not timezone:
            raise ValueError('Для обычного пользователя обязательны company, group и timezone')
        user = self.model(username=username, company=company, group=group, timezone=timezone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        superuser = self.model(username=username, **extra_fields)
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='users', blank=True,
                                null=True)
    group = models.ForeignKey('roles.UserGroup', on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    timezone = models.ForeignKey(TimezoneDict, on_delete=models.CASCADE, related_name='users',
                                 blank=True, null=True)

    username = models.CharField(max_length=60, unique=True)
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    patronymic = models.CharField(max_length=60, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    user_lock = models.BooleanField(default=False)
    comment = models.TextField(max_length=1000, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = [
            models.Index(fields=["group"], name="idx_users_group"),
            models.Index(fields=["timezone"], name="idx_users_timezone"),
            models.Index(fields=["company"], name="idx_users_company"),
            models.Index(fields=["username"], name="idx_users_username"),
            models.Index(fields=["company", "group"], name="idx_users_company_group"),
            models.Index(fields=["username", "user_lock"], name="idx_users_username_lock"),
            models.Index(fields=["id", "company"], name="idx_users_id_company"),
            models.Index(fields=["id", "group"], name="idx_users_id_group"),
        ]

    def __str__(self):
        return self.username


class PropertyCode(models.Model):
    id = models.SmallAutoField(primary_key=True)
    group_code = models.CharField(max_length=30)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "property_code_dict"
        verbose_name = "Код свойств"
        verbose_name_plural = "Коды свойств"
        indexes = [
            models.Index(fields=["code"], name="idx_property_code_dict_code"),
            models.Index(fields=["group_code", "code"], name="idx_property_group_code_code"),
        ]

    def __str__(self):
        return self.code


class UserProperty(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='properties')
    property = models.ForeignKey(PropertyCode,
                                 on_delete=models.CASCADE,
                                 related_name='users')
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "user_properties"
        verbose_name = "Свойство пользователей"
        verbose_name_plural = "Свойства пользователей"
        indexes = [
            models.Index(fields=["property"], name="idx_user_properties_property"),
            models.Index(fields=["user"], name="idx_user_properties_user"),
            models.Index(fields=["user", "property"],
                         name="idx_user_properties_user_prop"),
        ]

    def __str__(self):
        return f"Свойство {self.property} для пользователя {self.user}"


class StatusDict(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=60)

    class Meta:
        db_table = "status_dict"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        indexes = [
            models.Index(fields=["code"], name="idx_status_dict_code"),
        ]

    def __str__(self):
        return self.name


class UserSending(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='user_sendings')
    status = models.ForeignKey(StatusDict,
                               on_delete=models.CASCADE,
                               related_name='user_sendings')
    created_date = models.DateField(default=date.today)
    message = models.TextField(max_length=4000)

    class Meta:
        db_table = "user_sendings"
        verbose_name = "Рассылка пользователям"
        verbose_name_plural = "Рассылки пользователям"
        indexes = [
            models.Index(fields=["user"], name="idx_user_sendings_user"),
            models.Index(fields=["status"], name="idx_user_sendings_status"),
            models.Index(fields=["user", "status", "created_date"],
                         name="idx_user_sendings_us_st_creat"),
            models.Index(fields=["created_date"], name="idx_user_sendings_created"),
        ]

    def __str__(self):
        return f'Рассылка для пользователя {self.user}'


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    version = models.IntegerField()

    class Meta:
        db_table = "reports"
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        indexes = [
            models.Index(fields=["code"], name="idx_reports_code"),
            models.Index(fields=["code", "version"], name="idx_reports_code_version"),
        ]

    def __str__(self):
        return self.code


class UserReportLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='report_links')
    report = models.ForeignKey(Report,
                               on_delete=models.CASCADE,
                               related_name='report_links')
    created_date = models.DateField()
    active_from = models.DateField()
    active_to = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "user_report_links"
        verbose_name = "Связь пользователей и отчетов"
        verbose_name_plural = "Связи пользователей и отчетов"
        indexes = [
            models.Index(fields=["user"], name="idx_user_report_links_user"),
            models.Index(fields=["report"], name="idx_user_report_links_report"),
            models.Index(fields=["created_date"], name="idx_user_report_links_created"),
            models.Index(fields=["active_from"], name="idx_user_report_links_active_f"),
            models.Index(fields=["active_to"], name="idx_user_report_links_active_t"),
            models.Index(fields=["active_from", "active_to"], name="idx_user_report_links_act_f_t"),
            models.Index(fields=["user", "active_to"], name="idx_user_report_l_user_act_t"),
            models.Index(fields=["user", "active_from", "active_to"],
                         name="idx_user_report_l_user_act_ft"),
        ]

    def __str__(self):
        return f'Пользователь {self.user} - Отчет {self.report}'

