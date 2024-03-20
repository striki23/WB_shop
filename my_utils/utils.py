import os
from uuid import uuid4
from django.core.validators import ValidationError


def validate_image(img_file):
    """
    Проверка размера файла с изображением.
    """
    filesize = img_file.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {megabyte_limit} МБ.')


def get_file_path(instance, filename):
    #  TODO: Здесь Вы явно не используете, а другие части Django,
    #   могут ожидать или использовать этот аргумент
    expansion = filename.split('.')[-1]
    new_filename = f'{uuid4()}.{expansion}'
    return os.path.join('shop/', new_filename)
