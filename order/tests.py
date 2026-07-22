import pytest
from order.models.order import Order
from order.factories import OrderFactory, UserFactory
from order.serializers.order_serializer import OrderSerializer
from product.factories import ProductFactory

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