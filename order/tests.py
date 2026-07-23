import pytest
from order.models.order import Order
from order.factories import OrderFactory, UserFactory
from order.serializers.order_serializer import OrderSerializer
from product.factories import ProductFactory
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


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
    product = ProductFactory(title="Caneta", price=10)
    order = OrderFactory(product=(product,))
    
    url = reverse('order-list', kwargs={'version': 'v1'})
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['total'] == 10