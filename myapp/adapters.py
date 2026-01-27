from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError

class NoSignupAccountAdapter(DefaultAccountAdapter):
    """Адаптер для запрета самостоятельной регистрации"""
    
    def is_open_for_signup(self, request):
        """Полностью запрещаем самостоятельную регистрацию"""
        return False
    
    def clean_email(self, email):
        """Не требуем уникальный email"""
        return email
    
    def save_user(self, request, user, form, commit=True):
        """Сохраняем пользователя только через админку"""
        raise ValidationError("Регистрация разрешена только администратором")