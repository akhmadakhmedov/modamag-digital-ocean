from store.models import Cover, Product, ProductGallery, ReviewRating
from django.shortcuts import render
from store.models import Product, Cover
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def home(request):
    popular_products = Product.objects.all().filter(is_popular=True).order_by('created_date')
    newarrived_products = Product.objects.all().filter(is_newarrived = True).order_by('created_date')
    recommended_products = Product.objects.all().filter(is_recommended = True).order_by('created_date')
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    covers                  = Cover.objects.all()

    # Get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id, status=True)
    context = {
        'popular_products': popular_products,
        'newarrived_products': newarrived_products,
        'recommended_products': recommended_products,
        'covers': covers,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)