from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Airplane(models.Model):
    name = models.CharField(max_length=30)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        related_name="airplanes",
        on_delete=models.CASCADE
    )


class Airport(models.Model):
    name = models.CharField(max_length=30)
    closest_big_city = models.CharField(max_length=15)


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
    distance = models.IntegerField


class Crew(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        related_name="flights",
        on_delete=models.CASCADE,
    )
    airplane = models.ForeignKey(
        Airplane,
        related_name="flights",
        on_delete=models.CASCADE
    ),
    crews = models.ManyToManyField(
        Crew,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
