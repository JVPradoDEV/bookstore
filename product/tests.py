import pytest
from rest_framework import status
from product.models.product import Product
from product.models.category import Category
from product.factories import ProductFactory, CategoryFactory
from product.serializers.product_serializer import ProductSerializer
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_category_creation():
    category = CategoryFactory(title="Eletrônicos", slug="eletronicos")
    
    assert Category.objects.count() == 1
    assert category.title == "Eletrônicos"
    assert category.slug == "eletronicos"

@pytest.mark.django_db
def test_product_creation():
    product = ProductFactory(title="Notebook", price=5000)
    
    assert Product.objects.count() == 1
    assert product.title == "Notebook"
    assert product.price == 5000

@pytest.mark.django_db
def test_product_with_categories():
    category_1 = CategoryFactory(title="Tech")
    category_2 = CategoryFactory(title="Ofertas")
    
    product = ProductFactory(categories=(category_1, category_2))
    
    assert product.categories.count() == 2
    assert category_1 in product.categories.all()
    assert category_2 in product.categories.all()
    
    from product.serializers.product_serializer import ProductSerializer

@pytest.mark.django_db
def test_product_serializer():
    category = CategoryFactory(title="Tech", slug="tech")
    product = ProductFactory(title="Mouse", price=150, categories=(category,))
    
    serializer = ProductSerializer(product)
    
    assert serializer.data['title'] == "Mouse"
    assert serializer.data['price'] == 150
    assert serializer.data['categories'][0]['title'] == "Tech"

@pytest.mark.django_db
def test_category_viewset():
    client = APIClient()
    category = CategoryFactory(title="Livros", slug="livros")
    
    url = reverse('category-list', kwargs={'version': 'v1'}) 
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Livros"

@pytest.mark.django_db
def test_product_viewset():
    client = APIClient()
    product = ProductFactory(title="Clean Code", price=120)
    
    url = reverse('product-list', kwargs={'version': 'v1'})
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Clean Code"

# Create your tests here.
