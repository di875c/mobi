from django.db import models


class Currency(models.Model):
    date = models.fields.DateField(primary_key=True)
    eur = models.fields.DecimalField(name='EUR', max_digits=5, decimal_places=2)
    usd = models.fields.DecimalField(name='USD', max_digits=5, decimal_places=2)