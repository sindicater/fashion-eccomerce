<script>
  import { onMount } from 'svelte';

  let searchQuery = '';
  let selectedCategory = 'All';
  let products = [];
  let errorMessage = '';

  const categories = ['All', 'Vintage', 'Casual', 'Formal', 'Sportswear', 'Designer', 'Dresses', 'Shoes', 'Bags', 'Accessories'];

  async function fetchProducts() {
    try {
      const response = await fetch('http://127.0.0.1:5000/fetch_products');
      if (!response.ok) {
        throw new Error(`Failed to fetch products: ${response.statusText}`);
      }
      const data = await response.json();

      // Log the data received from the backend
      console.log('Data received from backend:', data);

      // Map backend data to frontend format
      products = data.map(product => {
        console.log('Product:', product);
        // Handle the base64 image
        let imageSrc = 'https://via.placeholder.com/200'; // Fallback image
        if (product.image_base64) {
          try {
            // Remove \\x sequences and convert hex to binary
            const hexString = product.image_base64.replace(/\\x/g, '');
            // Convert hex string to binary
            let binary = '';
            for (let i = 0; i < hexString.length; i += 2) {
              binary += String.fromCharCode(parseInt(hexString.substr(i, 2), 16));
            }
            // Encode binary to base64
            const base64 = btoa(binary);
            imageSrc = `data:${product.image_content_type || 'image/jpeg'};base64,${base64}`;
          } catch (e) {
            console.error(`Failed to decode image for product ${product.name}:`, e);
          }
        }
        return {
          name: product.name || 'Unnamed Product',
          image: imageSrc,
          price: product.price ? `$${parseFloat(product.price).toFixed(2)}` : '$0.00',
          category: product.category || 'Uncategorized',
          rating: product.rating != null ? parseFloat(product.rating) : 0
        };
      });
      filterProducts();
    } catch (error) {
      errorMessage = `Error fetching products: ${error.message}`;
      console.error(errorMessage);
      products = [];
    }
  }

  onMount(() => {
    fetchProducts();
  });

  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  function filterProducts() {
    let shuffledProducts = shuffleArray([...products]);
    products = shuffledProducts.filter(product =>
      (selectedCategory === 'All' || product.category === selectedCategory) &&
      product.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }

  function handleSearch() {
    filterProducts();
  }

  function handleCategoryChange(category) {
    selectedCategory = category;
    filterProducts();
  }

  // Function to render star rating
  function renderStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;
    return (
      '★'.repeat(fullStars) +
      (halfStar ? '☆' : '') +
      '☆'.repeat(emptyStars)
    );
  }
</script>

<style>
  body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
  }
  .container {
    padding: 20px;
  }
  .search-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  .search-bar input {
    width: 70%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1rem;
  }
  .search-bar button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #e91e63;
    color: #fff;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .search-bar button:hover {
    background-color: #c2185b;
  }
  .category-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }
  .category-buttons button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #fff;
    color: #333;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    border: 1px solid #ccc;
  }
  .category-buttons button.active {
    background-color: #e91e63;
    color: #fff;
    border-color: #e91e63;
  }
  .category-buttons button:hover {
    background-color: #f4f4f4;
  }
  .product-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  .product-card {
    background: #fff;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s;
  }
  .product-card:hover {
    transform: translateY(-10px);
  }
  .product-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 10px 10px 0 0;
  }
  .product-card .details {
    padding: 20px;
  }
  .product-card .details h3 {
    margin: 10px 0;
    font-size: 1.25rem;
  }
  .product-card .details p {
    font-size: 1.1rem;
    color: #e91e63;
  }
  .product-card .details .rating {
    color: #ff9800;
    font-size: 1.2rem;
  }
  .error-message {
    color: red;
    text-align: center;
    margin-bottom: 20px;
    font-size: 1.1rem;
  }
</style>

<div class="container">
  {#if errorMessage}
    <div class="error-message">{errorMessage}</div>
  {/if}
  <div class="search-bar">
    <input
      type="text"
      placeholder="Search products..."
      bind:value={searchQuery}
      on:input={handleSearch}
    />
    <button on:click={handleSearch}>Search</button>
  </div>

  <div class="category-buttons">
    {#each categories as category}
      <button
        class={selectedCategory === category ? 'active' : ''}
        on:click={() => handleCategoryChange(category)}
      >
        {category}
      </button>
    {/each}
  </div>

  <div class="product-list">
    {#each products as product}
      <div class="product-card">
        <img src={product.image} alt={product.name} />
        <div class="details">
          <h3>{product.name}</h3>
          <p>{product.price}</p>
          <p class="rating">{renderStars(product.rating)}</p>
        </div>
      </div>
    {/each}
  </div>
</div>
