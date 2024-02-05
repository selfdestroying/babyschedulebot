import os

from supabase import Client, create_client

from src.config import conf

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(conf.supabase.url, conf.supabase.key)
