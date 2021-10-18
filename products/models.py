from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    title = models.TextField(max_length=500, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Category(models.TextChoices):
        COCHES = 'CO', _('Coches')
        MOTOS = 'MO', _('Motos')
        MODA = 'MA', _('Moda y Accesorios')
        IMMOBILIARIA = 'IM', ('Immobiliaria')
        TVAUDIO = 'TV', _('TV, Audio y Foto')
        TELEFONIA = 'TE', _('Móviles y Telefonía')
        INFORMATICA = 'IE', _('Informática y Electrónica')
        DEPORTE = 'DO', _('Deporte y Ocio')
        BICICLETAS = 'BI', _('Bicicletas')
        CONSOLAS = 'CV', _('Consolas y Videojuegos')
        HOGAR = 'HJ', _('Hogar y Jardín')
        ELECTRODOMESTICOS = 'ED', _('Electrodomésticos')
        CULTURA = 'CU', _('Cine, Libros y Música')
        NINOS = 'NI', _('Niños y Bebés')
        COLECCIONISMO = 'CC', _('Coleccionismo')
        CONSTRUCCION = 'CT', _('Construcción y reformas')
        INDUSTRIA = 'IN', _('Industria y Agricultura')
        EMPLEO = 'EM', _('Empleo')
        SERVICIOS = 'SE', _('Servicios')
        OTROS = 'OT', _('Otros')

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.OTROS
    )


class Image (models.Model):
    product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)


