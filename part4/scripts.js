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
        const images = ['house1.jpg', 'house2.jpg','house3.jpg','house5.jpg'];

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
                placesToShow.forEach((place, index) => {
                    const card = document.createElement('div');
                    card.className = 'place-card';
                    const image = images[index % images.length];
                    card.innerHTML = `
                        <img src="${image}" alt="${place.title}">
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

    // ── PLACE DETAILS PAGE ──
    const placeDetails = document.getElementById('place-details');

    if (placeDetails) {
        checkAuth();

        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');

        if (!placeId) {
            placeDetails.innerHTML = '<p>Place not found.</p>';
        } else {
            const token = getCookie('token');

            fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            })
            .then(response => response.json())
            .then(place => {
                placeDetails.innerHTML = `
                    <img src="house1.jpg" alt="${place.title}" style="width:100%; height:300px; object-fit:cover; border-radius:10px 10px 0 0;">
                    <div class="place-info">
                        <h2>${place.title}</h2>
                        <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}</p>
                        <p><strong>Price:</strong> $${place.price} / night</p>
                        <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
                        <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
                        <p><strong>Amenities:</strong> ${place.amenities && place.amenities.length > 0 ? place.amenities.map(a => a.name).join(', ') : 'None'}</p>
                    </div>
                `;

                const addReviewSection = document.getElementById('add-review');
                if (addReviewSection) {
                    addReviewSection.style.display = token ? 'block' : 'none';
                }

                const reviewsSection = document.getElementById('reviews');
                fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
                    method: 'GET',
                    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
                })
                .then(response => response.json())
                .then(reviews => {
                    if (reviews.length === 0) {
                        reviewsSection.innerHTML = '<h2>Reviews</h2><p>No reviews yet.</p>';
                    } else {
                        reviewsSection.innerHTML = '<h2>Reviews</h2>';
                        reviews.forEach(review => {
                            const card = document.createElement('div');
                            card.className = 'review-card';
                            card.innerHTML = `
                                <p>${review.text}</p>
                                <p class="rating">Rating: ${'⭐'.repeat(review.rating)}</p>
                            `;
                            reviewsSection.appendChild(card);
                        });
                    }
                });
            })
            .catch(error => {
                console.error('Error:', error);
                placeDetails.innerHTML = '<p>Error loading place details.</p>';
            });
        }
    }

    // ── REVIEW FORM in place.html ──
    const placeReviewForm = document.getElementById('place-review-form');

    if (placeReviewForm) {
        const reviewToken = getCookie('token');
        const reviewUrlParams = new URLSearchParams(window.location.search);
        const reviewPlaceId = reviewUrlParams.get('id');

        placeReviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const text = document.getElementById('review-text').value;
            const rating = parseInt(document.getElementById('rating').value);

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${reviewToken}`
                    },
                    body: JSON.stringify({
                        text: text,
                        rating: rating,
                        place_id: reviewPlaceId,
                        user_id: 'will be overridden'
                    })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    window.location.reload();
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.error || 'Failed to submit review'}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

    // ── ADD REVIEW PAGE ──
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        const reviewPageToken = getCookie('token');

        if (!reviewPageToken) {
            window.location.href = 'login.html';
        }

        const reviewPageUrlParams = new URLSearchParams(window.location.search);
        const reviewPagePlaceId = reviewPageUrlParams.get('id');

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review');
            const ratingSelect = document.getElementById('rating');

            const text = reviewText ? reviewText.value : '';
            const rating = ratingSelect ? parseInt(ratingSelect.value) : 5;

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${reviewPageToken}`
                    },
                    body: JSON.stringify({
                        text: text,
                        rating: rating,
                        place_id: reviewPagePlaceId,
                        user_id: 'will be overridden'
                    })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    window.location.href = `place.html?id=${reviewPagePlaceId}`;
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.error || 'Failed to submit review'}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

}); // ← closure DOMContentLoaded