"""
Script para inicializar la base de datos con datos de prueba
Uso: python manage.py shell < init_database.py
"""

from django.utils import timezone
from datetime import timedelta
from apps.core.models import Location, BusinessPartner, SmartDevice, Compartment
from apps.authentication.models import User
from apps.products.models import FoodCategory, Product
from apps.analytics.models import DailyStatistics

# Crear superusuario
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@foodloopbox.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
        'is_verified': True,
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("✓ Superusuario creado: admin")

# Crear usuarios de prueba
test_users = [
    {'username': 'cliente1', 'email': 'cliente1@foodloopbox.com', 'role': 'customer', 'first_name': 'Juan'},
    {'username': 'cliente2', 'email': 'cliente2@foodloopbox.com', 'role': 'customer', 'first_name': 'María'},
    {'username': 'aliado1', 'email': 'aliado1@foodloopbox.com', 'role': 'partner', 'first_name': 'Restaurante'},
]

for user_data in test_users:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'role': user_data['role'],
            'is_verified': True,
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"✓ Usuario creado: {user_data['username']}")

# Crear ubicaciones
locations_data = [
    {
        'name': 'Centro Comercial Hayuelos',
        'location_type': 'commercial_center',
        'address': 'Carrera 81 #10-10',
        'city': 'Bogotá',
        'postal_code': '110811',
        'latitude': 4.635,
        'longitude': -74.133,
        'phone': '(1) 6237700',
        'email': 'info@hayuelos.com'
    },
    {
        'name': 'Restaurante El Buen Sabor',
        'location_type': 'restaurant',
        'address': 'Carrera 7 #45-12',
        'city': 'Bogotá',
        'postal_code': '110111',
        'latitude': 4.710,
        'longitude': -74.009,
        'phone': '(1) 3124567',
        'email': 'contact@buensabor.com'
    },
]

locations = {}
for loc_data in locations_data:
    location, created = Location.objects.get_or_create(
        name=loc_data['name'],
        defaults=loc_data
    )
    locations[loc_data['name']] = location
    if created:
        print(f"✓ Ubicación creada: {loc_data['name']}")

# Crear aliados
partners_data = [
    {
        'name': 'Restaurante Colombiano',
        'partner_type': 'restaurant',
        'location_name': 'Restaurante El Buen Sabor',
        'contact_person': 'Carlos García',
        'email': 'carlos@buensabor.com',
        'phone': '3001234567',
        'business_id': 'BUS001',
    },
]

for partner_data in partners_data:
    location = locations.get(partner_data.pop('location_name'))
    if location:
        partner, created = BusinessPartner.objects.get_or_create(
            name=partner_data['name'],
            defaults={**partner_data, 'location': location}
        )
        if created:
            print(f"✓ Aliado creado: {partner_data['name']}")

# Crear dispositivos inteligentes
devices_data = [
    {
        'device_id': 'FLB-001',
        'location_name': 'Centro Comercial Hayuelos',
        'total_compartments': 9,
        'available_compartments': 9,
    },
]

for device_data in devices_data:
    location = locations.get(device_data.pop('location_name'))
    if location:
        device, created = SmartDevice.objects.get_or_create(
            device_id=device_data['device_id'],
            defaults={**device_data, 'location': location}
        )
        if created:
            # Crear compartimientos
            for i in range(1, device_data['total_compartments'] + 1):
                Compartment.objects.create(
                    device=device,
                    compartment_number=i,
                    status='available',
                    temperature_setpoint=4.0
                )
            print(f"✓ Dispositivo creado: {device_data['device_id']} con {device_data['total_compartments']} compartimientos")

# Crear categorías de alimentos
categories_data = [
    'Frutas',
    'Verduras',
    'Productos Lácteos',
    'Carnes',
    'Pan y Repostería',
    'Bebidas',
]

categories = {}
for cat_name in categories_data:
    category, created = FoodCategory.objects.get_or_create(
        name=cat_name,
        defaults={'description': f'Categoría: {cat_name}'}
    )
    categories[cat_name] = category
    if created:
        print(f"✓ Categoría creada: {cat_name}")

# Crear productos de prueba
client = User.objects.filter(username='cliente1').first()
aliado = BusinessPartner.objects.first()

if aliado and client:
    products_data = [
        {
            'name': 'Arepa de Queso',
            'category': 'Pan y Repostería',
            'quantity': 5,
            'unit': 'unit',
            'original_price': 15000,
            'discounted_price': 7500,
            'product_type': 'sale',
            'expiration_date': timezone.now() + timedelta(hours=6),
        },
        {
            'name': 'Sopa del Día',
            'category': 'Comida',
            'quantity': 3,
            'unit': 'L',
            'product_type': 'donation',
            'expiration_date': timezone.now() + timedelta(hours=4),
        },
    ]
    
    for prod_data in products_data:
        category = categories.get(prod_data.pop('category'))
        if category:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                provider=aliado,
                defaults={
                    **prod_data,
                    'category': category,
                    'registered_by': client,
                }
            )
            if created:
                print(f"✓ Producto creado: {prod_data['name']}")

# Crear estadísticas diarias
today = timezone.now().date()
stats, created = DailyStatistics.objects.get_or_create(
    date=today,
    defaults={
        'total_products_registered': 10,
        'total_products_donated': 3,
        'total_products_sold': 7,
        'total_weight_rescued': 25.5,
        'total_transactions': 5,
        'total_amount': 50000,
    }
)
if created:
    print(f"✓ Estadísticas diarias creadas para {today}")

print("\n✅ Base de datos inicializada exitosamente!")
print("\nCredenciales de prueba:")
print("  - Admin: admin / admin123")
print("  - Cliente: cliente1 / test123")
print("  - Aliado: aliado1 / test123")
