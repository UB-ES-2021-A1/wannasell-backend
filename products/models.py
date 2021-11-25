from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


def category_gray_image_path(instance, filename):
    return 'images/categories/gray/{0}/{1}'.format(instance.name, filename)


def category_green_image_path(instance, filename):
    return 'images/categories/green/{0}/{1}'.format(instance.name, filename)


def image_path(instance, filename):
    return 'images/products/{0}/{1}'.format(instance.product.id, filename)


class Category(models.Model):

    class CategoryValues(models.TextChoices):
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

    name = models.CharField(
        max_length=2,
        choices=CategoryValues.choices,
        default=CategoryValues.OTROS
    )
    grayscale_image = models.ImageField(upload_to=category_gray_image_path, blank=False)
    green_image = models.ImageField(upload_to=category_green_image_path, blank=False)

    def __str__(self):
        return self.get_name_display()

class Product(models.Model):
    title = models.TextField(max_length=500, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte='0'), name='price_gte_0'),
        ]


class Image (models.Model):
    product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path)
