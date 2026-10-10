"""
urls.py — Express routes → Django URL patterns

Express                              Django
-------------------------------------------------
GET  /api/recipes               →   recipes/
POST /api/add-recipe            →   recipes/          (same view, different method)
PUT  /api/update-recipe/<id>    →   recipes/<id>/
DELETE /api/delete-recipe/<id>  →   recipes/<id>/     (same view, different method)
POST /api/addToFavorites        →   favorites/
DELETE /api/deleteFromFavorites/<id> → favorites/<id>/
GET  /api/retrieveAllFavorites  →   favorites/        (same view, different method)
POST /signup                    →   /signup
POST /login                     →   /login
GET  /                          →   /
"""

from django.urls import path
from . import views

urlpatterns = [
    # Recipe CRUD
    path('api/recipes', views.RecipeListView.as_view(), name='recipe-list'),
    path('api/add-recipe', views.RecipeListView.as_view(), name='recipe-add'),  # alias for POST
    path('api/update-recipe/<int:recipe_id>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('api/delete-recipe/<int:recipe_id>', views.RecipeDetailView.as_view(), name='recipe-delete'),

    # Favorites
    path('api/addToFavorites', views.AddToFavoritesView.as_view(), name='favorites-add'),
    path('api/deleteFromFavorites/<int:recipe_id>', views.DeleteFromFavoritesView.as_view(), name='favorites-delete'),
    path('api/retrieveAllFavorites', views.RetrieveAllFavoritesView.as_view(), name='favorites-list'),

    # Auth
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
]
