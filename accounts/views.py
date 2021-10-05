from carts.models import Cart, CartItem
from django.contrib import messages, auth
from accounts.models import Account, UserProfile
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm, forgotPasswordForm
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
import requests
from orders.models import Order, OrderProduct
from .forms import RegistrationForm, UserForm, UserProfileForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name            = form.cleaned_data['name']
            surname         = form.cleaned_data['surname']
            phone_number    = form.cleaned_data['phone_number']
            password        = form.cleaned_data['password']

            user = Account.objects.create_user(name = name, surname=surname, phone_number = phone_number, password = password)
            user.save()

            #Create User Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()


            messages.success(request, 'Регистрация успешна')
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        user = auth.authenticate(phone_number=phone_number, password = password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list= []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

                    #for item in cart_item:
                    #    item.user=user
                    #    item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request, 'Успешный вход в систему')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect(dashboard)
        else:
            messages.error(request, 'Неверные логин или пароль')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Успешный выход из системы')
    return redirect('login')


def forgotPassword(request):
    form = forgotPasswordForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Спасибо за обращение в нашу компанию. Мы ответим Вам в ближайшее время.')
        return redirect('forgotPassword')
    context = {
        'form': form
    }
    return render(request, 'accounts/forgotPassword.html', context)

@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered = True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id = request.user.id)

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,

    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = Account.objects.get(name__exact = request.user.name)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Пароль успешно обновлен')
                return redirect('change_password')
            else:
                messages.error(request, 'Пожалуйста, введите действующий пароль')
                return redirect('change_password')
        else:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')



@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number = order_id)
    order = Order.objects.get(order_number = order_id)
    subtotal = 0
    delivery_fee = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
        if subtotal > 800:
            delivery_fee = 0
        else:
            delivery_fee = 150
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
    }
    return render(request, 'accounts/order_detail.html', context)