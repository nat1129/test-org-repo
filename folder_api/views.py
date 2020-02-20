from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Icon, Folder, Template, Question, Resource
from django.core import serializers
from django.conf import settings
import glob
import errno
import json

# Create your views here.
@api_view(['GET'])
def index(request):
    folder_path = 'F:/pending/pocket-reporter/src/data/saved/folders/*.json'
    resource_path = 'F:/pending/pocket-reporter/src/data/saved/resources/*.json'
    question_path = 'F:/pending/pocket-reporter/src/data/saved/questions/*.json'
    folder_files = glob.glob(folder_path)
    resource_files = glob.glob(resource_path)
    question_files = glob.glob(question_path)

    print("Loading...")
    for folder_name in folder_files:
        try:
            with open(folder_name, encoding="mbcs") as folder_json: # encoding="mbcs" will solve multi file open
                folder_data = json.load(folder_json)
                try:
                    i = Icon.objects.get(name=folder_data['icon'])
                except Icon.DoesNotExist:
                    i = Icon(name=folder_data['icon'])
                    i.save()
                
                f = Folder(title=folder_data['title'], Icon=i)
                for lang_code, lang_name in settings.LANGUAGES:
                    try:
                        setattr(f, 'title_' + lang_code, folder_data["translations"][lang_code])
                    except KeyError:
                        continue
                f.save()
                for r in folder_data['resources']:
                    # return Response({"a": r['content']})
                    for resource_name in resource_files:
                        with open(resource_name, encoding="mbcs") as resource_json:
                            resource_data = json.load(resource_json)
                            # return resource_data['title']
                            if r['content'] == resource_data['title']:
                                rs = Resource(title=r['content'], body=resource_data['body'], Folder=f)
                                for lang_code, lang_name in settings.LANGUAGES:
                                    try:
                                        setattr(rs, 'title_' + lang_code, resource_data[lang_code]["title"])
                                        setattr(rs, 'body_' + lang_code, resource_data[lang_code]["body"])
                                    except KeyError:
                                        setattr(rs, 'title_' + lang_code, '')
                                        setattr(rs, 'body_' + lang_code, '')
                                rs.save()
                
                for q in folder_data['questions']:
                    for question_name in question_files:
                        with open(question_name, encoding="mbcs") as question_json:
                            question_data = json.load(question_json)
                            if q['content'] == question_data['title']:
                                t = Template(Folder=f, title=q['content'])
                                for lang_code, lang_name in settings.LANGUAGES:
                                    try:
                                        setattr(t, 'title_' + lang_code, question_data[lang_code]["title"])
                                    except KeyError:
                                        setattr(t, 'title_' + lang_code, '')
                                t.save()
                                for qt in question_data['questions']:
                                    try:
                                        qs = Question(Template=t, question=qt['question'], description=qt['description'], text_type="text")
                                        for lang_code, lang_name in settings.LANGUAGES:
                                            try:
                                                setattr(qs, 'questions_' + lang_code, question_data[lang_code]["questions"][qt])
                                                setattr(qs, 'description_' + lang_code, question_data[lang_code]["description"][qt])
                                            except:
                                                setattr(qs, 'questions_' + lang_code, '')
                                                setattr(qs, 'description_' + lang_code, '')
                                        qs.save()
                                    except KeyError:
                                        qs = Question(Template=t, question=qt['question'], text_type="text")
                                        for lang_code, lang_name in settings.LANGUAGES:
                                            try:
                                                setattr(qs, 'questions_' + lang_code, question_data[lang_code]["questions"][qt])
                                            except:
                                                setattr(qs, 'questions_' + lang_code, '')
                                        qs = Question(Template=t, question=qt['question'], text_type="text")
                                        qs.save()
                                    

        except IOError as exc:
            if exc.errno != errno.EISDIR:
                return Response({"initilaized": "Failed"})

    return Response({"initilaized": "Success"})

@api_view(['GET'])
def resource(request, resource_id):
    try:
        r = Resource.objects.get(pk=resource_id)
        lang_result = {}
        for lang_code, lang_name in settings.LANGUAGES: 
            lang_result[lang_code] = {
                'title': getattr(r, 'title_' + lang_code),
                'body': getattr(r, 'body_' + lang_code),
            }
        result = {
            "id": resource_id,
            "meta": {
                "folder": r.Folder.pk   
            },
            # "languages": {
            #     "title": r.title,
            #     "body": r.body,
            #     "other": lang_result
            # } 
            "languages": lang_result
        }
        return Response(result)
    except Resource.DoesNotExist:
        return Response({"resource response": "DoesNotExist at /resources/" + resource_id})

@api_view(['GET'])
def question(request, question_id):
    try:
        t = Template.objects.get(pk=question_id)
        q = Question.objects.filter(Template=t)
        lang_result = {}
        for lang_code, lang_name in settings.LANGUAGES: 
            form = []
            for qs in q:
                form.append({"question": getattr(qs, "question_" + lang_code), "description": getattr(qs, "description_" + lang_code)})
            lang_result[lang_code] = {
                "title": getattr(t, "title_" + lang_code),
                "type": "text",
                "form": form
            }
        
        result = {
            "id": question_id,
            "meta": {
                "folder": t.Folder.pk
            },
            # "languages": {
            #     "title": t.title,
            #     "body": q[0].text_type, # should be modfied later
            #     "form": form
            # } 
            "language": lang_result
        }
        return Response(result)
    except Template.DoesNotExist:
        return Response({"question response": "DoesNotExist at /questions/" + question_id})

@api_view(['GET'])
def folder(request):
    # try:
        folders = Folder.objects.all()
        folder_result = []
        for f in folders:
            questions = []
            resources = []
            ts = Template.objects.filter(Folder=f)
            rs = Resource.objects.filter(Folder=f)
            for t in ts:
                questions.append(t.pk)
            for r in rs:
                resources.append(r.pk)
            lang_result = {}
            for lang_code, lang_name in settings.LANGUAGES: 
                lang_result[lang_code] = {
                    "title": getattr(f, "title_" + lang_code)
                }
            result = {
                "id": f.pk,
                "icon": f.Icon.name,
                "meta": {
                    "questions": questions,
                    "resources": resources,
                    # "languages": {
                    #     "title": f.title
                    # } # should be modified
                    "languages": lang_result
                }
            }
            folder_result.append(result)
        
        return Response(folder_result)
    # except Template.DoesNotExist:
    #     return Response({"question response": "DoesNotExist at /questions/" + question_id})




    
    

