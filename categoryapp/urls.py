from django.urls import path
from .views import show_category

urlpatterns = [

	path('<str:cpu_slug>/', show_category, name='show_category'),
	
]
