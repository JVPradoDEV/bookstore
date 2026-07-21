import pytest
from product.models.product import Product
from product.models.category import Category
from product.factories import ProductFactory, CategoryFactory

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

# Create your tests here.
