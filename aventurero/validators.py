from django.core.exceptions import ValidationError


num_peso_max = 4
peso_maximo = num_peso_max * 1024 * 1024

ancho_max, alto_max = 4096, 4096

def validar_peso(valor):
    """Este valida el peso maximo de la foto de perfil"""
    if valor.size > peso_maximo:
        ValidationError(f'El peso del archivo es muy grande. El máximo de de {num_peso_max}.')

def validar_dimesiones_max(valor):
    """Este validara las dimensiones maximas que puede tener una foto de perfil"""
    if valor.width > ancho_max or valor.height > alto_max:
        ValidationError(f'La foto tiene dimensiones muy grandes, las dimenciones maximas son {ancho_max}x{alto_max}.')



