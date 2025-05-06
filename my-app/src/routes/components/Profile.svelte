<script lang="ts">
  export let username: string = '';
  export let email: string = '';

  let user = {
      phone: '123-456-7890',
      address: '123 Fashion Ave, Style City, ST12345'
  };

  let orderHistory = [
      { id: 1, date: '2023-10-01', total: 129.99, items: ['Summer Dress', 'Designer Handbag'] },
      { id: 2, date: '2023-09-15', total: 79.99, items: ['Sports Shoes'] },
      { id: 3, date: '2023-08-20', total: 59.99, items: ['Denim Jacket'] }
  ];

  let settings = {
      notifications: true,
      newsletter: false
  };

  function toggleSetting(setting: keyof typeof settings) {
      settings[setting] = !settings[setting];
  }
</script>

<div class="container">
  <div class="profile-header">
      <i class="fas fa-user-circle profile-icon"></i>
      <h1>{username || 'Guest'}'s Profile</h1>
  </div>

  <div class="section user-info">
      <div class="section-header">
          <i class="fas fa-user"></i>
          <h2>User Information</h2>
      </div>
      <p><strong>Username:</strong> {username || 'Guest'}</p>
      <p><strong>Email:</strong> {email || 'Not provided'}</p>
      <p><strong>Phone:</strong> {user.phone}</p>
      <p><strong>Address:</strong> {user.address}</p>
  </div>

  <div class="section order-history">
      <div class="section-header">
          <i class="fas fa-shopping-cart"></i>
          <h2>Order History</h2>
      </div>
      {#each orderHistory as order}
          <div class="order-history-item">
              <h3>Order #{order.id} - {order.date}</h3>
              <p><strong>Total:</strong> ${order.total.toFixed(2)}</p>
              <p><strong>Items:</strong> {order.items.join(', ')}</p>
          </div>
      {/each}
  </div>

  <div class="section settings">
      <div class="section-header">
          <i class="fas fa-cog"></i>
          <h2>Settings</h2>
      </div>
      <div class="settings-item">
          <label>Notifications</label>
          <input type="checkbox" checked={settings.notifications} on:change={() => toggleSetting('notifications')} />
      </div>
      <div class="settings-item">
          <label>Newsletter</label>
          <input type="checkbox" checked={settings.newsletter} on:change={() => toggleSetting('newsletter')} />
      </div>
  </div>
</div>

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
  .profile-header {
      display: flex;
      align-items: center;
      margin-bottom: 30px;
  }
  .profile-icon {
      font-size: 80px;
      color: #e91e63;
      border-radius: 50%;
      margin-right: 20px;
      line-height: 80px;
      text-align: center;
  }
  .profile-header h1 {
      font-size: 2rem;
      color: #333;
  }
  .section {
      background: #fff;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      margin-bottom: 20px;
  }
  .section-header {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
  }
  .section-header i {
      font-size: 1.5rem;
      margin-right: 10px;
      color: #e91e63;
  }
  .section-header h2 {
      font-size: 1.5rem;
      color: #333;
  }
  .user-info p, .order-history p, .settings p {
      font-size: 1rem;
      color: #666;
      margin-bottom: 5px;
  }
  .order-history-item {
      border-bottom: 1px solid #ddd;
      padding: 10px 0;
      margin-bottom: 10px;
  }
  .order-history-item:last-child {
      border-bottom: none;
      margin-bottom: 0;
  }
  .order-history-item h3 {
      font-size: 1.25rem;
      color: #333;
      margin-bottom: 5px;
  }
  .order-history-item p {
      font-size: 1rem;
      color: #666;
      margin-bottom: 5px;
  }
  .settings-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #ddd;
  }
  .settings-item:last-child {
      border-bottom: none;
  }
  .settings-item label {
      font-size: 1rem;
      color: #333;
  }
  .settings-item input[type='checkbox'] {
      width: 20px;
      height: 20px;
  }
</style>