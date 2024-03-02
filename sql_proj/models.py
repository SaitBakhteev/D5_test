from django.db import models
from datetime import datetime
from time import timezone



class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='ProductOrder')

    def get_duration(self):
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60

    def finish_order(self):
        self.time_out=datetime.now()
        self.complete=True
        self.save()



class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, val):
        self._amount =int(val) if val>=0 else 0
        self.save()

    def product_sum(self):
        self.product.price * self.amount


class Author(models.Model):
    full_name = models.CharField(max_length=64)
    name = models.CharField(null=True, max_length=64)

apple=Product.objects.create(name='Apple',price=100)
twisted_pair=Product.objects.create(name='Twisted Pair', price=200, composition='3 m')
keyboard=Product.objects.create(name='Keyboard', price=50)


# Create your models here.
