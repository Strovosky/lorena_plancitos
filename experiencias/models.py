from django.db.models import Model, CharField, DateTimeField, TextField, ImageField
from django.utils.translation import gettext_lazy as _
from PIL import Image

# Create your models here.

class Experiencia(Model):
    """Este modelo es el diseño para los planes que se ofreceran a la gente"""

    OPCIONES_ESTADOS = [
        ('ACTIVO', 'activo'),
        ('FINALIZADO', 'finalizado'),
        ('CANCELADO', 'cancelado')
    ]

    titulo = CharField(_('título'), max_length=150)
    estado = CharField(_('estado'), choices=OPCIONES_ESTADOS, max_length=11)
    descripcion = TextField(_('descripción'), max_length=600, blank=True, null=True)
    fecha_inicio = DateTimeField(_('fecha de inicio'))
    fecha_termina = DateTimeField(_('fecha de terminación'))
    ciudad = CharField(_('ciudad'), max_length=100)
    direccion = CharField(_('dirección'), max_length=200, blank=True, null=True)
    establecimiento = CharField(_('establecimiento'), max_length=150, blank=True, null=True)
    foto = ImageField(_('foto'), default='experiencia_generica.jpg', upload_to='imagenes_experiencias')

    def __str__(self):
        return f'{self.__class__.__name__}: {self.id} - {self.titulo}'

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        imagen = Image.open(self.foto.path)

        if imagen.width > 800 and imagen.height > 500:
            max_dimensiones = (800,500) #(width, height)
            imagen.thumbnail(max_dimensiones)
            imagen.save(self.foto.path)


