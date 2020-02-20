
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from markdownx import urls as markdownx

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('folder_api.urls'))
]
urlpatterns += [
    url(r'^markdownx/', include(markdownx))
]