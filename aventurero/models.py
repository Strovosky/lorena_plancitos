from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import EmailField, CharField, TextField, ImageField, DateTimeField, BooleanField
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .validators import validar_peso, validar_dimesiones_max
from PIL import Image

# Create your models here.

class MiManejadorUsuario(BaseUserManager):

    @staticmethod
    def validar_campos(c: str, u, t, n, a):
        print(c)

        if not c:
            raise ValueError(_('Debe proveer un correo electrónico.'))
        if not u:
            raise ValueError(_('Debe proveer un nombre de usuario.'))
        if not t:
            raise ValueError(_('Debe proveer un telefono.'))
        if not n:
            raise ValueError(_('Debe proveer un primer nombre.'))
        if not a:
            raise ValueError(_('Debe proveer un apellildo.'))

    def create_user(
            self,
            correo: str,
            usuario: str,
            nombre: str,
            apellido: str,
            telefono: str,
            password,
            **otros_campos
            ):

        self.validar_campos(
            c=correo,
            u=usuario,
            t=telefono,
            n=nombre,
            a=apellido)

        correo = self.normalize_email(correo)
        aventurero = self.model(correo=correo,
                             usuario=usuario.lower(),
                             nombre=nombre.lower(),
                             apellido=apellido.lower(),
                             telefono=telefono,
                             **otros_campos
                             )
        aventurero.set_password(password)
        aventurero.save()
        return aventurero

    def create_superuser(self, correo, usuario, nombre, apellido, telefono, password, **otros_campos):
        otros_campos.setdefault("is_staff", True)
        otros_campos.setdefault("is_active", True)
        otros_campos.setdefault("is_superuser", True)
        otros_campos.setdefault("is_admin", True)

        return self.create_user(correo, usuario, nombre, apellido, telefono, password, **otros_campos)


class Aventurero(AbstractBaseUser, PermissionsMixin):

    correo = EmailField(_('correo electrónico'), max_length=60, unique=True)
    usuario = CharField(_("nombre de usuario"), max_length=60, unique=True)
    fecha_registro = DateTimeField(_('fecha de registro'), auto_now_add=True)
    ultimo_login = DateTimeField(_('último login'), auto_now=True)
    is_admin = BooleanField(_('es administrador'), default=False)
    is_active = BooleanField(_('está activo'), default=False)
    is_staff = BooleanField(_('es staff'), default=False)
    is_superuser = BooleanField(_('es superusuario'), default=False)

    nombre = CharField(_('nombre'), max_length=100)
    apellido = CharField(_('apellido'), max_length=100)
    telefono = CharField(_('teléfono'), max_length=15, validators=[RegexValidator(r'^\d{10}$', 'El teléfono debe tener un máximo de 10 digitos.')])
    bio = TextField(max_length=500, null=True, blank=True, help_text="Cuénta un poco de ti.")
    motto = CharField(max_length=200, help_text="La frase que te define.", null=True, blank=True)
    profesion = CharField(_('profesión'), max_length=100, null=True, blank=True)
    foto = ImageField(_('foto'), default="default_imagen.png", validators=[validar_dimesiones_max, validar_peso], upload_to="imagenes_perfil")

    USERNAME_FIELD = "correo"

    # Fields required when creating a superuser
    REQUIRED_FIELDS = [
        "usuario",
        "nombre",
        "apellido",
        "telefono"
    ]

    objects = MiManejadorUsuario()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        imagen = Image.open(self.foto.path)

        if imagen.height > 300 and imagen.width > 300:
            max_dimensiones = (300,300)
            imagen.thumbnail(max_dimensiones)
            imagen.save(self.foto.path)


    def __str__(self):
        return f"{self.__class__.__name__}: {self.nombre} {self.apellido}"

    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

