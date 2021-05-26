from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from .views import show_catalog
from .views import show_good

urlpatterns = [
	path('', 	show_catalog, name='show_catalog'),
	path('<str:cpu_slug>/', show_good, name='show_good'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()