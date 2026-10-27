from django.db import models

class Users(models.Model):
    login = models.CharField(max_length=50, unique=True, verbose_name="Логин")
    password_hash = models.CharField(max_length=200, verbose_name="Хэш пароля")
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.CharField(max_length=100, verbose_name="Email")
    role = models.CharField(max_length=20, default='user', verbose_name="Роль")

    class Meta:
        db_table = 'users'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.full_name

class Products(models.Model):
    article = models.CharField(max_length=20, unique=True, verbose_name="Артикул")
    name = models.CharField(max_length=100, verbose_name="Наименование товара")
    unit = models.CharField(max_length=20, verbose_name="Единица измерения")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    supplier = models.CharField(max_length=100, blank=True, null=True, verbose_name="Поставщик")
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name="Производитель")
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name="Категория товара")
    discount = models.IntegerField(default=0, blank=True, null=True, verbose_name="Действующая скидка")
    stock = models.IntegerField(default=0, verbose_name="Количество на складе")
    description = models.TextField(blank=True, null=True, verbose_name="Описание товара")
    image_url = models.CharField(max_length=200, blank=True, null=True, verbose_name="Фото")

    class Meta:
        db_table = 'products'
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

class PickupPoints(models.Model):
    address = models.CharField(max_length=200, verbose_name="Адрес пункта")

    class Meta:
        db_table = 'pickuppoints'
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"

    def __str__(self):
        return self.address

class DeliveryPoints(models.Model):
    address = models.CharField(max_length=255, verbose_name="Адрес пункта выдачи")

    class Meta:
        db_table = 'deliverypoints'
        verbose_name = "Пункт доставки"
        verbose_name_plural = "Пункты доставки"

    def __str__(self):
        return self.address

class Orders(models.Model):
    
    STATUS_NEW = 'Новый'
    STATUS_PROCESSING = 'В обработке'
    STATUS_DONE = 'Готов'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новый'),
        (STATUS_PROCESSING, 'В обработке'),
        (STATUS_DONE, 'Готов'),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserId', verbose_name="Пользователь")
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заказа")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="Дата доставки")
    pickup_point = models.ForeignKey(PickupPoints, on_delete=models.SET_NULL, null=True, db_column='PickupPointId', verbose_name="Пункт выдачи")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name="Статус")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    payment_method = models.CharField(max_length=30, blank=True, null=True, verbose_name="Способ оплаты")

    class Meta:
        db_table = 'orders'
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.id} ({self.status})"

class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='OrderId', verbose_name="Заказ")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='ProductId', verbose_name="Продукт")
    quantity = models.IntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        db_table = 'orderitems'
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Детали заказов"

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class Feedbacks(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserId', verbose_name="Пользователь")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='ProductId', verbose_name="Товар")
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='OrderId', verbose_name="Заказ",null=True, blank=True)
    rating = models.IntegerField(verbose_name="Оценка")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = 'feedbacks'
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.login} на {self.product.name}" 
    
class CartItem(models.Model):
    user_id = models.IntegerField(verbose_name="ID пользователя")
    products = models.ForeignKey('Products', on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def total_price(self):
        return self.products.price * self.quantity

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"   

    