from django.urls import path
from . import views

urlpatterns = [
        path('', views.disp, name = 'mapping')
    # path('', views.MappingView.as_view(), name = 'mapping')

]
