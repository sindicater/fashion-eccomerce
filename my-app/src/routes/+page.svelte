<script lang="ts">
    import Navigation from './components/Navigation.svelte';
    import Home from './components/Home.svelte';
    import Products from './components/Products.svelte';
    import About from './components/About.svelte';
    import Cart from './components/Cart.svelte';
    import Profile from './components/Profile.svelte';
    import Authentication from './Authentication/Authentication.svelte';
  
    let currentPage = 'Home';
    let isAuthenticated = false;
    let username = '';
    let showPreferencesPopup = false;
    let fashionPreferences = {
      trend: '',
      style: '',
    };
  
    // Predefined style options for buttons
    const styleOptions = ['Denim', 'Jeans', 'Khaki', 'Casual', 'Boho'];
  
    // Check localStorage on load to restore authenticated state and preferences
    if (typeof window !== 'undefined') {
      const storedUserId = localStorage.getItem('user_id');
      const storedUsername = localStorage.getItem('username');
      const hasSeenPopup = localStorage.getItem('hasSeenPreferencesPopup');
      const storedPreferences = localStorage.getItem('fashionPreferences');
  
      if (storedUserId && storedUsername) {
        isAuthenticated = true;
        username = storedUsername;
        currentPage = 'Home';
      }
  
      if (storedPreferences) {
        fashionPreferences = JSON.parse(storedPreferences);
      }
  
      // Show popup if user is authenticated and hasn't seen it
      if (isAuthenticated && !hasSeenPopup) {
        showPreferencesPopup = true;
      }
    }
  
    function updatePage(page: string) {
      currentPage = page;
    }
  
    function handleAuthenticated(event: CustomEvent) {
      const { user_id, username: newUsername } = event.detail;
      // Save user_id and username to localStorage
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('username', newUsername);
      // Update state
      isAuthenticated = true;
      username = newUsername;
      currentPage = 'Home';
  
      // Check if popup has been shown before
      const hasSeenPopup = localStorage.getItem('hasSeenPreferencesPopup');
      if (!hasSeenPopup) {
        showPreferencesPopup = true;
      }
    }
  
    function selectStyle(style: string) {
      fashionPreferences.style = style;
    }
  
    function handlePreferencesSubmit() {
      // Save preferences to localStorage
      localStorage.setItem('fashionPreferences', JSON.stringify(fashionPreferences));
      localStorage.setItem('hasSeenPreferencesPopup', 'true');
      showPreferencesPopup = false;
    }
  
    function skipPreferences() {
      // Mark popup as seen without saving preferences
      localStorage.setItem('hasSeenPreferencesPopup', 'true');
      showPreferencesPopup = false;
    }
  </script>
  
  <main>
    <Navigation {currentPage} onNavigate={updatePage} username={username} />
    <div class="content">
      {#if !isAuthenticated}
        <Authentication on:authenticated={handleAuthenticated} />
      {:else}
        {#if showPreferencesPopup && currentPage === 'Home'}
          <div class="popup-overlay">
            <div class="popup">
              <h2>Welcome, {username}!</h2>
              <p>Tell us about your fashion preferences to personalize your experience.</p>
              <form on:submit|preventDefault={handlePreferencesSubmit}>
                <div class="form-group">
                  <label for="trend">What's the latest fashion trend you're into?</label>
                  <input
                    id="trend"
                    type="text"
                    bind:value={fashionPreferences.trend}
                    placeholder="e.g., Streetwear, Minimalism"
                  />
                </div>
                <div class="form-group">
                  <label for="style">What styles do you love? (e.g., Denim, Boho)</label>
                  <div class="style-buttons">
                    {#each styleOptions as style}
                      <button
                        type="button"
                        class="style-button"
                        class:active={fashionPreferences.style === style}
                        on:click={() => selectStyle(style)}
                      >
                        {style}
                      </button>
                    {/each}
                  </div>
                  <input
                    id="style"
                    type="text"
                    bind:value={fashionPreferences.style}
                    placeholder="e.g., Denim, Casual"
                  />
                </div>
                <div class="button-group">
                  <button type="submit">Save Preferences</button>
                  <button type="button" on:click={skipPreferences}>Skip</button>
                </div>
              </form>
            </div>
          </div>
        {/if}
        {#if currentPage === 'Home'}
          <Home username={username} preferences={fashionPreferences} onNavigate={updatePage} />
        {:else if currentPage === 'Products'}
          <Products />
        {:else if currentPage === 'About'}
          <About />
        {:else if currentPage === 'Cart'}
          <Cart />
        {:else if currentPage === 'Profile'}
          <Profile username={username} />
        {/if}
      {/if}
    </div>
  </main>
  
  <style lang="scss">
    main {
      font-family: Arial, sans-serif;
    }
  
    .content {
      max-width: 1200px;
      margin: 60px auto 0; /* Adjust based on nav height */
      transition: opacity 0.3s ease;
      position: relative;
    }
  
    .popup-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }
  
    .popup {
      background: white;
      padding: 2rem;
      border-radius: 8px;
      max-width: 500px;
      width: 90%;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      animation: fadeIn 0.3s ease-in;
    }
  
    .popup h2 {
      font-size: 1.8rem;
      margin-bottom: 1rem;
      color: #1f2937;
    }
  
    .popup p {
      font-size: 1rem;
      color: #6b7280;
      margin-bottom: 1.5rem;
    }
  
    .form-group {
      margin-bottom: 1.5rem;
    }
  
    .form-group label {
      display: block;
      font-weight: 600;
      color: #1f2937;
      margin-bottom: 0.5rem;
    }
  
    .form-group input {
      width: 100%;
      padding: 0.8rem;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      font-size: 1rem;
    }
  
    .form-group input:focus {
      outline: none;
      border-color: #a78bfa;
      box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2);
    }
  
    .style-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
  
    .style-button {
      padding: 0.5rem 1rem;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      background: #f9fafb;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.2s ease;
    }
  
    .style-button:hover {
      background: #e5e7eb;
    }
  
    .style-button.active {
      background: #a78bfa;
      color: white;
      border-color: #a78bfa;
    }
  
    .button-group {
      display: flex;
      gap: 1rem;
      justify-content: flex-end;
    }
  
    .button-group button {
      padding: 0.8rem 1.5rem;
      border: none;
      border-radius: 6px;
      font-size: 1rem;
      cursor: pointer;
      transition: all 0.3s ease;
    }
  
    .button-group button[type='submit'] {
      background: #a78bfa;
      color: white;
    }
  
    .button-group button[type='submit']:hover {
      background: #8b5cf6;
    }
  
    .button-group button[type='button'] {
      background: #e5e7eb;
      color: #1f2937;
    }
  
    .button-group button[type='button']:hover {
      background: #d1d5db;
    }
  
    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(-10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  
    :global(body) {
      background-color: #f8f9fa;
      color: #000;
      margin: 0;
    }
  
    @media (max-width: 768px) {
      .content {
        margin: 50px auto 0; /* Adjust based on nav height for mobile */
      }
    }
  
    @media (max-width: 480px) {
      .popup {
        padding: 1.5rem;
        width: 95%;
      }
  
      .popup h2 {
        font-size: 1.5rem;
      }
  
      .button-group {
        flex-direction: column;
        gap: 0.5rem;
      }
  
      .button-group button {
        width: 100%;
      }
  
      .style-button {
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
      }
    }
  </style>
  