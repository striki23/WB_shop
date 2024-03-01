import os
from uuid import uuid4
from django.core.validators import ValidationError


# проверка размера файла с изображением
def validate_image(img_file):
    filesize = img_file.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {megabyte_limit} МБ.')


def get_file_path(instance, filename):
    # зачем здесь instance если мы его не используем
    expansion = filename.split('.')[-1]
    new_filename = f'{uuid4()}.{expansion}'
    return os.path.join('shop/', new_filename)
