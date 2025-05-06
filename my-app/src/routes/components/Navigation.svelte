<script lang="ts">
  export let currentPage: string;
  export let onNavigate: (page: string) => void;
  let isMenuOpen = false;

  function handleNav(page: string) {
    onNavigate(page);
    isMenuOpen = false; // Close the menu after navigation
  }

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }
</script>

<nav class="nav">
  <div class="nav-container">
    <span class="logo" on:click={() => handleNav('Home')}>Fashion Boutique</span>
    <button class="hamburger" on:click={toggleMenu} aria-label="Toggle menu">
      <span class="hamburger-line"></span>
      <span class="hamburger-line"></span>
      <span class="hamburger-line"></span>
    </button>
    <div class="nav-items" class:open={isMenuOpen}>
      <span class="nav-item" class:active={currentPage === 'Home'} on:click={() => handleNav('Home')}>Home</span>
      <span class="nav-item" class:active={currentPage === 'Products'} on:click={() => handleNav('Products')}>Products</span>
      <span class="nav-item" class:active={currentPage === 'About'} on:click={() => handleNav('About')}>About</span>
      <span class="nav-item" class:active={currentPage === 'Cart'} on:click={() => handleNav('Cart')}>Cart</span>
      <span class="nav-item profile" class:active={currentPage === 'Profile'} on:click={() => handleNav('Profile')}>
        <svg class="profile-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
        Profile
      </span>
    </div>
  </div>
</nav>

<style lang="scss">
  .nav {
    background: linear-gradient(90deg, #c2185b, #7b1fa2);
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 100;
    margin: 0;
    
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo {
    font-size: 1.75rem;
    font-weight: 700;
    font-family: 'Georgia', serif;
    cursor: pointer;
    color: #fff;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
  }

  .hamburger {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    margin-right: 1rem;
  }

  .hamburger-line {
    display: block;
    width: 24px;
    height: 3px;
    background: #fff;
    margin: 5px 0;
    transition: all 0.3s ease;
  }

  .nav-items {
    display: flex;
    gap: 1.5rem;
    align-items: center;
  }

  .nav-item {
    cursor: pointer;
    color: #fff;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 700;
    position: relative;
    transition: background-color 0.3s;
  }

  .nav-item:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }

  .nav-item.active {
    background-color: rgba(255, 255, 255, 0.3);
  }

  .nav-item.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 50%;
    height: 2px;
    background-color: #fff;
  }

  .profile {
    display: flex;
    align-items: center;
  }

  .profile-icon {
    width: 1.2rem;
    height: 1.2rem;
    margin-right: 0.3rem;
  }

  @media (max-width: 768px) {
    .hamburger {
      display: block;
    }

    .nav-items {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: linear-gradient(90deg, #7b1fa2, #c2185b);
      flex-direction: column;
      align-items: flex-start;
      padding: 1rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }

    .nav-items.open {
      display: flex;
    }

    .nav-item {
      width: 100%;
      text-align: left;
      padding: 0.75rem 1rem; /* Adjusted padding */
      font-size: 0.9rem; /* Reduced font size */
    }

    .nav-item.active::after {
      width: 30%;
      left: 1rem;
      transform: none;
    }
  }
</style>
