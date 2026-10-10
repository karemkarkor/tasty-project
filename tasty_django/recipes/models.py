from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='normal'
    )

    def __str__(self):
        return self.username


class Recipe(models.Model):
    type = models.CharField(max_length=50, blank=True, default='')
    image = models.CharField(max_length=500, blank=True, default='')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    cook_time = models.CharField(max_length=50, blank=True, default='')
    ingredients = models.JSONField(default=list)
    steps = models.JSONField(default=list)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title

    def to_api_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'image': self.image,
            'title': self.title,
            'description': self.description,
            'cookTime': self.cook_time,
            'ingredients': self.ingredients,
            'steps': self.steps,
        }


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} -> {self.recipe.title}"