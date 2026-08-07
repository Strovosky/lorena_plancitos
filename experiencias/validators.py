from django.core.exceptions import ValidationError

### VARIABLES DE LAS FOTOS ###

# Las dimensiones minimas y maximas de las fotos
foto_ancho_min, foto_alto_min, foto_ancho_max, foto_alto_max = 1600, 900, 4096, 4096
dimensiones_max = (foto_ancho_max,foto_alto_max) #(width, height)
dimensiones_min = (foto_ancho_min, foto_alto_min)

# El peso máximo de una foto, si se trata de subir por encima de este, el validador no te dejará.
num_peso_max = 3
peso_maximo = num_peso_max * 1024 * 1024 # El num_peso_max ens MB in bytes

# Si la imagen esta dentro de las dimensiones deseadas, que peso es valido que tenga
# peso_minimo_if_ok es el peso para redimensionar la imagen si se pasa de esto. quiality 85%
# peso_maximo_if_ok es el peso para redimensionar la imagen si se pasa de esto, pero quality 75%
peso_minimo_if_ok = 500 * 1024 # 500 KB
peso_maximo_if_ok = 1.5 * 1024 * 1024


### VARIABLES DEL PRECIO ###
precio_maximo = 5000000



def validar_tamaño_archivo(valor):
    if valor.size > peso_maximo:
        raise ValidationError(f'El archivo no puede exceder las {num_peso_max}MB.')

def validar_max_dimension(valor):
    if valor.width > foto_ancho_max and valor.height > foto_alto_max:
        raise ValidationError(f'Las dimensiones del archivo son muy grandes. El maximo es ({dimensiones_max}) y la imagen tiene ({valor.width}, {valor.height})')
    elif valor.height > foto_alto_max:
        raise ValidationError(f'El ancho de la imagen esta bien pero esta muy alta. El máximo es {foto_alto_max} y la imagen tiene {valor.height}')
    elif valor.width > foto_ancho_max:
        raise ValidationError(f'El alto de la imagen esta bien pero esta muy ancha. El máximo es {foto_ancho_max} y la imagen tiene {valor.width}')


def validar_min_dimension(valor):
    if valor.width < foto_ancho_min and valor.height < foto_alto_min:
        raise ValidationError(f'Las dimensiones del archivo son muy pequeñas. El minimo es ({dimensiones_min}) y la imagen tiene ({valor.width}, {valor.height})')
    elif valor.height < foto_alto_min:
        raise ValidationError(f'El ancho de la imagen esta bien pero esta muy baja. El minimo es {foto_alto_min} y la imagen tiene {valor.height}')
    elif valor.width < foto_ancho_min:
        raise ValidationError(f'El alto de la imagen esta bien pero esta muy angosta. El minimo es {foto_ancho_min} y la imagen tiene {valor.width}')

def validar_precio_maximo(valor):
    """Verifica que el precio de una experiencia no supere cierto limite"""
    if valor > precio_maximo:
        raise ValidationError(f'El valor de un plan no puede estar por encima de {precio_maximo}')
