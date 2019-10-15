# coding: utf-8
from io import StringIO

from django.core import validators
from django.core.mail import EmailMessage
from django.db import models
from django.contrib.auth import models as auth_models
from django.db.models import Q
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import csv


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

    def get_csv(self):
        with StringIO() as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
            fields = ["product", "units", "client_id", "client_first_name", "client_last_name", "client_email",
                      "line_price"]
            writer.writerow(fields)

            for line in self.lines.all():
                writer.writerow([
                    line.product.name,
                    line.units,
                    self.client.pk,
                    self.client.first_name,
                    self.client.last_name,
                    self.client.email,
                    line.total
                ])
            return csv_file.getvalue()

    def send_email(self):
        email = EmailMessage(
            subject="[Bernini Shop] New order #{0}".format(self.pk),
            body=render_to_string('mails/new_order.txt', {"order": self}),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[
                u.email for u in auth_models.User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
            ]
        )
        email.attach('order.csv', self.get_csv(), 'text/csv')
        email.send(fail_silently=True)

    def __str__(self):
        return "Order #{id}. {price}€".format(id=self.pk, price=self.total_price)

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
