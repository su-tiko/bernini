# coding: utf-8
from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _


class Order(models.Model):
    client = models.ForeignKey(auth_models.User, on_delete=models.PROTECT, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)

    products = models.ManyToManyField('products.Product', through='OrderLine', related_name='orders')

    @property
    def total_price(self):
        return sum([line.total for line in self.lines.all()])

    @property
    def total_items(self):
        return sum([line.units for line in self.lines.all()])

    def __str__(self):
        return "Order #{id}. {price}€".format(id=self.pk, price=self.total_price)

    def send_email(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, send_email=True):

        if self.pk is None and send_email:
            self.send_email()

        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('created',)


class OrderLine(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='lines', verbose_name=_('Order'))

    product = models.ForeignKey('products.Product',
                                on_delete=models.PROTECT,
                                related_name='order_lines',
                                verbose_name=_('Product'))

    units = models.PositiveIntegerField(default=1,
                                        validators=[validators.MinValueValidator(1)],
                                        verbose_name=_('Units'))

    @property
    def total(self):
        return self.units * self.product.price

    def __str__(self):
        return '{units}x {product}'.format(units=self.units, product=self.product.name)

    class Meta:
        verbose_name = 'Order line'
        verbose_name_plural = 'Order lines'
