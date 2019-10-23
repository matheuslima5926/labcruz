import datetime
from django.db import models
from django.utils import timezone

#CONSTANTS
CAMUNDONGO = 'CM'
RATO = 'RT'

ANIMAL_TYPES = [
    (CAMUNDONGO, 'Camundongo'),
    (RATO, 'Rato')
]


# Create your models here.
class Animal(models.Model):
    animal_type = models.CharField(
        max_length=10,
        choices=ANIMAL_TYPES,
        default=RATO,
    )
    nickname = models.CharField(max_length=100)
    code_number = models.IntegerField(unique=True)

    def find_one():
        return 


class Maze(models.Model):
    nickname = models.CharField(max_length=100)
    open_arm_length = models.IntegerField(default=0)
    close_arm_length = models.IntegerField(default=0)

    def __str__(self):
        return self.nickname


class MazeAreaSelection(models.Model):
    initX = models.IntegerField(default=0)
    initY = models.IntegerField(default=0)
    areaW = models.IntegerField(default=0)
    areaH = models.IntegerField(default=0)



class Test(models.Model):
    #mudar para on_delete=models.CASCADE
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT)
    maze = models.ForeignKey(Maze, null=True, on_delete=models.SET_NULL)
    datetime_start = models.DateTimeField(auto_now=True)
    datetime_end = models.DateTimeField(null=True, auto_now=False)
    entrances_close_right = models.IntegerField(default=0)
    entrances_close_left = models.IntegerField(default=0)
    entrances_open_right = models.IntegerField(default=0)
    entrances_open_left = models.IntegerField(default=0)
    timein_close_right = models.FloatField(default=0.0)
    timein_close_left = models.FloatField(default=0.0)
    timein_open_right = models.FloatField(default=0.0)
    timein_open_left = models.FloatField(default=0.0)
    timein_open = models.FloatField(default=0.0)
    timein_close = models.FloatField(default=0.0)
    timein_center = models.FloatField(default=0.0)
    cruzamentos = models.IntegerField(default=0)
    time_moving = models.FloatField(default=0.0)
    time_idle = models.FloatField(default=0.0)
    max_speed = models.FloatField(default=0.0)
    min_speed = models.FloatField(default=0.0)


    def __str__(self):
        return "Performed at: {}".format(self.datetime_start)

    def was_performed_recently(self):
        return self.datetime_end >= timezone.now() - datetime.timedelta(days=1)






