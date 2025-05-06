<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    let email = '';
    let username = '';
    let password = '';
    let confirmPassword = '';
    let errors = { email: '', username: '', password: '', confirmPassword: '' };
    let isSignUp = false;
    let toastMessage = '';
    let toastType: 'success' | 'error' | '' = '';
    const dispatch = createEventDispatcher();

    function showToast(message: string, type: 'success' | 'error') {
        toastMessage = message;
        toastType = type;
        setTimeout(() => {
            toastMessage = '';
            toastType = '';
        }, 3000);
    }

    function validateForm() {
        errors = { email: '', username: '', password: '', confirmPassword: '' };
        let isValid = true;

        // Username validation (3-20 alphanumeric characters)
        if (!username) {
            errors.username = 'Username is required';
            isValid = false;
        } else if (!/^[a-zA-Z0-9]{3,20}$/.test(username)) {
            errors.username = 'Username must be 3-20 alphanumeric characters';
            isValid = false;
        }

        // Password validation (at least 8 characters, with letters and numbers)
        if (!password) {
            errors.password = 'Password is required';
            isValid = false;
        } else if (password.length < 8 || !/[A-Za-z]/.test(password) || !/[0-9]/.test(password)) {
            errors.password = 'Password must be at least 8 characters with letters and numbers';
            isValid = false;
        }

        if (isSignUp) {
            // Email validation
            if (!email) {
                errors.email = 'Email is required';
                isValid = false;
            } else if (!/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(email)) {
                errors.email = 'Invalid email address';
                isValid = false;
            }

            // Confirm password validation
            if (!confirmPassword) {
                errors.confirmPassword = 'Please confirm your password';
                isValid = false;
            } else if (password !== confirmPassword) {
                errors.confirmPassword = 'Passwords do not match';
                isValid = false;
            }
        }

        return isValid;
    }

    async function handleSubmit() {
        if (validateForm()) {
            // Placeholder for API call
            try {
                // Simulating API response (replace with actual API endpoint when available)
                const mockResponse = {
                    ok: true,
                    json: async () => ({
                        message: isSignUp ? 'User created successfully' : 'Authentication successful',
                        user_id: '123',
                        username
                    })
                };

                const result = await mockResponse.json();

                if (mockResponse.ok) {
                    showToast(result.message, 'success');
                    if (!isSignUp) {
                        dispatch('authenticated', { user_id: result.user_id, username: result.username });
                    } else {
                        toggleForm(); // Switch to sign-in after sign-up
                    }
                } else {
                    showToast(`Error: ${result.error}`, 'error');
                }
            } catch (error) {
                showToast('Error: Failed to connect to server', 'error');
                console.error('Error:', error);
            }
        } else {
            showToast('Please fix form errors', 'error');
        }
    }

    function toggleForm() {
        isSignUp = !isSignUp;
        email = '';
        username = '';
        password = '';
        confirmPassword = '';
        errors = { email: '', username: '', password: '', confirmPassword: '' };
    }
</script>

<div class="form-container">
    {#if toastMessage}
        <div class="toast" class:success={toastType === 'success'} class:error={toastType === 'error'}>
            {toastMessage}
        </div>
    {/if}
    <h1>{isSignUp ? 'Sign Up' : 'Sign In'}</h1>
    <p class="subtitle">{isSignUp ? 'Join AuthLux today' : 'Welcome back to AuthLux'}</p>
    <form on:submit|preventDefault={handleSubmit}>
        {#if isSignUp}
            <div class="form-group">
                <label for="email">Email</label>
                <input id="email" type="email" bind:value={email} placeholder="Enter your email" />
                {#if errors.email}
                    <div class="error">{errors.email}</div>
                {/if}
            </div>
        {/if}
        <div class="form-group">
            <label for="username">Username</label>
            <input id="username" type="text" bind:value={username} placeholder="Enter your username" />
            {#if errors.username}
                <div class="error">{errors.username}</div>
            {/if}
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input id="password" type="password" bind:value={password} placeholder={isSignUp ? 'Create a password' : 'Enter your password'} />
            {#if errors.password}
                <div class="error">{errors.password}</div>
            {/if}
        </div>
        {#if isSignUp}
            <div class="form-group">
                <label for="confirm-password">Confirm Password</label>
                <input id="confirm-password" type="password" bind:value={confirmPassword} placeholder="Confirm your password" />
                {#if errors.confirmPassword}
                    <div class="error">{errors.confirmPassword}</div>
                {/if}
            </div>
        {/if}
        <button type="submit">{isSignUp ? 'Sign Up' : 'Sign In'}</button>
    </form>
    <div class="text-center">
        <p>
            {isSignUp ? 'Already have an account?' : "Don't have an account?"}
            <a href="#" on:click={toggleForm}>{isSignUp ? 'Sign In' : 'Sign Up'}</a>
        </p>
    </div>
</div>

<style>
    .form-container {
        max-width: 480px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.6s ease-out;
        backdrop-filter: blur(10px);
        position: relative;
    }

    .toast {
        position: absolute;
        top: 10px;
        right: 10px;
        padding: 10px 20px;
        border-radius: 8px;
        color: white;
        font-size: 0.9rem;
        animation: fadeInOut 0.3s ease-in;
        z-index: 1000;
    }

    .toast.success {
        background-color: #22c55e; /* Green for success */
    }

    .toast.error {
        background-color: #ef4444; /* Red for error */
    }

    @keyframes fadeInOut {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }

    .form-group {
        margin-bottom: 1.8rem;
    }

    .form-group label {
        display: block;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }

    .form-group input {
        width: 100%;
        padding: 0.9rem;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        font-size: 1rem;
        background: #f9fafb;
        transition: all 0.3s ease;
    }

    .form-group input:focus {
        outline: none;
        border-color: #a78bfa;
        box-shadow: 0 0 0 4px rgba(167, 139, 250, 0.2);
        background: #ffffff;
    }

    .form-group input::placeholder {
        color: #9ca3af;
    }

    .form-group .error {
        color: #ef4444;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    button {
        width: 100%;
        padding: 1rem;
        background: linear-gradient(90deg, #a78bfa, #ec4899);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(167, 139, 250, 0.3);
    }

    button:hover {
        background: linear-gradient(90deg, #ec4899, #a78bfa);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(167, 139, 250, 0.5);
    }

    button:active {
        transform: translateY(0);
    }

    .text-center {
        text-align: center;
        margin-top: 1.5rem;
        color: #6b7280;
        font-size: 0.95rem;
    }

    .text-center a {
        color: #a78bfa;
        font-weight: 600;
        text-decoration: none;
        transition: color 0.3s ease;
    }

    .text-center a:hover {
        color: #ec4899;
        text-decoration: underline;
    }

    @media (max-width: 480px) {
        .form-container {
            padding: 1.5rem;
        }

        h1 {
            font-size: 2rem;
        }

        .subtitle {
            font-size: 0.9rem;
        }

        button {
            font-size: 1rem;
        }
    }
</style>