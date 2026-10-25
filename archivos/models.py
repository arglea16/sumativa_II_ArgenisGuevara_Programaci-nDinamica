import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


def almacen():
    return FileSystemStorage(location=settings.PRIVATE_ROOT)


def ruta_usuario(instance, filename):
    return f'{instance.propietario_id}/{uuid.uuid4().hex}_{filename}'


class Archivo(models.Model):
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='archivos')
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to=ruta_usuario, storage=almacen)
    tamano = models.BigIntegerField(default=0)
    subido = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    compartido = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
