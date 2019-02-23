from django.db import models

class Item(models.Model):
    # TODO: Support more than one list!
    text = models.TextField(default='')