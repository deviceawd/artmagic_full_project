from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from urllib.parse import urlparse, parse_qs
from django.core.serializers import serialize

from .models import (Products,
                     Category,
                     Attribute,
                     ProductAttribute,
                     ProductFilter,
                     FilterGroup,
                     Filter,
                     Manufacturer)

def add_to_cart(request):

    product_id = int(request.GET["id"])
    try:
        product = Products.objects.filter(pk=product_id)
        json_data = list(product.values('id', 'name', 'image', 'price'))[0]

        return JsonResponse(json_data, safe=False)
    except Products.DoesNotExist:
        return JsonResponse(status=404)


def parent_categories(request):
    products = Products.objects.order_by('-date_added')[:20].values('name', 'image', 'price', "pk")
    categories = Category.objects.filter(parent=None)
    return render(request, 'products/index.html', {'categories': categories, 'products': products})


def products_view(request):
    products = Products.objects.all()[:20].values('name', 'image', 'price')

    # Преобразование QuerySet в список для сериализации
    products_list = list(products)
    return JsonResponse(products_list, safe=False)




# def parent_categories(request):
#     parent_categories = Category.objects.filter(parent=None)
#     return render(request, 'parent_categories.html', {'parent_categories': parent_categories})


def sub_categories(request, slug):
    parent_category = get_object_or_404(Category, slug=slug)
    sub_categories = parent_category.children.all()
    products = Products.objects.filter(category_id=parent_category.pk)
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/category.html', {'parent_category': parent_category, 'sub_categories': sub_categories, 'page_obj': page_obj})


def sub_product(request, slug):
    count = 0
    parent_category = get_object_or_404(Category, slug=slug)

    """products это все товары выбранной категории включительно"""
    descendants = parent_category.get_descendants(include_self=True)
    category_ids = [descendant.pk for descendant in descendants]
    products = Products.objects.filter(category_id__in=category_ids)
    product = Products.objects.filter(category_id=Category.objects.get(slug=slug).pk)

    """Блок фильтров"""
    products_ids = products.values_list("pk", flat=True)
    product_filters = ProductAttribute.objects.filter(
        product__in=products_ids).distinct()  # product_filters это все отфильтрованые продукты у которых есть фильтра
    product_filters_ids = product_filters.values_list("attribute_id", flat=True)
    filters = Attribute.objects.filter(pk__in=product_filters_ids)  # filters это фильтра всех выведенных продуктов
    product_text = product_filters.values_list("attribute_id", "text")

    """Пагинация"""
    paginator = Paginator(product, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    manufacturer = Manufacturer.objects.filter(products__category=parent_category).distinct()
    for el in manufacturer:
        print('--------------------', el)
    return render(request, 'products/catalog.html',
                  {
                      'product_text': product_text,
                      'filters': filters,
                      'products': products,
                      'product': product,
                      'parent_category': parent_category,
                      'page_obj':page_obj,
                      'manufacturer': manufacturer
                  }
                  )


def detail(request, slug):
    product = Products.objects.filter(slug=slug).first()
    att = ProductAttribute.objects.filter(product_id=product.pk)
    print(att, '||||||||||||||||||||||||||||||||||')

    return render(request, 'products/product.html', {'product': product, 'att': att})

