import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as auth_login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import Recipe, Favorite, User


def parse_json_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return {}


def get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    return None


def logoutUser(request):
    logout(request)
    return redirect('login-html')



class HomePageView(TemplateView):
    template_name = 'home.html'


@method_decorator(csrf_exempt, name='dispatch')
class RecipeListView(View):

    def get(self, request):
        recipes = Recipe.objects.all()
        data = [r.to_api_dict() for r in recipes]
        return JsonResponse(data, safe=False, status=200)

    def post(self, request):
        body = parse_json_body(request)
        title = body.get('title', '').strip()
        if not title:
            return JsonResponse({'message': 'Title is required'}, status=400)
        recipe = Recipe.objects.create(
            type=body.get('type', ''),
            image=body.get('image', ''),
            title=title,
            description=body.get('description', ''),
            cook_time=body.get('cookTime', ''),
            ingredients=body.get('ingredients', []),
            steps=body.get('steps', []),
        )
        return JsonResponse({'message': 'Recipe saved to server!'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class RecipeDetailView(View):

    def put(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found.'}, status=404)

        body = parse_json_body(request)
        recipe.type = body.get('type', recipe.type)
        recipe.image = body.get('image', recipe.image)
        recipe.title = body.get('title', recipe.title)
        recipe.description = body.get('description', recipe.description)
        recipe.cook_time = body.get('cookTime', recipe.cook_time)
        recipe.ingredients = body.get('ingredients', recipe.ingredients)
        recipe.steps = body.get('steps', recipe.steps)
        recipe.save()
        return JsonResponse({'message': 'Recipe updated!'}, status=200)

    def delete(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found.'}, status=404)

        recipe.delete()
        return JsonResponse({'message': 'Recipe deleted!'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AddToFavoritesView(View):

    def post(self, request):
        user = get_current_user(request)
        if not user:
            return JsonResponse({'message': 'Please login first'}, status=401)

        body = parse_json_body(request)
        recipe_id = body.get('recipeid')

        if not recipe_id:
            return JsonResponse({'message': 'Recipe id is required'}, status=400)

        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found'}, status=404)

        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return JsonResponse({'message': 'Recipe already in favorites!'}, status=400)

        Favorite.objects.create(user=user, recipe=recipe)
        return JsonResponse({'message': 'Recipe added successfully'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFromFavoritesView(View):

    def delete(self, request, recipe_id):
        user = get_current_user(request)
        if not user:
            return JsonResponse({'message': 'Please login first'}, status=401)

        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse({'message': 'Recipe not found'}, status=404)

        try:
            favorite = Favorite.objects.get(user=user, recipe=recipe)
            favorite.delete()
            return JsonResponse({'message': 'recipe successfully got deleted'}, status=200)
        except Favorite.DoesNotExist:
            return JsonResponse({'message': 'Error deleting from favorites list'}, status=404)


class RetrieveAllFavoritesView(View):

    def get(self, request):
        user = get_current_user(request)
        if not user:
            return JsonResponse([], safe=False, status=200)

        favorited_ids = Favorite.objects.filter(user=user).values_list('recipe_id', flat=True)
        recipes = Recipe.objects.filter(id__in=favorited_ids)
        data = [r.to_api_dict() for r in recipes]
        return JsonResponse(data, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):

    def post(self, request):
        content_type = request.content_type or ''
        if 'application/json' in content_type:
            body = parse_json_body(request)
        else:
            body = request.POST.dict()

        username = body.get('username', '').strip()
        email = body.get('email', '').strip()
        password = body.get('password', '').strip()
        user_type = body.get('user_type', 'normal')

        if not username or not email or not password:
            if 'application/json' in content_type:
                return JsonResponse({'message': 'Please fill in all sign-up fields.'}, status=400)
            return HttpResponse(
                '<script>alert("Please fill in all sign-up fields."); window.history.back();</script>',
                status=400
            )

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            if 'application/json' in content_type:
                return JsonResponse({'message': 'Username or email already exists.'}, status=400)
            return HttpResponse(
                '<script>alert("Username or email already exists."); window.history.back();</script>',
                status=400
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type=user_type,
        )
        if user_type == 'admin':
            user.is_staff = True
            user.save()

        if 'application/json' in content_type:
            return JsonResponse({'message': 'Sign-up successful! Please login.'}, status=200)
        return HttpResponse(
            '<script>alert("Sign-up successful! Please login."); window.location.href = "/login.html";</script>'
        )


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def post(self, request):
        content_type = request.content_type or ''
        if 'application/json' in content_type:
            body = parse_json_body(request)
        else:
            body = request.POST.dict()

        username = body.get('username', '').strip()
        email = body.get('email', '').strip()
        password = body.get('password', '').strip()

        if not username or not email or not password:
            if 'application/json' in content_type:
                return JsonResponse({'message': 'Please fill in all login fields.'}, status=400)
            return HttpResponse(
                '<script>alert("Please fill in all login fields."); window.history.back();</script>',
                status=400
            )

        user = authenticate(request, username=username, password=password)
        if user is None or user.email != email:
            if 'application/json' in content_type:
                return JsonResponse({'message': 'Invalid username, email, or password.'}, status=401)
            return HttpResponse(
                '<script>alert("Invalid username, email, or password."); window.location.href = "/login.html";</script>',
                status=401
            )

        auth_login(request, user)
        request.session[' _auth_user_id'] = str(user.pk)
        request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
        request.session['_auth_user_hash'] = user.get_session_auth_hash()
        request.session.save()
        if user.user_type == 'admin':
            if 'application/json' in content_type:
                return JsonResponse({'message': 'Welcome admin!', 'redirect': '/admin.html'}, status=200)
            return HttpResponse(
                '<script>alert("Welcome admin!"); window.location.href = "/admin.html";</script>'
            )

        if 'application/json' in content_type:
            return JsonResponse({'message': 'Login successful!', 'redirect': '/home.html'}, status=200)
        return HttpResponse(
            '<script>alert("Login successful!"); window.location.href = "/home.html";</script>'
        )