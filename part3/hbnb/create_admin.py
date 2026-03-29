from app import create_app
from app.services import facade

app = create_app()

with app.app_context():
    # Vérifie si l'admin existe déjà
    existing = facade.get_user_by_email('admin@hbnb.com')
    if not existing:
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'HBnB',
            'email': 'admin@hbnb.com',
            'password': 'Admin-1234',
            'is_admin': True
        }
        admin = facade.create_user(admin_data)
        print(f"Admin créé : {admin.id}")
    else:
        print(f"Admin déjà existant : {existing.id}")

app.run(debug=True)