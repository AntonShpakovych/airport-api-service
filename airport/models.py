from django.core.exceptions import ValidationError
from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=30)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        related_name="airplanes",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["name"]

    @property
    def capacity(self) -> int:
        return self.seats_in_row * self.rows

    def __str__(self) -> str:
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=30)
    closest_big_city = models.CharField(max_length=15)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        related_name="sources",
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Airport,
        related_name="destinations",
        on_delete=models.CASCADE
    )
    distance = models.IntegerField()

    class Meta:
        ordering = ["source"]

    @staticmethod
    def validate_source_destination(source, destination, error_to_raise):
        if source == destination:
            raise error_to_raise(
                "Destination can't be the same with source"
            )

    def clean(self):
        super().clean()
        Route.validate_source_destination(
            self.source,
            self.destination,
            ValidationError
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)


class Crew(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    class Meta:
        ordering = ["first_name"]

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        related_name="flights",
        on_delete=models.CASCADE
    )
    airplane = models.ForeignKey(
        Airplane,
        related_name="flights",
        on_delete=models.CASCADE
    )
    crews = models.ManyToManyField(
        Crew,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["departure_time"]
