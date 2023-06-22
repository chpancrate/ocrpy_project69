from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True,
                                   verbose_name="Description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    IMAGE_MAX_SIZE = (250, 300)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[
                                                  MinValueValidator(0),
                                                  MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(max_length=8192, blank=True,
                            verbose_name="Contenu")
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
