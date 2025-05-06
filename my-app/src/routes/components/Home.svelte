<script>
  import { goto } from '$app/navigation';

  let featuredProducts = [
    { name: 'Summer Dress', price: '$49.99', image: '/path/to/summer-dress.jpg', rating: '★★★★☆' },
    { name: 'Designer Handbag', price: '$99.99', image: '/path/to/designer-handbag.jpg', rating: '★★★★★' },
    { name: 'Sports Shoes', price: '$79.99', image: '/path/to/sports-shoes.jpg', rating: '★★★☆☆' }
  ];

  let trendingItems = [
    { name: 'Denim Jacket', price: '$59.99', image: '/path/to/denim-jacket.jpg', rating: '★★★★☆' },
    { name: 'Sunglasses', price: '$29.99', image: '/path/to/sunglasses.jpg', rating: '★★★★★' },
    { name: 'Winter Coat', price: '$129.99', image: '/path/to/winter-coat.jpg', rating: '★★★☆☆' }
  ];

  function addToCart(productName) {
    alert(`${productName} added to cart!`);
  }

  function navigateToShop() {
    goto('/shop');
  }
</script>

<style>
  :global(body) {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f9f5ef;
    color: #333;
  }

  .hero {
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/hero-bg.jpg') no-repeat center center/cover;
    color: #fff;
    text-align: center;
    padding: 80px 0;
    width: 100vw;
    margin: 0;
    position: relative;
    left: calc(-50vw + 50%);
  }

  .hero-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .hero h1 {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 10px;
  }

  .hero p {
    font-size: 1.2rem;
    margin-bottom: 20px;
  }

  .hero-cta {
    background-color: #e91e63;
    color: #fff;
    border: none;
    padding: 12px 30px;
    border-radius: 25px;
    font-size: 1rem;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .hero-cta:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .limited-offer {
    background-color: #e91e63;
    color: #fff;
    text-align: center;
    padding: 12px 0;
    font-size: 1rem;
    font-weight: 600;
    width: 100vw;
    margin: 0;
    position: relative;
    left: calc(-50vw + 50%);
  }

  .limited-offer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .section {
    padding: 30px 20px;
    text-align: center;
  }

  .section h2 {
    font-size: 2rem;
    font-weight: 600;
    color: #e91e63;
    margin-bottom: 20px;
  }

  .product-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .product-card {
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
  }

  .product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }

  .product-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .details h3 {
    font-size: 1.2rem;
    color: #333;
    margin: 10px 0;
  }

  .price {
    font-size: 1rem;
    color: #e91e63;
    font-weight: 600;
  }

  .rating {
    color: #ff9800;
    font-size: 1.2rem;
    margin-top: 5px;
  }

  .add-to-cart {
    background-color: #e91e63;
    color: #fff;
    border: none;
    padding: 8px 15px;
    border-radius: 5px;
    font-size: 0.9rem;
    cursor: pointer;
    margin-top: 10px;
    transition: background-color 0.3s;
  }

  .add-to-cart:hover {
    background-color: #f06292;
  }

  .explore-section {
    background-color: #e91e63;
    color: #fff;
    padding: 30px 20px;
    margin: 0;
    text-align: center;
    width: 100vw;
    position: relative;
    left: calc(-50vw + 50%);
    top: 0; /* Ensure it touches the top */
  }

  .explore-section h2 {
    font-size: 2rem;
    margin-bottom: 10px;
  }

  .explore-section p {
    font-size: 1.2rem;
    margin-bottom: 20px;
  }

  .explore-cta {
    background-color: #fff;
    color: #e91e63;
    border: none;
    padding: 12px 30px;
    border-radius: 25px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .explore-cta:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .special-offer {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin: 30px auto;
    padding: 20px;
    max-width: 1200px;
  }

  .special-offer-card {
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
    width: 45%;
    margin-right: 20px;
  }

  .special-offer-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }

  .special-offer-card img {
    width: 100%;
    height: auto;
    border-radius: 8px;
  }

  .special-offer .details {
    width: 50%;
    padding: 20px;
    text-align: left;
  }

  .special-offer .details h3 {
    font-size: 1.5rem;
    color: #e91e63;
    margin-bottom: 10px;
  }

  .special-offer .details p {
    font-size: 1rem;
    color: #333;
    margin-bottom: 20px;
  }

  .special-offer .details .add-to-cart {
    margin-top: 0;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .hero h1 {
      font-size: 2rem;
    }
    .hero p {
      font-size: 1.1rem;
    }
    .hero-content, .limited-offer-content {
      padding: 0 15px;
    }
    .section h2, .explore-section h2 {
      font-size: 1.8rem;
    }
    .product-list {
      grid-template-columns: 1fr;
    }
    .special-offer {
      flex-direction: column;
      text-align: center;
    }
    .special-offer-card {
      width: 100%;
      margin-right: 0;
      margin-bottom: 20px;
    }
    .special-offer .details {
      width: 100%;
      padding: 0;
    }
  }

  @media (max-width: 480px) {
    .hero {
      padding: 50px 0;
    }
    .hero h1 {
      font-size: 1.8rem;
    }
    .hero p {
      font-size: 1rem;
    }
    .hero-cta, .explore-cta {
      padding: 10px 25px;
      font-size: 0.9rem;
    }
    .hero-content, .limited-offer-content {
      padding: 0 10px;
    }
  }
</style>

<div class="hero">
  <div class="hero-content">
    <h1>Unleash Your Style with our Fashion Boutique</h1>
    <p>Discover Sustainable, Trendy Fashion for Every Occasion</p>
    <button class="hero-cta" on:click={navigateToShop}>Shop Now</button>
  </div>
</div>

<div class="limited-offer">
  <div class="limited-offer-content">
    <h3>Flash Sale! Up to 40% Off – Ends in 24 Hours!</h3>
  </div>
</div>

<div class="special-offer">
  <div class="special-offer-card">
    <img src="/path/to/special-offer.jpg" alt="Special Offer" />
  </div>
  <div class="details">
    <h3>Special Offer</h3>
    <p>Get this exclusive item at a discounted price! Limited time offer.</p>
    <button class="add-to-cart" on:click={() => addToCart('Special Offer Item')}>Add to Cart</button>
  </div>
</div>

<div class="section">
  <h2>Featured Products</h2>
  <div class="product-list">
    {#each featuredProducts as product}
      <div class="product-card">
        <img src={product.image} alt={product.name} class="product-image" />
        <div class="details">
          <h3>{product.name}</h3>
          <p class="price">{product.price}</p>
          <p class="rating">{product.rating}</p>
          <button class="add-to-cart" on:click={() => addToCart(product.name)}>Add to Cart</button>
        </div>
      </div>
    {/each}
  </div>
</div>

<div class="section">
  <h2>Trending Items</h2>
  <div class="product-list">
    {#each trendingItems as item}
      <div class="product-card">
        <img src={item.image} alt={item.name} class="product-image" />
        <div class="details">
          <h3>{item.name}</h3>
          <p class="price">{item.price}</p>
          <p class="rating">{item.rating}</p>
          <button class="add-to-cart" on:click={() => addToCart(item.name)}>Add to Cart</button>
        </div>
      </div>
    {/each}
  </div>
</div>

<div class="explore-section">
  <h2>Explore Our Full Collection</h2>
  <p>Find Your Perfect Style with FashionRev’s Eco-Friendly Fashion</p>
  <button class="explore-cta" on:click={navigateToShop}>Shop Now</button>
</div>
