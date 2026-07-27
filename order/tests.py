import pytest
import json
from order.models.order import Order
from order.factories import OrderFactory, UserFactory
from order.serializers.order_serializer import OrderSerializer
from product.factories import ProductFactory
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from product.factories import ProductFactory, CategoryFactory


@pytest.mark.django_db
def test_user_creation():
    user = UserFactory(username="joao_silva")
    
    assert user.username == "joao_silva"

@pytest.mark.django_db
def test_order_creation_without_products():
    order = OrderFactory()
    
    assert Order.objects.count() == 1
    assert order.user is not None
    assert order.product.count() == 0 

@pytest.mark.django_db
def test_order_with_products():
    product_1 = ProductFactory(title="Mouse")
    product_2 = ProductFactory(title="Teclado")
    
    order = OrderFactory(product=(product_1, product_2))
    
    assert Order.objects.count() == 1
    assert order.product.count() == 2
    assert product_1 in order.product.all()
    assert product_2 in order.product.all()

@pytest.mark.django_db
def test_order_serializer_calculates_total():
    product_1 = ProductFactory(title="Mouse", price=100)
    product_2 = ProductFactory(title="Teclado", price=250)
    
    order = OrderFactory(product=(product_1, product_2))
    
    serializer = OrderSerializer(order)
    
    assert serializer.data['total'] == 350
    assert len(serializer.data['product']) == 2

@pytest.mark.django_db
def test_order_viewset():
    client = APIClient()
    user = UserFactory()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    category = CategoryFactory(title='technology')
    product = ProductFactory(title='mouse', price=100, categories=(category,)) 
    order = OrderFactory(product=(product,))
    
    url = reverse('order-list', kwargs={'version': 'v1'})
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    
    response_data = response.json()
    
    assert response_data['results'][0]['product'][0]['title'] == product.title
    assert response_data['results'][0]['product'][0]['price'] == float(product.price)
    assert response_data['results'][0]['product'][0]['active'] == product.active

@pytest.mark.django_db
def test_create_order():
    client = APIClient()
    user = UserFactory()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    product = ProductFactory()
    data = {
        'products_id': [product.id],
        'user': user.id
    }
    
    url = reverse('order-list', kwargs={'version': 'v1'})
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    
    assert response.status_code == status.HTTP_201_CREATED