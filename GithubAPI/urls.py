from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
# from django.views.generic.base import RedirectView
from django.contrib import admin
# from RestAPI.urls import event_router

urlpatterns = [
    url('admin/', admin.site.urls),
    url('', include("RestAPI.urls"))
]

# print("Before: ", urlpatterns)
# urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=True)
# print()
# print("After: ", urlpatterns)
# print()