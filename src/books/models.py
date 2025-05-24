from django.db import models


class Book(models.Model):
    """
    Model representing a book.
    """

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
