"""capybara URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


SchemaView = get_schema_view(
   openapi.Info(
      title="Capybara API",
      default_version='v1',
      description="API developed for TCC and ICV - UFPI",
   ),
   public=True,
)

urlpatterns = [
    url(r'^doc/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
