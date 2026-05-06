import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carga los secretos de tu archivo .env
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Si falta algún dato, nos avisa en la consola
if not url or not key:
    print("⚠️ Error: Faltan credenciales de Supabase en el .env")

# Crea el puente de conexión y lo exporta con el nombre "supabase"
supabase: Client = create_client(url, key)