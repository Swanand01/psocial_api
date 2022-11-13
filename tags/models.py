from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
