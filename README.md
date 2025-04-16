# 🎬 Movie Recommender System

Un sistema de recomendación de películas con Django que incluye:
- Motor de recomendación híbrido (colaborativo + basado en contenido)
- Sistema completo de reseñas y calificaciones
- Gestión de listas de seguimiento personalizadas

## 🌟 Características principales

### 🎥 Módulo de Películas
- Modelo completo con actores, directores y géneros
- Búsqueda y filtrado avanzado
- Calificaciones promedio automáticas

### ✨ Módulo de Reseñas
- Reseñas con puntuación múltiple (historia, actuación, cinematografía)
- Sistema de votación (útil/no útil)
- Comentarios y discusiones
- Badges y logros para usuarios

### 📋 Módulo de Watchlists
- Listas personalizables (ej: "Para ver", "Favoritas")
- Seguimiento de estado (pendiente/viendo/vista)
- Colaboración entre usuarios
- Notas y prioridades por película

## 🛠️ Tecnologías utilizadas

- **Backend**: Django 5.0 + Python 3.10+
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Otras librerías**: Pillow (manejo de imágenes)

## 🚀 Instalación

1. **Clonar repositorio**:
   ```bash
   git clone https://github.com/<tu-usuario>/movie_recommender.git
   cd movie_recommender
Configurar entorno virtual:

bash
Copy
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instalar dependencias:

bash
Copy
pip install -r src/requirements.txt
Configurar base de datos:

bash
Copy
cd src
python manage.py migrate
python manage.py seed_data
Ejecutar servidor:

bash
Copy
python manage.py runserver
Acceder al sistema:

Copy
http://localhost:8000
📊 Estructura del proyecto
Copy
movie_recommender/
├── src/                     # Código fuente principal
│   ├── config/              # Configuración Django
│   ├── movies/              # App de películas y recomendaciones
│   ├── reviews/             # Sistema de reseñas
│   ├── watchlists/          # Gestión de listas
│   ├── static/              # Archivos estáticos
│   ├── templates/           # Plantillas base
│   ├── manage.py
│   └── requirements.txt
├── .gitignore
└── README.md
🧑‍💻 Comandos útiles
Crear superusuario:

bash
Copy
python manage.py createsuperuser
Generar datos de prueba:

bash
Copy
python manage.py seed_data
Ejecutar tests:

bash
Copy
python manage.py test movies reviews watchlists
📝 Licencia
Este proyecto está bajo licencia MIT. Ver LICENSE para más detalles.

👨‍💻 Desarrollado por Alexandro Alarcon
📧 Contacto: alexandro.alarcon@tecsup.edu.pe
🔗 Repositorio: https://github.com/xlexandr0/MRV-LAB05.git