from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/hello/world', views.hello_world, name="hello-world"),
    url(r'^v1/scrabble/ai', views.scrabble_ai_v1, name="scrabble-ai-v1"),
]