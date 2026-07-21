import pytest
from order.models.order import Order
from order.factories import OrderFactory, UserFactory
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