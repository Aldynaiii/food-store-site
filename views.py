import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.apps import apps
from django.db.models import Q
from .forms import RegisterForm, LoginForm, OrderForm 
from django.contrib.auth.decorators import login_required
from .models import Products, Orders, CartItem 


def register(request):
    Users = apps.get_model('store', 'Users')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['login']
            
            if Users.objects.filter(login=login_input).exists():
                form.add_error('login', 'Пользователь с таким логином уже существует')
                return render(request, 'store/register.html', {'form': form})
                
            Users.objects.create(
                login=login_input,
                password_hash=form.cleaned_data['password'],
                full_name=form.cleaned_data.get('full_name', 'Новый покупатель'),
                role='user',
                phone=form.cleaned_data.get('phone', ''),
                email=form.cleaned_data.get('email', '')
            )
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    Users = apps.get_model('store', 'Users')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['login']
            password = form.cleaned_data['password']
            
            if login_input == 'Admin' and password == 'KorokNET':
                request.session['user_id'] = 9999  # Выдаем фиксированный ID для админа
                request.session['user_login'] = 'Admin'
                request.session['user_role'] = 'admin'
                messages.success(request, 'Вы успешно вошли как Администратор!')
                return redirect('/')
                
            try:
                user = Users.objects.get(login=login_input)
            
                if password == user.password_hash:
                    request.session['user_id'] = user.id
                    request.session['user_login'] = user.login
                    request.session['user_role'] = user.role
                    return redirect('/')
                else:
                    form.add_error(None, 'Неверный логин или пароль')
            except Users.DoesNotExist:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def create_order(request):
    if not request.session.get('user_id'):
        return redirect('login')
        
    Orders = apps.get_model('store', 'Orders')
    OrderItems = apps.get_model('store', 'OrderItems')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            delivery_date = form.cleaned_data['delivery_date']
            payment_method = form.cleaned_data['payment_method']
            
            total = product.price * Decimal(quantity)
            random_number = f"ORD-{str(uuid.uuid4().hex[:6].upper())}"
            
            order = Orders(
                user_id=request.session['user_id'],
                order_number=random_number,
                delivery_date=delivery_date,
                status='Новый',
                total_amount=total,
                payment_method=payment_method
            )
            order.save()
            
            OrderItems.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
            return redirect('my_orders')
    else:
        form = OrderForm() 
        return render(request, 'store/create_order.html', {'form': form})

def my_orders(request):
    if not request.session.get('user_id'):
        return redirect('login')
    Orders = apps.get_model('store', 'Orders')
    
    orders = Orders.objects.filter(user_id=request.session['user_id'])
    return render(request, 'store/my_orders.html', {'orders': orders})

def index(request):
    Products = apps.get_model('store', 'Products')
    Points = apps.get_model('store', 'DeliveryPoints')
    
    category_name = request.GET.get('category')
    products = Products.objects.all()
    points = Points.objects.all()
    
    if category_name and category_name != 'Все продукты':
        
        if category_name == 'Moloko' or category_name == 'Молоко':
            products = products.filter(
                Q(name__icontains='молоко') | 
                Q(name__icontains='сыр') | 
                Q(name__icontains='кефир') | 
                Q(name__icontains='йогурт') | 
                Q(name__icontains='творог') | 
                Q(name__icontains='сметана') |
                Q(name__icontains='ряженка')
            )
        
        elif category_name == 'Хлеб':
            products = products.filter(
                Q(name__icontains='хлеб') | 
                Q(name__icontains='батон') | 
                Q(name__icontains='булоч') | 
                Q(name__icontains='выпеч') |
                Q(name__icontains='бородинск')
            )
        
        elif category_name == 'Колбасы':
            products = products.filter(
                Q(name__icontains='колбас') | 
                Q(name__icontains='сосиск') | 
                Q(name__icontains='мясо') | 
                Q(name__icontains='ветчин') |
                Q(name__icontains='докторская')
            )
        
        elif category_name == 'Масло':
            products = products.filter(
                Q(name__icontains='масло') | 
                Q(name__icontains='маргарин')
            )
        
        elif category_name == 'Бакалея':
            products = products.filter(
                Q(name__icontains='яйца') |
                Q(name__icontains='макарон') |
                Q(name__icontains='рис') |
                Q(name__icontains='гречка') |
                Q(name__icontains='сахар') |
                Q(name__icontains='мука') |
                Q(name__icontains='соль')
            )
        
        elif category_name == 'Напитки':
            products = products.filter(
                Q(name__icontains='чай') |
                Q(name__icontains='кофе') |
                Q(name__icontains='сок') |
                Q(name__icontains='вода')
            )
        
        elif category_name == 'Сладости':
            products = products.filter(
                Q(name__icontains='печенье') |
                Q(name__icontains='вафли') |
                Q(name__icontains='конфеты') |
                Q(name__icontains='шоколад') |
                Q(name__icontains='мороженое')
            )
       
        elif category_name == 'Заморозка':
            products = products.filter(
                Q(name__icontains='пельмени') |
                Q(name__icontains='вареники') |
                Q(name__icontains='заморожен')
            )

    return render(request, 'store/index.html', {
        'products': products, 
        'points': points, 
        'selected_category': category_name
    })

def leave_feedback(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    Users = apps.get_model('store', 'Users')
    Orders = apps.get_model('store', 'Orders')
    Products = apps.get_model('store', 'Products')
    Feedbacks = apps.get_model('store', 'Feedbacks')
    
    user = get_object_or_404(Users, id=user_id)
    order = get_object_or_404(Orders, id=order_id, user_id=user.id)
    
    if order.status != 'Готов':
        messages.error(request, "Вы не можете оставить отзыв. Заказ еще не завершен!")
        return redirect('my_orders')
        
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        product_id = request.POST.get('product_id')
        
        if not rating:
            messages.error(request, "Пожалуйста, поставьте оценку!")
            return redirect('my_orders')
            
        product = get_object_or_404(Products, id=product_id)
        
        Feedbacks.objects.create(
            user=user,
            product=product,
            order=order,
            rating=int(rating),
            comment=comment
        )
        messages.success(request, "Отзыв успешно добавлен!")
        return redirect('my_orders')
        
    return render(request, 'store/reviews.html', {'order': order})

def product_detail(request, product_id):
    Products = apps.get_model('store', 'Products')
    product = get_object_or_404(Products, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    Orders = apps.get_model('store', 'Orders')
    user_orders = Orders.objects.filter(user_id=request.session['user_id']).order_by('-id')
    
    return render(request, 'store/profile.html', {'orders': user_orders})


def add_to_cart(request, product_id):
    user_id = request.session.get('user_id') 
    if not user_id:
        return redirect('login')  
        
    from django.apps import apps
    ProductsModel = apps.get_model('store', 'Products')
    CartItemModel = apps.get_model('store', 'CartItem')
        
    product_obj = get_object_or_404(ProductsModel, id=product_id)
    cart_item, created = CartItemModel.objects.get_or_create(
        user_id=user_id, 
        products=product_obj
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('index')


def cart_detail(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Перенаправляем на ТВОЙ url login

    from django.apps import apps
    CartItemModel = apps.get_model('store', 'CartItem')
    OrdersModel = apps.get_model('store', 'Orders')

    cart_items = CartItemModel.objects.filter(user_id=user_id)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        pickup_point_address = request.POST.get('pickup_point')
        
        # Получаем модель точек выдачи
        PickupPointsModel = apps.get_model('store', 'PickupPoints')
        
        # Ищем строго по полю address, которое точно есть в базе данных
        pickup_point_obj = PickupPointsModel.objects.filter(address=pickup_point_address).first()
        
        # Если почему-то не нашли, берем самый первый пункт выдачи из базы
        if not pickup_point_obj:
            pickup_point_obj = PickupPointsModel.objects.first()
        import uuid  # Подключаем генератор уникальных кодов

        for item in cart_items:
            order = OrdersModel()
            order.user_id = user_id
            order.pickup_point = pickup_point_obj
            order.status = "Новый"
            
            # АВТОМАТИЧЕСКИЙ УНИКАЛЬНЫЙ НОМЕР ЗАКАЗА
            # Берем первые 6 символов случайного UUID и переводим в верхний регистр
            random_code = str(uuid.uuid4()).split('-')[0][:6].upper()
            
            if hasattr(order, 'order_number'):
                order.order_number = f"ORD-{random_code}"
            elif hasattr(order, 'number'):
                order.number = f"ORD-{random_code}"
            
            # Проверяем, как называется поле товара в Orders
            if hasattr(order, 'product'):
                order.product = item.products
            elif hasattr(order, 'products'):
                order.products = item.products
                
            # Проверяем, как называется поле количества в Orders
            if hasattr(order, 'quantity'):
                order.quantity = item.quantity
            elif hasattr(order, 'count'):
                order.count = item.quantity
            
            # Рассчитываем сумму
            if hasattr(order, 'total_amount'):
                order.total_amount = item.quantity * item.products.price
            elif hasattr(order, 'total_price'):
                order.total_price = item.quantity * item.products.price
                
            order.save()

        cart_items.delete()
        return redirect('my_orders')

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def remove_from_cart(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Перенаправляем на ТВОЙ url login

    from django.apps import apps
    CartItemModel = apps.get_model('store', 'CartItem')
    
    cart_item = get_object_or_404(CartItemModel, id=item_id, user_id=user_id)
    cart_item.delete()
    return redirect('cart_detail')

def add_review(request, product_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')  # Если пользователь не вошел, отправляем на авторизацию

        from django.apps import apps
        from django.shortcuts import get_object_or_404, redirect
        
        ProductsModel = apps.get_model('store', 'Products')
        FeedbackModel = apps.get_model('store', 'Feedback')  # Твоя модель отзывов из модели базы данных
        
        product_obj = get_object_or_404(ProductsModel, id=product_id)
        text = request.POST.get('text')
        
        if text:
            feedback = FeedbackModel()
            feedback.product = product_obj
            
            # Проверяем, как называется поле текста в твоей модели feedbacks
            if hasattr(feedback, 'comment'):
                feedback.comment = text
            elif hasattr(feedback, 'text'):
                feedback.text = text
                
            # Проверяем поле пользователя
            if hasattr(feedback, 'user_id'):
                feedback.user_id = user_id
                
            feedback.save()
            
    return redirect('product_detail', product_id=product_id)

def add_review(request, product_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        from django.apps import apps
        from django.shortcuts import get_object_or_404, redirect
        
        ProductsModel = apps.get_model('store', 'Products')
        FeedbackModel = apps.get_model('store', 'Feedbacks')  
        
        product_obj = get_object_or_404(ProductsModel, id=product_id)
        text = request.POST.get('text')
        
        if text:
            feedback = FeedbackModel()
            feedback.product = product_obj
            feedback.user_id = user_id 
            feedback.comment = text
            feedback.rating = 5
            

            
            if hasattr(feedback, 'comment'):
                feedback.comment = text
            elif hasattr(feedback, 'text'):
                feedback.text = text
                
            if hasattr(feedback, 'user_id'):
                feedback.user_id = user_id
                
            feedback.save()
            
   
    return redirect(request.META.get('HTTP_REFERER', '/'))