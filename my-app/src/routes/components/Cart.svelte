<script>
  let cartItems = [
    { id: 1, name: 'Summer Dress', image: 'summer-dress.jpg', price: 49.99, quantity: 1, rating: '★★★★☆' },
    { id: 2, name: 'Designer Handbag', image: 'handbag.jpg', price: 99.99, quantity: 1, rating: '★★★★★' },
    { id: 3, name: 'Sports Shoes', image: 'sports-shoes.jpg', price: 79.99, quantity: 2, rating: '★★★☆☆' }
  ];

  function updateQuantity(itemId, quantity) {
    const item = cartItems.find(item => item.id === itemId);
    if (item) {
      item.quantity = quantity;
    }
  }

  function removeItem(itemId) {
    cartItems = cartItems.filter(item => item.id !== itemId);
  }

  function calculateTotal() {
    return cartItems.reduce((total, item) => total + item.price * item.quantity, 0).toFixed(2);
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
  .cart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  .cart-header h1 {
    font-size: 2rem;
    color: #333;
  }
  .cart-header button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #e91e63;
    color: #fff;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .cart-header button:hover {
    background-color: #c2185b;
  }
  .cart-items {
    margin-bottom: 40px;
  }
  .cart-item {
    display: flex;
    align-items: center;
    background: #fff;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    padding: 20px;
  }
  .cart-item img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 10px;
    margin-right: 20px;
  }
  .cart-item-details {
    flex: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .cart-item-details h2 {
    font-size: 1.25rem;
    color: #333;
  }
  .cart-item-details p {
    font-size: 1.1rem;
    color: #e91e63;
  }
  .rating {
    color: #ff9800;
    font-size: 1.2rem;
    margin-top: 5px;
  }
  .cart-item-actions {
    display: flex;
    align-items: center;
  }
  .cart-item-actions input {
    width: 50px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
    text-align: center;
    margin-right: 10px;
  }
  .cart-item-actions button {
    padding: 5px 10px;
    border: none;
    border-radius: 5px;
    background-color: #e91e63;
    color: #fff;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .cart-item-actions button:hover {
    background-color: #c2185b;
  }
  .cart-summary {
    background: #fff;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  .cart-summary h2 {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 10px;
  }
  .cart-summary p {
    font-size: 1.25rem;
    color: #e91e63;
    margin-bottom: 20px;
  }
  .cart-summary button {
    padding: 15px 30px;
    border: none;
    border-radius: 5px;
    background-color: #e91e63;
    color: #fff;
    font-size: 1.25rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .cart-summary button:hover {
    background-color: #c2185b;
  }
</style>

<div class="container">
  <div class="cart-header">
    <h1>Your Cart</h1>
    <button on:click={() => alert('Proceed to Checkout')}>Checkout</button>
  </div>

  <div class="cart-items">
    {#each cartItems as item}
      <div class="cart-item">
        <img src={item.image} alt={item.name}>
        <div class="cart-item-details">
          <div>
            <h2>{item.name}</h2>
            <p>${item.price.toFixed(2)} each</p>
            <p class="rating">{item.rating}</p>
          </div>
          <div class="cart-item-actions">
            <input
              type="number"
              min="1"
              bind:value={item.quantity}
              on:change={() => updateQuantity(item.id, item.quantity)}
            />
            <button on:click={() => removeItem(item.id)}>Remove</button>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <div class="cart-summary">
    <h2>Order Summary</h2>
    <p>Total: ${calculateTotal()}</p>
    <button on:click={() => alert('Proceed to Checkout')}>Checkout</button>
  </div>
</div>
