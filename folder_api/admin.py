from django.contrib import admin
from folder_api.models import *
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    pass

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    pass

# @admin.register(Resource)
# class ResourceAdmin(admin.ModelAdmin):
#     pass

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Resource, MarkdownxModelAdmin)

