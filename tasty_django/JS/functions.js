// General variables
var Total = 0,
  main = 0,
  snacks = 0,
  dessert = 0;

let allRecipes = []; // Local cache for the search algorithm
function isINfavoriteslist(id,addToFavoritesbutton,title){
  fetch(`/api/retrieveAllFavorites`,{
    method:"get",
    headers:{
      'Content-Type': 'application/json',
    },
     credentials: "include",
  }).then((res)=> res.json())
  .then((data)=>{
    for(let recipe of data){
      if(recipe.id===id) 
        addToFavoritesbutton.style.display="none";
    }
    title.appendChild(addToFavoritesbutton);
  })
}
function adminAddRemoveFavorites(id,addToFavoritesbutton,deletefromFavoritesbutton,actionButtons,row,tableBody){
  fetch(`/api/retrieveAllFavorites`,{
    method:"get",
    headers:{
      'Content-Type': 'application/json',
    },
      credentials: "include",

  }).then((res)=> res.json())
  .then((data)=>{
    for(let recipe of data){
      if(recipe.id===id) 
      {
        addToFavoritesbutton.style.display="none";
        deletefromFavoritesbutton.style.display="inline-block";
        console.log("the delete button should be there now");
      }
    }
    actionButtons.appendChild(addToFavoritesbutton);
    actionButtons.appendChild(deletefromFavoritesbutton);
    row.appendChild(actionButtons);
    tableBody.appendChild(row);
  })
}

function addToFavorites(id,addToFavoritesbutton,deletefromFavoritesbutton=undefined){
   fetch("/api/addToFavorites", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ recipeid: id }),
  })
    .then(async(res)=>{
      let data=await res.json();
      if(!res.ok) throw new Error(`${data.message}`);
      return data;
    })
    .then((data)=>{
      alert(data.message);
      addToFavoritesbutton.style.display="none";
      if(deletefromFavoritesbutton){
        deletefromFavoritesbutton.style.display="inline-block";
      }
    })
    .catch((error)=>{
      alert(error)
      console.error(error);
    });
  
}
// For the recipes page
const recipesContainer = document.querySelector(".recipes-container");
function showRecipes(recipesData) {
  if (!recipesContainer) return;
  recipesContainer.innerHTML = ""; // Clear existing cards before adding new ones

  recipesData.forEach((recipe) => {
    const title = document.createElement("h2");
    title.textContent = recipe.title;
    const addToFavoritesbutton=document.createElement("button");
    addToFavoritesbutton.onclick=()=>{addToFavorites(recipe.id,addToFavoritesbutton)};
    addToFavoritesbutton.innerText="❤️";
    addToFavoritesbutton.className="add-button";
    isINfavoriteslist(recipe.id,addToFavoritesbutton,title);
    const description = document.createElement("p");
    description.textContent = recipe.description;
    const image = document.createElement("img");
    image.src = recipe.image;
    image.alt = recipe.title;
    const cookTime = document.createElement("strong");
    cookTime.innerText = "Cooking time : " + recipe.cookTime;
    const ingredientsTitle = document.createElement("h3");
    ingredientsTitle.innerText = "Ingredients";
    const ingredients = document.createElement("ul");

    recipe.ingredients.forEach((ingredient) => {
      const ingredientE = document.createElement("li");
      ingredientE.innerText = ingredient;
      ingredients.appendChild(ingredientE);
    });

    const card = document.createElement("div");
    card.classList.add("card");
    card.style.cursor = "pointer";
     // Add click handler to navigate to recipe template
    card.addEventListener("click", (e) => {
      // Don't navigate if the favorite button was clicked
      if (e.target === addToFavoritesbutton || addToFavoritesbutton.contains(e.target)) {
        return;
      }
      window.location.href = `recipe-template.html?id=${recipe.id}`;
    });
    card.append(
      title,
      description,
      image,
      cookTime,
      ingredientsTitle,
      ingredients,
    );

    recipesContainer.append(card);
  });
}
if (recipesContainer) {
  fetch("/api/recipes")
    .then((response) => response.json())
    .then((data) => {
      allRecipes = data; // Save the data globally in our module

      // If a user comes from the home page with a '?search=...' query, we handle it here.
      const urlParams = new URLSearchParams(window.location.search);
      const searchQuery = urlParams.get("search");

      if (searchQuery) {
        const searchInput = document.getElementById("searchInput");
        if (searchInput) searchInput.value = searchQuery;
        filterAndShow(searchQuery);
      } else {
        showRecipes(allRecipes);
      }
    });
}


// We use a linear search algorithm: it iterates through the entire list (Array.filter)
// and checks if the search string (query) exists in our target fields (title, description, ingredients).
// Performance: O(n) where 'n' is the number of recipes. Efficient for small lists!
function filterAndShow(query) {
  const q = query.toLowerCase().trim();

  // The 'filter' method creates a new array with all elements that pass the test
  const filtered = allRecipes.filter((recipe) => {
    // Check title, description, and every ingredient for a match
    return (
      recipe.title.toLowerCase().includes(q) ||
      recipe.description.toLowerCase().includes(q) ||
      recipe.ingredients.some((ing) => ing.toLowerCase().includes(q))
    );
  });

  showRecipes(filtered);
}

// EVENT LISTENERS for Search
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");

if (searchInput) {
  // Real-time search: updates as you type
  searchInput.addEventListener("input", (e) => {
    filterAndShow(e.target.value);
  });
}

if (searchBtn) {
  searchBtn.addEventListener("click", () => {
    const query = searchInput ? searchInput.value : "";
    filterAndShow(query);
  });
}

// Home page search logic (redirection)
const homeSearchInput = document.getElementById("homeSearchInput");
const homeSearchBtn = document.getElementById("homeSearchBtn");

if (homeSearchBtn && homeSearchInput) {
  homeSearchBtn.addEventListener("click", () => {
    const query = homeSearchInput.value;
    // Redirect to the recipes page with the query in the URL
    window.location.href = `Recipies.html?search=${encodeURIComponent(query)}`;
  });

  // Also allow pressing 'Enter' to search
  homeSearchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") homeSearchBtn.click();
  });
}

/**
 * GLOBAL NAVIGATION SEARCH LOGIC
 * This handles the search bar present in the navigation of every page.
 */
const navSearchInput = document.getElementById("navSearchInput");
const navSearchBtn = document.getElementById("navSearchBtn");

// Helper function to process the search action
function performGlobalSearch(query) {
  const searchQuery = query.trim();
  if (!searchQuery) return;

  // Check if we are already on the Recipes page
  const isRecipesPage = window.location.pathname.includes("Recipies.html");

  if (isRecipesPage) {
    // Already on recipes page: just filter results in real-time
    filterAndShow(searchQuery);
  } else {
    // On another page: redirect to Recipes page with the search term
    window.location.href = `Recipies.html?search=${encodeURIComponent(searchQuery)}`;
  }
}

if (navSearchBtn && navSearchInput) {
  // Listen for the button click
  navSearchBtn.addEventListener("click", () => {
    performGlobalSearch(navSearchInput.value);
  });

  // Listen for 'Enter' key in the search box
  navSearchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") performGlobalSearch(navSearchInput.value);
  });
}
// For the Add Recipe page
// Add ingredients
function addIngredient() {
  const ingredientsContainer = document.getElementById("ingredientsContainer");
  const rowContainer = document.createElement("div");

  rowContainer.className = "input-row";
  rowContainer.innerHTML = `
            <input type="text" name="ingredients" placeholder="Next ingredient..." required>
            <button type="button" class="remove-btn" onclick="removeRow(this)">X</button>
        `;
  ingredientsContainer.appendChild(rowContainer);
}

// Add steps
function addStep() {
  const stepsContainer = document.getElementById("stepsContainer");
  const rowContainer = document.createElement("div");

  rowContainer.className = "input-row";
  rowContainer.innerHTML = `
            <textarea name="steps" rows="2" placeholder="Next step..." required></textarea>
            <button type="button" class="remove-btn" onclick="removeRow(this)">X</button>
        `;
  stepsContainer.appendChild(rowContainer);
}

// Remove row
function removeRow(button) {
  button.parentElement.remove();
}

// For submitting the recipe
const recipeForm = document.getElementById("addRecipeForm");
if (recipeForm) {
  recipeForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const ingredientInputs = document.querySelectorAll(
      'input[name="ingredients"]',
    );
    const ingredientsArray = Array.from(ingredientInputs).map(
      (input) => input.value,
    );

    const stepInputs = document.querySelectorAll('textarea[name="steps"]');
    const stepsArray = Array.from(stepInputs).map((textarea) => textarea.value);

    const recipeData = {
      type: document.getElementById("recipeType").value,
      image: document.getElementById("image").value,
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      ingredients: ingredientsArray,
      cookTime: document.getElementById("cookTime").value,
      steps: stepsArray,
    };

    fetch("/api/add-recipe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(recipeData),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Recipe saved permanently to the server!");
        recipeForm.reset();
      })
      .catch((error) => {
        console.error("Error saving recipe:", error);
        alert("There was an error saving the recipe.");
      });
  });
}

// For the Admin page

const tableBody = document.getElementById("tableBody");
function showEditableRecipes(recipesData) {
  recipesData.forEach((recipe) => {
    const row = document.createElement("tr");

    const name = document.createElement("td");
    name.innerText = recipe.title;
    row.appendChild(name);

    const type = document.createElement("td");
    type.innerText = recipe.type;
    if (recipe.type == "Appetizers") {
      snacks += 1;
    } else if (recipe.type == "Main course") {
      main += 1;
    } else {
      dessert += 1;
    }
    row.appendChild(type);

    const ingredients = document.createElement("td");
    ingredients.innerText = `${recipe.ingredients.length} ingredients`;
    row.appendChild(ingredients);

    const actionButtons = document.createElement("td");
    actionButtons.className = "action-buttons";
    actionButtons.innerHTML = `
      <a href="edit-recipe.html?id=${recipe.id}" class="edit-btn">Edit</a>
      <button onclick="deleteRecipe(${recipe.id})" class="delete-btn" style="cursor: pointer;">Delete</button>
    `;
    const deletefromFavoritesbutton=document.createElement("button");
    deletefromFavoritesbutton.onclick=()=>{deleteFromFavorites(recipe.id)};
    deletefromFavoritesbutton.innerText="-";
    deletefromFavoritesbutton.className="delete-favorite-button";
    deletefromFavoritesbutton.style.display="none";
    const addToFavoritesbutton=document.createElement("button");
    addToFavoritesbutton.onclick=()=>{addToFavorites(recipe.id,addToFavoritesbutton,deletefromFavoritesbutton)};
    addToFavoritesbutton.innerText="❤️";
    addToFavoritesbutton.className="add-button";
    adminAddRemoveFavorites(recipe.id,addToFavoritesbutton,deletefromFavoritesbutton,actionButtons,row,tableBody);
    
  });
  document.getElementById("Total-recipes").innerText = recipesData.length;
  document.getElementById("mian-course").innerText = main;
  document.getElementById("Appetizers").innerText = snacks;
  document.getElementById("dessert").innerText = dessert;
}
if (tableBody) {
  fetch("/api/recipes")
    .then((response) => response.json())
    .then((data) => {
      showEditableRecipes(data);
    });
}
// for Editing the recipes

const editRecipeForm = document.getElementById("editRecipeForm");

if (editRecipeForm) {
  const urlParams = new URLSearchParams(window.location.search);
  const recipeId = urlParams.get("id");

  if (recipeId) {
    fetch("/api/recipes")
      .then((response) => response.json())
      .then((recipes) => {
        const recipe = recipes.find((r) => r.id == recipeId);

        if (recipe) {
          document.getElementById("recipeType").value = recipe.type;
          document.getElementById("title").value = recipe.title;
          document.getElementById("image").value = recipe.image;
          document.getElementById("description").value = recipe.description;
          document.getElementById("cookTime").value = recipe.cookTime;

          // fill the ingredients
          // Remove the initial empty label
          const ingContainer = document.getElementById("ingredientsContainer");
          ingContainer.innerHTML = "";
          // add the ingredients from the database
          recipe.ingredients.forEach((ing) => {
            const row = document.createElement("div");
            row.className = "input-row";
            row.innerHTML = `
              <input type="text" name="ingredients" value="${ing}" required>
              <button type="button" class="remove-btn" onclick="removeRow(this)">X</button>
            `;
            ingContainer.appendChild(row);
          });

          // fill the steps
          // Remove the initial empty label
          const stepsContainer = document.getElementById("stepsContainer");
          stepsContainer.innerHTML = "";

          // add the steps from the database
          recipe.steps.forEach((step) => {
            const row = document.createElement("div");
            row.className = "input-row";
            row.innerHTML = `
              <textarea name="steps" rows="2" required>${step}</textarea>
              <button type="button" class="remove-btn" onclick="removeRow(this)">X</button>
            `;
            stepsContainer.appendChild(row);
          });
        }
      })
      .catch((error) => console.error("Error loading recipe data:", error));
  }

  // handle form submission
  editRecipeForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const ingredientInputs = document.querySelectorAll(
      'input[name="ingredients"]',
    );
    const ingredientsArray = Array.from(ingredientInputs).map(
      (input) => input.value,
    );

    const stepInputs = document.querySelectorAll('textarea[name="steps"]');
    const stepsArray = Array.from(stepInputs).map((textarea) => textarea.value);

    const updatedRecipeData = {
      type: document.getElementById("recipeType").value,
      image: document.getElementById("image").value,
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      ingredients: ingredientsArray,
      cookTime: document.getElementById("cookTime").value,
      steps: stepsArray,
    };

    // Send the edit request to the server
    fetch(`/api/update-recipe/${recipeId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedRecipeData),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Recipe updated successfully!");
        window.location.href = "admin.html";
      })
      .catch((error) => {
        console.error("Error updating recipe:", error);
        alert("There was an error updating the recipe.");
      });
  });
}

// for deleting a recipe

function deleteRecipe(id) {
  // Catch undefined IDs (which happens if old recipes don't have an ID in your JSON)
  if (!id || id === "undefined") {
    alert("Error: This recipe doesn't have a valid ID in the database!");
    return;
  }
  if (
    confirm(
      "Are you sure you want to delete this recipe? This cannot be undone.",
    )
  ) {
    fetch(`/api/delete-recipe/${id}`, {
      method: "DELETE",
    })
      .then((response) => {
        // Force the code to jump to the catch block if the server fails
        if (!response.ok) throw new Error("Server failed to delete recipe.");
        return response.json();
      })
      .then((data) => {
        alert("Recipe deleted!");
        window.location.reload(); // Reload the table
      })
      .catch((error) => {
        console.error("Error deleting recipe:", error);
        alert(
          "Failed to delete recipe. Check your terminal console for clues!",
        );
      });
  }
}

function deleteFromFavorites(id){
  if(confirm(`Are you sure you want to delete this recipe from your favorites list ?`)){
      fetch(`/api/deleteFromFavorites/${id}`,{
      method:"delete",
      headers:{
              'Content-Type': 'application/json'
          },
           credentials: "include",
      }
    ).then((res)=>{
      if(!res.ok){throw new Error("Error deleting from favorites list")}
      return  res.json();
    }).then((data)=>{
      alert(data.message);
      location.reload();
    })
    .catch((error)=>{
      console.error(error);
      alert("Failed to delete from your favorites list ,check you terminal for clues! ");
    })
  }
}

function showFavoritesList(){
  fetch(`/api/retrieveAllFavorites`,{
    method:"get",
    headers:{
            'Content-Type': 'application/json'
        },
        credentials: "include",

    })
  .then((res)=>{
    if(!res.ok){throw Error("Error fetching the favorites list")}
    return res.json();
  })
  .then((favoritesList)=>{
    const list=document.getElementById("myFavRecipes");//<ul>
    for(var recipe of favoritesList){
      let recipeContainer=document.createElement("div");
      recipeContainer.className="recipe-container";
      let ingredientsContainer="Ingredients:\n";
      for(let string of recipe.ingredients){
        ingredientsContainer += "➡️"+string+"\n";
      }
      let stepsContainer="Steps:\n";
      for(let string of recipe.steps){
        stepsContainer += "➡️"+string+"\n";
      }
      let cookTime= `Cook Time: ${recipe.cookTime}`;
      recipeContainer.innerHTML=`
        <h2 class="recipe-title">${recipe.title}<span><pre>${cookTime}</pre><button class="delete-recipe" onclick="deleteFromFavorites(${recipe.id})">-</button></span></h2>
        <p class="description">${recipe.description}</p>
      <li>
          <div class="content-cont">
            <div class="ingredient-container"><pre>${ingredientsContainer}</pre></div>
            <div class="steps-container"><pre>${stepsContainer}</pre></div>
          </div>
      </li>
      `;
      list.appendChild(recipeContainer);
    }
  })
  .catch((error)=>console.error(error))
} 



























// for visibility
window.addIngredient = addIngredient;
window.addStep = addStep;
window.removeRow = removeRow;
window.deleteRecipe = deleteRecipe;
