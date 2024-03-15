from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from wb_shop_root.constants import MAX_IMAGE_SIZE, MIN_IMAGE_SIZE


class ProductTitleValidator(RegexValidator):
    message = 'Используйте буквы только латинского и русского алфавита'
    regex = r'[^a-zA-ZА-Яа-яЁё0-9,.%*() ]'
    inverse_match = True


class ProfileImageValidator(FileExtensionValidator):
    """
    Класс валидатора для проверки изображений, загружаемых в профиль
    пользователя.

    Проверяет, что файл является изображением в форматах JPEG, JPG или PNG,
    имеет размер не менее 500x500 и не более 1024x1024 пикселей и не превышает
    максимальный размер, определенный в настройках проекта.

    Аргументы:
    ---------
    * min_width - int, опционально. Минимальная ширина изображения.
    По умолчанию - {constants.MIN_IMAGE_SIZE} пикселей,
    заданное в настройках проекта.
    * min_height - int, опционально. Минимальная высота изображения.
    По умолчанию - {constants.MIN_IMAGE_SIZE}  пикселей.
    заданное в настройках проекта.
    * max_width - int, опционально. Максимальная ширина изображения.
    По умолчанию - {constants.MAX_IMAGE_SIZE} пикселей,
    заданное в настройках проекта.
    * max_height - int, опционально. Максимальная высота изображения.
    По умолчанию - {constants.MAX_IMAGE_SIZE} пикселей,
    заданное в настройках проекта.

    Поля:
    ---------
    * allowed_extensions (tuple): допустимые расширения файлов
    изображений.
    * message (str): текст сообщения об ошибке при невалидном файле.

    Методы:
    ---------
    * __init__: конструктор класса, принимающий опциональные параметры.
    * __call__: метод, вызываемый при проверке входного файла.
    """
    MAX_SIZE = MAX_IMAGE_SIZE * MAX_IMAGE_SIZE
    MIN_SIZE = MIN_IMAGE_SIZE
    allowed_extensions = ('jpg', 'jpeg', 'png')
    message = _(
        "Файл должен быть изображением в формате JPEG, JPG или PNG,"
        " и размером не менее 500x500 не более 1024x1024 пикселей."
    )

    def __init__(self, *args, **kwargs) -> None:
        """
        Конструктор класса.

        :param min_width: int, опционально. Минимальная ширина изображения.
        По умолчанию - {constants.MIN_IMAGE_SIZE} пикселей.
        :param min_height: int, опционально. Минимальная высота изображения.
        По умолчанию - {constants.MIN_IMAGE_SIZE}  пикселей.
        :param max_width: int, опционально. Максимальная ширина изображения.
        По умолчанию - {constants.MAX_IMAGE_SIZE} пикселей,
        заданное в настройках проекта.
        :param max_height: int, опционально. Максимальная высота изображения.
        По умолчанию - {constants.MAX_IMAGE_SIZE} пикселей,
        заданное в настройках проекта.
        """
        self.min_width = kwargs.pop('min_width', self.MIN_SIZE)
        self.min_height = kwargs.pop('min_height', self.MIN_SIZE)
        self.max_width = kwargs.pop('max_width', self.MAX_SIZE)
        self.max_height = kwargs.pop('max_height', self.MAX_SIZE)
        super().__init__(*args, **kwargs)

    def __call__(self, value) -> None:
        """
        Проверяет, что загруженный файл является изображением в формате
        JPEG, JPG или PNG, и что его размер не меньше заданных
        минимальных значений и не больше заданных максимальных значений.

        Если проверка не пройдена, выбрасывается исключение ValidationError
         с соответствующим сообщением.

        :param value: объект загруженного файла
        :type value: django.core.files.uploadedfile.InMemoryUploadedFile
        or django.core.files.uploadedfile.TemporaryUploadedFile
        :raises ValidationError: если файл не является изображением в формате
        JPEG, JPG или PNG, или если его размер меньше заданных минимальных
        значений или больше заданных максимальных значений
        :return: None
        """

        super().__call__(value)
        from PIL import Image

        with Image.open(value) as img:
            width, height = img.size

        if (width * height) > self.MAX_SIZE:
            raise ValidationError(
                _(f"Размер изображения не должен превышать {self.MAX_SIZE} байт.")
            )

        if width < self.min_width or height < self.min_height:
            raise ValidationError(self.message)

        if self.min_width and self.min_height:
            if width < self.min_width or height < self.min_height:
                raise ValidationError(
                    f"Минимальный размер изображения {self.min_width}x{self.min_height} пикселей."
                )

        if self.max_width and self.max_height:
            if width > self.max_width or height > self.max_height:
                raise ValidationError(
                    f"Максимальный размер изображения {self.max_width}x{self.max_height} пикселей."
                )
