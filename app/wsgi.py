# app/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings') # Ensure this matches your project name

application = get_wsgi_application()
app = application  # Add this for Vercel