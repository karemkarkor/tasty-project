// Import the shared functions
import './functions.js';

// Function to load recipe data based on URL parameter
async function loadRecipe() {
  const urlParams = new URLSearchParams(window.location.search);
  const recipeId = urlParams.get('id');
  
  if (!recipeId) {
    window.location.href = 'Recipies.html';
    return;
  }

  try {
    const response = await fetch('/api/recipes');
    const recipes = await response.json();
    
    const recipe = recipes.find(r => r.id === parseInt(recipeId));
    
    if (!recipe) {
      window.location.href = 'Recipies.html';
      return;
    }

    displayRecipe(recipe);
  } catch (error) {
    console.error('Error loading recipe:', error);
    window.location.href = 'Recipies.html';
  }
}

// Function to display the recipe data
function displayRecipe(recipe) {
  // Set page title
  document.getElementById('pageTitle').textContent = `${recipe.title} — Tasty Recipe`;
  
  // Set hero section
  document.getElementById('recipeImage').src = recipe.image;
  document.getElementById('recipeImage').alt = recipe.title;
  document.getElementById('cookTime').textContent = recipe.cookTime;
  document.getElementById('recipeTitle').textContent = recipe.title;
  document.getElementById('recipeDescription').textContent = recipe.description;
  
  // Build ingredients list
  const ingredientsList = document.getElementById('ingredientsList');
  ingredientsList.innerHTML = '';
  recipe.ingredients.forEach(ingredient => {
    const ingredientItem = document.createElement('div');
    ingredientItem.className = 'ingredient-item';
    ingredientItem.innerHTML = `
      <span class="ingredient-dot"></span>
      ${ingredient}
    `;
    ingredientsList.appendChild(ingredientItem);
  });
  
  // Build steps list
  const stepsList = document.getElementById('stepsList');
  stepsList.innerHTML = '';
  recipe.steps.forEach((step, index) => {
    const stepItem = document.createElement('div');
    stepItem.className = 'step-item';
    stepItem.innerHTML = `
      <div class="step-number">${index + 1}</div>
      <div class="step-text">${step}</div>
    `;
    stepsList.appendChild(stepItem);
  });
}

// Load recipe when page loads
document.addEventListener('DOMContentLoaded', loadRecipe);