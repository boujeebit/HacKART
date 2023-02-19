from django.db import models

class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name
