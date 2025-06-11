from django.urls import path
from booking import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name="home"),
    path('location-list/', views.location_list, name='locations'),
    path('location-detail/<int:location_id>', views.location_detail, name='location_detail'),  # 127.0.0.1/location-detail/2
]
