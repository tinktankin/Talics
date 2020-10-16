from django.urls import path
from mapping import views

urlpatterns = [
        path('import', views.import_data),
        path('fieldmatching', views.fieldmatching),
        path('choose', views.choose),
        path('import_p', views.import_data_p),

]
