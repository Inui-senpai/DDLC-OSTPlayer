
python early:

    class UnknownImageFileType(Exception):
        def __str__(self):
            return "В предопределённом треке был обнаружен неизвестный тип изображения."
