document.addEventListener('DOMContentLoaded', () => {

    // ── LOGIN FORM ──
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // stop the form from submitting normally

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // store the token in a cookie (you can also use localStorage if you prefer)
                    document.cookie = `token=${data.access_token}; path=/`;
                    // redirect to the homepage
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed. Please check your credentials.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

});