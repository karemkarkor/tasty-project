"""
tasty_django/urls.py — Root URL configuration

Includes the recipes app URLs and also serves static HTML files
(the existing frontend) via TemplateView, mirroring Express's
app.use(express.static(...)) behavior.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import re
from pathlib import Path
from recipes.views import logoutUser
BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin panel (separate from the app's admin.html)

    # All API routes and auth routes from the recipes app
    path('', include('recipes.urls')),

    # Serve the static HTML pages — mirrors Express's express.static() middleware.
    # Express served ALL files from the project root; we map the known HTML pages explicitly.
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home.html', TemplateView.as_view(template_name='home.html'), name='home-html'),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login-html'),
    path('signup.html', TemplateView.as_view(template_name='signup.html'), name='signup-html'),
    path('admin.html', TemplateView.as_view(template_name='admin.html'), name='admin-html'),
    path('Recipies.html', TemplateView.as_view(template_name='Recipies.html'), name='recipes-html'),
    path('addrecipe.html', TemplateView.as_view(template_name='addrecipe.html'), name='addrecipe-html'),
    path('edit-recipe.html', TemplateView.as_view(template_name='edit-recipe.html'), name='edit-recipe-html'),
    path('delete-recipe.html', TemplateView.as_view(template_name='delete-recipe.html'), name='delete-recipe-html'),
    path('Myfavoriteslist.html', TemplateView.as_view(template_name='Myfavoriteslist.html'), name='myfavoriteslist-html'),
    path('about.html', TemplateView.as_view(template_name='about.html'), name='about-html'),
    path('recipe-template.html', TemplateView.as_view(template_name='recipe-template.html'), name='recipe-template-html'),
    path('logout/',logoutUser,name='logout')
]

# Serve user-uploaded media files in development
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^(?P<path>JS/.*)$', serve, {'document_root': BASE_DIR}),
        re_path(r'^(?P<path>Styles/.*)$', serve, {'document_root': BASE_DIR}),
        re_path(r'^(?P<path>images/.*)$', serve, {'document_root': BASE_DIR}),
        re_path(r'^(?P<path>Images/.*)$', serve, {'document_root': BASE_DIR}),
    ]