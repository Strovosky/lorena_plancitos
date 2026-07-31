from django.db.models import Model, CharField, DateTimeField, TextField, ImageField
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from .validators import validar_tamaño_archivo
from PIL import Image
import os
from io import BytesIO
from .validators import (
    num_peso_max,
    peso_maximo_if_ok,
    peso_minimo_if_ok,
    foto_alto_min,
    foto_ancho_min,
    dimensiones_min,
    validar_min_dimension,
    validar_max_dimension
    )

class Experiencia(Model):
    """Este modelo es el diseño para los planes que se ofreceran a la gente"""

    OPCIONES_ESTADOS = [
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado')
    ]

    titulo = CharField(_('título'), max_length=150)
    estado = CharField(_('estado'), choices=OPCIONES_ESTADOS, max_length=11)
    descripcion = TextField(_('descripción'), max_length=600, blank=True, null=True)
    fecha_inicio = DateTimeField(_('fecha de inicio'))
    fecha_termina = DateTimeField(_('fecha de terminación'))
    ciudad = CharField(_('ciudad'), max_length=100)
    direccion = CharField(_('dirección'), max_length=200, blank=True, null=True)
    establecimiento = CharField(_('establecimiento'), max_length=150, blank=True, null=True)
    foto = ImageField(
        _('foto'),
        default='experiencia_generica.webp',
        upload_to='imagenes_experiencias',
        validators=[validar_tamaño_archivo, validar_min_dimension, validar_max_dimension],
        help_text=_(f'El archivo no puede pesar más de {num_peso_max}.')
        )

    def __str__(self):
        return f'{self.__class__.__name__}: {self.id} - {self.titulo}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.foto and self.foto.name != 'experiencia_generica.webp': # Si la foto existe y no es la generica
            try:
                imagen = Image.open(self.foto.path)
                necesita_procesar = False
                quality = 100

                # Si la foto es mas grande de lo necesario, procesala a dimensiones aceptables maximas
                if imagen.width > foto_ancho_min or imagen.height > foto_alto_min:
                    necesita_procesar = True

                # Si la foto pesa mucho a pesar de estar en dimensiones ideales, procesala para bajarle calidad y peso
                if self.foto.size > peso_minimo_if_ok:
                    if self.foto.size > peso_maximo_if_ok:
                        quality = 75
                    elif self.foto.size > peso_minimo_if_ok:
                        quality = 85
                    else:
                        quality = 90
                    necesita_procesar = True

                # Si la imagen es un cuadrado, queremos volverlo 
                if self.foto.width == self.foto.height:
                    imagen = imagen.resize(dimensiones_min, Image.Resampling.LANCZOS)
                    
                if necesita_procesar:
                    imagen.thumbnail(dimensiones_min, Image.Resampling.LANCZOS) #dimensiones_min es (1600*1000)

                    buffer = BytesIO()
                    imagen.save(buffer, format='WEBP', quality=quality)
                    buffer.seek(0)

                    # Obtengamos el nombre sin el path
                    # Porque self.foto.name me da el nombre con el path 'experiencias/la_foto.webp'
                    nombre_base = os.path.basename(self.foto.name)
                    nombre, ext = os.path.splitext(nombre_base)

                    # Si la foto vieja que se haya subido aun existe, borrala
                    path_foto_vieja = self.foto.path

                    self.foto.save(content=ContentFile(buffer.read()), name=f'{nombre}.webp', save=False)
                    super().save(*args, **kwargs)

                    if ext.lower() != '.webp' or path_foto_vieja != self.foto.path:
                        os.remove(path_foto_vieja)
                                 
            except Exception as e:
                RuntimeError(_(f'Hubo un error al procesar la foto de la experiencia {self.id}'))


