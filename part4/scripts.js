document.addEventListener('DOMContentLoaded', () => {

    // ── UTILITY: Retrieve a cookie by its name ──
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return null;
    }

    // ── UTILITY: Check if user is logged in ──
    function checkAuth() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
        if (loginLink) {
            if (token) {
                loginLink.textContent = 'Logout';
                loginLink.href = '#';
                loginLink.addEventListener('click', () => {
                    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                    window.location.href = 'login.html';
                });
            } else {
                loginLink.textContent = 'Login';
                loginLink.href = 'login.html';
            }
        }
        return token;
    }

    // ── LOGIN FORM ──
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
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

    // ── INDEX PAGE : list of places ──
    const placesList = document.getElementById('places-list');
    if (placesList) {
        const token = checkAuth();

        fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        })
        .then(response => response.json())
        .then(places => {
            const priceFilter = document.getElementById('price-filter');
            priceFilter.innerHTML = `
                <option value="all">All prices</option>
                <option value="50">Max $50</option>
                <option value="100">Max $100</option>
                <option value="200">Max $200</option>
            `;

            function displayPlaces(placesToShow) {
                placesList.innerHTML = '';
                if (placesToShow.length === 0) {
                    placesList.innerHTML = '<p>No places found.</p>';
                    return;
                }
                placesToShow.forEach(place => {
                    const card = document.createElement('div');
                    card.className = 'place-card';
                    card.innerHTML = `
                        <h3>${place.title}</h3>
                        <p class="price">$${place.price} / night</p>
                        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                    `;
                    placesList.appendChild(card);
                });
            }

            displayPlaces(places);

            priceFilter.addEventListener('change', () => {
                const maxPrice = priceFilter.value;
                if (maxPrice === 'all') {
                    displayPlaces(places);
                } else {
                    const filtered = places.filter(p => p.price <= parseInt(maxPrice));
                    displayPlaces(filtered);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching places:', error);
            placesList.innerHTML = '<p>Error loading places. Please try again.</p>';
        });
    }

}); // ← closure DOMContentLoaded