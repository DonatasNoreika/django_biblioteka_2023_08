from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200,
                            help_text='Įveskite knygos žanrą (pvz. detektyvas)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Žanras'
        verbose_name_plural = 'Žanrai'


class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas", max_length=100)
    last_name = models.CharField(verbose_name="Pavardė", max_length=100)
    description = models.TextField(verbose_name='Aprašymas', max_length=2000, default='')

    def display_books(self):
        books = self.books.all()
        res = ", ".join(book.title for book in books)
        return res

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Autorius'
        verbose_name_plural = 'Autoriai'


class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=200)
    author = models.ForeignKey(to="Author", on_delete=models.SET_NULL, null=True, related_name="books")
    summary = models.TextField(verbose_name="Aprašymas", max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField(verbose_name="ISBN", max_length=13,
                            help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    genre = models.ManyToManyField(to="Genre", help_text='Išrinkite žanrą(us) šiai knygai')
    cover = models.ImageField(verbose_name="Viršelis", upload_to='covers', null=True, blank=True)

    def display_genre(self):
        genres = self.genre.all()
        res = ", ".join(genre.name for genre in genres)
        return res

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Knyga'
        verbose_name_plural = 'Knygos'


class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="Unikalus kodas", default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE, related_name="instances")
    due_back = models.DateField(verbose_name="Gražinimo data", null=True, blank=True)
    reader = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        return self.due_back and self.due_back < date.today()

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField(verbose_name="Būsena", choices=LOAN_STATUS, default="a", max_length=1, blank=True)

    def __str__(self):
        return f"{self.uuid} ({self.book.title})"

    class Meta:
        verbose_name = 'Egzempliorius'
        verbose_name_plural = 'Egzemplioriai'
