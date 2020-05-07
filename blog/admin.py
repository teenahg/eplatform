from django.contrib import admin
from .models import Post, Comment, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date_posted', 'category')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    list_filter = ('author',)
    
admin.site.register(Comment, CommentAdmin)