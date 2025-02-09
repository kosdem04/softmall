from django.db import models

class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    inn = models.CharField(max_length=16)
    kpp = models.CharField(max_length=9)
    ogrn = models.CharField(max_length=13, blank=True, null=True)
    bic = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        db_table = "companies"
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        indexes = [
            models.Index(fields=["inn"], name="idx_companies_inn"),
            models.Index(fields=["kpp"], name="idx_companies_kpp"),
            models.Index(fields=["ogrn"], name="idx_companies_ogrn"),
            models.Index(fields=["bic"], name="idx_companies_bic"),
            # models.Index(fields=["property"], name="idx_companies_property"),
        ]

    def __str__(self):
        return self.name


class License(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='licenses')
    license_key = models.CharField(max_length=1000)
    active_from = models.DateField()
    active_to = models.DateField()

    class Meta:
        db_table = "license"
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"
        indexes = [
            models.Index(fields=["company"], name="idx_license_company"),
            models.Index(fields=["company", "active_from"], name="idx_license_company_active_f"),
            models.Index(fields=["active_from", "active_to"], name="idx_license_active_from_to"),
            models.Index(fields=["company", "active_from", "active_to"],
                         name="idx_license_company_act_f_t"),
        ]

    def __str__(self):
        return f'Лицензия {self.license_key} для компании {self.company}'


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=60)

    class Meta:
        db_table = "modules"
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"
        indexes = [
            models.Index(fields=["code"], name="idx_modules_code"),
        ]

    def __str__(self):
        return self.name


class ModuleCompanyLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name='company_links')
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='company_links')
    position = models.IntegerField()
    active_from = models.DateField()
    active_to = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "module_company_links"
        verbose_name = "Связь модулей и компаний"
        verbose_name_plural = "Связи модулей и компаний"
        indexes = [
            models.Index(fields=["company"], name="idx_module_company_l_company"),
            models.Index(fields=["module"], name="idx_module_company_l_module"),
            models.Index(fields=["active_from"], name="idx_module_company_l_act_f"),
            models.Index(fields=["active_to"], name="idx_module_company_l_act_t"),
            models.Index(fields=["company", "active_from", "active_to"],
                         name="idx_module_comp_l_comp_act_ft"),
        ]

    def __str__(self):
        return f'Компания {self.company} - Модуль {self.module}'


class CompanyProperty(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='company_properties')
    property = models.ForeignKey('users.PropertyCode',
                                 on_delete=models.CASCADE,
                                 related_name='company_properties')
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "company_properties"
        verbose_name = "Свойство компаний"
        verbose_name_plural = "Свойства компаний"
        indexes = [
            models.Index(fields=["property"], name="idx_company_properties_prop"),
            models.Index(fields=["company"], name="idx_company_properties_comp"),
            models.Index(fields=["company", "property"],
                         name="idx_company_prop_comp_prop"),
        ]

    def __str__(self):
        return f'Компания {self.company} - Свойство {self.property}'


class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='departments')
    code = models.BigIntegerField()
    name = models.CharField(max_length=255)
    created_date = models.DateField()

    class Meta:
        db_table = "departments"
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"
        indexes = [
            models.Index(fields=["code"], name="idx_departments_code"),
            models.Index(fields=["company"], name="idx_departments_company"),
        ]

    def __str__(self):
        return f'Компания {self.company} - Подразделение {self.name}'