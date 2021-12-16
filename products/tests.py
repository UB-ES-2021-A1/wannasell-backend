import tempfile

from django.test import TestCase
import PIL
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from products.models import Product, Category, Image

# Create your tests here.


class ProductsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = Category.objects.create(name='MO', grayscale_image='img.png', green_image='img.png')
        self.u = User.objects.create_user('testUser2', 'lennon@thebeatles.com', 'johnpassword')
        self.token = Token.objects.get_or_create(user=self.u)[0].__str__()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_products_succesfull(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        request = self.client.get('/api/v1/products/', format='json')
        self.assertEqual(request.status_code, 200)

    def test_get_empty_products(self):
        request = self.client.get('/api/v1/products/', format='json')
        self.assertEqual(request.status_code, 204)

    def test_get_products_by_category_fail(self):
        request = self.client.get("/api/v1/products/?category=MA", format='json')
        self.assertEqual(request.status_code, 204)

    def test_get_products_by_category_success(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        request = self.client.get("/api/v1/products/?category=MO", format='json')
        self.assertEqual(request.status_code, 200)

    def test_get_products_by_category_empty_success(self):
        request = self.client.get("/api/v1/products/?category=MO", format='json')
        self.assertEqual(request.status_code, 204)

    def test_get_category(self):
        request = self.client.get("/api/v1/products/categories/")
        self.assertEqual(request.status_code, 200)

    def test_post_product(self):
        data = {
            'title': 'Moto',
            'description': 'Una moto',
            'price': 12,
            'user': self.u,
            'category_name': 'MO'
        }
        request = self.client.post("/api/v1/products/", data)
        pord = Product.objects.filter(seller=self.u).first()
        assert request.status_code == 200
        assert request.data['id'] == pord.id
        self.assertEqual(request.status_code, 200)

    def test_patch_product(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()

        data = {
            'title': 'New title',
            'description': 'New description',
            'price': 2,
            'user': self.u,
            'category_name': 'CO',
            'sold': True
        }

        prod_id = (Product.objects.get(title='Title')).id
        url = "/api/v1/products/?id=" + str(prod_id)
        request = self.client.patch(url, data)
        prod = Product.objects.filter(seller=self.u).first()

        assert request.data['title'] == prod.title
        assert request.data['description'] == prod.description
        assert request.data['price'] == str(prod.price)
        assert request.data['category_name'] == prod.category.name
        assert request.data['sold'] == prod.sold
        self.assertEqual(request.status_code, 200)

    def test_patch_product_not_found(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()

        data = {
            'title': 'New title',
            'description': 'New description',
            'price': 2,
            'user': self.u,
            'category_name': 'CO'
        }

        url = "/api/v1/products/?id=3"
        request = self.client.patch(url, data)

        self.assertEqual(request.status_code, 404)

    def test_get_product_by_id(self):
        Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        request = self.client.get("/api/v1/products/?id=1", format='json')
        self.assertEqual(request.status_code, 200)

    def test_get_product_default_sold_false(self):
        Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        request = self.client.get("/api/v1/products/?id=1", format='json')
        assert not request.data[0]['sold']
        self.assertEqual(request.status_code, 200)

    def test_get_images_of_product(self):
        # Arrange
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        prod_id = (Product.objects.get(title='Title')).id
        Image.objects.create(product=p, image='fake1')
        Image.objects.create(product=p, image='fake2')

        # Act
        request = self.client.get("/api/v1/products/images/?id=" + str(prod_id), format='json')

        # Assert
        images = request.data
        assert len(images) == 2
        assert 'id' in images[0]
        assert 'image' in images[0]
        self.assertEqual(request.status_code, 200)

    def test_post_product_image_form(self):
        # Arrange
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        prod_id = (Product.objects.get(title='Title')).id
        url = "/api/v1/products/images/?id=" + str(prod_id)

        image = PIL.Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        # Act
        request = self.client.post(url, {'image': tmp_file}, format="multipart")

        # Assert
        self.assertEqual(request.status_code, 201)

    def test_post_product_image_id_not_provided(self):
        # Arrange
        url = "/api/v1/products/images/"

        image = PIL.Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        # Act
        request = self.client.post(url, {'image': tmp_file}, format="multipart")

        # Assert
        self.assertEqual(request.status_code, 400)

    def test_post_product_image_image_not_provided(self):
        # Arrange
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        prod_id = (Product.objects.get(title='Title')).id
        url = "/api/v1/products/images/?id=" + str(prod_id)

        # Act
        request = self.client.post(url, format="multipart")

        # Assert
        self.assertEqual(request.status_code, 400)

    def test_search_product_by_name(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        p2.save()
        url = "/api/v1/products/?search=Title"

        # Act
        request = self.client.get(url)
        assert request.data[0]['title'] == 'Title'

    def test_search_product_by_category(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        p2.save()
        url = "/api/v1/products/?category=" + self.c.name

        # Act
        request = self.client.get(url)
        assert request.data[0]['title'] == 'Title'
        assert len(request.data) == 2

    def test_search_product_by_title_and_category(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        p2.save()
        url = "/api/v1/products/?category=" + self.c.name + "&search=Title"

        # Act
        request = self.client.get(url)
        assert request.data[0]['title'] == 'Title'
        assert len(request.data) == 1

    def test_search_products_by_username(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        p2.save()
        url = "/api/v1/products/?username=testUser2"

        # Act
        request = self.client.get(url)
        assert request.data[0]['title'] == 'Title'
        assert len(request.data) == 2

    def test_search_empty_strings(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        p2.save()

        url = "/api/v1/products/?category=&search="

        # Act
        request = self.client.get(url)
        assert request.data[0]['title'] == 'Title'
        assert len(request.data) == 2

    def test_get_product_by_id(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.save()
        p2.save()

        url = "/api/v1/products/1/"

        # Act
        request = self.client.get(url)
        assert request.data['title'] == 'Title'
        assert request.data['description'] == 'Description'

    def test_delete_product_image(self):
        # Arrange
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()

        image = PIL.Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        url = "/api/v1/products/images/?id=" + str(p.id)
        self.client.post(url, {'image': tmp_file}, format="multipart")

        prod_image = Image.objects.filter(product=p).first()
        url = "/api/v1/products/images/?id=" + str(prod_image.id)

        # Act
        request = self.client.delete(url)

        # Assert
        self.assertEqual(request.status_code, 200)

    def test_delete_product_image_not_found(self):
        # Arrange
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()

        url = "/api/v1/products/images/?id=10"

        # Act
        request = self.client.delete(url)

        # Assert
        self.assertEqual(request.status_code, 404)

    def test_get_sold_products_no_products(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.save()

        url = "/api/v1/products/sold/?sold=True&seller=" + self.u.username
        request = self.client.get(url)
        assert request.data == []
        assert request.status_code == 204

    def test_get_sold_products(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.sold = True
        p.save()
        p2.save()
        url = "/api/v1/products/sold/?sold=True&seller=" + self.u.username
        request = self.client.get(url)
        assert request.data[0]['title'] == 'Title'
        assert request.status_code == 200

    def test_get_unsold_products_no_products(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p.sold = True
        p.save()
        url = "/api/v1/products/sold/?sold=False&seller=" + self.u.username
        request = self.client.get(url)
        assert request.data == []
        assert request.status_code == 204

    def test_get_unsold_products(self):
        p = Product.objects.create(title='Title', description='Description', price=1, seller=self.u, category=self.c)
        p2 = Product.objects.create(title='Pepe', description='Description', price=1, seller=self.u, category=self.c)
        p.sold = True
        p.save()
        p2.save()
        url = "/api/v1/products/sold/?sold=False&seller=" + self.u.username
        request = self.client.get(url)
        assert request.data[0]['title'] == 'Pepe'
        assert request.status_code == 200

    def test_get_sold_products_not_enough_args1(self):
        url = "/api/v1/products/sold/?sold=False"
        request = self.client.get(url)
        assert request.data == "Not enough arguments"
        assert request.status_code == 400

    def test_get_sold_products_not_enough_args2(self):
        url = "/api/v1/products/sold/?seller=" + self.u.username
        request = self.client.get(url)
        assert request.data == "Not enough arguments"
        assert request.status_code == 400
