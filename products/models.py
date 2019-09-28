from django.db import models
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=125, blank=False, null=False, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Price"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ('name', )
