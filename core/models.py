from django.db import models
from django.db.models import Sum, F


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(wealthy=F(Sum('property__value')) > 500000)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()

    with_extras = PersonManager()

    def add_wealthy(self):
        return self.annotate(
            wealthy=F(Sum('property_value')) > 500000
        )

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Property(models.Model):
    street = models.CharField(max_length=128)
    suburb = models.CharField(max_length=50)
    STATE_OPTIONS = (
        ('WA', 'WA'),
        ('NT', 'NT'),
        ('QLD', 'QLD'),
        ('NSW', 'NSW'),
        ('VIC', 'VIC'),
        ('ACT', 'ACT'),
        ('TAS', 'TAS'),
        ('SA', 'SA'),
    )
    state = models.CharField(max_length=3, choices=STATE_OPTIONS)
    postcode = models.IntegerField()
    value = models.IntegerField(default=0)

    owner = models.ForeignKey('Person', null=True, on_delete=models.SET_NULL)

    @property
    def address(self):
        kwargs = {
            'street': self.street,
            'suburb': self.suburb,
            'state': self.state,
            'postcode': self.postcode,
        }
        return "{street}, {suburb} {state} {postcode}".format(**kwargs)

    def __str__(self):
        return self.street
