from django.contrib import admin
from .models import *

# Register your models here.
# class PinBoardInline(admin.TabularInline):
#     model = PinBoard
#     extra = 1
#
# class UserBoardInline(admin.TabularInline):
#     model = UserBoard
#     extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    #inlines = [UserBoardInline]

@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user__username', 'created_at',
                    'updated_at', 'is_private', 'user')
    list_display_links = ('title', 'id', 'user')
    search_fields = ('title', 'user__username')
    list_editable = ('is_private',)
    list_filter = ('is_private',)
    date_hierarchy = 'created_at' #навигация по дате
    empty_value_display = "-empty-" #отображение для пустых полей
    #inlines = [PinBoardInline, CommentInline]

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'is_private')
    list_editable = ('is_private',)
    #inlines = [PinBoardInline, UserBoardInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'pin', 'user__username',
                    'content', 'created_at', 'updated_at')

    list_display_links = ('id', 'user__username')



