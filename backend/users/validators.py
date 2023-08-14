from django.core.exceptions import ValidationError


def validate_username(username):
    """Запрещает пользователям присваивать себе username me."""
    if username == 'me':
        raise ValidationError(
            'Использовать имя me запрещено'
        )
    return username
