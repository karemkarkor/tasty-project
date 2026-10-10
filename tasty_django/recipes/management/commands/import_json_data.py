"""
management/commands/import_json_data.py

One-time migration utility: reads the original recipes.json,
favoriteRecipesIDs.json, and users.json files and imports them
into the Django database.

Usage:
    python manage.py import_json_data --recipes path/to/recipes.json \
                                      --favorites path/to/favoriteRecipesIDs.json \
                                      --users path/to/users.json
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password

from recipes.models import Recipe, Favorite, User


class Command(BaseCommand):
    help = 'Import existing JSON data files into the Django database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recipes',
            type=str,
            default='JS/recipes.json',
            help='Path to recipes.json (default: JS/recipes.json)',
        )
        parser.add_argument(
            '--favorites',
            type=str,
            default='JS/favoriteRecipesIDs.json',
            help='Path to favoriteRecipesIDs.json (default: JS/favoriteRecipesIDs.json)',
        )
        parser.add_argument(
            '--users',
            type=str,
            default='JS/users.json',
            help='Path to users.json (default: JS/users.json)',
        )

    def handle(self, *args, **options):
        self._import_recipes(options['recipes'])
        self._import_favorites(options['favorites'])
        self._import_users(options['users'])
        self.stdout.write(self.style.SUCCESS('✅ JSON data import complete!'))

    def _import_recipes(self, path):
        p = Path(path)
        if not p.exists():
            self.stdout.write(self.style.WARNING(f'⚠️  recipes file not found: {path}, skipping'))
            return

        with open(p) as f:
            recipes_data = json.load(f)

        created = 0
        skipped = 0
        for r in recipes_data:
            # Preserve original IDs so favorites FK still works
            if Recipe.objects.filter(pk=r.get('id')).exists():
                skipped += 1
                continue

            Recipe.objects.create(
                id=r.get('id'),
                type=r.get('type', ''),
                image=r.get('image', ''),
                title=r.get('title', ''),
                description=r.get('description', ''),
                cook_time=r.get('cookTime', ''),     # camelCase in JSON → snake_case in model
                ingredients=r.get('ingredients', []),
                steps=r.get('steps', []),
            )
            created += 1

        self.stdout.write(f'  Recipes: {created} created, {skipped} skipped (already exist)')

    def _import_favorites(self, path):
        p = Path(path)
        if not p.exists():
            self.stdout.write(self.style.WARNING(f'⚠️  favorites file not found: {path}, skipping'))
            return

        with open(p) as f:
            fav_ids = json.load(f)

        created = 0
        skipped = 0
        for recipe_id in fav_ids:
            try:
                recipe = Recipe.objects.get(pk=recipe_id)
            except Recipe.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Recipe id={recipe_id} not found, skipping favorite'))
                continue

            if Favorite.objects.filter(recipe=recipe).exists():
                skipped += 1
                continue

            Favorite.objects.create(recipe=recipe)
            created += 1

        self.stdout.write(f'  Favorites: {created} created, {skipped} skipped (already exist)')

    def _import_users(self, path):
        p = Path(path)
        if not p.exists():
            self.stdout.write(self.style.WARNING(f'⚠️  users file not found: {path}, skipping'))
            return

        with open(p) as f:
            users_data = json.load(f)

        created = 0
        skipped = 0
        for u in users_data:
            if User.objects.filter(username=u['username']).exists():
                skipped += 1
                continue

            # IMPORTANT: The original users.json stores passwords in plain text.
            # We hash them here using Django's password hashing system.
            # After import, users log in with their original plain-text password
            # because Django's authenticate() verifies against the hash.
            user = User(
                username=u['username'],
                email=u.get('email', ''),
                user_type=u.get('user_type', 'normal'),
                password=make_password(u['password']),  # hash the plain-text password
            )
            if u.get('user_type') == 'admin':
                user.is_staff = True
            user.save()
            created += 1

        self.stdout.write(f'  Users: {created} created, {skipped} skipped (already exist)')
