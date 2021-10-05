from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.http import JsonResponse


def payments(request):
    # Get the order number from session
    order_no_Session = request.session.get('order_number')
    order = Order.objects.get(user=request.user,order_number=order_no_Session)
    order.is_ordered = True
    order.save()


    #Move the cart items to Order Product Table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        #orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of sold products
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart    
    CartItem.objects.filter(user=request.user).delete()

    #data = {
    #    'order_number': order.order_number,
    #    'transID': payment.payment_id,
    #}

    return redirect('/orders/order_complete?order_number='+order.order_number)


def place_order(request, total=0, quantity=0,):
    current_user = request.user

    #If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    delivery_fee = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    if total >799:
        delivery_fee = 0
    else:
        delivery_fee = 150
    grand_total = total + delivery_fee

    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.name = form.cleaned_data['name']
            data.surname = form.cleaned_data['surname']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            #data.payment_method = form.cleaned_data['payment_method']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.delivery_fee = delivery_fee
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            #Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            # Store order number in session
            request.session['order_number'] = order_number
            data.save()

            order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'delivery_fee': delivery_fee,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    #transID = request.GET.get('payment_id')
    
    #payment = Payment.objects.get(payment_id = transID)

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            #'transID': payment.payment_id,
            #'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

def dostavka(request):
    return render(request, 'orders/dostavka.html')

def paymentinfo(request):
    return render(request, 'orders/paymentinfo.html')

def aboutus(request):
    return render(request, 'orders/aboutus.html')

def refund(request):
    return render(request, 'orders/refund.html')

def rule(request):
    return render(request, 'orders/rule.html')


def faq(request):
    return render(request, 'orders/faq.html')