from django.db import models


class SettingsDict(models.Model):
    id = models.SmallAutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "settings_dict"
        verbose_name = "Справочник кодов системы"
        verbose_name_plural = "Справочник кодов системы"
        indexes = [
            models.Index(fields=["code"], name="idx_settings_dict_code"),
        ]

    def __str__(self):
        return self.name


class Settings(models.Model):
    id = models.SmallAutoField(primary_key=True)
    setting = models.ForeignKey(SettingsDict,
                                on_delete=models.CASCADE,
                                related_name='settings')
    value = models.CharField(max_length=255)
    active_from = models.DateField()
    active_to = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "settings"
        verbose_name = "Общие свойства"
        verbose_name_plural = "Общие свойства"
        indexes = [
            models.Index(fields=["setting"], name="idx_settings_setting"),
            models.Index(fields=["active_from"], name="idx_settings_active_from"),
            models.Index(fields=["active_to"], name="idx_settings_active_to"),
            models.Index(fields=["active_from", "active_to"], name="idx_settings_active_from_to"),
            models.Index(fields=["setting", "active_from", "active_to"],
                         name="idx_settings_setting_act_f_t"),
            models.Index(fields=["setting", "active_to"], name="idx_settings_setting_act_to"),
        ]

    def __str__(self):
        return f'Код в системе: {self.setting}, значение: {self.value}'


class ShablonDict(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "shablon_dict"
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"
        indexes = [
            models.Index(fields=["code"], name="idx_shablon_dict_code"),
        ]

    def __str__(self):
        return self.code