from django.db import models


class UserGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey('companies.Company',
                                on_delete=models.CASCADE,
                                related_name='user_groups')
    group_name = models.CharField(max_length=255)
    comment = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "user_groups"
        verbose_name = "Группа пользователей"
        verbose_name_plural = "Группы пользователей"
        indexes = [
            models.Index(fields=["company"], name="idx_user_groups_company"),
        ]

    def __str__(self):
        return f'{self.group_name} ({self.company})'


class RolesDict(models.Model):
    id = models.SmallAutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=60)

    class Meta:
        db_table = "roles_dict"
        verbose_name = "Справочник ролей пользователя"
        verbose_name_plural = "Справочник ролей пользователя"

    def __str__(self):
        return self.name


class UserRoles(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.CustomUser',
                             on_delete=models.CASCADE,
                             related_name='user_roles')
    role = models.ForeignKey(RolesDict,
                             on_delete=models.CASCADE,
                             related_name='user_roles')
    active_from = models.DateField()
    active_to = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "user_roles"
        verbose_name = "Роль пользователей"
        verbose_name_plural = "Роли пользователей"
        indexes = [
            models.Index(fields=["user"], name="idx_user_roles_user"),
            models.Index(fields=["role"], name="idx_user_roles_role"),
            models.Index(fields=["user", "role", "active_to"], name="idx_user_roles_user_role_act_t"),
            models.Index(fields=["active_from"], name="idx_user_roles_active_from"),
            models.Index(fields=["active_to"], name="idx_user_roles_active_to")
        ]

    def __str__(self):
        return f'Пользователь: {self.user}, роль: {self.role}'


class FunctionsDict(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    version = models.SmallIntegerField()

    class Meta:
        db_table = "functions_dict"
        verbose_name = "Справочник ролевых функций"
        verbose_name_plural = "Справочник ролевых функций"

    def __str__(self):
        return self.code


class RoleFunctions(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(RolesDict,
                             on_delete=models.CASCADE,
                             related_name='role_functions')
    function = models.ForeignKey(FunctionsDict,
                                 on_delete=models.CASCADE,
                                 related_name='role_functions')

    class Meta:
        db_table = "role_functions"
        verbose_name = "Ролевые функции"
        verbose_name_plural = "Ролевые функции"
        indexes = [
            models.Index(fields=["role"], name="idx_role_functions_role"),
            models.Index(fields=["function"], name="idx_role_functions_function")
        ]

    def __str__(self):
        return f'Роль: {self.role}, функция: {self.function}'



