from django.contrib import admin
from .models import Author, Book, Genre, BookInstance, BookReview, Profilis


class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    readonly_fields = ['uuid']
    can_delete = False


class BookReviewInLine(admin.TabularInline):
    model = BookReview
    extra = 0

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'display_genre']
    inlines = [BookReviewInLine, BookInstanceInLine]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'uuid', 'status', 'due_back', 'reader']
    list_filter = ['book', 'status', 'due_back']
    list_editable = ['status', 'due_back', 'reader']

    search_fields = ['uuid', 'book__title']

    fieldsets = (
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back', 'reader')}),
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'date_created', 'reviewer', 'content']

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Profilis)
