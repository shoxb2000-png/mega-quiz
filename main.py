import os
from telegram.ext import Application
from supabase import create_client

# Supabase ulanish sozlamalari
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_ID = 8177774841

# Foydalanuvchi ma'lumotlarini olish yoki yaratish
def get_or_create_user(user_id):
    user = supabase.table("users").select("*").eq("user_id", user_id).execute()
    if not user.data:
        # Yangi foydalanuvchini bazaga qo'shish
        return supabase.table("users").insert({"user_id": user_id}).execute().data[0]
    return user.data[0]

# Reklama yuborish imkoniyatini tekshirish
def can_user_post(user_id):
    user = get_or_create_user(user_id)
    settings = supabase.table("settings").select("*").eq("id", 1).execute().data[0]

    if user['is_banned']: return False, "Siz bloklangansiz."
    if settings['is_blocked']: return False, "Admin reklama yuborishni taqiqlagan."
    
    # VIP tekshiruvi (4 soat)
    # ... bu yerga time logic qo'shiladi
    return True, "OK"
