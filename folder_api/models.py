from django.db import models
from markdownx.models import MarkdownxField
# Create your models here.

class Icon(models.Model):
    name = models.CharField(max_length=30)

class Folder(models.Model):
    Icon = models.ForeignKey(Icon, on_delete=models.CASCADE)
    title = models.TextField()

    # def serialize_hook(self, hook):
    #     # optional, there are serialization defaults
    #     # we recommend always sending the Hook
    #     # metadata along for the ride as well
    # #     return {
    # #         'hook': hook.dict(),
    # #         'data': {
    # #             'id': self.id,
    # #             'Icon': self.Icon,
    # #             'title': self.title,
    # #             # ... other fields here ...
    # #         }
    # #     }

    # # def mark_as_read(self):
    # #     # models can also have custom defined events
    # #     from rest_hooks.signals import hook_event
    # #     hook_event.send(
    # #         sender=self.__class__,
    # #         action='read',
    # #         instance=self # the Book object
    # #     )

class Resource(models.Model):
    Folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    title = models.TextField()
    # body = models.TextField()
    body = MarkdownxField()

class Template(models.Model):
    title = models.TextField()
    Folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    
class Question(models.Model):
    TEXT_TYPE_CHOICE = (
        ('text', 'text'),
        ('textarea', 'textarea'),
    )
    Template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True)
    question = models.TextField(null=True)
    description = models.TextField(null=True)
    text_type = models.CharField(max_length=20, choices=TEXT_TYPE_CHOICE, null=True)
