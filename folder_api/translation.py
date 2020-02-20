from modeltranslation.translator import translator, TranslationOptions
from .models import Template, Resource, Folder, Question

class ResourceTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)

translator.register(Resource, ResourceTranslationOptions)

class TemplateTranslationOptions(TranslationOptions):
    fields = ('title', )

translator.register(Template, TemplateTranslationOptions)
class FolderTranslationOptions(TranslationOptions):
    fields = ('title'), 

translator.register(Folder, FolderTranslationOptions)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question', 'description',)

translator.register(Question, QuestionTranslationOptions)
