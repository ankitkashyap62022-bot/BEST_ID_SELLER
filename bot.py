import logging
import re
import threading
import time
import random
import sys
import os
from datetime import datetime, timedelta
from bson import ObjectId
import asyncio

# Event loop initialization
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Simple fix
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import telebot.types

@classmethod
def _disable_story(cls, obj):
    # Telegram stories completely ignored
    return None

telebot.types.Story.de_json = _disable_story
from pymongo import MongoClient
import os
import requests
from pyrogram import Client, enums
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid,
    PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid,
    FloodWait, PhoneCodeEmpty
)

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

BOT_TOKEN = os.getenv('BOT_TOKEN', '<emoji id=5354924568492383911>😈</emoji> **8765933531:ᴀᴀꜰᴍʏᴍᴛᴡꞯᴛ0ᴋᴇᴏᴩᴅʀ3ᴇᴄᴊᴩ21ᴋʜꜱᴡʏᴇᴢꞯ--ᴋ**')
ADMIN_ID = int(os.getenv('ADMIN_ID', '<emoji id=6307553838073124532>✨</emoji> **8394041476**'))
MONGO_URL = os.getenv('MONGO_URL', '<emoji id=6309640268761011366>🌙</emoji> **ᴍᴏɴɢᴏᴅʙ+ꜱʀᴠ://ʙꜱᴅᴋ:ʙᴇᴛɪᴄʜᴏᴅ@ᴄʟᴜꜱᴛᴇʀ0.ꜰɢᴊ1ʀ9ᴢ.ᴍᴏɴɢᴏᴅʙ.ɴᴇᴛ/?ʀᴇᴛʀʏᴡʀɪᴛᴇꜱ=ᴛʀᴜᴇ&ᴡ=ᴍᴀᴊᴏʀɪᴛʏ**')
API_ID = int(os.getenv('API_ID', '<emoji id=5280606902533783431>😽</emoji> **36326629**'))
API_HASH = os.getenv('API_HASH', '<emoji id=6151981777490548710>✅</emoji> **823ᴇ6ᴇ8ᴄ081ꜰᴇ363ᴇ6ᴅ739ʙ39ᴅᴄ19ᴇ07**')

# Multiple owners support (up to 5, comma-separated in OWNER_IDS env var)
# e.g. OWNER_IDS=8316947415,6509168409,987654321
_raw_owner_ids = os.getenv('OWNER_IDS', '')
OWNER_IDS = [int(x.strip()) for x in _raw_owner_ids.split(',') if x.strip().isdigit()]
if ADMIN_ID not in OWNER_IDS:
    OWNER_IDS.insert(0, ADMIN_ID)
OWNER_IDS = OWNER_IDS[:5]  # Max 5 owners

# Recharge QR and UPI settings (configurable via env vars)
QR_IMAGE_URL = os.getenv('QR_IMAGE_URL', '<emoji id=5352870513267973607>✨</emoji> **ʜᴛᴛᴩꜱ://ꜰɪʟᴇꜱ.ᴄᴀᴛʙᴏx.ᴍᴏᴇ/0ᴍᴋʀ56.ᴊᴩᴇɢ**')
UPI_ID = os.getenv('UPI_ID', '<emoji id=6111390922044344694>✅</emoji> **ꜱʜᴜʙʜ412@ꜰᴀᴍ**')

# MUST JOIN CHANNELS - TWO CHANNELS
MUST_JOIN_CHANNEL_1 = "<emoji id=6307821174017496029>🔥</emoji> **@ʙᴇꜱᴛ_ᴏᴛᴩ_ɢʀᴏᴜᴩ_ꜱᴜᴩᴩᴏʀᴛ**"
MUST_JOIN_CHANNEL_2 = "<emoji id=6154635934135490309>💗</emoji> **@ɢᴍꜱ_ᴄᴏᴍᴇʙᴀᴄᴋ_ꜱᴏᴏɴ**"
# LOG CHANNEL
LOG_CHANNEL_ID = "<emoji id=6111418418424973677>✅</emoji> **-1003795881392**"

# Referral commission percentage
REFERRAL_COMMISSION = 1.5

# Global API Credentials for Pyrogram Login
GLOBAL_API_ID = 36326629
GLOBAL_API_HASH = "<emoji id=5280904324724063665>😽</emoji> **823ᴇ6ᴇ8ᴄ081ꜰᴇ363ᴇ6ᴅ739ʙ39ᴅᴄ19ᴇ07**"

# Premium account session string (for sending premium custom emoji)
PREMIUM_SESSION = os.getenv('PREMIUM_SESSION', '<emoji id=5040016479722931047>✨</emoji> **ᴀɢꜰᴡʏᴢ4ᴀᴩᴩᴅʀɪꞯᴩᴠʏɪꜰᴄɴ92ᴡᴇɢᴍꜰx0ᴢᴊᴜᴡᴀ8ʏᴡᴄᴊ0ʟᴏᴠᴠᴍᴏᴡʜ7ᴠᴏᴍxᴅɴᴏ4ᴠ71-ᴜɴᴛꞯᴊʏꜱʜᴅᴠ-ᴛᴋᴛꜱᴇᴏᴊʙᴋᴢʀɴ9ᴡᴡᴇ6ᴋᴛᴊʜʙᴢᴛꜱʙᴇ-ᴇᴩᴄɢ5ᴠʙᴏɪ4ɪᴄʀᴍᴠʏᴏʀᴋ1ᴏᴋʙ1ꞯꜱɪᴜᴠʙᴊᴩꞯᴄᴅᴅɴᴛ07ᴍʏʟɪ4ᴇ96xᴀᴠᴊᴍʙᴛᴡᴜ94ᴍ0ɢꞯ14ɪᴜᴠᴩɢᴍᴢʙᴋꜱʀᴜᴛᴊʙʙᴅᴛᴠɢʙɴᴏʏʙᴡᴀᴀɢᴇᴏɴᴍꞯɴʟᴀᴋᴋ4xꜱᴇᴢᴠʏ0ʀᴏ9ᴏʙᴛᴛʜ6ɢᴡʟᴩᴢʀꜰ4ꜰᴋᴩᴩʀ5ʙxᴛ7ɴɢᴋ-ʟꜱʀᴅᴋᴊʙ0ᴀᴠᴠᴇᴅᴡ_ʜᴇᴀᴢᴛꞯᴢᴀ5ᴇᴀᴄʟᴍᴢʏꜰᴩʟᴡʙᴋʙ4ᴩᴢꜱʙɴᴍxʜɢᴢ_ꜱᴢᴀᴍꞯᴊʀ4ᴊꜱꞯʟᴠᴏᴅxꞯɴᴀɢ_ᴋɴᴩʜꞯᴋᴊᴋʟʀᴍᴩꜱʏᴩꜰᴅ8-ꞯ0ᴢ6ɪ_ᴏᴄᴠᴄ4ᴊᴠᴀᴇᴀᴀᴀᴀᴀʜꞯᴡ472ᴀᴀ**')

# Premium custom emoji constants (Pyrogram HTML format)
E_DEVIL    = "<emoji id=6307569802466563145>🎶</emoji> **<ᴇᴍᴏᴊɪ ɪᴅ='5352542184493031170'>😈</ᴇᴍᴏᴊɪ>**"
E_CROWN    = "<emoji id=6154635934135490309>💗</emoji> **<ᴇᴍᴏᴊɪ ɪᴅ='6307750079423845494'>👑</ᴇᴍᴏᴊɪ>**"
E_DIAMOND  = "<emoji id=6307568836098922002>🌙</emoji> **<ᴇᴍᴏᴊɪ ɪᴅ='4929195195225867512'>💎</ᴇᴍᴏᴊɪ>**"
E_BUTTERFLY= "<emoji id=5999210495146465994>💖</emoji> **<ᴇᴍᴏᴊɪ ɪᴅ='6307643744623531146'>🦋</ᴇᴍᴏᴊɪ>**"
E_MAGIC    = "<emoji id=5285100774060227768>😽</emoji> **<ᴇᴍᴏᴊɪ ɪᴅ='5352870513267973607'>✨</ᴇᴍᴏᴊɪ>**"
E_HEART    = "<emoji id=5280904324724063665>😽</emoji> **<ᴇᴍᴏᴊɪ ɪᴅ='6123125485661591081'>🩷</ᴇᴍᴏᴊɪ>**"

# ---------------------------------------------------------------------
# INIT
# ---------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='<emoji id=5999340396432333728>☺️</emoji> **%(ᴀꜱᴄᴛɪᴍᴇ)ꜱ - %(ʟᴇᴠᴇʟɴᴀᴍᴇ)ꜱ - %(ᴍᴇꜱꜱᴀɢᴇ)ꜱ**')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)

# MongoDB Setup
try:
    client = MongoClient(MONGO_URL, tlsAllowInvalidCertificates=True)
    db = client['otp_bot']
    users_col = db['users']
    accounts_col = db['accounts']
    orders_col = db['orders']
    wallets_col = db['wallets']
    recharges_col = db['recharges']
    otp_sessions_col = db['otp_sessions']
    referrals_col = db['referrals']
    countries_col = db['countries']
    banned_users_col = db['banned_users']
    transactions_col = db['transactions']
    coupons_col = db['coupons']
    admins_col = db['admins']  # New collection for multiple admins
    logger.info("<emoji id=5395580801930771895>🤍</emoji> **✅ ᴍᴏɴɢᴏᴅʙ ᴄᴏɴɴᴇᴄᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ**")
except Exception as e:
    logger.error(f"<emoji id=6152142357727811958>🦋</emoji> **❌ ᴍᴏɴɢᴏᴅʙ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ꜰᴀɪʟᴇᴅ: {ᴇ}**")

# Store temporary data
user_states = {}
pending_messages = {}
active_chats = {}
user_stage = {}
user_last_message = {}
user_orders = {}
order_messages = {}
cancellation_trackers = {}
order_timers = {}
change_number_requests = {}
whatsapp_number_timers = {}
payment_orders = {}
admin_deduct_state = {}
referral_data = {}
broadcast_data = {}
edit_price_state = {}
coupon_state = {}
recharge_method_state = {}
upi_payment_states = {}
admin_add_state = {}  # For /addadmin flow
admin_remove_state = {}  # For /removeadmin flow

# add this line for bordcast 
IS_BROADCASTING = False

# Pyrogram login states
login_states = {}

# BULK ADD STATES
bulk_add_states = {}

# Recharge approval tracking
recharge_approvals = {}  # Track who approved/rejected which recharge

# Import account management
try:
    from account import AccountManager
    account_manager = AccountManager(GLOBAL_API_ID, GLOBAL_API_HASH)
    logger.info("<emoji id=5999340396432333728>☺️</emoji> **✅ ᴀᴄᴄᴏᴜɴᴛ ᴍᴀɴᴀɢᴇʀ ʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ**")
except ImportError as e:
    logger.error(f"<emoji id=5999210495146465994>💖</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ᴀᴄᴄᴏᴜɴᴛ ᴍᴏᴅᴜʟᴇ: {ᴇ}**")
    account_manager = None

# Import logging module
try:
    from logs import init_logger, log_purchase_async, log_otp_received_async, log_recharge_approved_async
    init_logger(BOT_TOKEN, LOG_CHANNEL_ID)
    logger.info(f"<emoji id=6298684666182371615>❤️</emoji> **✅ ᴛᴇʟᴇɢʀᴀᴍ ʟᴏɢɢᴇʀ ɪɴɪᴛɪᴀʟɪᴢᴇᴅ ꜰᴏʀ ᴄʜᴀɴɴᴇʟ: {ʟᴏɢ_ᴄʜᴀɴɴᴇʟ_ɪᴅ}**")
except ImportError as e:
    logger.error(f"<emoji id=6307457716705040156>👍</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ʟᴏɢɢɪɴɢ ᴍᴏᴅᴜʟᴇ: {ᴇ}**")

# Async manager for background tasks
async_manager = None
if account_manager:
    async_manager = account_manager.async_manager

# Initialize admin in database
def init_admin():
    """<emoji id=6309709550878463216>🌟</emoji> **ɪɴɪᴛɪᴀʟɪᴢᴇ ᴛʜᴇ ꜰɪʀꜱᴛ ᴀᴅᴍɪɴ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ**"""
    try:
        # Check if admins collection exists and has any admins
        if 'admins' not in db.list_collection_names():
            db.create_collection('admins')

        admin_count = admins_col.count_documents({})
        if admin_count == 0:
            # Add all owners from OWNER_IDS as super admins
            for owner_id in OWNER_IDS:
                admin_data = {
                    "user_id": owner_id,
                    "added_by": "SYSTEM",
                    "added_at": datetime.utcnow(),
                    "is_super_admin": True
                }
                admins_col.update_one({"user_id": owner_id}, {"<emoji id=6224236403153179330>🎀</emoji> **$ꜱᴇᴛᴏɴɪɴꜱᴇʀᴛ**": admin_data}, upsert=True)
                logger.info(f"<emoji id=5041955142060999726>🌈</emoji> **✅ ᴏᴡɴᴇʀ {ᴏᴡɴᴇʀ_ɪᴅ} ᴀᴅᴅᴇᴅ ᴛᴏ ᴅᴀᴛᴀʙᴀꜱᴇ**")
        else:
            # Ensure all owners are always in the admins collection
            for owner_id in OWNER_IDS:
                admins_col.update_one(
                    {"user_id": owner_id},
                    {"<emoji id=5280904324724063665>😽</emoji> **$ꜱᴇᴛ**": {"is_super_admin": True, "added_by": "SYSTEM"}},
                    upsert=True
                )
    except Exception as e:
        logger.error(f"<emoji id=5280678521113443426>😽</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ɪɴɪᴛɪᴀʟɪᴢᴇ ᴀᴅᴍɪɴ: {ᴇ}**")

# Call init_admin
init_admin()

# ---------------------------------------------------------------------
# ADMIN MANAGEMENT FUNCTIONS
# ---------------------------------------------------------------------
def get_admin_info(user_id):
    """<emoji id=6307490397111195260>🦋</emoji> **ɢᴇᴛ ᴀᴅᴍɪɴ ɪɴꜰᴏ ʙʏ ᴜꜱᴇʀ ɪᴅ**"""
    try:
        # Check if it's one of the owners
        if int(user_id) in OWNER_IDS:
            user = users_col.find_one({"user_id": user_id})
            return {
                "user_id": user_id,
                "is_super_admin": True,
                "name": user.get("name", "Owner") if user else "Owner"
            }

        # Check in admins collection
        admin = admins_col.find_one({"user_id": user_id})
        if admin:
            user = users_col.find_one({"user_id": user_id})
            admin["name"] = user.get("name", "Admin") if user else "Admin"
            return admin
        return None
    except Exception as e:
        logger.error(f"<emoji id=6309666601205503867>💌</emoji> **ᴇʀʀᴏʀ ɪɴ ɢᴇᴛ_ᴀᴅᴍɪɴ_ɪɴꜰᴏ: {ᴇ}**")
        return None

def is_admin(user_id):
    """<emoji id=6111418418424973677>✅</emoji> **ᴄʜᴇᴄᴋ ɪꜰ ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴ**"""
    try:
        # Check if it's one of the owners
        if int(user_id) in OWNER_IDS:
            return True

        # Check in admins collection
        admin = admins_col.find_one({"user_id": user_id})
        return admin is not None
    except:
        return False

def is_super_admin(user_id):
    """<emoji id=6309709550878463216>🌟</emoji> **ᴄʜᴇᴄᴋ ɪꜰ ᴜꜱᴇʀ ɪꜱ ᴏɴᴇ ᴏꜰ ᴛʜᴇ ᴏᴡɴᴇʀꜱ (ꜱᴜᴩᴇʀ ᴀᴅᴍɪɴꜱ)**"""
    try:
        return int(user_id) in OWNER_IDS
    except:
        return str(user_id) == str(ADMIN_ID)

def add_admin(user_id, added_by):
    """<emoji id=4929195195225867512>💎</emoji> **ᴀᴅᴅ ᴀ ɴᴇᴡ ᴀᴅᴍɪɴ (ᴍᴀx 5 ᴀᴅᴍɪɴꜱ)**"""
    try:
        # Check if already admin
        if is_admin(user_id):
            return False, "<emoji id=4929195195225867512>💎</emoji> **ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ**"

        # Count current admins (excluding super admin if counting separately)
        admin_count = admins_col.count_documents({})
        if admin_count >= 5:
            return False, "<emoji id=6001589602085771497>✅</emoji> **ᴍᴀxɪᴍᴜᴍ 5 ᴀᴅᴍɪɴꜱ ʀᴇᴀᴄʜᴇᴅ**"

        # Add new admin
        admin_data = {
            "user_id": user_id,
            "added_by": added_by,
            "added_at": datetime.utcnow(),
            "is_super_admin": False
        }
        admins_col.insert_one(admin_data)

        # Get user info
        user = users_col.find_one({"user_id": user_id})
        username = user.get("username", "<emoji id=6307605493644793241>📒</emoji> **ɴᴏ ᴜꜱᴇʀɴᴀᴍᴇ**") if user else "Unknown"

        return True, f"<emoji id=5280721097124249567>😽</emoji> **✅ ᴀᴅᴍɪɴ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**"
    except Exception as e:
        logger.error(f"<emoji id=5280721097124249567>😽</emoji> **ᴇʀʀᴏʀ ᴀᴅᴅɪɴɢ ᴀᴅᴍɪɴ: {ᴇ}**")
        return False, f"<emoji id=5040016479722931047>✨</emoji> **ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**"

def remove_admin(user_id, removed_by):
    """<emoji id=5999041732996504081>✨</emoji> **ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ**"""
    try:
        # Check if user is admin
        admin = admins_col.find_one({"user_id": user_id})
        if not admin:
            return False, "<emoji id=5040016479722931047>✨</emoji> **ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ**"

        # Check if trying to remove an owner
        if int(user_id) in OWNER_IDS:
            return False, "<emoji id=6307447640711763730>💟</emoji> **ᴄᴀɴɴᴏᴛ ʀᴇᴍᴏᴠᴇ ᴀɴ ᴏᴡɴᴇʀ**"

        # Remove admin
        result = admins_col.delete_one({"user_id": user_id})

        if result.deleted_count > 0:
            return True, f"<emoji id=6298717844804733009>♾</emoji> **✅ ᴀᴅᴍɪɴ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**"
        else:
            return False, "<emoji id=6310044717241340733>🔄</emoji> **ꜰᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ**"
    except Exception as e:
        logger.error(f"<emoji id=6111418418424973677>✅</emoji> **ᴇʀʀᴏʀ ʀᴇᴍᴏᴠɪɴɢ ᴀᴅᴍɪɴ: {ᴇ}**")
        return False, f"<emoji id=5999340396432333728>☺️</emoji> **ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**"

def get_all_admins():
    """<emoji id=6001589602085771497>✅</emoji> **ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴀʟʟ ᴀᴅᴍɪɴꜱ**"""
    try:
        admins = list(admins_col.find({}))
        # Also include main admin if not in collection
        main_admin_exists = any(str(a.get("user_id")) == str(ADMIN_ID) for a in admins)

        admin_list = []

        # Add main admin first
        if not main_admin_exists:
            admin_list.append({
                "user_id": ADMIN_ID,
                "username": "<emoji id=5999210495146465994>💖</emoji> **ᴍᴀɪɴ ᴀᴅᴍɪɴ**",
                "name": "<emoji id=6310022800023229454>✡️</emoji> **ᴍᴀɪɴ ᴀᴅᴍɪɴ**",
                "added_at": datetime.utcnow(),
                "added_by": "SYSTEM",
                "is_super_admin": True
            })

        # Add other admins
        for admin in admins:
            user_id = admin["user_id"]
            user = users_col.find_one({"user_id": user_id})
            username = user.get("username", "<emoji id=6309640268761011366>🌙</emoji> **ɴᴏ ᴜꜱᴇʀɴᴀᴍᴇ**") if user else "Unknown"
            name = user.get("name", "Unknown") if user else "Unknown"

            admin_list.append({
                "user_id": user_id,
                "username": username,
                "name": name,
                "added_at": admin.get("added_at"),
                "added_by": admin.get("added_by"),
                "is_super_admin": admin.get("is_super_admin", False)
            })
        return admin_list
    except Exception as e:
        logger.error(f"<emoji id=5999151980512024620>🥰</emoji> **ᴇʀʀᴏʀ ɢᴇᴛᴛɪɴɢ ᴀᴅᴍɪɴꜱ: {ᴇ}**")
        return []

def get_admin_count():
    """<emoji id=5999340396432333728>☺️</emoji> **ɢᴇᴛ ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏꜰ ᴀᴅᴍɪɴꜱ**"""
    try:
        return admins_col.count_documents({}) + 1  # +1 for main admin
    except:
        return 1

# ---------------------------------------------------------------------
# ADMIN COMMAND HANDLERS
# ---------------------------------------------------------------------

@bot.message_handler(commands=['addadmin'])
def add_admin_command(msg):
    """<emoji id=6111390922044344694>✅</emoji> **ᴀᴅᴅ ᴀ ɴᴇᴡ ᴀᴅᴍɪɴ - ᴏɴʟʏ ᴍᴀɪɴ ᴀᴅᴍɪɴ ᴄᴀɴ ᴜꜱᴇ**"""
    user_id = msg.from_user.id

    # Only main admin can add admins
    if not is_super_admin(user_id):
        bot.reply_to(msg, "<emoji id=5040016479722931047>✨</emoji> **❌ ꜱɪʀꜰ ᴍᴀɪɴ ᴀᴅᴍɪɴ ʜɪ ᴀᴅᴅᴀᴅᴍɪɴ ᴜꜱᴇ ᴋᴀʀ ꜱᴀᴋᴛᴀ ʜᴀɪ!**")
        return

    # Start the add admin flow
    admin_add_state[user_id] = {"step": "waiting_user_id"}

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("<emoji id=6298717844804733009>♾</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_add_admin"))

    bot.reply_to(
        msg,
        "<emoji id=6307569802466563145>🎶</emoji> **👤 **ᴀᴅᴅ ɴᴇᴡ ᴀᴅᴍɪɴ**\ɴ\ɴ**"
        "<emoji id=5318828550940293906>🐱</emoji> **ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴜꜱᴇʀ ɪᴅ ᴏꜰ ᴛʜᴇ ᴩᴇʀꜱᴏɴ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴍᴀᴋᴇ ᴀᴅᴍɪɴ:\ɴ\ɴ**"
        "<emoji id=4929195195225867512>💎</emoji> **📝 ᴜꜱᴇʀ ɪᴅ ᴍɪʟɴᴇ ᴋᴇ ʟɪʏᴇ:\ɴ**"
        "<emoji id=6309709550878463216>🌟</emoji> **• ᴜꜱᴇʀ ᴋᴏ /ꜱᴛᴀʀᴛ ᴋᴀʀɴᴀ ʜᴏɢᴀ ʙᴏᴛ ᴍᴇɪɴ\ɴ**"
        "<emoji id=6307750079423845494>👑</emoji> **• ʏᴀ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ ꜱᴇ ᴜꜱᴇʀ ꜱᴇᴀʀᴄʜ ᴋᴀʀᴏ\ɴ\ɴ**"
        "<emoji id=6307569802466563145>🎶</emoji> **ᴇxᴀᴍᴩʟᴇ: `123456789`**",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(commands=['removeadmin'])
def remove_admin_command(msg):
    """<emoji id=6307821174017496029>🔥</emoji> **ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ - ᴏɴʟʏ ᴍᴀɪɴ ᴀᴅᴍɪɴ ᴄᴀɴ ᴜꜱᴇ**"""
    user_id = msg.from_user.id

    # Only main admin can remove admins
    if not is_super_admin(user_id):
        bot.reply_to(msg, "<emoji id=5280606902533783431>😽</emoji> **❌ ꜱɪʀꜰ ᴍᴀɪɴ ᴀᴅᴍɪɴ ʜɪ ʀᴇᴍᴏᴠᴇᴀᴅᴍɪɴ ᴜꜱᴇ ᴋᴀʀ ꜱᴀᴋᴛᴀ ʜᴀɪ!**")
        return

    # Get list of admins
    admins = get_all_admins()

    if len(admins) <= 1:  # Only main admin
        bot.reply_to(
            msg,
            "<emoji id=4929369656797431200>🪐</emoji> **📋 **ᴀᴅᴍɪɴ ʟɪꜱᴛ**\ɴ\ɴ**"
            "<emoji id=5999270482954691955>🦋</emoji> **ᴋᴏɪ ᴀᴜʀ ᴀᴅᴍɪɴ ɴᴀʜɪ ʜᴀɪ ʀᴇᴍᴏᴠᴇ ᴋᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ.\ɴ\ɴ**"
            f"<emoji id=6224236403153179330>🎀</emoji> **👑 ᴍᴀɪɴ ᴀᴅᴍɪɴ: `{ᴀᴅᴍɪɴ_ɪᴅ}`**",
            parse_mode="Markdown"
        )
        return

    # Show list of admins
    admin_list_text = "<emoji id=6307447640711763730>💟</emoji> **📋 **ᴇxɪꜱᴛɪɴɢ ᴀᴅᴍɪɴꜱ:**\ɴ\ɴ**"
    for admin in admins:
        if not admin.get("is_super_admin", False):
            admin_list_text += f"<emoji id=5999041732996504081>✨</emoji> **• `{ᴀᴅᴍɪɴ['ᴜꜱᴇʀ_ɪᴅ']}` - {ᴀᴅᴍɪɴ['ɴᴀᴍᴇ']}\ɴ**"

    admin_list_text += "<emoji id=5999041732996504081>✨</emoji> **\ɴᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴜꜱᴇʀ ɪᴅ ᴏꜰ ᴛʜᴇ ᴀᴅᴍɪɴ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ:**"

    admin_remove_state[user_id] = {"step": "waiting_user_id"}

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("<emoji id=6307457716705040156>👍</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_remove_admin"))

    bot.reply_to(
        msg,
        admin_list_text,
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ["cancel_add_admin", "cancel_remove_admin"])
def handle_cancel_admin(call):
    user_id = call.from_user.id

    if call.data == "cancel_add_admin":
        if user_id in admin_add_state:
            del admin_add_state[user_id]
        bot.edit_message_text(
            "<emoji id=5280606902533783431>😽</emoji> **❌ ᴀᴅᴅ ᴀᴅᴍɪɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.**",
            call.message.chat.id,
            call.message.message_id
        )
    elif call.data == "cancel_remove_admin":
        if user_id in admin_remove_state:
            del admin_remove_state[user_id]
        bot.edit_message_text(
            "<emoji id=6307553838073124532>✨</emoji> **❌ ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.**",
            call.message.chat.id,
            call.message.message_id
        )

@bot.message_handler(func=lambda m: m.from_user.id in admin_add_state and admin_add_state[m.from_user.id]["step"] == "waiting_user_id")
def handle_add_admin_userid(msg):
    user_id = msg.from_user.id

    try:
        target_user_id = int(msg.text.strip())

        # Check if trying to add self
        if target_user_id == user_id:
            bot.reply_to(msg, "<emoji id=6307457716705040156>👍</emoji> **❌ ᴀᴀᴩ ᴋʜᴜᴅᴋᴏ ᴀᴅᴍɪɴ ɴᴀʜɪ ʙᴀɴᴀ ꜱᴀᴋᴛᴇ! ᴀᴀᴩ ᴀʟʀᴇᴀᴅʏ ᴍᴀɪɴ ᴀᴅᴍɪɴ ʜᴏ.**")
            del admin_add_state[user_id]
            return

        # Check if user exists
        user = users_col.find_one({"user_id": target_user_id})
        if not user:
            bot.reply_to(
                msg,
                f"<emoji id=6307447640711763730>💟</emoji> **❌ ᴜꜱᴇʀ `{ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}` ᴅᴀᴛᴀʙᴀꜱᴇ ᴍᴇɪɴ ɴᴀʜɪ ᴍɪʟᴀ.\ɴ\ɴ**"
                f"<emoji id=6111778259374971023>🔥</emoji> **ᴩᴇʜʟᴇ ᴜꜱᴇʀ ᴋᴏ /ꜱᴛᴀʀᴛ ᴋᴀʀᴡᴀɪʏᴇ ʙᴏᴛ ᴍᴇɪɴ.**",
                parse_mode="Markdown"
            )
            del admin_add_state[user_id]
            return

        # Check if already admin
        if is_admin(target_user_id):
            bot.reply_to(
                msg,
                f"<emoji id=5281001756057175314>😽</emoji> **⚠️ ᴜꜱᴇʀ `{ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}` ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴ ʜᴀɪ!**",
                parse_mode="Markdown"
            )
            del admin_add_state[user_id]
            return

        # Check max admins
        admin_count = admins_col.count_documents({})
        if admin_count >= 5:
            bot.reply_to(
                msg,
                "<emoji id=5285100774060227768>😽</emoji> **❌ ᴍᴀxɪᴍᴜᴍ 5 ᴀᴅᴍɪɴꜱ ʜᴏ ᴄʜᴜᴋᴇ ʜᴀɪɴ. ᴩᴇʜʟᴇ ᴋɪꜱɪ ᴀᴅᴍɪɴ ᴋᴏ ʀᴇᴍᴏᴠᴇ ᴋᴀʀᴏ.**",
                parse_mode="Markdown"
            )
            del admin_add_state[user_id]
            return

        # Add admin
        success, message = add_admin(target_user_id, user_id)

        if success:
            # Get updated admin count
            new_count = admins_col.count_documents({})

            bot.reply_to(
                msg,
                f"<emoji id=6152142357727811958>🦋</emoji> **✅ **ᴀᴅᴍɪɴ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
                f"<emoji id=5281001756057175314>😽</emoji> **👤 ᴜꜱᴇʀ ɪᴅ: `{ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}`\ɴ**"
                f"<emoji id=5235985147265837746>🗒</emoji> **👤 ɴᴀᴍᴇ: {ᴜꜱᴇʀ.ɢᴇᴛ('ɴᴀᴍᴇ', 'ᴜɴᴋɴᴏᴡɴ')}\ɴ**"
                f"<emoji id=6309819721084573392>🌙</emoji> **📊 ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴꜱ: {ɴᴇᴡ_ᴄᴏᴜɴᴛ + 1}/6 (ᴍᴀɪɴ ᴀᴅᴍɪɴ + {ɴᴇᴡ_ᴄᴏᴜɴᴛ})\ɴ\ɴ**"
                f"<emoji id=5285100774060227768>😽</emoji> **ᴀʙ ʏᴇ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ ᴀᴄᴄᴇꜱꜱ ᴋᴀʀ ꜱᴀᴋᴛᴇ ʜᴀɪɴ!**",
                parse_mode="Markdown"
            )

            # Notify new admin
            try:
                bot.send_message(
                    target_user_id,
                    f"<emoji id=6001132493011425597>💖</emoji> **🎉 **ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ! ʏᴏᴜ'ᴠᴇ ʙᴇᴇɴ ᴩʀᴏᴍᴏᴛᴇᴅ ᴛᴏ ᴀᴅᴍɪɴ!**\ɴ\ɴ**"
                    f"<emoji id=5998881015320287132>💊</emoji> **ᴀʙ ᴀᴀᴩ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ ᴜꜱᴇ ᴋᴀʀ ꜱᴀᴋᴛᴇ ʜᴀɪɴ:\ɴ**"
                    f"<emoji id=5999151980512024620>🥰</emoji> **• ʀᴇᴄʜᴀʀɢᴇ ᴀᴩᴩʀᴏᴠᴇ/ʀᴇᴊᴇᴄᴛ\ɴ**"
                    f"<emoji id=5899776109548934640>💲</emoji> **• ᴀᴅᴅ/ʀᴇᴍᴏᴠᴇ ᴄᴏᴜɴᴛʀɪᴇꜱ\ɴ**"
                    f"<emoji id=6310022800023229454>✡️</emoji> **• ᴀᴅᴅ ᴀᴄᴄᴏᴜɴᴛꜱ\ɴ**"
                    f"<emoji id=5280904324724063665>😽</emoji> **• ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇꜱ\ɴ**"
                    f"<emoji id=6001132493011425597>💖</emoji> **• ᴀɴᴅ ᴍᴏʀᴇ!\ɴ\ɴ**"
                    f"<emoji id=6111742817304841054>✅</emoji> **ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ ᴋᴇ ʟɪʏᴇ /ꜱᴛᴀʀᴛ ᴋᴀʀᴏ.**",
                    parse_mode="Markdown"
                )
            except:
                bot.reply_to(msg, "<emoji id=5280606902533783431>😽</emoji> **⚠️ ɴᴇᴡ ᴀᴅᴍɪɴ ᴋᴏ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ ɴᴀʜɪ ʙʜᴇᴊ ꜱᴀᴋᴛᴇ (ᴜɴʜᴏɴᴇ ʙᴏᴛ ʙʟᴏᴄᴋ ᴋᴀʀ ᴅɪʏᴀ ʜᴀɪ)**")
        else:
            bot.reply_to(msg, f"<emoji id=4929369656797431200>🪐</emoji> **❌ {ᴍᴇꜱꜱᴀɢᴇ}**")

        del admin_add_state[user_id]

    except ValueError:
        bot.reply_to(msg, "<emoji id=6001589602085771497>✅</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ. ꜱɪʀꜰ ɴᴜᴍʙᴇʀꜱ ᴅᴀᴀʟᴏ.**")
    except Exception as e:
        logger.error(f"<emoji id=6154635934135490309>💗</emoji> **ᴀᴅᴅ ᴀᴅᴍɪɴ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.reply_to(msg, f"<emoji id=6154635934135490309>💗</emoji> **❌ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")
        del admin_add_state[user_id]

@bot.message_handler(func=lambda m: m.from_user.id in admin_remove_state and admin_remove_state[m.from_user.id]["step"] == "waiting_user_id")
def handle_remove_admin_userid(msg):
    user_id = msg.from_user.id

    try:
        target_user_id = int(msg.text.strip())

        # Check if trying to remove self
        if target_user_id == user_id:
            bot.reply_to(msg, "<emoji id=6309640268761011366>🌙</emoji> **❌ ᴀᴀᴩ ᴋʜᴜᴅᴋᴏ ʀᴇᴍᴏᴠᴇ ɴᴀʜɪ ᴋᴀʀ ꜱᴀᴋᴛᴇ! ᴀᴀᴩ ᴍᴀɪɴ ᴀᴅᴍɪɴ ʜᴏ.**")
            del admin_remove_state[user_id]
            return

        # Check if user is admin
        if not is_admin(target_user_id):
            bot.reply_to(
                msg,
                f"<emoji id=5041955142060999726>🌈</emoji> **❌ ᴜꜱᴇʀ `{ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}` ᴀᴅᴍɪɴ ɴᴀʜɪ ʜᴀɪ!**",
                parse_mode="Markdown"
            )
            del admin_remove_state[user_id]
            return

        # Remove admin
        success, message = remove_admin(target_user_id, user_id)

        if success:
            # Get user info
            user = users_col.find_one({"user_id": target_user_id})
            name = user.get('name', 'Unknown') if user else 'Unknown'

            # Get updated admin count
            new_count = admins_col.count_documents({})

            bot.reply_to(
                msg,
                f"<emoji id=6309709550878463216>🌟</emoji> **✅ **ᴀᴅᴍɪɴ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
                f"<emoji id=5280904324724063665>😽</emoji> **👤 ᴜꜱᴇʀ ɪᴅ: `{ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}`\ɴ**"
                f"<emoji id=5999340396432333728>☺️</emoji> **👤 ɴᴀᴍᴇ: {ɴᴀᴍᴇ}\ɴ**"
                f"<emoji id=6309640268761011366>🌙</emoji> **📊 ʀᴇᴍᴀɪɴɪɴɢ ᴀᴅᴍɪɴꜱ: {ɴᴇᴡ_ᴄᴏᴜɴᴛ + 1}/6 (ᴍᴀɪɴ ᴀᴅᴍɪɴ + {ɴᴇᴡ_ᴄᴏᴜɴᴛ})\ɴ\ɴ**"
                f"<emoji id=5040016479722931047>✨</emoji> **ᴀʙ ʏᴇ ᴀᴅᴍɪɴ ɴᴀʜɪ ʀᴀʜᴇ.**",
                parse_mode="Markdown"
            )

            # Notify removed admin
            try:
                bot.send_message(
                    target_user_id,
                    f"<emoji id=5281001756057175314>😽</emoji> **⚠️ **ʏᴏᴜʀ ᴀᴅᴍɪɴ ᴀᴄᴄᴇꜱꜱ ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ**\ɴ\ɴ**"
                    f"<emoji id=6154635934135490309>💗</emoji> **ᴀᴀᴩ ᴀʙ ᴀᴅᴍɪɴ ɴᴀʜɪ ʀᴀʜᴇ. ʙᴏᴛ ᴜꜱᴇ ᴋᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ /ꜱᴛᴀʀᴛ ᴋᴀʀᴏ.**",
                    parse_mode="Markdown"
                )
            except:
                pass
        else:
            bot.reply_to(msg, f"<emoji id=6309709550878463216>🌟</emoji> **❌ {ᴍᴇꜱꜱᴀɢᴇ}**")

        del admin_remove_state[user_id]

    except ValueError:
        bot.reply_to(msg, "<emoji id=6307568836098922002>🌙</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ. ꜱɪʀꜰ ɴᴜᴍʙᴇʀꜱ ᴅᴀᴀʟᴏ.**")
    except Exception as e:
        logger.error(f"<emoji id=5999041732996504081>✨</emoji> **ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.reply_to(msg, f"<emoji id=6287579968109024771>✅</emoji> **❌ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")
        del admin_remove_state[user_id]

# ---------------------------------------------------------------------
# UTILITY FUNCTIONS - UPDATED FOR TWO CHANNELS
# ---------------------------------------------------------------------

def ensure_user_exists(user_id, user_name=None, username=None, referred_by=None):
    user = users_col.find_one({"user_id": user_id})
    if not user:
        user_data = {
            "user_id": user_id,
            "name": user_name or "Unknown",
            "username": username,
            "referred_by": referred_by,
            "referral_code": f"<emoji id=5999210495146465994>💖</emoji> **ʀᴇꜰ{ᴜꜱᴇʀ_ɪᴅ}**",
            "total_commission_earned": 0.0,
            "total_referrals": 0,
            "created_at": datetime.utcnow()
        }
        users_col.insert_one(user_data)

        if referred_by:
            referral_record = {
                "referrer_id": referred_by,
                "referred_id": user_id,
                "referral_code": user_data['referral_code'],
                "status": "pending",
                "created_at": datetime.utcnow()
            }
            referrals_col.insert_one(referral_record)
            users_col.update_one(
                {"user_id": referred_by},
                {"<emoji id=6298717844804733009>♾</emoji> **$ɪɴᴄ**": {"total_referrals": 1}}
            )
            logger.info(f"<emoji id=6152444560216693216>🥰</emoji> **ʀᴇꜰᴇʀʀᴀʟ ʀᴇᴄᴏʀᴅᴇᴅ: {ʀᴇꜰᴇʀʀᴇᴅ_ʙʏ} -> {ᴜꜱᴇʀ_ɪᴅ}**")

    wallets_col.update_one(
        {"user_id": user_id},
        {"<emoji id=6309739370836399696>🌙</emoji> **$ꜱᴇᴛᴏɴɪɴꜱᴇʀᴛ**": {"user_id": user_id, "balance": 0.0}},
        upsert=True
    )

def get_balance(user_id):
    rec = wallets_col.find_one({"user_id": user_id})
    return float(rec.get("balance", 0.0)) if rec else 0.0

def add_balance(user_id, amount):
    wallets_col.update_one(
        {"user_id": user_id},
        {"<emoji id=6307568836098922002>🌙</emoji> **$ɪɴᴄ**": {"balance": float(amount)}},
        upsert=True
    )

def deduct_balance(user_id, amount):
    wallets_col.update_one(
        {"user_id": user_id},
        {"<emoji id=5999041732996504081>✨</emoji> **$ɪɴᴄ**": {"balance": -float(amount)}},
        upsert=True
    )

def format_currency(x):
    try:
        x = float(x)
        if x.is_integer():
            return f"<emoji id=5998881015320287132>💊</emoji> **₹{ɪɴᴛ(x)}**"
        return f"<emoji id=6309666601205503867>💌</emoji> **₹{x:.2ꜰ}**"
    except:
        return "₹0"

def get_available_accounts_count(country):
    return accounts_col.count_documents({"country": country, "status": "active", "used": False})

def is_user_banned(user_id):
    banned = banned_users_col.find_one({"user_id": user_id, "status": "active"})
    return banned is not None

def get_all_countries():
    return list(countries_col.find({"status": "active"}))

def get_country_by_name(country_name):
    return countries_col.find_one({
        "name": {"<emoji id=6309640268761011366>🌙</emoji> **$ʀᴇɢᴇx**": f"<emoji id=6309666601205503867>💌</emoji> **^{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}$**", "<emoji id=6152444560216693216>🥰</emoji> **$ᴏᴩᴛɪᴏɴꜱ**": "i"},
        "status": "active"
    })

def add_referral_commission(referrer_id, recharge_amount, recharge_id):
    try:
        commission = (recharge_amount * REFERRAL_COMMISSION) / 100
        add_balance(referrer_id, commission)

        transaction_id = f"<emoji id=6307490397111195260>🦋</emoji> **ᴄᴏᴍ{ʀᴇꜰᴇʀʀᴇʀ_ɪᴅ}{ɪɴᴛ(ᴛɪᴍᴇ.ᴛɪᴍᴇ())}**"
        transaction_record = {
            "transaction_id": transaction_id,
            "user_id": referrer_id,
            "amount": commission,
            "type": "referral_commission",
            "description": f"<emoji id=5352542184493031170>😈</emoji> **ʀᴇꜰᴇʀʀᴀʟ ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ꜰʀᴏᴍ ʀᴇᴄʜᴀʀɢᴇ #{ʀᴇᴄʜᴀʀɢᴇ_ɪᴅ}**",
            "timestamp": datetime.utcnow(),
            "recharge_id": str(recharge_id)
        }
        transactions_col.insert_one(transaction_record)

        users_col.update_one(
            {"user_id": referrer_id},
            {"<emoji id=5235985147265837746>🗒</emoji> **$ɪɴᴄ**": {"total_commission_earned": commission}}
        )

        referrals_col.update_one(
            {"referred_id": recharge_id.get("user_id"), "referrer_id": referrer_id},
            {"<emoji id=5395580801930771895>🤍</emoji> **$ꜱᴇᴛ**": {"status": "completed", "commission": commission, "completed_at": datetime.utcnow()}}
        )

        try:
            bot.send_message(
                referrer_id,
                f"<emoji id=6298684666182371615>❤️</emoji> **💰 **ʀᴇꜰᴇʀʀᴀʟ ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ᴇᴀʀɴᴇᴅ!**\ɴ\ɴ**"
                f"<emoji id=6123125485661591081>🩷</emoji> **✅ ʏᴏᴜ ᴇᴀʀɴᴇᴅ {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴏᴍᴍɪꜱꜱɪᴏɴ)} ᴄᴏᴍᴍɪꜱꜱɪᴏɴ!\ɴ**"
                f"<emoji id=6123125485661591081>🩷</emoji> **📊 ꜰʀᴏᴍ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ʀᴇᴄʜᴀʀɢᴇ_ᴀᴍᴏᴜɴᴛ)} ʀᴇᴄʜᴀʀɢᴇ\ɴ**"
                f"<emoji id=4929195195225867512>💎</emoji> **📈 ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ʀᴀᴛᴇ: {ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ}%\ɴ**"
                f"<emoji id=6307568836098922002>🌙</emoji> **💳 ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɢᴇᴛ_ʙᴀʟᴀɴᴄᴇ(ʀᴇꜰᴇʀʀᴇʀ_ɪᴅ))}\ɴ\ɴ**"
                f"<emoji id=6111418418424973677>✅</emoji> **ᴋᴇᴇᴩ ʀᴇꜰᴇʀʀɪɴɢ ᴛᴏ ᴇᴀʀɴ ᴍᴏʀᴇ! 🎉**"
            )
        except:
            pass

        logger.info(f"<emoji id=6309666601205503867>💌</emoji> **ʀᴇꜰᴇʀʀᴀʟ ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ᴀᴅᴅᴇᴅ: {ʀᴇꜰᴇʀʀᴇʀ_ɪᴅ} - {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴏᴍᴍɪꜱꜱɪᴏɴ)}**")
    except Exception as e:
        logger.error(f"<emoji id=4927247234283603387>🩷</emoji> **ᴇʀʀᴏʀ ᴀᴅᴅɪɴɢ ʀᴇꜰᴇʀʀᴀʟ ᴄᴏᴍᴍɪꜱꜱɪᴏɴ: {ᴇ}**")

# ---------------------------------------------------------------------
# UPDATED: CHECK BOTH CHANNELS MEMBERSHIP
# ---------------------------------------------------------------------

def has_user_joined_channels(user_id):
    """<emoji id=6309666601205503867>💌</emoji> **ᴄʜᴇᴄᴋ ɪꜰ ᴜꜱᴇʀ ʜᴀꜱ ᴊᴏɪɴᴇᴅ ʙᴏᴛʜ ᴍᴀɴᴅᴀᴛᴏʀʏ ᴄʜᴀɴɴᴇʟꜱ**"""
    try:
        # Check first channel
        member1 = bot.get_chat_member(MUST_JOIN_CHANNEL_1, user_id)
        status1 = member1.status in ['member', 'administrator', 'creator']

        # Check second channel
        member2 = bot.get_chat_member(MUST_JOIN_CHANNEL_2, user_id)
        status2 = member2.status in ['member', 'administrator', 'creator']

        return status1 and status2
    except Exception as e:
        logger.error(f"<emoji id=6307605493644793241>📒</emoji> **ᴇʀʀᴏʀ ᴄʜᴇᴄᴋɪɴɢ ᴄʜᴀɴɴᴇʟ ᴍᴇᴍʙᴇʀꜱʜɪᴩ: {ᴇ}**")
        return False

def get_missing_channels(user_id):
    """<emoji id=6111418418424973677>✅</emoji> **ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴄʜᴀɴɴᴇʟꜱ ᴜꜱᴇʀ ʜᴀꜱɴ'ᴛ ᴊᴏɪɴᴇᴅ ʏᴇᴛ**"""
    missing = []
    try:
        # Check first channel
        try:
            member1 = bot.get_chat_member(MUST_JOIN_CHANNEL_1, user_id)
            if member1.status not in ['member', 'administrator', 'creator']:
                missing.append(MUST_JOIN_CHANNEL_1)
        except:
            missing.append(MUST_JOIN_CHANNEL_1)

        # Check second channel
        try:
            member2 = bot.get_chat_member(MUST_JOIN_CHANNEL_2, user_id)
            if member2.status not in ['member', 'administrator', 'creator']:
                missing.append(MUST_JOIN_CHANNEL_2)
        except:
            missing.append(MUST_JOIN_CHANNEL_2)

        return missing
    except Exception as e:
        logger.error(f"<emoji id=5395580801930771895>🤍</emoji> **ᴇʀʀᴏʀ ɢᴇᴛᴛɪɴɢ ᴍɪꜱꜱɪɴɢ ᴄʜᴀɴɴᴇʟꜱ: {ᴇ}**")
        return [MUST_JOIN_CHANNEL_1, MUST_JOIN_CHANNEL_2]

# ---------------------------------------------------------------------
# COUPON UTILITY FUNCTIONS
# ---------------------------------------------------------------------

def get_coupon(code):
    return coupons_col.find_one({"coupon_code": code})

def is_coupon_claimed_by_user(coupon_code, user_id):
    coupon = get_coupon(coupon_code)
    if not coupon:
        return False
    claimed_users = coupon.get("claimed_users", [])
    return user_id in claimed_users

def claim_coupon(coupon_code, user_id):
    try:
        coupon = get_coupon(coupon_code)
        if not coupon:
            return False, "<emoji id=5999210495146465994>💖</emoji> **ᴄᴏᴜᴩᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ**"

        if user_id in coupon.get("claimed_users", []):
            return False, "<emoji id=6111418418424973677>✅</emoji> **ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ**"

        if coupon.get("status") != "active":
            status = coupon.get("status", "inactive")
            return False, f"<emoji id=6307821174017496029>🔥</emoji> **ᴄᴏᴜᴩᴏɴ {ꜱᴛᴀᴛᴜꜱ}**"

        total_claimed = coupon.get("total_claimed_count", 0)
        max_users = coupon.get("max_users", 0)
        if total_claimed >= max_users:
            coupons_col.update_one(
                {"coupon_code": coupon_code},
                {"<emoji id=6111418418424973677>✅</emoji> **$ꜱᴇᴛ**": {"status": "expired"}}
            )
            return False, "<emoji id=5999270482954691955>🦋</emoji> **ꜰᴜʟʟʏ ᴄʟᴀɪᴍᴇᴅ**"

        result = coupons_col.update_one(
            {
                "coupon_code": coupon_code,
                "status": "active",
                "total_claimed_count": {"$lt": max_users}
            },
            {
                "<emoji id=6307605493644793241>📒</emoji> **$ɪɴᴄ**": {"total_claimed_count": 1},
                "<emoji id=6001132493011425597>💖</emoji> **$ᴩᴜꜱʜ**": {"claimed_users": user_id},
                "<emoji id=5280606902533783431>😽</emoji> **$ꜱᴇᴛ**": {
                    "last_claimed_at": datetime.utcnow(),
                    "last_claimed_by": user_id
                }
            }
        )

        if result.modified_count == 0:
            return False, "<emoji id=5318828550940293906>🐱</emoji> **ᴄᴏᴜᴩᴏɴ ɴᴏ ʟᴏɴɢᴇʀ ᴀᴠᴀɪʟᴀʙʟᴇ**"

        amount = coupon.get("amount", 0)
        add_balance(user_id, amount)

        transaction_id = f"<emoji id=6309666601205503867>💌</emoji> **ᴄᴩɴ{ᴜꜱᴇʀ_ɪᴅ}{ɪɴᴛ(ᴛɪᴍᴇ.ᴛɪᴍᴇ())}**"
        transaction_record = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "amount": amount,
            "type": "coupon_redeem",
            "description": f"<emoji id=6111390922044344694>✅</emoji> **ᴄᴏᴜᴩᴏᴜ ʀᴇᴅᴇᴇᴍ: {ᴄᴏᴜᴩᴏɴ_ᴄᴏᴅᴇ}**",
            "coupon_code": coupon_code,
            "timestamp": datetime.utcnow()
        }
        transactions_col.insert_one(transaction_record)

        updated_coupon = get_coupon(coupon_code)
        if updated_coupon and updated_coupon.get("total_claimed_count", 0) >= max_users:
            coupons_col.update_one(
                {"coupon_code": coupon_code},
                {"<emoji id=6307821174017496029>🔥</emoji> **$ꜱᴇᴛ**": {"status": "expired"}}
            )

        return True, amount
    except Exception as e:
        logger.error(f"<emoji id=6152444560216693216>🥰</emoji> **ᴇʀʀᴏʀ ᴄʟᴀɪᴍɪɴɢ ᴄᴏᴜᴩᴏɴ: {ᴇ}**")
        return False, "<emoji id=6151981777490548710>✅</emoji> **ᴇʀʀᴏʀ ᴩʀᴏᴄᴇꜱꜱɪɴɢ ᴄᴏᴜᴩᴏɴ**"

def create_coupon(code, amount, max_users, created_by):
    try:
        if amount < 1:
            return False, "<emoji id=5352542184493031170>😈</emoji> **ᴀᴍᴏᴜɴᴛ ᴍᴜꜱᴛ ʙᴇ ᴀᴛ ʟᴇᴀꜱᴛ ₹1**"
        if max_users < 1:
            return False, "<emoji id=4926993814033269936>🖕</emoji> **ᴍᴀx ᴜꜱᴇʀꜱ ᴍᴜꜱᴛ ʙᴇ ᴀᴛ ʟᴇᴀꜱᴛ 1**"

        existing = get_coupon(code)
        if existing:
            return False, "<emoji id=5040016479722931047>✨</emoji> **ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ ᴀʟʀᴇᴀᴅʏ ᴇxɪꜱᴛꜱ**"

        coupon_data = {
            "coupon_code": code,
            "amount": float(amount),
            "max_users": int(max_users),
            "total_claimed_count": 0,
            "claimed_users": [],
            "status": "active",
            "created_at": datetime.utcnow(),
            "created_by": created_by
        }
        coupons_col.insert_one(coupon_data)
        return True, "<emoji id=6111390922044344694>✅</emoji> **ᴄᴏᴜᴩᴏɴ ᴄʀᴇᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ**"
    except Exception as e:
        logger.error(f"<emoji id=6298717844804733009>♾</emoji> **ᴇʀʀᴏʀ ᴄʀᴇᴀᴛɪɴɢ ᴄᴏᴜᴩᴏɴ: {ᴇ}**")
        return False, f"<emoji id=5281001756057175314>😽</emoji> **ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**"

def remove_coupon(code, removed_by):
    try:
        coupon = get_coupon(code)
        if not coupon:
            return False, "<emoji id=5999041732996504081>✨</emoji> **ᴄᴏᴜᴩᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ**"

        result = coupons_col.update_one(
            {"coupon_code": code},
            {"<emoji id=6111390922044344694>✅</emoji> **$ꜱᴇᴛ**": {
                "status": "removed",
                "removed_at": datetime.utcnow(),
                "removed_by": removed_by
            }}
        )

        if result.modified_count == 0:
            return False, "<emoji id=6123125485661591081>🩷</emoji> **ꜰᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴄᴏᴜᴩᴏɴ**"
        return True, "<emoji id=5280678521113443426>😽</emoji> **ᴄᴏᴜᴩᴏɴ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ**"
    except Exception as e:
        logger.error(f"<emoji id=6310022800023229454>✡️</emoji> **ᴇʀʀᴏʀ ʀᴇᴍᴏᴠɪɴɢ ᴄᴏᴜᴩᴏɴ: {ᴇ}**")
        return False, f"<emoji id=4927247234283603387>🩷</emoji> **ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**"

def get_coupon_status(code):
    coupon = get_coupon(code)
    if not coupon:
        return None

    claimed = coupon.get("total_claimed_count", 0)
    max_users = coupon.get("max_users", 0)
    remaining = max(0, max_users - claimed)

    return {
        "code": coupon.get("coupon_code"),
        "amount": coupon.get("amount", 0),
        "max_users": max_users,
        "claimed": claimed,
        "remaining": remaining,
        "status": coupon.get("status", "unknown"),
        "created_at": coupon.get("created_at"),
        "created_by": coupon.get("created_by"),
        "claimed_users": coupon.get("claimed_users", [])[:10]
    }

# ---------------------------------------------------------------------
# ENHANCED RECHARGE APPROVAL FUNCTIONS
# ---------------------------------------------------------------------

def process_recharge_approval(admin_id, req_id, action):
    """<emoji id=6123125485661591081>🩷</emoji> **ᴩʀᴏᴄᴇꜱꜱ ʀᴇᴄʜᴀʀɢᴇ ᴀᴩᴩʀᴏᴠᴀʟ/ʀᴇᴊᴇᴄᴛɪᴏɴ ᴡɪᴛʜ ᴛʀᴀᴄᴋɪɴɢ**"""
    try:
        # Get recharge request
        req = recharges_col.find_one({"req_id": req_id})
        if not req:
            return False, "<emoji id=4929483658114368660>💎</emoji> **ʀᴇꞯᴜᴇꜱᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ**", None

        # Check if already processed
        if req.get("status") != "pending":
            return False, f"<emoji id=6307568836098922002>🌙</emoji> **ʀᴇꞯᴜᴇꜱᴛ ᴀʟʀᴇᴀᴅʏ {ʀᴇꞯ.ɢᴇᴛ('ꜱᴛᴀᴛᴜꜱ')}**", None

        # Get admin info
        admin_info = get_admin_info(admin_id)
        admin_name = f"<emoji id=5395580801930771895>🤍</emoji> **ᴀᴅᴍɪɴ {ᴀᴅᴍɪɴ_ɪᴅ}**"
        if admin_info:
            user = users_col.find_one({"user_id": admin_id})
            if user:
                admin_name = user.get("name", f"<emoji id=5352870513267973607>✨</emoji> **ᴀᴅᴍɪɴ {ᴀᴅᴍɪɴ_ɪᴅ}**")

        user_target = req.get("user_id")
        amount = float(req.get("amount", 0))

        # Track this approval
        approval_key = f"<emoji id=5999041732996504081>✨</emoji> **{ʀᴇꞯ_ɪᴅ}_{ᴀᴄᴛɪᴏɴ}**"

        # Check if another admin already processed this (via tracking)
        if approval_key in recharge_approvals:
            prev_admin = recharge_approvals[approval_key]
            return False, f"<emoji id=5041955142060999726>🌈</emoji> **ᴀʟʀᴇᴀᴅʏ {ᴀᴄᴛɪᴏɴ}ᴇᴅ ʙʏ {ᴩʀᴇᴠ_ᴀᴅᴍɪɴ['ᴀᴅᴍɪɴ_ɴᴀᴍᴇ']}**", None

        if action == "approve":
            # Add balance to user
            add_balance(user_target, amount)

            # Update recharge status
            recharges_col.update_one(
                {"req_id": req_id},
                {"<emoji id=6310044717241340733>🔄</emoji> **$ꜱᴇᴛ**": {
                    "status": "approved", 
                    "processed_at": datetime.utcnow(), 
                    "processed_by": admin_id,
                    "processed_by_name": admin_name
                }}
            )

            # Log approval
            try:
                from logs import log_recharge_approved_async
                log_recharge_approved_async(
                    user_id=user_target,
                    amount=amount,
                    method=req.get("method", "UPI"),
                    utr=req.get("utr")
                )
            except:
                pass

            # Add referral commission if applicable
            user_data = users_col.find_one({"user_id": user_target})
            if user_data and user_data.get("referred_by"):
                add_referral_commission(user_data["referred_by"], amount, req)

            # Mark this approval in tracking
            recharge_approvals[approval_key] = {
                "admin_id": admin_id,
                "admin_name": admin_name,
                "timestamp": datetime.utcnow()
            }

            return True, f"<emoji id=6298717844804733009>♾</emoji> **✅ ʀᴇᴄʜᴀʀɢᴇ ᴀᴩᴩʀᴏᴠᴇᴅ ʙʏ {ᴀᴅᴍɪɴ_ɴᴀᴍᴇ}**", {
                "admin_name": admin_name,
                "admin_id": admin_id,
                "action": "approved"
            }

        else:  # cancel/reject
            # Update recharge status
            recharges_col.update_one(
                {"req_id": req_id},
                {"<emoji id=6310022800023229454>✡️</emoji> **$ꜱᴇᴛ**": {
                    "status": "cancelled", 
                    "processed_at": datetime.utcnow(), 
                    "processed_by": admin_id,
                    "processed_by_name": admin_name
                }}
            )

            # Mark this rejection in tracking
            recharge_approvals[approval_key] = {
                "admin_id": admin_id,
                "admin_name": admin_name,
                "timestamp": datetime.utcnow()
            }

            return True, f"<emoji id=6307490397111195260>🦋</emoji> **❌ ʀᴇᴄʜᴀʀɢᴇ ʀᴇᴊᴇᴄᴛᴇᴅ ʙʏ {ᴀᴅᴍɪɴ_ɴᴀᴍᴇ}**", {
                "admin_name": admin_name,
                "admin_id": admin_id,
                "action": "rejected"
            }

    except Exception as e:
        logger.error(f"<emoji id=5899776109548934640>💲</emoji> **ᴇʀʀᴏʀ ɪɴ ʀᴇᴄʜᴀʀɢᴇ ᴀᴩᴩʀᴏᴠᴀʟ: {ᴇ}**")
        return False, f"<emoji id=6309819721084573392>🌙</emoji> **ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**", None

# ---------------------------------------------------------------------
# UI HELPER FUNCTIONS - FIXED
# ---------------------------------------------------------------------

def edit_or_resend(chat_id, message_id, text, markup=None, parse_mode=None, photo_url=None):
    """<emoji id=5999041732996504081>✨</emoji> **ᴇᴅɪᴛ ᴍᴇꜱꜱᴀɢᴇ ɪꜰ ᴩᴏꜱꜱɪʙʟᴇ, ᴏᴛʜᴇʀᴡɪꜱᴇ ᴅᴇʟᴇᴛᴇ ᴀɴᴅ ꜱᴇɴᴅ ɴᴇᴡ**"""
    try:
        if photo_url:
            # For photos, we need to send new message
            try:
                bot.delete_message(chat_id, message_id)
            except:
                pass
            return bot.send_photo(chat_id, photo_url, caption=text, parse_mode=parse_mode, reply_markup=markup)
        else:
            # For text messages, try to edit first
            try:
                return bot.edit_message_text(
                    text,
                    chat_id=chat_id,
                    message_id=message_id,
                    parse_mode=parse_mode,
                    reply_markup=markup
                )
            except Exception as e:
                # If edit fails, delete and send new
                try:
                    bot.delete_message(chat_id, message_id)
                except:
                    pass
                return bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=markup)
    except Exception as e:
        logger.error(f"<emoji id=6309739370836399696>🌙</emoji> **ᴇʀʀᴏʀ ɪɴ ᴇᴅɪᴛ_ᴏʀ_ʀᴇꜱᴇɴᴅ: {ᴇ}**")
        return bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=markup)

def clean_ui_and_send_menu(chat_id, user_id, text=None, markup=None):
    """<emoji id=4926993814033269936>🖕</emoji> **ᴄʟᴇᴀɴ ᴜɪ ᴀɴᴅ ꜱᴇɴᴅ ᴍᴀɪɴ ᴍᴇɴᴜ - ꜰɪxᴇᴅ: ᴀʟᴡᴀʏꜱ ᴅᴇʟᴇᴛᴇꜱ ᴏʟᴅ ᴍᴇꜱꜱᴀɢᴇ**"""
    try:
        # ALWAYS try to delete the previous message
        if user_id in user_last_message:
            try:
                bot.delete_message(chat_id, user_last_message[user_id])
            except:
                pass

        # Main menu caption with expandable blockquotes
        caption = (
            '<emoji id=6309985824649780135>🌙</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5373082993207921989">🌟</ᴛɢ-ᴇᴍᴏᴊɪ> <ʙ>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ɢᴍꜱ ᴏᴛᴩ ʙᴏᴛ</ʙ> <ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5373082993207921989">🌟</ᴛɢ-ᴇᴍᴏᴊɪ>\ɴ**'
            "<emoji id=6307605493644793241>📒</emoji> **<ʙʟᴏᴄᴋꞯᴜᴏᴛᴇ ᴇxᴩᴀɴᴅᴀʙʟᴇ>\ɴ**"
            '<emoji id=6001132493011425597>💖</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5368324170671202286">✨</ᴛɢ-ᴇᴍᴏᴊɪ> ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴏᴛᴩꜱ — ɪɴꜱᴛᴀɴᴛ & ꜰᴀꜱᴛ\ɴ**'
            '<emoji id=6111418418424973677>✅</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5350537057272218572">💎</ᴛɢ-ᴇᴍᴏᴊɪ> ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ — ꜱɪᴍᴩʟᴇ ɪɴᴛᴇʀꜰᴀᴄᴇ\ɴ**'
            '<emoji id=6309739370836399696>🌙</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5271604874419737411">🔥</ᴛɢ-ᴇᴍᴏᴊɪ> 24/7 ꜱᴜᴩᴩᴏʀᴛ — ᴀʟᴡᴀʏꜱ ʜᴇʀᴇ\ɴ**'
            '<emoji id=6310044717241340733>🔄</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5469654973107908278">⚡</ᴛɢ-ᴇᴍᴏᴊɪ> ɪɴꜱᴛᴀɴᴛ ᴩᴀʏᴍᴇɴᴛ ᴀᴩᴩʀᴏᴠᴀʟꜱ\ɴ**'
            "<emoji id=6307447640711763730>💟</emoji> **</ʙʟᴏᴄᴋꞯᴜᴏᴛᴇ>\ɴ**"
            "<emoji id=5280904324724063665>😽</emoji> **<ʙʟᴏᴄᴋꞯᴜᴏᴛᴇ ᴇxᴩᴀɴᴅᴀʙʟᴇ>\ɴ**"
            '<emoji id=6307750079423845494>👑</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5368322952606296312">👑</ᴛɢ-ᴇᴍᴏᴊɪ> <ʙ>ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ɢᴍꜱ ʙᴏᴛ:</ʙ>\ɴ**'
            "<emoji id=5285100774060227768>😽</emoji> **1️⃣ ᴀᴅᴅ ꜰᴜɴᴅꜱ ᴛᴏ ᴡᴀʟʟᴇᴛ\ɴ**"
            "<emoji id=5999210495146465994>💖</emoji> **2️⃣ ꜱᴇʟᴇᴄᴛ ᴄᴏᴜɴᴛʀʏ\ɴ**"
            "<emoji id=6307553838073124532>✨</emoji> **3️⃣ ʙᴜʏ ᴀᴄᴄᴏᴜɴᴛ\ɴ**"
            "<emoji id=6001132493011425597>💖</emoji> **4️⃣ ʟᴏɢɪɴ ᴠɪᴀ ᴛᴇʟᴇɢʀᴀᴍ / ᴛᴇʟᴇɢʀᴀᴍ x / ᴛᴀʀʙᴏᴛᴇʟ\ɴ**"
            "<emoji id=6111418418424973677>✅</emoji> **5️⃣ ʀᴇᴄᴇɪᴠᴇ ᴏᴛᴩ & ᴅᴏɴᴇ ✅\ɴ**"
            "<emoji id=5280721097124249567>😽</emoji> **</ʙʟᴏᴄᴋꞯᴜᴏᴛᴇ>\ɴ**"
            '<emoji id=6224236403153179330>🎀</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ="5469654973107908278">⚡</ᴛɢ-ᴇᴍᴏᴊɪ> <ʙ>ɢᴍꜱ — ꜰᴀꜱᴛ. ʀᴇʟɪᴀʙʟᴇ. ᴀʟᴡᴀʏꜱ ᴏɴ!</ʙ>**'
        )

        if markup is None:
            markup = InlineKeyboardMarkup(row_width=2)
            # Row 1: 2 buttons
            markup.add(
                InlineKeyboardButton("<emoji id=4926993814033269936>🖕</emoji> **🛍️ ʙᴜʏ ᴀᴄᴄᴏᴜɴᴛ**", callback_data="buy_account", style="success"),
                InlineKeyboardButton("<emoji id=6152444560216693216>🥰</emoji> **💎 ᴍʏ ʙᴀʟᴀɴᴄᴇ**", callback_data="balance", style="primary")
            )
            # Row 2: 1 button
            markup.add(
                InlineKeyboardButton("<emoji id=5041955142060999726>🌈</emoji> **💸 ᴀᴅᴅ ꜰᴜɴᴅꜱ**", callback_data="recharge", style="success")
            )
            # Row 3: 2 buttons
            markup.add(
                InlineKeyboardButton("<emoji id=4929369656797431200>🪐</emoji> **🤝 ʀᴇꜰᴇʀ & ᴇᴀʀɴ**", callback_data="refer_friends", style="primary"),
                InlineKeyboardButton("<emoji id=6152444560216693216>🥰</emoji> **🎁 ʀᴇᴅᴇᴇᴍ ᴄᴏᴜᴩᴏɴ**", callback_data="redeem_coupon", style="danger")
            )
            # Row 4: 1 button
            markup.add(
                InlineKeyboardButton("<emoji id=6152142357727811958>🦋</emoji> **🆘 ꜱᴜᴩᴩᴏʀᴛ**", callback_data="support", style="primary")
            )
            # Row 5: 1 button (only for admin)
            if is_admin(user_id):
                markup.add(InlineKeyboardButton("<emoji id=5395580801930771895>🤍</emoji> **⚡ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ**", callback_data="admin_panel", style="danger"))

        # Send new message (TEXT ONLY - NO PHOTO)
        sent_msg = bot.send_message(
            chat_id,
            text or caption,
            parse_mode="HTML",
            reply_markup=markup,
            disable_web_page_preview=True
        )
        user_last_message[user_id] = sent_msg.message_id
        return sent_msg
    except Exception as e:
        logger.error(f"<emoji id=6287579968109024771>✅</emoji> **ᴇʀʀᴏʀ ɪɴ ᴄʟᴇᴀɴ_ᴜɪ_ᴀɴᴅ_ꜱᴇɴᴅ_ᴍᴇɴᴜ: {ᴇ}**")
        # Fallback
        try:
            sent_msg = bot.send_message(chat_id, text or caption, parse_mode="HTML", reply_markup=markup)
            user_last_message[user_id] = sent_msg.message_id
            return sent_msg
        except:
            pass

# ---------------------------------------------------------------------
# BALANCE TRANSFER FUNCTIONS
# ---------------------------------------------------------------------

def transfer_balance(sender_id, receiver_id, amount):
    """<emoji id=6307447640711763730>💟</emoji> **ʙᴀʟᴀɴᴄᴇ ᴛʀᴀɴꜱꜰᴇʀ ꜰᴜɴᴄᴛɪᴏɴ**"""
    try:
        # Sender ka balance check
        sender_balance = get_balance(sender_id)

        if sender_balance < amount:
            return False, "<emoji id=6152142357727811958>🦋</emoji> **ɪɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ ʙᴀʟᴀɴᴄᴇ**"

        if amount <= 0:
            return False, "<emoji id=5280678521113443426>😽</emoji> **ᴀᴍᴏᴜɴᴛ ᴍᴜꜱᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 0**"

        if sender_id == receiver_id:
            return False, "<emoji id=5999151980512024620>🥰</emoji> **ᴄᴀɴɴᴏᴛ ꜱᴇɴᴅ ᴛᴏ ʏᴏᴜʀꜱᴇʟꜰ**"

        # Check if receiver exists
        receiver = users_col.find_one({"user_id": receiver_id})
        if not receiver:
            return False, "<emoji id=6309709550878463216>🌟</emoji> **ʀᴇᴄᴇɪᴠᴇʀ ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ**"

        # Transfer balance
        deduct_balance(sender_id, amount)
        add_balance(receiver_id, amount)

        # Transaction record
        transaction_id = f"<emoji id=5281001756057175314>😽</emoji> **ᴛʀꜰ{ɪɴᴛ(ᴛɪᴍᴇ.ᴛɪᴍᴇ())}{ꜱᴇɴᴅᴇʀ_ɪᴅ}**"
        transaction_record = {
            "transaction_id": transaction_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "amount": amount,
            "type": "transfer",
            "timestamp": datetime.utcnow()
        }
        transactions_col.insert_one(transaction_record)

        return True, f"<emoji id=6310022800023229454>✡️</emoji> **✅ {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)} ᴛʀᴀɴꜱꜰᴇʀʀᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**"

    except Exception as e:
        logger.error(f"<emoji id=6001132493011425597>💖</emoji> **ᴛʀᴀɴꜱꜰᴇʀ ᴇʀʀᴏʀ: {ᴇ}**")
        return False, f"<emoji id=6224236403153179330>🎀</emoji> **ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**"

# ---------------------------------------------------------------------
# PREMIUM INTRO FUNCTION
# ---------------------------------------------------------------------

PREMIUM_STICKER_PACK = "Udif7rr7_by_fStikBot"

# Bot API HTML format for premium custom emoji (<tg-emoji> works for bots natively)
E_MAGIC_TG    = "<emoji id=6001589602085771497>✅</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ='5352870513267973607'>✨</ᴛɢ-ᴇᴍᴏᴊɪ>**"
E_DEVIL_TG    = "<emoji id=6307643744623531146>🦋</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ='5352542184493031170'>😈</ᴛɢ-ᴇᴍᴏᴊɪ>**"
E_CROWN_TG    = "<emoji id=6111390922044344694>✅</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ='6307750079423845494'>👑</ᴛɢ-ᴇᴍᴏᴊɪ>**"
E_DIAMOND_TG  = "<emoji id=4927247234283603387>🩷</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ='4929195195225867512'>💎</ᴛɢ-ᴇᴍᴏᴊɪ>**"
E_BUTTERFLY_TG= "<emoji id=6152444560216693216>🥰</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ='6307643744623531146'>🦋</ᴛɢ-ᴇᴍᴏᴊɪ>**"
E_HEART_TG    = "<emoji id=5285100774060227768>😽</emoji> **<ᴛɢ-ᴇᴍᴏᴊɪ ᴇᴍᴏᴊɪ-ɪᴅ='6123125485661591081'>🩷</ᴛɢ-ᴇᴍᴏᴊɪ>**"

# Cache sticker file_ids from the premium pack (fetched once via Bot API)
_cached_sticker_ids = []

def _get_random_sticker_file_id():
    """<emoji id=6310022800023229454>✡️</emoji> **ꜰᴇᴛᴄʜ ꜱᴛɪᴄᴋᴇʀ ꜱᴇᴛ ᴏɴᴄᴇ ᴠɪᴀ ʙᴏᴛ ᴀᴩɪ ᴀɴᴅ ʀᴇᴛᴜʀɴ ᴀ ʀᴀɴᴅᴏᴍ ꜱᴛɪᴄᴋᴇʀ ꜰɪʟᴇ_ɪᴅ**"""
    global _cached_sticker_ids
    if not _cached_sticker_ids:
        try:
            sticker_set = bot.get_sticker_set(PREMIUM_STICKER_PACK)
            _cached_sticker_ids = [s.file_id for s in sticker_set.stickers]
            logger.info(f"<emoji id=6309985824649780135>🌙</emoji> **✅ ʟᴏᴀᴅᴇᴅ {ʟᴇɴ(_ᴄᴀᴄʜᴇᴅ_ꜱᴛɪᴄᴋᴇʀ_ɪᴅꜱ)} ꜱᴛɪᴄᴋᴇʀꜱ ꜰʀᴏᴍ {ᴩʀᴇᴍɪᴜᴍ_ꜱᴛɪᴄᴋᴇʀ_ᴩᴀᴄᴋ}**")
        except Exception as e:
            logger.error(f"<emoji id=6307821174017496029>🔥</emoji> **ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ ꜱᴛɪᴄᴋᴇʀ ꜱᴇᴛ: {ᴇ}**")
    if _cached_sticker_ids:
        return random.choice(_cached_sticker_ids)
    return None

def run_premium_intro(user_id):
    """<emoji id=6309819721084573392>🌙</emoji> **ꜱᴇɴᴅ ᴀɴɪᴍᴀᴛᴇᴅ ɪɴᴛʀᴏ ᴡɪᴛʜ ᴩʀᴇᴍɪᴜᴍ ᴄᴜꜱᴛᴏᴍ ᴇᴍᴏᴊɪ + ʀᴀɴᴅᴏᴍ ꜱᴛɪᴄᴋᴇʀ ᴠɪᴀ ʙᴏᴛ ᴀᴩɪ**"""
    try:
        m1 = bot.send_message(user_id, f"<emoji id=5352870513267973607>✨</emoji> **{ᴇ_ᴍᴀɢɪᴄ_ᴛɢ} ʜʟᴏ ꜱɪʀ......**", parse_mode='HTML')
        time.sleep(1)
        bot.delete_message(user_id, m1.message_id)
        m2 = bot.send_message(user_id, f"<emoji id=4929369656797431200>🪐</emoji> **{ᴇ_ᴅᴇᴠɪʟ_ᴛɢ} ᴩɪɴɢ ᴩᴏɴɢ........**", parse_mode='HTML')
        time.sleep(1)
        bot.delete_message(user_id, m2.message_id)
        m3 = bot.send_message(user_id, f"<emoji id=6307750079423845494>👑</emoji> **{ᴇ_ᴄʀᴏᴡɴ_ᴛɢ} ɢᴍꜱ ᴏᴩ......**", parse_mode='HTML')
        time.sleep(1)
        bot.delete_message(user_id, m3.message_id)

        # Send a random sticker from the premium sticker pack
        sticker_file_id = _get_random_sticker_file_id()
        if sticker_file_id:
            bot.send_sticker(user_id, sticker_file_id)
    except Exception as e:
        logger.error(f"<emoji id=6307568836098922002>🌙</emoji> **ᴩʀᴇᴍɪᴜᴍ ɪɴᴛʀᴏ ᴇʀʀᴏʀ: {ᴇ}**")
        try:
            m1 = bot.send_message(user_id, '<emoji id=6111778259374971023>🔥</emoji> **✨ ʜʟᴏ ꜱɪʀ......**')
            time.sleep(1)
            bot.delete_message(user_id, m1.message_id)
            m2 = bot.send_message(user_id, '<emoji id=6307643744623531146>🦋</emoji> **🔥 ᴩɪɴɢ ᴩᴏɴɢ........**')
            time.sleep(1)
            bot.delete_message(user_id, m2.message_id)
            m3 = bot.send_message(user_id, '<emoji id=6310044717241340733>🔄</emoji> **💎 ɢᴍꜱ ᴏᴩ......**')
            time.sleep(1)
            bot.delete_message(user_id, m3.message_id)
        except:
            pass

# ---------------------------------------------------------------------
# BOT HANDLERS - UPDATED WITH TWO CHANNELS
# ---------------------------------------------------------------------

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.from_user.id
    logger.info(f"<emoji id=4929369656797431200>🪐</emoji> **ꜱᴛᴀʀᴛ ᴄᴏᴍᴍᴀɴᴅ ꜰʀᴏᴍ ᴜꜱᴇʀ {ᴜꜱᴇʀ_ɪᴅ}**")

    if is_user_banned(user_id):
        try:
            bot.delete_message(msg.chat.id, msg.message_id)
        except:
            pass
        return

    # Check if user has joined BOTH channels
    if not has_user_joined_channels(user_id):
        missing_channels = get_missing_channels(user_id)

        caption = """<b>🚀 Join Both Channels First!</b> 

📢 To use this bot, you must join our official channels.

👉 Get updates, new features & support from our channels.

Click the buttons below to join both channels, then press VERIFY ✅"""

        markup = InlineKeyboardMarkup(row_width=2)

        # Add buttons for both channels
        for channel in missing_channels:
            markup.add(InlineKeyboardButton(
                f"<emoji id=5999151980512024620>🥰</emoji> **📢 ᴊᴏɪɴ {ᴄʜᴀɴɴᴇʟ}**",
                url=f"<emoji id=5395580801930771895>🤍</emoji> **ʜᴛᴛᴩꜱ://ᴛ.ᴍᴇ/{ᴄʜᴀɴɴᴇʟ[1:]}**"
            ))

        markup.add(InlineKeyboardButton("<emoji id=6309709550878463216>🌟</emoji> **✅ ᴠᴇʀɪꜰʏ ᴊᴏɪɴ**", callback_data="verify_join"))

        try:
            bot.send_message(
                user_id,
                caption,
                parse_mode="HTML",
                reply_markup=markup
            )
        except Exception as e:
            logger.error(f"<emoji id=6309985824649780135>🌙</emoji> **ᴇʀʀᴏʀ ꜱᴇɴᴅɪɴɢ ᴊᴏɪɴ ᴍᴇꜱꜱᴀɢᴇ: {ᴇ}**")
        return

    referred_by = None
    if len(msg.text.split()) > 1:
        referral_code = msg.text.split()[1]
        if referral_code.startswith('REF'):
            try:
                referrer_id = int(referral_code[3:])
                referrer = users_col.find_one({"user_id": referrer_id})
                if referrer:
                    referred_by = referrer_id
                    logger.info(f"<emoji id=6309640268761011366>🌙</emoji> **ʀᴇꜰᴇʀʀᴀʟ ᴅᴇᴛᴇᴄᴛᴇᴅ: {ʀᴇꜰᴇʀʀᴇʀ_ɪᴅ} -> {ᴜꜱᴇʀ_ɪᴅ}**")
            except:
                pass

    ensure_user_exists(user_id, msg.from_user.first_name, msg.from_user.username, referred_by)

    # Animated intro with real premium emoji via premium account
    run_premium_intro(user_id)

    clean_ui_and_send_menu(user_id, user_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    data = call.data

    if is_user_banned(user_id):
        bot.answer_callback_query(call.id, "<emoji id=6307568836098922002>🌙</emoji> **🚫 ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ɪꜱ ʙᴀɴɴᴇᴅ**", show_alert=True)
        return

    logger.info(f"<emoji id=6111390922044344694>✅</emoji> **ᴄᴀʟʟʙᴀᴄᴋ ʀᴇᴄᴇɪᴠᴇᴅ: {ᴅᴀᴛᴀ} ꜰʀᴏᴍ ᴜꜱᴇʀ {ᴜꜱᴇʀ_ɪᴅ}**")

    try:
        if data == "verify_join":
            # Check if user has joined BOTH channels
            if has_user_joined_channels(user_id):
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except:
                    pass
                clean_ui_and_send_menu(call.message.chat.id, user_id)
                bot.answer_callback_query(call.id, "<emoji id=5280678521113443426>😽</emoji> **✅ ᴠᴇʀɪꜰɪᴇᴅ! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ.**", show_alert=True)
            else:
                missing_channels = get_missing_channels(user_id)

                caption = """<b>🚀 Join Both Channels First!</b> 

📢 To use this bot, you must join our official channels.

👉 Get updates, new features & support from our channels.

Click the buttons below to join both channels, then press VERIFY ✅"""

                markup = InlineKeyboardMarkup(row_width=2)

                # Add buttons for both channels
                for channel in missing_channels:
                    markup.add(InlineKeyboardButton(
                        f"<emoji id=5354924568492383911>😈</emoji> **📢 ᴊᴏɪɴ {ᴄʜᴀɴɴᴇʟ}**",
                        url=f"<emoji id=6151981777490548710>✅</emoji> **ʜᴛᴛᴩꜱ://ᴛ.ᴍᴇ/{ᴄʜᴀɴɴᴇʟ[1:]}**"
                    ))

                markup.add(InlineKeyboardButton("<emoji id=5318828550940293906>🐱</emoji> **✅ ᴠᴇʀɪꜰʏ ᴊᴏɪɴ**", callback_data="verify_join"))

                try:
                    bot.edit_message_text(
                        caption,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode="HTML",
                        reply_markup=markup
                    )
                except:
                    pass

                missing_list = "\n".join([f"<emoji id=6309819721084573392>🌙</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6309819721084573392>🌙</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴛʜᴇꜱᴇ ᴄʜᴀɴɴᴇʟꜱ ꜰɪʀꜱᴛ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )

        elif data == "buy_account":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6298684666182371615>❤️</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6298717844804733009>♾</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            show_countries(call.message.chat.id)

        elif data == "balance":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=5999210495146465994>💖</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6111418418424973677>✅</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            balance = get_balance(user_id)
            user_data = users_col.find_one({"user_id": user_id}) or {}
            commission_earned = user_data.get("total_commission_earned", 0)

            message = f"<emoji id=6307490397111195260>🦋</emoji> **💰 **ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ:** {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"
            message += f"<emoji id=6307750079423845494>👑</emoji> **📊 **ʀᴇꜰᴇʀʀᴀʟ ꜱᴛᴀᴛꜱ:**\ɴ**"
            message += f"<emoji id=6001589602085771497>✅</emoji> **• ᴛᴏᴛᴀʟ ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ᴇᴀʀɴᴇᴅ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴏᴍᴍɪꜱꜱɪᴏɴ_ᴇᴀʀɴᴇᴅ)}\ɴ**"
            message += f"<emoji id=6287579968109024771>✅</emoji> **• ᴛᴏᴛᴀʟ ʀᴇꜰᴇʀʀᴀʟꜱ: {ᴜꜱᴇʀ_ᴅᴀᴛᴀ.ɢᴇᴛ('ᴛᴏᴛᴀʟ_ʀᴇꜰᴇʀʀᴀʟꜱ', 0)}\ɴ**"
            message += f"<emoji id=6307750079423845494>👑</emoji> **• ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ʀᴀᴛᴇ: {ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ}%\ɴ\ɴ**"
            message += f"<emoji id=6152444560216693216>🥰</emoji> **ʏᴏᴜʀ ʀᴇꜰᴇʀʀᴀʟ ᴄᴏᴅᴇ: `{ᴜꜱᴇʀ_ᴅᴀᴛᴀ.ɢᴇᴛ('ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴅᴇ', 'ʀᴇꜰ' + ꜱᴛʀ(ᴜꜱᴇʀ_ɪᴅ))}`**"

            # Sirf Send Balance aur Back button
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("<emoji id=5354924568492383911>😈</emoji> **📤 ꜱᴇɴᴅ ʙᴀʟᴀɴᴄᴇ**", callback_data="send_balance_menu")
            )
            markup.add(
                InlineKeyboardButton("<emoji id=5280904324724063665>😽</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="back_to_menu")
            )

            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass

            sent_msg = bot.send_message(
                call.message.chat.id,
                message,
                parse_mode="Markdown",
                reply_markup=markup
            )
            user_last_message[user_id] = sent_msg.message_id

        elif data == "send_balance_menu":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6152142357727811958>🦋</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6310022800023229454>✡️</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            balance = get_balance(user_id)

            message = f"<emoji id=6307447640711763730>💟</emoji> **📤 **ꜱᴇɴᴅ ʙᴀʟᴀɴᴄᴇ - ꜱᴛᴇᴩ 1/2**\ɴ\ɴ**"
            message += f"<emoji id=5040016479722931047>✨</emoji> **💰 ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"
            message += f"<emoji id=6309709550878463216>🌟</emoji> **ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴛʜᴇ **ʀᴇᴄᴇɪᴠᴇʀ'ꜱ ᴜꜱᴇʀ ɪᴅ**:\ɴ**"
            message += f"<emoji id=5280904324724063665>😽</emoji> **_(ᴏɴʟʏ ɴᴜᴍᴇʀɪᴄ ɪᴅ, ᴇ.ɢ., 123456789)_**"

            # Sirf Back button
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("<emoji id=6307457716705040156>👍</emoji> **⬅️ ʙᴀᴄᴋ ᴛᴏ ʙᴀʟᴀɴᴄᴇ**", callback_data="balance"))

            edit_or_resend(
                call.message.chat.id,
                call.message.message_id,
                message,
                markup=markup,
                parse_mode="Markdown"
            )

            # Set user state for user ID input
            user_stage[user_id] = "waiting_receiver_id"

        elif data == "transfer_confirm":
            # Transfer confirmation screen
            transfer_data = user_states.get(user_id, {})
            if not transfer_data or "receiver_id" not in transfer_data or "amount" not in transfer_data:
                bot.answer_callback_query(call.id, "<emoji id=5280606902533783431>😽</emoji> **❌ ꜱᴇꜱꜱɪᴏɴ ᴇxᴩɪʀᴇᴅ**", show_alert=True)
                clean_ui_and_send_menu(call.message.chat.id, user_id)
                return

            receiver_id = transfer_data["receiver_id"]
            receiver_name = transfer_data.get("receiver_name", f"<emoji id=4926993814033269936>🖕</emoji> **ɪᴅ: {ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}**")
            amount = transfer_data["amount"]
            sender_balance = get_balance(user_id)

            message = f"<emoji id=5235985147265837746>🗒</emoji> **📤 **ᴄᴏɴꜰɪʀᴍ ᴛʀᴀɴꜱꜰᴇʀ**\ɴ\ɴ**"
            message += f"<emoji id=6309709550878463216>🌟</emoji> **👤 ʀᴇᴄᴇɪᴠᴇʀ: {ʀᴇᴄᴇɪᴠᴇʀ_ɴᴀᴍᴇ}\ɴ**"
            message += f"<emoji id=6309819721084573392>🌙</emoji> **🆔 ʀᴇᴄᴇɪᴠᴇʀ ɪᴅ: `{ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}`\ɴ**"
            message += f"<emoji id=5352870513267973607>✨</emoji> **💰 ᴀᴍᴏᴜɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
            message += f"<emoji id=5280606902533783431>😽</emoji> **💳 ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ꜱᴇɴᴅᴇʀ_ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"
            message += f"<emoji id=5354924568492383911>😈</emoji> **ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴩʀᴏᴄᴇᴇᴅ?**"

            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("<emoji id=6309640268761011366>🌙</emoji> **✅ ᴄᴏɴꜰɪʀᴍ**", callback_data="transfer_execute"),
                InlineKeyboardButton("<emoji id=6307821174017496029>🔥</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="balance")
            )

            edit_or_resend(
                call.message.chat.id,
                call.message.message_id,
                message,
                markup=markup,
                parse_mode="Markdown"
            )

        elif data == "transfer_execute":
            # Execute transfer
            transfer_data = user_states.get(user_id, {})
            if not transfer_data or "receiver_id" not in transfer_data or "amount" not in transfer_data:
                bot.answer_callback_query(call.id, "<emoji id=5280904324724063665>😽</emoji> **❌ ꜱᴇꜱꜱɪᴏɴ ᴇxᴩɪʀᴇᴅ**", show_alert=True)
                clean_ui_and_send_menu(call.message.chat.id, user_id)
                return

            receiver_id = transfer_data["receiver_id"]
            receiver_name = transfer_data.get("receiver_name", f"<emoji id=5999210495146465994>💖</emoji> **ɪᴅ: {ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}**")
            amount = transfer_data["amount"]

            success, message_text = transfer_balance(user_id, receiver_id, amount)

            if success:
                # Get updated balances
                sender_new_balance = get_balance(user_id)
                receiver_new_balance = get_balance(receiver_id)

                # Message for sender
                sender_message = f"<emoji id=5999151980512024620>🥰</emoji> **✅ **ᴛʀᴀɴꜱꜰᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ!**\ɴ\ɴ**"
                sender_message += f"<emoji id=6224236403153179330>🎀</emoji> **👤 ꜱᴇɴᴛ ᴛᴏ: {ʀᴇᴄᴇɪᴠᴇʀ_ɴᴀᴍᴇ}\ɴ**"
                sender_message += f"<emoji id=5998881015320287132>💊</emoji> **🆔 ʀᴇᴄᴇɪᴠᴇʀ ɪᴅ: `{ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}`\ɴ**"
                sender_message += f"<emoji id=5280678521113443426>😽</emoji> **💰 ᴀᴍᴏᴜɴᴛ ꜱᴇɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
                sender_message += f"<emoji id=6111778259374971023>🔥</emoji> **💳 ʏᴏᴜʀ ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ꜱᴇɴᴅᴇʀ_ɴᴇᴡ_ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"

                # Sirf Back to Balance button
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("<emoji id=6001589602085771497>✅</emoji> **⬅️ ʙᴀᴄᴋ ᴛᴏ ʙᴀʟᴀɴᴄᴇ**", callback_data="balance"))

                edit_or_resend(
                    call.message.chat.id,
                    call.message.message_id,
                    sender_message,
                    markup=markup,
                    parse_mode="Markdown"
                )

                # Send notification to receiver
                try:
                    # Get sender name
                    sender = users_col.find_one({"user_id": user_id})
                    sender_name = sender.get("name", "Unknown") if sender else "Unknown"

                    receiver_message = f"<emoji id=6309666601205503867>💌</emoji> **📥 **ʙᴀʟᴀɴᴄᴇ ʀᴇᴄᴇɪᴠᴇᴅ!**\ɴ\ɴ**"
                    receiver_message += f"<emoji id=6152444560216693216>🥰</emoji> **👤 ꜰʀᴏᴍ: {ꜱᴇɴᴅᴇʀ_ɴᴀᴍᴇ}\ɴ**"
                    receiver_message += f"<emoji id=4927247234283603387>🩷</emoji> **🆔 ꜱᴇɴᴅᴇʀ ɪᴅ: `{ᴜꜱᴇʀ_ɪᴅ}`\ɴ**"
                    receiver_message += f"<emoji id=6309666601205503867>💌</emoji> **💰 ᴀᴍᴏᴜɴᴛ ʀᴇᴄᴇɪᴠᴇᴅ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
                    receiver_message += f"<emoji id=6152142357727811958>🦋</emoji> **💳 ʏᴏᴜʀ ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ʀᴇᴄᴇɪᴠᴇʀ_ɴᴇᴡ_ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"

                    # Sirf Close button for receiver
                    receiver_markup = InlineKeyboardMarkup()
                    receiver_markup.add(InlineKeyboardButton("<emoji id=6307568836098922002>🌙</emoji> **❌ ᴄʟᴏꜱᴇ**", callback_data="back_to_menu"))

                    bot.send_message(
                        receiver_id,
                        receiver_message,
                        parse_mode="Markdown",
                        reply_markup=receiver_markup
                    )
                except Exception as e:
                    logger.warning(f"<emoji id=4927247234283603387>🩷</emoji> **ᴄᴏᴜʟᴅ ɴᴏᴛ ɴᴏᴛɪꜰʏ ʀᴇᴄᴇɪᴠᴇʀ {ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}: {ᴇ}**")

            else:
                # Transfer failed
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("<emoji id=4929195195225867512>💎</emoji> **🔄 ᴛʀʏ ᴀɢᴀɪɴ**", callback_data="send_balance_menu"),
                    InlineKeyboardButton("<emoji id=4927247234283603387>🩷</emoji> **⬅️ ʙᴀᴄᴋ ᴛᴏ ʙᴀʟᴀɴᴄᴇ**", callback_data="balance")
                )

                edit_or_resend(
                    call.message.chat.id,
                    call.message.message_id,
                    f"<emoji id=5352870513267973607>✨</emoji> **❌ **ᴛʀᴀɴꜱꜰᴇʀ ꜰᴀɪʟᴇᴅ!**\ɴ\ɴ{ᴍᴇꜱꜱᴀɢᴇ_ᴛᴇxᴛ}**",
                    markup=markup,
                    parse_mode="Markdown"
                )

            # Clear transfer state
            if user_id in user_states:
                user_states.pop(user_id, None)
            if user_id in user_stage:
                user_stage.pop(user_id, None)

        elif data == "redeem_coupon":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6307643744623531146>🦋</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6111742817304841054>✅</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            msg_text = "<emoji id=5280606902533783431>😽</emoji> **🎟 **ʀᴇᴅᴇᴇᴍ ᴄᴏᴜᴩᴏɴ**\ɴ\ɴᴇɴᴛᴇʀ ʏᴏᴜʀ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ:**"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("<emoji id=6307643744623531146>🦋</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="back_to_menu"))

            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass

            sent_msg = bot.send_message(
                call.message.chat.id,
                msg_text,
                parse_mode="Markdown",
                reply_markup=markup
            )
            user_last_message[user_id] = sent_msg.message_id
            user_stage[user_id] = "waiting_coupon"

        elif data == "recharge":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6111418418424973677>✅</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6152142357727811958>🦋</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            show_recharge_methods(call.message.chat.id, call.message.message_id, user_id)

        elif data == "refer_friends":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6224236403153179330>🎀</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6307821174017496029>🔥</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            show_referral_info(user_id, call.message.chat.id)

        elif data == "support":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6307821174017496029>🔥</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6307447640711763730>💟</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            msg_text = "<emoji id=5040016479722931047>✨</emoji> **🛠️ ꜱᴜᴩᴩᴏʀᴛ:@ᴍᴀᴅᴀʀᴀ_x_ᴅɪꜱᴛʀᴏʏᴇʀ**"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("<emoji id=6111418418424973677>✅</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="back_to_menu"))

            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass

            sent_msg = bot.send_message(
                call.message.chat.id,
                msg_text,
                reply_markup=markup
            )
            user_last_message[user_id] = sent_msg.message_id

        elif data == "admin_panel":
            if is_admin(user_id):
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except:
                    pass
                show_admin_panel(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6151981777490548710>✅</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data.startswith("bulk_account_"):
            if not is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=6307553838073124532>✨</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)
                return

            country_name = data.replace("bulk_account_", "")

            bulk_add_states[user_id] = {
                "mode": "bulk",
                "country": country_name,
                "phone_numbers": [],
                "current_index": 0,
                "total_numbers": 0,
                "success_count": 0,
                "failed_count": 0,
                "failed_numbers": [],
                "current_client": None,
                "current_phone_code_hash": None,
                "current_phone": None,
                "current_manager": None,
                "password_attempts": 0,
                "message_id": call.message.message_id,
                "step": "waiting_numbers",
                "chat_id": call.message.chat.id,
                "is_processing": False
            }

            edit_or_resend(
                call.message.chat.id,
                call.message.message_id,
                f"<emoji id=6152142357727811958>🦋</emoji> **📦 **ʙᴜʟᴋ ᴀᴄᴄᴏᴜɴᴛ ᴀᴅᴅɪᴛɪᴏɴ**\ɴ\ɴ**"
                f"<emoji id=6001589602085771497>✅</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}\ɴ\ɴ**"
                "<emoji id=6309985824649780135>🌙</emoji> **📱 ᴇɴᴛᴇʀ ᴩʜᴏɴᴇ ɴᴜᴍʙᴇʀꜱ (ᴏɴᴇ ᴩᴇʀ ʟɪɴᴇ):\ɴ**"
                "<emoji id=6151981777490548710>✅</emoji> **ꜰᴏʀᴍᴀᴛ:\ɴ**"
                "<emoji id=6152142357727811958>🦋</emoji> **+91xxxxxxxxxx\ɴ**"
                "<emoji id=4929483658114368660>💎</emoji> **+91828xxxxxxx\ɴ**"
                "<emoji id=6307750079423845494>👑</emoji> **+91999xxxxxxx\ɴ\ɴ**"
                "<emoji id=4929195195225867512>💎</emoji> **⚠️ ᴍᴀx 50 ɴᴜᴍʙᴇʀꜱ ᴀᴛ ᴏɴᴄᴇ\ɴ**"
                "<emoji id=6001132493011425597>💖</emoji> **⚠️ ɪɴᴄʟᴜᴅᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ\ɴ**"
                "<emoji id=5280606902533783431>😽</emoji> **⚠️ ᴏɴᴇ ɴᴜᴍʙᴇʀ ᴩᴇʀ ʟɪɴᴇ**",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=5999041732996504081>✨</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_bulk")
                )
            )

        elif data.startswith("single_account_"):
            country_name = data.replace("single_account_", "")
            login_states[user_id]["country"] = country_name
            login_states[user_id]["step"] = "phone"
            login_states[user_id]["mode"] = "single"

            edit_or_resend(
                call.message.chat.id,
                call.message.message_id,
                f"<emoji id=5285100774060227768>😽</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}\ɴ\ɴ**"
                "<emoji id=6307750079423845494>👑</emoji> **📱 ᴇɴᴛᴇʀ ᴩʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ:\ɴ**"
                "<emoji id=6307643744623531146>🦋</emoji> **ᴇxᴀᴍᴩʟᴇ: +919876543210**",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=6310022800023229454>✡️</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_login")
                )
            )

        elif data == "start_bulk_add":
            if not is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=6152444560216693216>🥰</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)
                return

            if user_id not in bulk_add_states:
                bot.answer_callback_query(call.id, "<emoji id=4929195195225867512>💎</emoji> **❌ ꜱᴇꜱꜱɪᴏɴ ᴇxᴩɪʀᴇᴅ**", show_alert=True)
                return

            state = bulk_add_states[user_id]
            if not state.get("phone_numbers"):
                bot.answer_callback_query(call.id, "<emoji id=6001589602085771497>✅</emoji> **❌ ɴᴏ ᴩʜᴏɴᴇ ɴᴜᴍʙᴇʀꜱ ᴛᴏ ᴩʀᴏᴄᴇꜱꜱ**", show_alert=True)
                return

            bot.answer_callback_query(call.id, "<emoji id=6309985824649780135>🌙</emoji> **🚀 ꜱᴛᴀʀᴛɪɴɢ ʙᴜʟᴋ ᴀᴄᴄᴏᴜɴᴛ ᴀᴅᴅɪᴛɪᴏɴ...**")
            start_bulk_processing(user_id)

        elif data == "cancel_bulk":
            handle_cancel_bulk(call)

        elif data == "pause_bulk":
            if user_id in bulk_add_states:
                bulk_add_states[user_id]["is_processing"] = False
                bot.answer_callback_query(call.id, "<emoji id=6307553838073124532>✨</emoji> **⏸️ ᴩʀᴏᴄᴇꜱꜱɪɴɢ ᴩᴀᴜꜱᴇᴅ**", show_alert=True)

        elif data == "resume_bulk":
            if user_id in bulk_add_states:
                bulk_add_states[user_id]["is_processing"] = True
                bot.answer_callback_query(call.id, "<emoji id=6307821174017496029>🔥</emoji> **▶️ ᴩʀᴏᴄᴇꜱꜱɪɴɢ ʀᴇꜱᴜᴍᴇᴅ**", show_alert=True)
                process_next_bulk_number(user_id)

        elif data == "skip_bulk_number":
            if user_id in bulk_add_states:
                state = bulk_add_states[user_id]
                state["failed_count"] += 1
                state["failed_numbers"].append({
                    "number": state.get("current_phone", "Unknown"),
                    "reason": "<emoji id=5999151980512024620>🥰</emoji> **ꜱᴋɪᴩᴩᴇᴅ ʙʏ ᴀᴅᴍɪɴ**"
                })

                if state.get("current_client") and account_manager:
                    try:
                        asyncio.run(account_manager.pyrogram_manager.safe_disconnect(state["current_client"]))
                    except:
                        pass

                state["current_index"] += 1
                state["password_attempts"] = 0
                bot.answer_callback_query(call.id, "<emoji id=5999210495146465994>💖</emoji> **⏭️ ɴᴜᴍʙᴇʀ ꜱᴋɪᴩᴩᴇᴅ**", show_alert=True)
                process_next_bulk_number(user_id)

        elif data.startswith("country_raw_"):
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=4929483658114368660>💎</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6111742817304841054>✅</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            country_name = data.replace("country_raw_", "")
            show_country_details(user_id, country_name, call.message.chat.id, call.message.message_id, call.id)

        elif data.startswith("buy_"):
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6310044717241340733>🔄</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6309666601205503867>💌</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            account_id = data.split("_", 1)[1]
            process_purchase(user_id, account_id, call.message.chat.id, call.message.message_id, call.id)

        elif data.startswith("logout_session_"):
            session_id = data.split("_", 2)[2]
            handle_logout_session(user_id, session_id, call.message.chat.id, call.id)

        elif data.startswith("get_otp_"):
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=5999151980512024620>🥰</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=5041955142060999726>🌈</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            session_id = data.split("_", 2)[2]
            get_latest_otp(user_id, session_id, call.message.chat.id, call.id)

        elif data == "back_to_countries":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=5999151980512024620>🥰</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=5281001756057175314>😽</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            show_countries(call.message.chat.id)

        elif data == "back_to_menu":
            clean_ui_and_send_menu(call.message.chat.id, user_id)

        elif data == "recharge_upi":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6307490397111195260>🦋</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=5285100774060227768>😽</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            recharge_method_state[user_id] = "upi"
            edit_or_resend(
                call.message.chat.id,
                call.message.message_id,
                "<emoji id=6224236403153179330>🎀</emoji> **💳 ᴇɴᴛᴇʀ ʀᴇᴄʜᴀʀɢᴇ ᴀᴍᴏᴜɴᴛ ꜰᴏʀ ᴜᴩɪ (ᴍɪɴɪᴍᴜᴍ ₹1):**",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=6111418418424973677>✅</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="back_to_menu")
                )
            )
            bot.register_next_step_handler(call.message, process_recharge_amount)

        elif data == "recharge_crypto":
            if not has_user_joined_channels(user_id):
                missing_channels = get_missing_channels(user_id)
                missing_list = "\n".join([f"<emoji id=6151981777490548710>✅</emoji> **• {ᴄʜ}**" for ch in missing_channels])
                bot.answer_callback_query(
                    call.id, 
                    f"<emoji id=6287579968109024771>✅</emoji> **❌ ᴩʟᴇᴀꜱᴇ ᴊᴏɪɴ:\ɴ{ᴍɪꜱꜱɪɴɢ_ʟɪꜱᴛ}**", 
                    show_alert=True
                )
                start(call.message)
                return

            recharge_method_state[user_id] = "crypto"
            edit_or_resend(
                call.message.chat.id,
                call.message.message_id,
                "<emoji id=5395580801930771895>🤍</emoji> **💳 ᴇɴᴛᴇʀ ʀᴇᴄʜᴀʀɢᴇ ᴀᴍᴏᴜɴᴛ ɪɴ ɪɴʀ ꜰᴏʀ ᴄʀʏᴩᴛᴏ (ᴍɪɴɪᴍᴜᴍ ₹1):**",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=6307447640711763730>💟</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="back_to_menu")
                )
            )
            bot.register_next_step_handler(call.message, process_recharge_amount)

        elif data == "upi_deposited":
            user_id = call.from_user.id
            amount = upi_payment_states.get(user_id, {}).get("amount", 0)
            if amount <= 0:
                bot.answer_callback_query(call.id, "<emoji id=5352542184493031170>😈</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ**", show_alert=True)
                return

            bot.answer_callback_query(call.id, "<emoji id=5998977626314643141>🦋</emoji> **📝 ᴩʟᴇᴀꜱᴇ ꜱᴇɴᴅ ʏᴏᴜʀ 12-ᴅɪɢɪᴛ ᴜᴛʀ ɴᴜᴍʙᴇʀ**", show_alert=False)

            upi_payment_states[user_id] = {
                "step": "waiting_utr",
                "amount": amount,
                "chat_id": call.message.chat.id
            }

            bot.send_message(
                call.message.chat.id,
                "<emoji id=6123125485661591081>🩷</emoji> **📝 **ꜱᴛᴇᴩ 1: ᴇɴᴛᴇʀ ᴜᴛʀ**\ɴ\ɴ**"
                "<emoji id=5280606902533783431>😽</emoji> **ᴩʟᴇᴀꜱᴇ ꜱᴇɴᴅ ʏᴏᴜʀ 12-ᴅɪɢɪᴛ ᴜᴛʀ ɴᴜᴍʙᴇʀ:\ɴ**"
                "<emoji id=5999210495146465994>💖</emoji> **_(ꜱᴇɴᴛ ʙʏ ʏᴏᴜʀ ʙᴀɴᴋ ᴀꜰᴛᴇʀ ᴩᴀʏᴍᴇɴᴛ)_**"
            )

        elif data.startswith("<emoji id=6309739370836399696>🌙</emoji> **ᴀᴩᴩʀᴏᴠᴇ_ʀᴇᴄʜ|**") or data.startswith("<emoji id=4926993814033269936>🖕</emoji> **ᴄᴀɴᴄᴇʟ_ʀᴇᴄʜ|**"):
            if is_admin(user_id):
                parts = data.split("|")
                action = parts[0]
                req_id = parts[1] if len(parts) > 1 else None

                # Process approval/rejection
                success, message, admin_info = process_recharge_approval(user_id, req_id, 
                                                                        "approve" if action == "approve_rech" else "reject")

                if success:
                    bot.answer_callback_query(call.id, message, show_alert=True)

                    # Delete the original admin message
                    try:
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass

                    # Send new message showing which admin approved/rejected
                    admin_action_msg = f"<emoji id=5352870513267973607>✨</emoji> **✅ **ʀᴇᴄʜᴀʀɢᴇ ʀᴇꞯᴜᴇꜱᴛ ᴩʀᴏᴄᴇꜱꜱᴇᴅ**\ɴ\ɴ**"
                    admin_action_msg += f"<emoji id=5040016479722931047>✨</emoji> **📋 ʀᴇꞯᴜᴇꜱᴛ ɪᴅ: `{ʀᴇꞯ_ɪᴅ}`\ɴ**"
                    admin_action_msg += f"<emoji id=5235985147265837746>🗒</emoji> **👤 ᴩʀᴏᴄᴇꜱꜱᴇᴅ ʙʏ: {ᴀᴅᴍɪɴ_ɪɴꜰᴏ['ᴀᴅᴍɪɴ_ɴᴀᴍᴇ']}\ɴ**"
                    admin_action_msg += f"<emoji id=6307750079423845494>👑</emoji> **🆔 ᴀᴅᴍɪɴ ɪᴅ: `{ᴀᴅᴍɪɴ_ɪɴꜰᴏ['ᴀᴅᴍɪɴ_ɪᴅ']}`\ɴ**"
                    admin_action_msg += f"<emoji id=6307643744623531146>🦋</emoji> **📌 ᴀᴄᴛɪᴏɴ: **{ᴀᴅᴍɪɴ_ɪɴꜰᴏ['ᴀᴄᴛɪᴏɴ'].ᴜᴩᴩᴇʀ()}**\ɴ**"
                    admin_action_msg += f"<emoji id=6224236403153179330>🎀</emoji> **⏰ ᴛɪᴍᴇ: {ᴅᴀᴛᴇᴛɪᴍᴇ.ᴜᴛᴄɴᴏᴡ().ꜱᴛʀꜰᴛɪᴍᴇ('%ʏ-%ᴍ-%ᴅ %ʜ:%ᴍ:%ꜱ')}**"

                    bot.send_message(
                        call.message.chat.id,
                        admin_action_msg,
                        parse_mode="Markdown"
                    )
                else:
                    bot.answer_callback_query(call.id, f"<emoji id=6309819721084573392>🌙</emoji> **❌ {ᴍᴇꜱꜱᴀɢᴇ}**", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "<emoji id=5352870513267973607>✨</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "add_account":
            logger.info(f"<emoji id=4926993814033269936>🖕</emoji> **ᴀᴅᴅ ᴀᴄᴄᴏᴜɴᴛ ʙᴜᴛᴛᴏɴ ᴄʟɪᴄᴋᴇᴅ ʙʏ ᴜꜱᴇʀ {ᴜꜱᴇʀ_ɪᴅ}**")
            if not is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5285100774060227768>😽</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)
                return

            login_states[user_id] = {
                "step": "select_country",
                "message_id": call.message.message_id,
                "chat_id": call.message.chat.id
            }

            countries = get_all_countries()
            if not countries:
                bot.answer_callback_query(call.id, "<emoji id=6111742817304841054>✅</emoji> **❌ ɴᴏ ᴄᴏᴜɴᴛʀɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ. ᴀᴅᴅ ᴀ ᴄᴏᴜɴᴛʀʏ ꜰɪʀꜱᴛ.**", show_alert=True)
                return

            markup = InlineKeyboardMarkup(row_width=2)
            for country in countries:
                markup.add(InlineKeyboardButton(
                    country['name'],
                    callback_data=f"<emoji id=6123040393769521180>☄️</emoji> **ʟᴏɢɪɴ_ᴄᴏᴜɴᴛʀʏ_{ᴄᴏᴜɴᴛʀʏ['ɴᴀᴍᴇ']}**"
                ))
            markup.add(InlineKeyboardButton("<emoji id=5280904324724063665>😽</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_login"))

            edit_or_resend(
                call.message.chat.id,
                call.message.message_id,
                "<emoji id=6309709550878463216>🌟</emoji> **🌍 **ꜱᴇʟᴇᴄᴛ ᴄᴏᴜɴᴛʀʏ ꜰᴏʀ ᴀᴄᴄᴏᴜɴᴛ**\ɴ\ɴᴄʜᴏᴏꜱᴇ ᴄᴏᴜɴᴛʀʏ:**",
                markup=markup
            )

        elif data.startswith("login_country_"):
            handle_login_country_selection(call)

        elif data == "cancel_login":
            handle_cancel_login(call)

        elif data == "out_of_stock":
            bot.answer_callback_query(call.id, "<emoji id=6111778259374971023>🔥</emoji> **❌ ᴏᴜᴛ ᴏꜰ ꜱᴛᴏᴄᴋ! ɴᴏ ᴀᴄᴄᴏᴜɴᴛꜱ ᴀᴠᴀɪʟᴀʙʟᴇ.**", show_alert=True)

        elif data == "edit_price":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5998977626314643141>🦋</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                show_edit_price_country_selection(call.message.chat.id, call.message.message_id)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6111742817304841054>✅</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data.startswith("edit_price_country_"):
            if is_admin(user_id):
                country_name = data.replace("edit_price_country_", "")
                show_edit_price_details(call.message.chat.id, call.message.message_id, country_name)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6111778259374971023>🔥</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data.startswith("edit_price_confirm_"):
            if is_admin(user_id):
                country_name = data.replace("edit_price_confirm_", "")
                edit_price_state[user_id] = {"country": country_name, "step": "waiting_price"}
                try:
                    country = get_country_by_name(country_name)
                    if country:
                        current_price = country.get("price", 0)
                        edit_or_resend(
                            call.message.chat.id,
                            call.message.message_id,
                            f"<emoji id=6152444560216693216>🥰</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}\ɴ💰 ᴄᴜʀʀᴇɴᴛ ᴩʀɪᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴜʀʀᴇɴᴛ_ᴩʀɪᴄᴇ)}\ɴ\ɴ**"
                            f"<emoji id=5352870513267973607>✨</emoji> **ᴇɴᴛᴇʀ ɴᴇᴡ ᴩʀɪᴄᴇ ꜰᴏʀ {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}:**",
                            markup=InlineKeyboardMarkup().add(
                                InlineKeyboardButton("<emoji id=5235985147265837746>🗒</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="manage_countries")
                            )
                        )
                    else:
                        bot.answer_callback_query(call.id, "<emoji id=6287579968109024771>✅</emoji> **❌ ᴄᴏᴜɴᴛʀʏ ɴᴏᴛ ꜰᴏᴜɴᴅ**", show_alert=True)
                except:
                    pass
            else:
                bot.answer_callback_query(call.id, "<emoji id=4927247234283603387>🩷</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "cancel_edit_price":
            if is_admin(user_id):
                show_country_management(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, "<emoji id=5899776109548934640>💲</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "admin_coupon_menu":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5318828550940293906>🐱</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**")
                show_coupon_management(call.message.chat.id, call.message.message_id)
            else:
                bot.answer_callback_query(call.id, "<emoji id=5899776109548934640>💲</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "admin_create_coupon":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=6298684666182371615>❤️</emoji> **ᴄʀᴇᴀᴛɪɴɢ ᴄᴏᴜᴩᴏɴ...**")
                coupon_state[user_id] = {"step": "ask_code"}
                edit_or_resend(
                    call.message.chat.id,
                    call.message.message_id,
                    "<emoji id=4929369656797431200>🪐</emoji> **🎟 **ᴄʀᴇᴀᴛᴇ ᴄᴏᴜᴩᴏɴ**\ɴ\ɴᴇɴᴛᴇʀ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ:**",
                    markup=InlineKeyboardMarkup().add(
                        InlineKeyboardButton("<emoji id=5041955142060999726>🌈</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="admin_coupon_menu")
                    ),
                    parse_mode="Markdown"
                )
            else:
                bot.answer_callback_query(call.id, "<emoji id=5041955142060999726>🌈</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "admin_remove_coupon":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5352870513267973607>✨</emoji> **ʀᴇᴍᴏᴠɪɴɢ ᴄᴏᴜᴩᴏɴ...**")
                coupon_state[user_id] = {"step": "ask_remove_code"}
                edit_or_resend(
                    call.message.chat.id,
                    call.message.message_id,
                    "<emoji id=6309985824649780135>🌙</emoji> **🗑 **ʀᴇᴍᴏᴠᴇ ᴄᴏᴜᴩᴏɴ**\ɴ\ɴᴇɴᴛᴇʀ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ:**",
                    markup=InlineKeyboardMarkup().add(
                        InlineKeyboardButton("<emoji id=5285100774060227768>😽</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="admin_coupon_menu")
                    ),
                    parse_mode="Markdown"
                )
            else:
                bot.answer_callback_query(call.id, "<emoji id=6298684666182371615>❤️</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "admin_coupon_status":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=6309640268761011366>🌙</emoji> **ᴄʜᴇᴄᴋɪɴɢ ᴄᴏᴜᴩᴏɴ ꜱᴛᴀᴛᴜꜱ...**")
                coupon_state[user_id] = {"step": "ask_status_code"}
                edit_or_resend(
                    call.message.chat.id,
                    call.message.message_id,
                    "<emoji id=5318828550940293906>🐱</emoji> **📊 **ᴄᴏᴜᴩᴏɴ ꜱᴛᴀᴛᴜꜱ**\ɴ\ɴᴇɴᴛᴇʀ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ ᴛᴏ ᴄʜᴇᴄᴋ:**",
                    markup=InlineKeyboardMarkup().add(
                        InlineKeyboardButton("<emoji id=6307457716705040156>👍</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="admin_coupon_menu")
                    ),
                    parse_mode="Markdown"
                )
            else:
                bot.answer_callback_query(call.id, "<emoji id=5041955142060999726>🌈</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "broadcast_menu":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5999041732996504081>✨</emoji> **📢 ʀᴇᴩʟʏ ᴀɴʏ ᴩʜᴏᴛᴏ / ᴅᴏᴄᴜᴍᴇɴᴛ / ᴠɪᴅᴇᴏ / ᴛᴇxᴛ ᴡɪᴛʜ /ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ**")
                bot.send_message(call.message.chat.id, "<emoji id=6298717844804733009>♾</emoji> **📢 **ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ**\ɴ\ɴʀᴇᴩʟʏ ᴛᴏ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ (ᴩʜᴏᴛᴏ / ᴅᴏᴄᴜᴍᴇɴᴛ / ᴠɪᴅᴇᴏ / ᴛᴇxᴛ) ᴡɪᴛʜ /ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ\ɴ\ɴ✅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴀꜱ-ɪꜱ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ.**")
            else:
                bot.answer_callback_query(call.id, "<emoji id=6307457716705040156>👍</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "refund_start":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=4929483658114368660>💎</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                msg = bot.send_message(call.message.chat.id, "<emoji id=6154635934135490309>💗</emoji> **💸 ᴇɴᴛᴇʀ ᴜꜱᴇʀ ɪᴅ ꜰᴏʀ ʀᴇꜰᴜɴᴅ:**")
                bot.register_next_step_handler(msg, ask_refund_user)
            else:
                bot.answer_callback_query(call.id, "<emoji id=5280721097124249567>😽</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "ranking":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=6152142357727811958>🦋</emoji> **📊 ɢᴇɴᴇʀᴀᴛɪɴɢ ʀᴀɴᴋɪɴɢ...**")
                show_user_ranking(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, "<emoji id=5318828550940293906>🐱</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "message_user":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=4926993814033269936>🖕</emoji> **👤 ᴇɴᴛᴇʀ ᴜꜱᴇʀ ɪᴅ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ:**")
                msg = bot.send_message(call.message.chat.id, "<emoji id=5281001756057175314>😽</emoji> **👤 ᴇɴᴛᴇʀ ᴜꜱᴇʀ ɪᴅ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ:**")
                bot.register_next_step_handler(msg, ask_message_content)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6307553838073124532>✨</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "admin_deduct_start":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5354924568492383911>😈</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                admin_deduct_state[user_id] = {"step": "ask_user_id"}
                msg = bot.send_message(call.message.chat.id, "<emoji id=5318828550940293906>🐱</emoji> **👤 ᴇɴᴛᴇʀ ᴜꜱᴇʀ ɪᴅ ᴡʜᴏꜱᴇ ʙᴀʟᴀɴᴄᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇᴅᴜᴄᴛ:**")
                if user_id in broadcast_data:
                    del broadcast_data[user_id]
            else:
                bot.answer_callback_query(call.id, "<emoji id=6111778259374971023>🔥</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "ban_user":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=6307457716705040156>👍</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                msg = bot.send_message(call.message.chat.id, "<emoji id=6111778259374971023>🔥</emoji> **🚫 ᴇɴᴛᴇʀ ᴜꜱᴇʀ ɪᴅ ᴛᴏ ʙᴀɴ:**")
                bot.register_next_step_handler(msg, ask_ban_user)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6309739370836399696>🌙</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "unban_user":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5999340396432333728>☺️</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                msg = bot.send_message(call.message.chat.id, "<emoji id=5998881015320287132>💊</emoji> **✅ ᴇɴᴛᴇʀ ᴜꜱᴇʀ ɪᴅ ᴛᴏ ᴜɴʙᴀɴ:**")
                bot.register_next_step_handler(msg, ask_unban_user)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6111418418424973677>✅</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "manage_countries":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5999270482954691955>🦋</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                show_country_management(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6309985824649780135>🌙</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "add_country":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=5281001756057175314>😽</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                msg = bot.send_message(call.message.chat.id, "<emoji id=6309819721084573392>🌙</emoji> **🌍 ᴇɴᴛᴇʀ ᴄᴏᴜɴᴛʀʏ ɴᴀᴍᴇ ᴛᴏ ᴀᴅᴅ:**")
                bot.register_next_step_handler(msg, ask_country_name)
            else:
                bot.answer_callback_query(call.id, "<emoji id=5352542184493031170>😈</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data == "remove_country":
            if is_admin(user_id):
                bot.answer_callback_query(call.id, "<emoji id=6111390922044344694>✅</emoji> **ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**")
                show_country_removal(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, "<emoji id=6152142357727811958>🦋</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        elif data.startswith("remove_country_"):
            if is_admin(user_id):
                country_name = data.split("_", 2)[2]
                result = remove_country(country_name, call.message.chat.id, call.message.message_id)
                bot.answer_callback_query(call.id, result, show_alert=True)
            else:
                bot.answer_callback_query(call.id, "<emoji id=5999210495146465994>💖</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**", show_alert=True)

        else:
            bot.answer_callback_query(call.id, "<emoji id=6307750079423845494>👑</emoji> **❌ ᴜɴᴋɴᴏᴡɴ ᴀᴄᴛɪᴏɴ**", show_alert=True)

    except Exception as e:
        logger.error(f"<emoji id=5998881015320287132>💊</emoji> **ᴄᴀʟʟʙᴀᴄᴋ ᴇʀʀᴏʀ: {ᴇ}**")
        try:
            bot.answer_callback_query(call.id, "<emoji id=6309640268761011366>🌙</emoji> **❌ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ**", show_alert=True)
            if is_admin(user_id):
                bot.send_message(call.message.chat.id, f"<emoji id=6111418418424973677>✅</emoji> **ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀ ᴇʀʀᴏʀ:\ɴ{ᴇ}**")
        except:
            pass

# ---------------------------------------------------------------------
# BULK ACCOUNT FUNCTIONS
# ---------------------------------------------------------------------

def handle_cancel_bulk(call):
    user_id = call.from_user.id

    if user_id in bulk_add_states:
        state = bulk_add_states[user_id]

        if state.get("current_client") and account_manager:
            try:
                asyncio.run(account_manager.pyrogram_manager.safe_disconnect(state["current_client"]))
            except:
                pass

        del bulk_add_states[user_id]

    edit_or_resend(
        call.message.chat.id,
        call.message.message_id,
        "<emoji id=6111778259374971023>🔥</emoji> **❌ ʙᴜʟᴋ ᴀᴄᴄᴏᴜɴᴛ ᴀᴅᴅɪᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.**",
        markup=None
    )
    show_admin_panel(call.message.chat.id)

@bot.message_handler(func=lambda m: bulk_add_states.get(m.from_user.id, {}).get("step") == "waiting_numbers")
def handle_bulk_numbers_input(msg):
    user_id = msg.from_user.id

    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]
    if state.get("step") != "waiting_numbers":
        return

    text = msg.text.strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    valid_numbers = []
    invalid_numbers = []

    for line in lines[:50]:
        if re.match(r'<emoji id=6307568836098922002>🌙</emoji> **^\+\ᴅ{10,15}$**', line):
            valid_numbers.append(line)
        else:
            invalid_numbers.append(line)

    if not valid_numbers:
        bot.send_message(
            msg.chat.id,
            "<emoji id=4927247234283603387>🩷</emoji> **❌ ɴᴏ ᴠᴀʟɪᴅ ᴩʜᴏɴᴇ ɴᴜᴍʙᴇʀꜱ ꜰᴏᴜɴᴅ.\ɴ**"
            "<emoji id=5998881015320287132>💊</emoji> **ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀꜱ ɪɴ ꜰᴏʀᴍᴀᴛ: +91xxxxxxxxxx\ɴ**"
            "<emoji id=6307568836098922002>🌙</emoji> **ᴏɴᴇ ᴩᴇʀ ʟɪɴᴇ.**"
        )
        return

    state["phone_numbers"] = valid_numbers
    state["total_numbers"] = len(valid_numbers)
    state["step"] = "confirm_numbers"

    message = f"<emoji id=6309666601205503867>💌</emoji> **📦 **ʙᴜʟᴋ ᴀᴄᴄᴏᴜɴᴛ ᴀᴅᴅɪᴛɪᴏɴ**\ɴ\ɴ**"
    message += f"<emoji id=5899776109548934640>💲</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ꜱᴛᴀᴛᴇ['ᴄᴏᴜɴᴛʀʏ']}\ɴ**"
    message += f"<emoji id=4929195195225867512>💎</emoji> **📱 ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀꜱ: {ʟᴇɴ(ᴠᴀʟɪᴅ_ɴᴜᴍʙᴇʀꜱ)}\ɴ**"

    if invalid_numbers:
        message += f"<emoji id=6152142357727811958>🦋</emoji> **⚠️ ɪɴᴠᴀʟɪᴅ (ꜱᴋɪᴩᴩᴇᴅ): {ʟᴇɴ(ɪɴᴠᴀʟɪᴅ_ɴᴜᴍʙᴇʀꜱ)}\ɴ**"

    message += f"<emoji id=5998881015320287132>💊</emoji> **\ɴ**ꜰɪʀꜱᴛ 5 ɴᴜᴍʙᴇʀꜱ:**\ɴ**"
    for i, num in enumerate(valid_numbers[:5], 1):
        message += f"<emoji id=6152142357727811958>🦋</emoji> **{ɪ}. `{ɴᴜᴍ}`\ɴ**"

    if len(valid_numbers) > 5:
        message += f"<emoji id=6307750079423845494>👑</emoji> **... ᴀɴᴅ {ʟᴇɴ(ᴠᴀʟɪᴅ_ɴᴜᴍʙᴇʀꜱ) - 5} ᴍᴏʀᴇ\ɴ**"

    message += f"<emoji id=5280904324724063665>😽</emoji> **\ɴᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴛᴀʀᴛ ᴀᴅᴅɪɴɢ ᴀᴄᴄᴏᴜɴᴛꜱ:**"

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("<emoji id=6309640268761011366>🌙</emoji> **▶️ ꜱᴛᴀʀᴛ ᴀᴅᴅɪɴɢ ᴀᴄᴄᴏᴜɴᴛꜱ**", callback_data="start_bulk_add"),
        InlineKeyboardButton("<emoji id=5999340396432333728>☺️</emoji> **✏️ ᴇᴅɪᴛ ɴᴜᴍʙᴇʀꜱ**", callback_data="edit_bulk_numbers")
    )
    markup.add(InlineKeyboardButton("<emoji id=6309666601205503867>💌</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_bulk"))

    sent_msg = bot.send_message(msg.chat.id, message, parse_mode="Markdown", reply_markup=markup)
    state["message_id"] = sent_msg.message_id
    user_last_message[user_id] = sent_msg.message_id

def start_bulk_processing(user_id):
    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]
    state["is_processing"] = True

    edit_or_resend(
        state["chat_id"],
        state["message_id"],
        f"<emoji id=5998977626314643141>🦋</emoji> **🚀 **ʙᴜʟᴋ ᴩʀᴏᴄᴇꜱꜱɪɴɢ ꜱᴛᴀʀᴛᴇᴅ**\ɴ\ɴ**"
        f"<emoji id=6309985824649780135>🌙</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ꜱᴛᴀᴛᴇ['ᴄᴏᴜɴᴛʀʏ']}\ɴ**"
        f"<emoji id=5998881015320287132>💊</emoji> **📱 ᴛᴏᴛᴀʟ: {ꜱᴛᴀᴛᴇ['ᴛᴏᴛᴀʟ_ɴᴜᴍʙᴇʀꜱ']} ɴᴜᴍʙᴇʀꜱ\ɴ**"
        f"<emoji id=6307605493644793241>📒</emoji> **⏳ ᴩʀᴏᴄᴇꜱꜱɪɴɢ ꜰɪʀꜱᴛ ɴᴜᴍʙᴇʀ...**",
        markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("<emoji id=6152142357727811958>🦋</emoji> **⏸️ ᴩᴀᴜꜱᴇ**", callback_data="pause_bulk"),
            InlineKeyboardButton("<emoji id=5998977626314643141>🦋</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_bulk")
        )
    )

    process_next_bulk_number(user_id)

def process_next_bulk_number(user_id):
    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]

    if not state.get("is_processing", True):
        return

    if state["current_index"] >= state["total_numbers"]:
        show_bulk_summary(user_id)
        return

    phone_number = state["phone_numbers"][state["current_index"]]
    state["current_phone"] = phone_number
    state["password_attempts"] = 0

    progress = state["current_index"] + 1
    total = state["total_numbers"]
    percentage = (progress / total) * 100

    edit_or_resend(
        state["chat_id"],
        state["message_id"],
        f"<emoji id=6307568836098922002>🌙</emoji> **🔄 **ᴩʀᴏᴄᴇꜱꜱɪɴɢ ɴᴜᴍʙᴇʀ {ᴩʀᴏɢʀᴇꜱꜱ}/{ᴛᴏᴛᴀʟ}**\ɴ\ɴ**"
        f"<emoji id=6224236403153179330>🎀</emoji> **📱 ᴩʜᴏɴᴇ: `{ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ}`\ɴ**"
        f"<emoji id=5354924568492383911>😈</emoji> **📊 ᴩʀᴏɢʀᴇꜱꜱ: {ᴩʀᴏɢʀᴇꜱꜱ}/{ᴛᴏᴛᴀʟ} ({ᴩᴇʀᴄᴇɴᴛᴀɢᴇ:.1ꜰ}%)\ɴ**"
        f"<emoji id=6310022800023229454>✡️</emoji> **✅ ꜱᴜᴄᴄᴇꜱꜱ: {ꜱᴛᴀᴛᴇ['ꜱᴜᴄᴄᴇꜱꜱ_ᴄᴏᴜɴᴛ']}\ɴ**"
        f"<emoji id=5899776109548934640>💲</emoji> **❌ ꜰᴀɪʟᴇᴅ: {ꜱᴛᴀᴛᴇ['ꜰᴀɪʟᴇᴅ_ᴄᴏᴜɴᴛ']}\ɴ\ɴ**"
        f"<emoji id=6307643744623531146>🦋</emoji> **⏳ ꜱᴇɴᴅɪɴɢ ᴏᴛᴩ...**",
        markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("<emoji id=5280678521113443426>😽</emoji> **⏸️ ᴩᴀᴜꜱᴇ**", callback_data="pause_bulk"),
            InlineKeyboardButton("<emoji id=4929195195225867512>💎</emoji> **⏭️ ꜱᴋɪᴩ**", callback_data="skip_bulk_number"),
            InlineKeyboardButton("<emoji id=4929195195225867512>💎</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_bulk")
        )
    )

    send_bulk_otp(user_id, phone_number)

def send_bulk_otp(user_id, phone_number):
    try:
        if not account_manager:
            bulk_number_failed(user_id, "<emoji id=6111418418424973677>✅</emoji> **ᴀᴄᴄᴏᴜɴᴛ ᴍᴏᴅᴜʟᴇ ɴᴏᴛ ʟᴏᴀᴅᴇᴅ**")
            return

        state = bulk_add_states[user_id]

        result = account_manager.bulk_send_code_sync(phone_number)

        if result.get("success"):
            state["current_client"] = result["client"]
            state["current_phone_code_hash"] = result["phone_code_hash"]
            state["current_manager"] = result["manager"]
            state["step"] = "waiting_bulk_otp"

            edit_or_resend(
                state["chat_id"],
                state["message_id"],
                f"<emoji id=6152444560216693216>🥰</emoji> **📱 ᴩʜᴏɴᴇ: `{ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ}`\ɴ\ɴ**"
                f"<emoji id=6298684666182371615>❤️</emoji> **✅ ᴏᴛᴩ ꜱᴇɴᴛ!\ɴ**"
                f"<emoji id=5999041732996504081>✨</emoji> **ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴩ ʀᴇᴄᴇɪᴠᴇᴅ ꜰᴏʀ ᴛʜɪꜱ ɴᴜᴍʙᴇʀ:\ɴ\ɴ**"
                f"<emoji id=5280721097124249567>😽</emoji> **_(ᴛʏᴩᴇ 'ꜱᴋɪᴩ' ᴛᴏ ꜱᴋɪᴩ ᴛʜɪꜱ ɴᴜᴍʙᴇʀ)_**",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=6224236403153179330>🎀</emoji> **⏭️ ꜱᴋɪᴩ ᴛʜɪꜱ ɴᴜᴍʙᴇʀ**", callback_data="skip_bulk_number"),
                    InlineKeyboardButton("<emoji id=6152142357727811958>🦋</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_bulk")
                )
            )
        else:
            error_msg = result.get("error", "<emoji id=6307569802466563145>🎶</emoji> **ᴜɴᴋɴᴏᴡɴ ᴇʀʀᴏʀ**")
            bulk_number_failed(user_id, f"<emoji id=5998977626314643141>🦋</emoji> **ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇɴᴅ ᴏᴛᴩ: {ᴇʀʀᴏʀ_ᴍꜱɢ}**")

    except Exception as e:
        logger.error(f"<emoji id=6309709550878463216>🌟</emoji> **ʙᴜʟᴋ ꜱᴇɴᴅ ᴏᴛᴩ ᴇʀʀᴏʀ: {ᴇ}**")
        bulk_number_failed(user_id, f"<emoji id=5041955142060999726>🌈</emoji> **ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")

def bulk_number_failed(user_id, reason):
    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]
    state["failed_count"] += 1
    state["failed_numbers"].append({
        "number": state.get("current_phone", "Unknown"),
        "reason": reason
    })

    if state.get("current_client") and account_manager:
        try:
            asyncio.run(account_manager.pyrogram_manager.safe_disconnect(state["current_client"]))
        except:
            pass

    state["current_index"] += 1
    state["password_attempts"] = 0
    process_next_bulk_number(user_id)

def bulk_number_success(user_id):
    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]
    state["success_count"] += 1

    if state.get("current_client") and account_manager:
        try:
            asyncio.run(account_manager.pyrogram_manager.safe_disconnect(state["current_client"]))
        except:
            pass

    state["current_index"] += 1
    state["password_attempts"] = 0
    process_next_bulk_number(user_id)

@bot.message_handler(func=lambda m: bulk_add_states.get(m.from_user.id, {}).get("step") == "waiting_bulk_otp")
def handle_bulk_otp_input(msg):
    user_id = msg.from_user.id

    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]
    if state.get("step") != "waiting_bulk_otp":
        return

    otp_code = msg.text.strip()

    if otp_code.lower() == 'skip':
        bulk_number_failed(user_id, "<emoji id=6309666601205503867>💌</emoji> **ꜱᴋɪᴩᴩᴇᴅ ʙʏ ᴀᴅᴍɪɴ**")
        return

    if not otp_code.isdigit() or len(otp_code) != 5:
        bot.send_message(
            msg.chat.id,
            "<emoji id=6307643744623531146>🦋</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴏᴛᴩ ꜰᴏʀᴍᴀᴛ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ 5-ᴅɪɢɪᴛ ᴏᴛᴩ ᴏʀ ᴛʏᴩᴇ 'ꜱᴋɪᴩ' ᴛᴏ ꜱᴋɪᴩ:**"
        )
        return

    try:
        result = account_manager.bulk_verify_otp_sync(
            state["current_client"],
            state["current_phone"],
            state["current_phone_code_hash"],
            otp_code,
            state["current_manager"]
        )

        if result.get("success"):
            save_bulk_account(user_id)

        elif result.get("status") == "password_required":
            state["step"] = "waiting_bulk_password"
            state["password_attempts"] = 0

            edit_or_resend(
                state["chat_id"],
                state["message_id"],
                f"<emoji id=6307569802466563145>🎶</emoji> **📱 ᴩʜᴏɴᴇ: `{ꜱᴛᴀᴛᴇ['ᴄᴜʀʀᴇɴᴛ_ᴩʜᴏɴᴇ']}`\ɴ\ɴ**"
                f"<emoji id=5354924568492383911>😈</emoji> **🔐 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ ʀᴇꞯᴜɪʀᴇᴅ!\ɴ**"
                f"<emoji id=5235985147265837746>🗒</emoji> **ᴇɴᴛᴇʀ ʏᴏᴜʀ 2-ꜱᴛᴇᴩ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴩᴀꜱꜱᴡᴏʀᴅ:\ɴ\ɴ**"
                f"<emoji id=6152444560216693216>🥰</emoji> **_(ᴛʏᴩᴇ 'ꜱᴋɪᴩ' ᴛᴏ ꜱᴋɪᴩ ᴛʜɪꜱ ɴᴜᴍʙᴇʀ)_**",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=5999041732996504081>✨</emoji> **⏭️ ꜱᴋɪᴩ ᴛʜɪꜱ ɴᴜᴍʙᴇʀ**", callback_data="skip_bulk_number"),
                    InlineKeyboardButton("<emoji id=5899776109548934640>💲</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_bulk")
                )
            )

        else:
            error_msg = result.get("error", "<emoji id=6307750079423845494>👑</emoji> **ᴏᴛᴩ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜰᴀɪʟᴇᴅ**")
            bulk_number_failed(user_id, f"<emoji id=6152444560216693216>🥰</emoji> **ᴏᴛᴩ ᴇʀʀᴏʀ: {ᴇʀʀᴏʀ_ᴍꜱɢ}**")

    except Exception as e:
        logger.error(f"<emoji id=4929369656797431200>🪐</emoji> **ʙᴜʟᴋ ᴏᴛᴩ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴇʀʀᴏʀ: {ᴇ}**")
        bulk_number_failed(user_id, f"<emoji id=6111778259374971023>🔥</emoji> **ᴏᴛᴩ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")

@bot.message_handler(func=lambda m: bulk_add_states.get(m.from_user.id, {}).get("step") == "waiting_bulk_password")
def handle_bulk_password_input(msg):
    user_id = msg.from_user.id

    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]
    if state.get("step") != "waiting_bulk_password":
        return

    password = msg.text.strip()

    if password.lower() == 'skip':
        bulk_number_failed(user_id, "<emoji id=5999340396432333728>☺️</emoji> **ꜱᴋɪᴩᴩᴇᴅ ʙʏ ᴀᴅᴍɪɴ**")
        return

    if not password:
        bot.send_message(
            msg.chat.id,
            "<emoji id=5280678521113443426>😽</emoji> **❌ ᴩᴀꜱꜱᴡᴏʀᴅ ᴄᴀɴɴᴏᴛ ʙᴇ ᴇᴍᴩᴛʏ. ᴇɴᴛᴇʀ 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ ᴏʀ ᴛʏᴩᴇ 'ꜱᴋɪᴩ' ᴛᴏ ꜱᴋɪᴩ:**"
        )
        return

    state["password_attempts"] = state.get("password_attempts", 0) + 1

    if state["password_attempts"] > 2:
        bulk_number_failed(user_id, "<emoji id=5041955142060999726>🌈</emoji> **ᴍᴀx ᴩᴀꜱꜱᴡᴏʀᴅ ᴀᴛᴛᴇᴍᴩᴛꜱ ᴇxᴄᴇᴇᴅᴇᴅ**")
        return

    try:
        result = account_manager.bulk_verify_password_sync(
            state["current_client"],
            password,
            state["current_manager"]
        )

        if result.get("success"):
            save_bulk_account(user_id, password)
        else:
            error_msg = result.get("error", "<emoji id=6298684666182371615>❤️</emoji> **ɪɴᴄᴏʀʀᴇᴄᴛ ᴩᴀꜱꜱᴡᴏʀᴅ**")

            if state["password_attempts"] >= 2:
                bulk_number_failed(user_id, f"<emoji id=5999210495146465994>💖</emoji> **ᴩᴀꜱꜱᴡᴏʀᴅ ᴇʀʀᴏʀ: {ᴇʀʀᴏʀ_ᴍꜱɢ}**")
            else:
                attempts_left = 2 - state["password_attempts"]
                bot.send_message(
                    msg.chat.id,
                    f"<emoji id=6309666601205503867>💌</emoji> **❌ ɪɴᴄᴏʀʀᴇᴄᴛ ᴩᴀꜱꜱᴡᴏʀᴅ. {ᴀᴛᴛᴇᴍᴩᴛꜱ_ʟᴇꜰᴛ} ᴀᴛᴛᴇᴍᴩᴛ(ꜱ) ʟᴇꜰᴛ.\ɴ**"
                    f"<emoji id=5352542184493031170>😈</emoji> **ᴇɴᴛᴇʀ ᴩᴀꜱꜱᴡᴏʀᴅ ᴀɢᴀɪɴ ᴏʀ ᴛʏᴩᴇ 'ꜱᴋɪᴩ' ᴛᴏ ꜱᴋɪᴩ:**"
                )

    except Exception as e:
        logger.error(f"<emoji id=5999340396432333728>☺️</emoji> **ʙᴜʟᴋ ᴩᴀꜱꜱᴡᴏʀᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴇʀʀᴏʀ: {ᴇ}**")
        bulk_number_failed(user_id, f"<emoji id=5041955142060999726>🌈</emoji> **ᴩᴀꜱꜱᴡᴏʀᴅ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")

def save_bulk_account(user_id, password=None):
    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]

    try:
        success, message = account_manager.bulk_save_account_sync(
            state["current_client"],
            state["current_phone"],
            state["country"],
            user_id,
            state["current_manager"],
            accounts_col,
            password
        )

        if success:
            progress = state["current_index"] + 1
            total = state["total_numbers"]

            edit_or_resend(
                state["chat_id"],
                state["message_id"],
                f"<emoji id=6310022800023229454>✡️</emoji> **✅ **ɴᴜᴍʙᴇʀ {ᴩʀᴏɢʀᴇꜱꜱ}/{ᴛᴏᴛᴀʟ} ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
                f"<emoji id=6307457716705040156>👍</emoji> **📱 ᴩʜᴏɴᴇ: `{ꜱᴛᴀᴛᴇ['ᴄᴜʀʀᴇɴᴛ_ᴩʜᴏɴᴇ']}`\ɴ**"
                f"<emoji id=6298684666182371615>❤️</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ꜱᴛᴀᴛᴇ['ᴄᴏᴜɴᴛʀʏ']}\ɴ**"
                f"<emoji id=6309666601205503867>💌</emoji> **🔐 2ꜰᴀ: {'✅ ᴇɴᴀʙʟᴇᴅ' ɪꜰ ᴩᴀꜱꜱᴡᴏʀᴅ ᴇʟꜱᴇ '❌ ᴅɪꜱᴀʙʟᴇᴅ'}\ɴ\ɴ**"
                f"<emoji id=4929483658114368660>💎</emoji> **📊 ᴩʀᴏɢʀᴇꜱꜱ: {ᴩʀᴏɢʀᴇꜱꜱ}/{ᴛᴏᴛᴀʟ}\ɴ**"
                f"<emoji id=5999340396432333728>☺️</emoji> **✅ ꜱᴜᴄᴄᴇꜱꜱ: {ꜱᴛᴀᴛᴇ['ꜱᴜᴄᴄᴇꜱꜱ_ᴄᴏᴜɴᴛ'] + 1}\ɴ**"
                f"<emoji id=5999041732996504081>✨</emoji> **❌ ꜰᴀɪʟᴇᴅ: {ꜱᴛᴀᴛᴇ['ꜰᴀɪʟᴇᴅ_ᴄᴏᴜɴᴛ']}\ɴ\ɴ**"
                f"<emoji id=6001589602085771497>✅</emoji> **⏳ ᴍᴏᴠɪɴɢ ᴛᴏ ɴᴇxᴛ ɴᴜᴍʙᴇʀ...**",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=6111418418424973677>✅</emoji> **⏸️ ᴩᴀᴜꜱᴇ**", callback_data="pause_bulk"),
                    InlineKeyboardButton("<emoji id=6152142357727811958>🦋</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_bulk")
                )
            )

            bulk_number_success(user_id)

        else:
            bulk_number_failed(user_id, f"<emoji id=5280721097124249567>😽</emoji> **ꜱᴀᴠᴇ ᴇʀʀᴏʀ: {ᴍᴇꜱꜱᴀɢᴇ}**")

    except Exception as e:
        logger.error(f"<emoji id=5281001756057175314>😽</emoji> **ʙᴜʟᴋ ꜱᴀᴠᴇ ᴀᴄᴄᴏᴜɴᴛ ᴇʀʀᴏʀ: {ᴇ}**")
        bulk_number_failed(user_id, f"<emoji id=5352870513267973607>✨</emoji> **ꜱᴀᴠᴇ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")

def show_bulk_summary(user_id):
    if user_id not in bulk_add_states:
        return

    state = bulk_add_states[user_id]

    summary = f"<emoji id=6111418418424973677>✅</emoji> **📊 **ʙᴜʟᴋ ᴩʀᴏᴄᴇꜱꜱɪɴɢ ᴄᴏᴍᴩʟᴇᴛᴇ!**\ɴ\ɴ**"
    summary += f"<emoji id=6309739370836399696>🌙</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ꜱᴛᴀᴛᴇ['ᴄᴏᴜɴᴛʀʏ']}\ɴ**"
    summary += f"<emoji id=5999270482954691955>🦋</emoji> **📱 ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀꜱ: {ꜱᴛᴀᴛᴇ['ᴛᴏᴛᴀʟ_ɴᴜᴍʙᴇʀꜱ']}\ɴ**"
    summary += f"<emoji id=6224236403153179330>🎀</emoji> **✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ: {ꜱᴛᴀᴛᴇ['ꜱᴜᴄᴄᴇꜱꜱ_ᴄᴏᴜɴᴛ']}\ɴ**"
    summary += f"<emoji id=6307447640711763730>💟</emoji> **❌ ꜰᴀɪʟᴇᴅ/ꜱᴋɪᴩᴩᴇᴅ: {ꜱᴛᴀᴛᴇ['ꜰᴀɪʟᴇᴅ_ᴄᴏᴜɴᴛ']}\ɴ\ɴ**"

    if state['failed_numbers']:
        summary += f"<emoji id=5998977626314643141>🦋</emoji> ****ꜰᴀɪʟᴇᴅ ɴᴜᴍʙᴇʀꜱ:**\ɴ**"
        for i, failed in enumerate(state['failed_numbers'][:10], 1):
            summary += f"<emoji id=6123040393769521180>☄️</emoji> **{ɪ}. {ꜰᴀɪʟᴇᴅ['ɴᴜᴍʙᴇʀ']} - {ꜰᴀɪʟᴇᴅ['ʀᴇᴀꜱᴏɴ']}\ɴ**"

        if len(state['failed_numbers']) > 10:
            summary += f"<emoji id=5280606902533783431>😽</emoji> **... ᴀɴᴅ {ʟᴇɴ(ꜱᴛᴀᴛᴇ['ꜰᴀɪʟᴇᴅ_ɴᴜᴍʙᴇʀꜱ']) - 10} ᴍᴏʀᴇ\ɴ**"

    summary += f"<emoji id=5280606902533783431>😽</emoji> **\ɴ⏰ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ᴀᴛ: {ᴅᴀᴛᴇᴛɪᴍᴇ.ᴜᴛᴄɴᴏᴡ().ꜱᴛʀꜰᴛɪᴍᴇ('%ʜ:%ᴍ:%ꜱ')}**"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("<emoji id=6154635934135490309>💗</emoji> **⚡ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ**", callback_data="admin_panel"))

    edit_or_resend(
        state["chat_id"],
        state["message_id"],
        summary,
        markup=markup
    )

    del bulk_add_states[user_id]

# ---------------------------------------------------------------------
# EXISTING FUNCTIONS
# ---------------------------------------------------------------------

def handle_login_country_selection(call):
    user_id = call.from_user.id

    if user_id not in login_states:
        bot.answer_callback_query(call.id, "<emoji id=6298684666182371615>❤️</emoji> **❌ ꜱᴇꜱꜱɪᴏɴ ᴇxᴩɪʀᴇᴅ**", show_alert=True)
        return

    country_name = call.data.replace("login_country_", "")

    login_states[user_id]["country"] = country_name

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("<emoji id=5041955142060999726>🌈</emoji> **➕ ꜱɪɴɢʟᴇ ᴀᴄᴄᴏᴜɴᴛ**", callback_data=f"<emoji id=6309985824649780135>🌙</emoji> **ꜱɪɴɢʟᴇ_ᴀᴄᴄᴏᴜɴᴛ_{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}**"),
        InlineKeyboardButton("<emoji id=5280721097124249567>😽</emoji> **📦 ʙᴜʟᴋ ᴀᴄᴄᴏᴜɴᴛꜱ**", callback_data=f"<emoji id=4929195195225867512>💎</emoji> **ʙᴜʟᴋ_ᴀᴄᴄᴏᴜɴᴛ_{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}**")
    )
    markup.add(InlineKeyboardButton("<emoji id=5280904324724063665>😽</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_login"))

    edit_or_resend(
        call.message.chat.id,
        call.message.message_id,
        f"<emoji id=6307605493644793241>📒</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}\ɴ\ɴ**"
        "<emoji id=5280904324724063665>😽</emoji> **📱 ꜱᴇʟᴇᴄᴛ ᴀᴄᴄᴏᴜɴᴛ ᴀᴅᴅɪɴɢ ᴍᴏᴅᴇ:**",
        markup=markup
    )

def handle_cancel_login(call):
    user_id = call.from_user.id

    if user_id in login_states:
        state = login_states[user_id]
        if "client" in state:
            try:
                if account_manager and account_manager.pyrogram_manager:
                    import asyncio
                    asyncio.run(account_manager.pyrogram_manager.safe_disconnect(state["client"]))
            except:
                pass
        login_states.pop(user_id, None)

    edit_or_resend(
        call.message.chat.id,
        call.message.message_id,
        "<emoji id=5352542184493031170>😈</emoji> **❌ ʟᴏɢɪɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.**",
        markup=None
    )
    show_admin_panel(call.message.chat.id)

def handle_logout_session(user_id, session_id, chat_id, callback_id):
    try:
        if not account_manager:
            bot.answer_callback_query(callback_id, "<emoji id=6123040393769521180>☄️</emoji> **❌ ᴀᴄᴄᴏᴜɴᴛ ᴍᴏᴅᴜʟᴇ ɴᴏᴛ ʟᴏᴀᴅᴇᴅ**", show_alert=True)
            return

        bot.answer_callback_query(callback_id, "<emoji id=6224236403153179330>🎀</emoji> **🔄 ʟᴏɢɢɪɴɢ ᴏᴜᴛ...**", show_alert=False)
        success, message = account_manager.logout_session_sync(
            session_id, user_id, otp_sessions_col, accounts_col, orders_col
        )

        if success:
            try:
                bot.delete_message(chat_id, callback_id.message.message_id)
            except:
                pass

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("<emoji id=5354924568492383911>😈</emoji> **🏠 ᴍᴀɪɴ ᴍᴇɴᴜ**", callback_data="back_to_menu"))

            sent_msg = bot.send_message(
                chat_id,
                "<emoji id=5280904324724063665>😽</emoji> **✅ **ʟᴏɢɢᴇᴅ ᴏᴜᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
                "<emoji id=6298684666182371615>❤️</emoji> **ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʟᴏɢɢᴇᴅ ᴏᴜᴛ ꜰʀᴏᴍ ᴛʜɪꜱ ꜱᴇꜱꜱɪᴏɴ.\ɴ**"
                "<emoji id=6152142357727811958>🦋</emoji> **ᴏʀᴅᴇʀ ᴍᴀʀᴋᴇᴅ ᴀꜱ ᴄᴏᴍᴩʟᴇᴛᴇᴅ.\ɴ\ɴ**"
                "<emoji id=5998881015320287132>💊</emoji> **ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜꜱɪɴɢ ᴏᴜʀ ꜱᴇʀᴠɪᴄᴇ!**",
                reply_markup=markup
            )
            user_last_message[user_id] = sent_msg.message_id
        else:
            bot.answer_callback_query(callback_id, f"<emoji id=6307568836098922002>🌙</emoji> **❌ {ᴍᴇꜱꜱᴀɢᴇ}**", show_alert=True)
    except Exception as e:
        logger.error(f"<emoji id=6001589602085771497>✅</emoji> **ʟᴏɢᴏᴜᴛ ʜᴀɴᴅʟᴇʀ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.answer_callback_query(callback_id, "<emoji id=6111418418424973677>✅</emoji> **❌ ᴇʀʀᴏʀ ʟᴏɢɢɪɴɢ ᴏᴜᴛ**", show_alert=True)

def get_latest_otp(user_id, session_id, chat_id, callback_id):
    try:
        session_data = otp_sessions_col.find_one({"session_id": session_id})
        if not session_data:
            bot.answer_callback_query(callback_id, "<emoji id=6154635934135490309>💗</emoji> **❌ ꜱᴇꜱꜱɪᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ**", show_alert=True)
            return

        # ALWAYS fetch fresh OTP, don't use cached
        bot.answer_callback_query(callback_id, "<emoji id=6298717844804733009>♾</emoji> **🔍 ꜱᴇᴀʀᴄʜɪɴɢ ꜰᴏʀ ʟᴀᴛᴇꜱᴛ ᴏᴛᴩ...**", show_alert=False)

        session_string = session_data.get("session_string")
        if not session_string:
            bot.answer_callback_query(callback_id, "<emoji id=6123040393769521180>☄️</emoji> **❌ ɴᴏ ꜱᴇꜱꜱɪᴏɴ ꜱᴛʀɪɴɢ ꜰᴏᴜɴᴅ**", show_alert=True)
            return

        # Always fetch new OTP
        otp_code = account_manager.get_latest_otp_sync(session_string)

        if not otp_code:
            bot.answer_callback_query(callback_id, "<emoji id=6307643744623531146>🦋</emoji> **❌ ɴᴏ ᴏᴛᴩ ʀᴇᴄᴇɪᴠᴇᴅ ʏᴇᴛ. ᴩʟᴇᴀꜱᴇ ᴡᴀɪᴛ...**", show_alert=True)
            return

        # Update database with the new OTP
        otp_sessions_col.update_one(
            {"session_id": session_id},
            {"<emoji id=5280904324724063665>😽</emoji> **$ꜱᴇᴛ**": {
                "has_otp": True,
                "last_otp": otp_code,
                "last_otp_time": datetime.utcnow(),
                "status": "otp_received"
            }}
        )

        try:
            from logs import log_otp_received_async
            order = orders_col.find_one({"session_id": session_id})
            if order:
                log_otp_received_async(
                    user_id=user_id,
                    phone=session_data.get('phone', 'N/A'),
                    otp_code=otp_code,
                    country=order.get('country', 'Unknown'),
                    price=order.get('price', 0)
                )
        except:
            pass

        account_id = session_data.get("account_id")
        account = None
        two_step_password = ""
        if account_id:
            try:
                account = accounts_col.find_one({"_id": ObjectId(account_id)})
                if account:
                    two_step_password = account.get("two_step_password", "")
            except:
                pass

        message = f"<emoji id=6154635934135490309>💗</emoji> **✅ **ʟᴀᴛᴇꜱᴛ ᴏᴛᴩ**\ɴ\ɴ**"
        message += f"<emoji id=6310044717241340733>🔄</emoji> **📱 ᴩʜᴏɴᴇ: `{ꜱᴇꜱꜱɪᴏɴ_ᴅᴀᴛᴀ.ɢᴇᴛ('ᴩʜᴏɴᴇ', 'ɴ/ᴀ')}`\ɴ**"
        message += f"<emoji id=6307568836098922002>🌙</emoji> **🔢 ᴏᴛᴩ ᴄᴏᴅᴇ: `{ᴏᴛᴩ_ᴄᴏᴅᴇ}`\ɴ**"
        if two_step_password:
            message += f"<emoji id=5040016479722931047>✨</emoji> **🔐 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ: `{ᴛᴡᴏ_ꜱᴛᴇᴩ_ᴩᴀꜱꜱᴡᴏʀᴅ}`\ɴ**"
        elif account and account.get("two_step_password"):
            message += f"<emoji id=5999270482954691955>🦋</emoji> **🔐 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ: `{ᴀᴄᴄᴏᴜɴᴛ.ɢᴇᴛ('ᴛᴡᴏ_ꜱᴛᴇᴩ_ᴩᴀꜱꜱᴡᴏʀᴅ')}`\ɴ**"
        message += f"<emoji id=6111778259374971023>🔥</emoji> **\ɴ⏰ ᴛɪᴍᴇ: {ᴅᴀᴛᴇᴛɪᴍᴇ.ᴜᴛᴄɴᴏᴡ().ꜱᴛʀꜰᴛɪᴍᴇ('%ʜ:%ᴍ:%ꜱ')}**"
        message += f"<emoji id=6307569802466563145>🎶</emoji> **\ɴ\ɴᴇɴᴛᴇʀ ᴛʜɪꜱ ᴄᴏᴅᴇ ɪɴ ᴛᴇʟᴇɢʀᴀᴍ x ᴀᴩᴩ.**"

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("<emoji id=5318828550940293906>🐱</emoji> **🔄 ɢᴇᴛ ᴏᴛᴩ ᴀɢᴀɪɴ**", callback_data=f"<emoji id=6307821174017496029>🔥</emoji> **ɢᴇᴛ_ᴏᴛᴩ_{ꜱᴇꜱꜱɪᴏɴ_ɪᴅ}**"),
            InlineKeyboardButton("<emoji id=6152142357727811958>🦋</emoji> **🚪 ʟᴏɢᴏᴜᴛ**", callback_data=f"<emoji id=6307821174017496029>🔥</emoji> **ʟᴏɢᴏᴜᴛ_ꜱᴇꜱꜱɪᴏɴ_{ꜱᴇꜱꜱɪᴏɴ_ɪᴅ}**")
        )

        try:
            bot.edit_message_text(
                message,
                chat_id,
                callback_id.message.message_id,
                parse_mode="Markdown",
                reply_markup=markup
            )
        except:
            sent_msg = bot.send_message(
                chat_id,
                message,
                parse_mode="Markdown",
                reply_markup=markup
            )
            user_last_message[user_id] = sent_msg.message_id

        bot.answer_callback_query(callback_id, "<emoji id=4929195195225867512>💎</emoji> **✅ ʟᴀᴛᴇꜱᴛ ᴏᴛᴩ ꜰᴇᴛᴄʜᴇᴅ!**", show_alert=False)
    except Exception as e:
        logger.error(f"<emoji id=6152142357727811958>🦋</emoji> **ɢᴇᴛ ᴏᴛᴩ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.answer_callback_query(callback_id, "<emoji id=5280678521113443426>😽</emoji> **❌ ᴇʀʀᴏʀ ɢᴇᴛᴛɪɴɢ ᴏᴛᴩ**", show_alert=True)

# ---------------------------------------------------------------------
# COUPON MANAGEMENT FUNCTIONS
# ---------------------------------------------------------------------

def show_coupon_management(chat_id, message_id=None):
    if not is_admin(chat_id):
        bot.send_message(chat_id, "<emoji id=5040016479722931047>✨</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    text = "<emoji id=5041955142060999726>🌈</emoji> **🎟 **ᴄᴏᴜᴩᴏɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**\ɴ\ɴᴄʜᴏᴏꜱᴇ ᴀɴ ᴏᴩᴛɪᴏɴ:**"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("<emoji id=5999340396432333728>☺️</emoji> **➕ ᴀᴅᴅ ᴄᴏᴜᴩᴏɴ**", callback_data="admin_create_coupon"),
        InlineKeyboardButton("<emoji id=6309666601205503867>💌</emoji> **❌ ʀᴇᴍᴏᴠᴇ ᴄᴏᴜᴩᴏɴ**", callback_data="admin_remove_coupon")
    )
    markup.add(
        InlineKeyboardButton("<emoji id=5354924568492383911>😈</emoji> **📊 ᴄᴏᴜᴩᴏɴ ꜱᴛᴀᴛᴜꜱ**", callback_data="admin_coupon_status"),
        InlineKeyboardButton("<emoji id=6307553838073124532>✨</emoji> **🔙 ʙᴀᴄᴋ ᴛᴏ ᴀᴅᴍɪɴ**", callback_data="admin_panel")
    )

    if message_id:
        edit_or_resend(
            chat_id,
            message_id,
            text,
            markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

# ---------------------------------------------------------------------
# COUPON MESSAGE HANDLERS
# ---------------------------------------------------------------------

@bot.message_handler(func=lambda m: user_stage.get(m.from_user.id) == "waiting_coupon")
def handle_coupon_input(msg):
    user_id = msg.from_user.id

    if user_stage.get(user_id) != "waiting_coupon":
        return

    coupon_code = msg.text.strip().upper()
    user_stage.pop(user_id, None)

    success, result = claim_coupon(coupon_code, user_id)

    if success:
        amount = result
        new_balance = get_balance(user_id)
        text = f"<emoji id=6001132493011425597>💖</emoji> **✅ **ᴄᴏᴜᴩᴏɴ ʀᴇᴅᴇᴇᴍᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
        text += f"<emoji id=6154635934135490309>💗</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ: `{ᴄᴏᴜᴩᴏɴ_ᴄᴏᴅᴇ}`\ɴ**"
        text += f"<emoji id=4927247234283603387>🩷</emoji> **💰 ᴀᴍᴏᴜɴᴛ ᴀᴅᴅᴇᴅ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
        text += f"<emoji id=6307750079423845494>👑</emoji> **💳 ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɴᴇᴡ_ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"
        text += f"<emoji id=5280904324724063665>😽</emoji> **ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜꜱɪɴɢ ᴏᴜʀ ꜱᴇʀᴠɪᴄᴇ! 🎉**"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("<emoji id=5285100774060227768>😽</emoji> **🏠 ᴍᴀɪɴ ᴍᴇɴᴜ**", callback_data="back_to_menu"))

        sent_msg = bot.send_message(
            msg.chat.id,
            text,
            parse_mode="Markdown",
            reply_markup=markup
        )
        user_last_message[user_id] = sent_msg.message_id
    else:
        error_msg = result
        if error_msg == "<emoji id=5280606902533783431>😽</emoji> **ᴄᴏᴜᴩᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ**":
            response = "<emoji id=6224236403153179330>🎀</emoji> **❌ **ɪɴᴠᴀʟɪᴅ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ**\ɴ\ɴ**"
            response += "<emoji id=5352542184493031170>😈</emoji> **ᴛʜᴇ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴅᴏᴇꜱ ɴᴏᴛ ᴇxɪꜱᴛ.\ɴ**"
            response += "<emoji id=6111778259374971023>🔥</emoji> **ᴩʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴄᴏᴅᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.**"
        elif error_msg == "<emoji id=6307568836098922002>🌙</emoji> **ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ**":
            response = "<emoji id=5281001756057175314>😽</emoji> **⚠️ **ᴄᴏᴜᴩᴏɴ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ**\ɴ\ɴ**"
            response += "<emoji id=6123125485661591081>🩷</emoji> **ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ᴛʜɪꜱ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ.\ɴ**"
            response += "<emoji id=6001589602085771497>✅</emoji> **ᴇᴀᴄʜ ᴄᴏᴜᴩᴏɴ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴄʟᴀɪᴍᴇᴅ ᴏɴᴄᴇ ᴩᴇʀ ᴜꜱᴇʀ.**"
        elif error_msg == "<emoji id=6307750079423845494>👑</emoji> **ꜰᴜʟʟʏ ᴄʟᴀɪᴍᴇᴅ**":
            response = "<emoji id=4929195195225867512>💎</emoji> **🚫 **ᴄᴏᴜᴩᴏɴ ꜰᴜʟʟʏ ᴄʟᴀɪᴍᴇᴅ**\ɴ\ɴ**"
            response += "<emoji id=5999210495146465994>💖</emoji> **ᴛʜɪꜱ ᴄᴏᴜᴩᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴄʟᴀɪᴍᴇᴅ ʙʏ ᴀʟʟ ᴇʟɪɢɪʙʟᴇ ᴜꜱᴇʀꜱ.\ɴ**"
            response += "<emoji id=6111778259374971023>🔥</emoji> **ɴᴏ ᴍᴏʀᴇ ᴄʟᴀɪᴍꜱ ᴀʀᴇ ᴀᴠᴀɪʟᴀʙʟᴇ.**"
        elif error_msg in ["removed", "expired"]:
            response = f"<emoji id=6298717844804733009>♾</emoji> **🚫 **ᴄᴏᴜᴩᴏɴ {ᴇʀʀᴏʀ_ᴍꜱɢ.ᴄᴀᴩɪᴛᴀʟɪᴢᴇ()}**\ɴ\ɴ**"
            response += "<emoji id=6310044717241340733>🔄</emoji> **ᴛʜɪꜱ ᴄᴏᴜᴩᴏɴ ɪꜱ ɴᴏ ʟᴏɴɢᴇʀ ᴠᴀʟɪᴅ ꜰᴏʀ ʀᴇᴅᴇᴍᴩᴛɪᴏɴ.\ɴ**"
            response += "<emoji id=6111778259374971023>🔥</emoji> **ɪᴛ ᴍᴀʏ ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ᴏʀ ᴇxᴩɪʀᴇᴅ.**"
        else:
            response = f"<emoji id=5999210495146465994>💖</emoji> **❌ **ᴇʀʀᴏʀ:** {ᴇʀʀᴏʀ_ᴍꜱɢ}**"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("<emoji id=6309640268761011366>🌙</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="back_to_menu"))

        sent_msg = bot.send_message(
            msg.chat.id,
            response,
            parse_mode="Markdown",
            reply_markup=markup
        )
        user_last_message[user_id] = sent_msg.message_id

@bot.message_handler(func=lambda m: coupon_state.get(m.from_user.id, {}).get("step") == "ask_code")
def handle_coupon_code_input(msg):
    user_id = msg.from_user.id

    if user_id not in coupon_state or coupon_state[user_id]["step"] != "ask_code":
        return

    if not is_admin(user_id):
        bot.send_message(msg.chat.id, "<emoji id=5999210495146465994>💖</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        coupon_state.pop(user_id, None)
        return

    code = msg.text.strip().upper()
    if not code:
        bot.send_message(msg.chat.id, "<emoji id=5999340396432333728>☺️</emoji> **❌ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ ᴄᴀɴɴᴏᴛ ʙᴇ ᴇᴍᴩᴛʏ. ᴇɴᴛᴇʀ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ:**")
        return

    existing = get_coupon(code)
    if existing:
        bot.send_message(
            msg.chat.id,
            f"<emoji id=6154635934135490309>💗</emoji> **❌ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ `{ᴄᴏᴅᴇ}` ᴀʟʀᴇᴀᴅʏ ᴇxɪꜱᴛꜱ.\ɴ\ɴᴇɴᴛᴇʀ ᴀ ᴅɪꜰꜰᴇʀᴇɴᴛ ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ:**"
        )
        return

    coupon_state[user_id] = {
        "step": "ask_amount",
        "code": code
    }

    bot.send_message(
        msg.chat.id,
        f"<emoji id=5280721097124249567>😽</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ: `{ᴄᴏᴅᴇ}`\ɴ\ɴ**"
        f"<emoji id=6111742817304841054>✅</emoji> **💰 ᴇɴᴛᴇʀ ᴄᴏᴜᴩᴏɴ ᴀᴍᴏᴜɴᴛ (ᴍɪɴɪᴍᴜᴍ ₹1):**"
    )

@bot.message_handler(func=lambda m: coupon_state.get(m.from_user.id, {}).get("step") == "ask_amount")
def handle_coupon_amount_input(msg):
    user_id = msg.from_user.id

    if user_id not in coupon_state or coupon_state[user_id]["step"] != "ask_amount":
        return

    if not is_admin(user_id):
        bot.send_message(msg.chat.id, "<emoji id=4926993814033269936>🖕</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        coupon_state.pop(user_id, None)
        return

    try:
        amount = float(msg.text.strip())
        if amount < 1:
            bot.send_message(msg.chat.id, "<emoji id=5998881015320287132>💊</emoji> **❌ ᴀᴍᴏᴜɴᴛ ᴍᴜꜱᴛ ʙᴇ ᴀᴛ ʟᴇᴀꜱᴛ ₹1. ᴇɴᴛᴇʀ ᴀᴍᴏᴜɴᴛ:**")
            return

        coupon_state[user_id] = {
            "step": "ask_max_users",
            "code": coupon_state[user_id]["code"],
            "amount": amount
        }

        bot.send_message(
            msg.chat.id,
            f"<emoji id=5999210495146465994>💖</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ: `{ᴄᴏᴜᴩᴏɴ_ꜱᴛᴀᴛᴇ[ᴜꜱᴇʀ_ɪᴅ]['ᴄᴏᴅᴇ']}`\ɴ**"
            f"<emoji id=6307457716705040156>👍</emoji> **💰 ᴀᴍᴏᴜɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ\ɴ**"
            f"<emoji id=5998977626314643141>🦋</emoji> **👥 ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ ᴏꜰ ᴜꜱᴇʀꜱ ᴡʜᴏ ᴄᴀɴ ᴄʟᴀɪᴍ ᴛʜɪꜱ ᴄᴏᴜᴩᴏɴ (ᴍɪɴɪᴍᴜᴍ 1):**"
        )
    except ValueError:
        bot.send_message(msg.chat.id, "<emoji id=5280678521113443426>😽</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ. ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀꜱ ᴏɴʟʏ (ᴇ.ɢ., 100):**")

@bot.message_handler(func=lambda m: coupon_state.get(m.from_user.id, {}).get("step") == "ask_max_users")
def handle_coupon_max_users_input(msg):
    user_id = msg.from_user.id

    if user_id not in coupon_state or coupon_state[user_id]["step"] != "ask_max_users":
        return

    if not is_admin(user_id):
        bot.send_message(msg.chat.id, "<emoji id=5999151980512024620>🥰</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        coupon_state.pop(user_id, None)
        return

    try:
        max_users = int(msg.text.strip())
        if max_users < 1:
            bot.send_message(msg.chat.id, "<emoji id=6310044717241340733>🔄</emoji> **❌ ᴍᴜꜱᴛ ʙᴇ ᴀᴛ ʟᴇᴀꜱᴛ 1 ᴜꜱᴇʀ. ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ:**")
            return

        code = coupon_state[user_id]["code"]
        amount = coupon_state[user_id]["amount"]

        success, message = create_coupon(code, amount, max_users, user_id)

        if success:
            text = f"<emoji id=6298717844804733009>♾</emoji> **✅ **ᴄᴏᴜᴩᴏɴ ᴄʀᴇᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
            text += f"<emoji id=6111418418424973677>✅</emoji> **🎟 ᴄᴏᴅᴇ: `{ᴄᴏᴅᴇ}`\ɴ**"
            text += f"<emoji id=6309739370836399696>🌙</emoji> **💰 ᴀᴍᴏᴜɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
            text += f"<emoji id=5999270482954691955>🦋</emoji> **👥 ᴍᴀx ᴜꜱᴇʀꜱ: {ᴍᴀx_ᴜꜱᴇʀꜱ}\ɴ\ɴ**"
            text += f"<emoji id=5280606902533783431>😽</emoji> **ᴄᴏᴜᴩᴏɴ ɪꜱ ɴᴏᴡ ᴀᴄᴛɪᴠᴇ ᴀɴᴅ ʀᴇᴀᴅʏ ꜰᴏʀ ᴜꜱᴇʀꜱ ᴛᴏ ʀᴇᴅᴇᴇᴍ.**"

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("<emoji id=5395580801930771895>🤍</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**", callback_data="admin_coupon_menu"))

            bot.send_message(
                msg.chat.id,
                text,
                parse_mode="Markdown",
                reply_markup=markup
            )
        else:
            bot.send_message(
                msg.chat.id,
                f"<emoji id=6309709550878463216>🌟</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴄᴏᴜᴩᴏɴ: {ᴍᴇꜱꜱᴀɢᴇ}\ɴ\ɴ**"
                f"<emoji id=5280606902533783431>😽</emoji> **ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴩᴩᴏʀᴛ.**"
            )

        coupon_state.pop(user_id, None)
    except ValueError:
        bot.send_message(msg.chat.id, "<emoji id=6309985824649780135>🌙</emoji> **❌ ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ. ᴇɴᴛᴇʀ ᴡʜᴏʟᴇ ɴᴜᴍʙᴇʀꜱ ᴏɴʟʏ (ᴇ.ɢ., 100):**")

@bot.message_handler(func=lambda m: coupon_state.get(m.from_user.id, {}).get("step") == "ask_remove_code")
def handle_coupon_remove_input(msg):
    user_id = msg.from_user.id

    if user_id not in coupon_state or coupon_state[user_id]["step"] != "ask_remove_code":
        return

    if not is_admin(user_id):
        bot.send_message(msg.chat.id, "<emoji id=6307457716705040156>👍</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        coupon_state.pop(user_id, None)
        return

    code = msg.text.strip().upper()

    success, message = remove_coupon(code, user_id)

    if success:
        text = f"<emoji id=6111742817304841054>✅</emoji> **✅ **ᴄᴏᴜᴩᴏɴ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
        text += f"<emoji id=5395580801930771895>🤍</emoji> **🎟 ᴄᴏᴅᴇ: `{ᴄᴏᴅᴇ}`\ɴ**"
        text += f"<emoji id=4929195195225867512>💎</emoji> **🚫 ꜱᴛᴀᴛᴜꜱ: ʀᴇᴍᴏᴠᴇᴅ\ɴ\ɴ**"
        text += f"<emoji id=6309985824649780135>🌙</emoji> **ᴛʜɪꜱ ᴄᴏᴜᴩᴏɴ ᴄᴀɴ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ᴄʟᴀɪᴍᴇᴅ ʙʏ ᴜꜱᴇʀꜱ.**"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("<emoji id=5280606902533783431>😽</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**", callback_data="admin_coupon_menu"))

        bot.send_message(
            msg.chat.id,
            text,
            parse_mode="Markdown",
            reply_markup=markup
        )
    else:
        if message == "<emoji id=6309666601205503867>💌</emoji> **ᴄᴏᴜᴩᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ**":
            response = f"<emoji id=6309640268761011366>🌙</emoji> **❌ **ᴄᴏᴜᴩᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ**\ɴ\ɴ**"
            response += f"<emoji id=6307643744623531146>🦋</emoji> **ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ `{ᴄᴏᴅᴇ}` ᴅᴏᴇꜱ ɴᴏᴛ ᴇxɪꜱᴛ.\ɴ**"
            response += f"<emoji id=5235985147265837746>🗒</emoji> **ᴩʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴄᴏᴅᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.**"
        else:
            response = f"<emoji id=6310044717241340733>🔄</emoji> **❌ **ᴇʀʀᴏʀ:** {ᴍᴇꜱꜱᴀɢᴇ}**"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("<emoji id=6123125485661591081>🩷</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**", callback_data="admin_coupon_menu"))

        bot.send_message(
            msg.chat.id,
            response,
            parse_mode="Markdown",
            reply_markup=markup
        )

    coupon_state.pop(user_id, None)

@bot.message_handler(func=lambda m: coupon_state.get(m.from_user.id, {}).get("step") == "ask_status_code")
def handle_coupon_status_input(msg):
    user_id = msg.from_user.id

    if user_id not in coupon_state or coupon_state[user_id]["step"] != "ask_status_code":
        return

    if not is_admin(user_id):
        bot.send_message(msg.chat.id, "<emoji id=5354924568492383911>😈</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        coupon_state.pop(user_id, None)
        return

    code = msg.text.strip().upper()

    status = get_coupon_status(code)

    if not status:
        text = f"<emoji id=5352870513267973607>✨</emoji> **❌ **ᴄᴏᴜᴩᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ**\ɴ\ɴ**"
        text += f"<emoji id=5352870513267973607>✨</emoji> **ᴄᴏᴜᴩᴏɴ ᴄᴏᴅᴇ `{ᴄᴏᴅᴇ}` ᴅᴏᴇꜱ ɴᴏᴛ ᴇxɪꜱᴛ.\ɴ**"
        text += f"<emoji id=5041955142060999726>🌈</emoji> **ᴩʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴄᴏᴅᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.**"
    else:
        status_text = status["status"].capitalize()
        if status["status"] == "active":
            status_text = "<emoji id=6224236403153179330>🎀</emoji> **🟢 ᴀᴄᴛɪᴠᴇ**"
        elif status["status"] == "expired":
            status_text = "<emoji id=6309709550878463216>🌟</emoji> **🔴 ᴇxᴩɪʀᴇᴅ**"
        elif status["status"] == "removed":
            status_text = "<emoji id=6298684666182371615>❤️</emoji> **⚫ ʀᴇᴍᴏᴠᴇᴅ**"

        text = f"<emoji id=6154635934135490309>💗</emoji> **📊 **ᴄᴏᴜᴩᴏɴ ᴅᴇᴛᴀɪʟꜱ**\ɴ\ɴ**"
        text += f"<emoji id=6307457716705040156>👍</emoji> **🎟 ᴄᴏᴅᴇ: `{ꜱᴛᴀᴛᴜꜱ['ᴄᴏᴅᴇ']}`\ɴ**"
        text += f"<emoji id=6310044717241340733>🔄</emoji> **💰 ᴀᴍᴏᴜɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ꜱᴛᴀᴛᴜꜱ['ᴀᴍᴏᴜɴᴛ'])}\ɴ**"
        text += f"<emoji id=6111742817304841054>✅</emoji> **👥 ᴍᴀx ᴜꜱᴇʀꜱ: {ꜱᴛᴀᴛᴜꜱ['ᴍᴀx_ᴜꜱᴇʀꜱ']}\ɴ**"
        text += f"<emoji id=6307457716705040156>👍</emoji> **✅ ᴄʟᴀɪᴍᴇᴅ: {ꜱᴛᴀᴛᴜꜱ['ᴄʟᴀɪᴍᴇᴅ']}\ɴ**"
        text += f"<emoji id=5395580801930771895>🤍</emoji> **🔄 ʀᴇᴍᴀɪɴɪɴɢ: {ꜱᴛᴀᴛᴜꜱ['ʀᴇᴍᴀɪɴɪɴɢ']}\ɴ**"
        text += f"<emoji id=5235985147265837746>🗒</emoji> **📊 ꜱᴛᴀᴛᴜꜱ: {ꜱᴛᴀᴛᴜꜱ_ᴛᴇxᴛ}\ɴ**"
        text += f"<emoji id=5395580801930771895>🤍</emoji> **📅 ᴄʀᴇᴀᴛᴇᴅ: {ꜱᴛᴀᴛᴜꜱ['ᴄʀᴇᴀᴛᴇᴅ_ᴀᴛ'].ꜱᴛʀꜰᴛɪᴍᴇ('%ʏ-%ᴍ-%ᴅ %ʜ:%ᴍ') ɪꜰ ꜱᴛᴀᴛᴜꜱ['ᴄʀᴇᴀᴛᴇᴅ_ᴀᴛ'] ᴇʟꜱᴇ 'ɴ/ᴀ'}\ɴ**"

        if status['claimed'] > 0:
            text += f"<emoji id=5280678521113443426>😽</emoji> **\ɴ👤 ʀᴇᴄᴇɴᴛ ᴜꜱᴇʀꜱ (ꜰɪʀꜱᴛ 10):\ɴ**"
            for i, uid in enumerate(status['claimed_users'][:10], 1):
                text += f"<emoji id=4929369656797431200>🪐</emoji> **{ɪ}. ᴜꜱᴇʀ ɪᴅ: {ᴜɪᴅ}\ɴ**"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("<emoji id=5280678521113443426>😽</emoji> **🎟 ᴄᴏᴜᴩᴏɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**", callback_data="admin_coupon_menu"))

    bot.send_message(
        msg.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=markup
    )

    coupon_state.pop(user_id, None)

# ---------------------------------------------------------------------
# RECHARGE METHODS FUNCTIONS - UPDATED WITH TOTAL AND TODAY RECHARGE
# ---------------------------------------------------------------------

def show_recharge_methods(chat_id, message_id, user_id):
    # Calculate total recharge and today's recharge for this user
    total_recharge = 0
    today_recharge = 0
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # Get all approved recharges for this user
    user_recharges = recharges_col.find({
        "user_id": user_id,
        "status": "approved"
    })

    for recharge in user_recharges:
        amount = float(recharge.get("amount", 0))
        total_recharge += amount

        # Check if recharge was done today
        recharge_date = recharge.get("created_at") or recharge.get("submitted_at")
        if recharge_date and recharge_date >= today_start:
            today_recharge += amount

    text = f"<emoji id=6307750079423845494>👑</emoji> **💳 **ʀᴇᴄʜᴀʀɢᴇ**\ɴ\ɴ**"
    text += f"<emoji id=6152142357727811958>🦋</emoji> **💰 **ᴛᴏᴛᴀʟ ʀᴇᴄʜᴀʀɢᴇ:** {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴛᴏᴛᴀʟ_ʀᴇᴄʜᴀʀɢᴇ)}\ɴ**"
    text += f"<emoji id=5281001756057175314>😽</emoji> **📅 **ᴛᴏᴅᴀʏ'ꜱ ʀᴇᴄʜᴀʀɢᴇ:** {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴛᴏᴅᴀʏ_ʀᴇᴄʜᴀʀɢᴇ)}\ɴ\ɴ**"
    text += f"<emoji id=5352870513267973607>✨</emoji> **⬇️ **ꜱᴇʟᴇᴄᴛ ᴩᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ:****"

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("<emoji id=6309666601205503867>💌</emoji> **💳 ᴜᴩɪ ᴩᴀʏᴍᴇɴᴛ**", callback_data="recharge_upi", style="success")
    )
    markup.add(InlineKeyboardButton("<emoji id=6309666601205503867>💌</emoji> **🔙 ʙᴀᴄᴋ**", callback_data="back_to_menu", style="primary"))

    edit_or_resend(
        chat_id,
        message_id,
        text,
        markup=markup,
        parse_mode="Markdown"
    )

# ---------------------------------------------------------------------
# PROCESS RECHARGE AMOUNT FUNCTION - FIXED DATABASE ISSUE
# ---------------------------------------------------------------------

def process_recharge_amount(msg):
    try:
        amount = float(msg.text)
        if amount < 1:
            bot.send_message(msg.chat.id, "<emoji id=6287579968109024771>✅</emoji> **❌ ᴍɪɴɪᴍᴜᴍ ʀᴇᴄʜᴀʀɢᴇ ɪꜱ ₹1. ᴇɴᴛᴇʀ ᴀᴍᴏᴜɴᴛ ᴀɢᴀɪɴ:**")
            bot.register_next_step_handler(msg, process_recharge_amount)
            return

        user_id = msg.from_user.id

        caption = f"""<blockquote>💳 <b>UPI Payment Details</b> 

💰 Amount: {format_currency(amount)}
📱 UPI ID: {UPI_ID}

📋 Instructions:
1. Scan QR code OR send {format_currency(amount)} to above UPI
2. After payment, click **Deposited ✅** button
3. Follow the steps to submit proof

</blockquote>"""

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("<emoji id=4926993814033269936>🖕</emoji> **✅ ɪ'ᴠᴇ ᴩᴀɪᴅ — ᴄᴏɴꜰɪʀᴍ**", callback_data="upi_deposited", style="success"))

        upi_payment_states[user_id] = {
            "amount": amount,
            "step": "qr_shown"
        }

        bot.send_photo(
            msg.chat.id,
            QR_IMAGE_URL,
            caption=caption,
            parse_mode="HTML",
            reply_markup=markup
        )
    except ValueError:
        bot.send_message(msg.chat.id, "<emoji id=6307605493644793241>📒</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ. ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀꜱ ᴏɴʟʏ:**")
        bot.register_next_step_handler(msg, process_recharge_amount)

# FIXED UTR HANDLER - Now properly checks and stores in database
@bot.message_handler(func=lambda m: upi_payment_states.get(m.from_user.id, {}).get("step") == "waiting_utr")
def handle_utr_input(msg):
    user_id = msg.from_user.id

    if user_id not in upi_payment_states or upi_payment_states[user_id]["step"] != "waiting_utr":
        return

    utr = msg.text.strip()

    if not utr.isdigit() or len(utr) != 12:
        bot.send_message(msg.chat.id, "<emoji id=6307569802466563145>🎶</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜᴛʀ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ 12-ᴅɪɢɪᴛ ᴜᴛʀ ɴᴜᴍʙᴇʀ:**")
        return

    # Store UTR and move to screenshot step
    upi_payment_states[user_id]["utr"] = utr
    upi_payment_states[user_id]["step"] = "waiting_screenshot"

    bot.send_message(
        msg.chat.id,
        "<emoji id=5235985147265837746>🗒</emoji> **✅ ᴜᴛʀ ʀᴇᴄᴇɪᴠᴇᴅ!\ɴ\ɴ**"
        "<emoji id=5999151980512024620>🥰</emoji> **📸 ꜱᴛᴇᴩ 2: ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ\ɴ\ɴ**"
        "<emoji id=6152444560216693216>🥰</emoji> **ɴᴏᴡ ᴩʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛʜᴇ ᴩᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ꜰʀᴏᴍ ʏᴏᴜʀ ʙᴀɴᴋ ᴀᴩᴩ:\ɴ**"
        "<emoji id=5899776109548934640>💲</emoji> **_(ᴍᴀᴋᴇ ꜱᴜʀᴇ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ꜱʜᴏᴡꜱ ᴀᴍᴏᴜɴᴛ, ᴅᴀᴛᴇ, ᴀɴᴅ ᴜᴛʀ)_**"
    )

# FIXED SCREENSHOT HANDLER - Now properly saves to database
@bot.message_handler(content_types=['photo'], func=lambda m: upi_payment_states.get(m.from_user.id, {}).get("step") == "waiting_screenshot")
def handle_screenshot_input(msg):
    user_id = msg.from_user.id

    if user_id not in upi_payment_states or upi_payment_states[user_id]["step"] != "waiting_screenshot":
        return

    try:
        screenshot_file_id = msg.photo[-1].file_id

        amount = upi_payment_states[user_id]["amount"]
        utr = upi_payment_states[user_id].get("utr", "")

        # Generate unique request ID
        req_id = f"<emoji id=6123040393769521180>☄️</emoji> **ʀ{ɪɴᴛ(ᴛɪᴍᴇ.ᴛɪᴍᴇ())}{ᴜꜱᴇʀ_ɪᴅ}**"

        # Save to database with proper fields
        recharge_data = {
            "user_id": user_id,
            "amount": amount,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "method": "upi",
            "utr": utr,
            "screenshot": screenshot_file_id,
            "submitted_at": datetime.utcnow(),
            "req_id": req_id
        }

        recharge_id = recharges_col.insert_one(recharge_data).inserted_id

        # Update with req_id
        recharges_col.update_one(
            {"_id": ObjectId(recharge_id)},
            {"<emoji id=5040016479722931047>✨</emoji> **$ꜱᴇᴛ**": {"req_id": req_id}}
        )

        # Get all admins to send notification
        all_admins = get_all_admins()

        admin_caption = f"""📋 **UPI Payment Request** 

👤 User: {user_id}
💰 Amount: {format_currency(amount)}
🔢 UTR: {utr}
📅 Submitted: {datetime.utcnow().strftime('<emoji id=6111418418424973677>✅</emoji> **%ʏ-%ᴍ-%ᴅ %ʜ:%ᴍ:%ꜱ**')}
🆔 Request ID: {req_id}

✅ Both UTR and Screenshot received."""

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("<emoji id=5040016479722931047>✨</emoji> **✅ ᴀᴩᴩʀᴏᴠᴇ**", callback_data=f"<emoji id=5352542184493031170>😈</emoji> **ᴀᴩᴩʀᴏᴠᴇ_ʀᴇᴄʜ|{ʀᴇꞯ_ɪᴅ}**", style="success"),
            InlineKeyboardButton("<emoji id=6309739370836399696>🌙</emoji> **❌ ʀᴇᴊᴇᴄᴛ**", callback_data=f"<emoji id=6307568836098922002>🌙</emoji> **ᴄᴀɴᴄᴇʟ_ʀᴇᴄʜ|{ʀᴇꞯ_ɪᴅ}**", style="danger")
        )

        # Send to all admins
        for admin in all_admins:
            admin_user_id = admin["user_id"]
            try:
                bot.send_photo(
                    admin_user_id,
                    screenshot_file_id,
                    caption=admin_caption,
                    parse_mode="HTML",
                    reply_markup=markup
                )
            except Exception as e:
                logger.error(f"<emoji id=6307605493644793241>📒</emoji> **ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇɴᴅ ʀᴇᴄʜᴀʀɢᴇ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ ᴛᴏ ᴀᴅᴍɪɴ {ᴀᴅᴍɪɴ_ᴜꜱᴇʀ_ɪᴅ}: {ᴇ}**")

        bot.send_message(
            msg.chat.id,
            f"<emoji id=6111742817304841054>✅</emoji> **✅ **ᴩᴀʏᴍᴇɴᴛ ᴩʀᴏᴏꜰ ꜱᴜʙᴍɪᴛᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
            f"<emoji id=6307568836098922002>🌙</emoji> **📋 **ᴅᴇᴛᴀɪʟꜱ:**\ɴ**"
            f"<emoji id=4929369656797431200>🪐</emoji> **💰 ᴀᴍᴏᴜɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
            f"<emoji id=5285100774060227768>😽</emoji> **🔢 ᴜᴛʀ: {ᴜᴛʀ}\ɴ**"
            f"<emoji id=5281001756057175314>😽</emoji> **📸 ꜱᴄʀᴇᴇɴꜱʜᴏᴛ: ✅ ʀᴇᴄᴇɪᴠᴇᴅ\ɴ\ɴ**"
            f"<emoji id=5998977626314643141>🦋</emoji> **⏳ **ꜱᴛᴀᴛᴜꜱ:** ᴀᴅᴍɪɴ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴩᴇɴᴅɪɴɢ\ɴ**"
            f"<emoji id=5235985147265837746>🗒</emoji> **🆔 ʀᴇꞯᴜᴇꜱᴛ ɪᴅ: `{ʀᴇꞯ_ɪᴅ}`\ɴ\ɴ**"
            f"<emoji id=5352870513267973607>✨</emoji> **ᴀᴅᴍɪɴ ᴡɪʟʟ ʀᴇᴠɪᴇᴡ ᴀɴᴅ ᴀᴩᴩʀᴏᴠᴇ ꜱᴏᴏɴ. ᴛʜᴀɴᴋ ʏᴏᴜ! 🎉**"
        )

        # Clear state after successful submission
        upi_payment_states.pop(user_id, None)

    except Exception as e:
        logger.error(f"<emoji id=5280721097124249567>😽</emoji> **ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʜᴀɴᴅʟᴇʀ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.send_message(msg.chat.id, f"<emoji id=5998881015320287132>💊</emoji> **❌ ᴇʀʀᴏʀ ꜱᴜʙᴍɪᴛᴛɪɴɢ ᴩᴀʏᴍᴇɴᴛ: {ꜱᴛʀ(ᴇ)}**")

# =============================================================
# RECEIVER ID INPUT HANDLER - FIXED NAME DISPLAY
# =============================================================

@bot.message_handler(func=lambda m: user_stage.get(m.from_user.id) == "waiting_receiver_id")
def handle_receiver_id(msg):
    user_id = msg.from_user.id

    if user_stage.get(user_id) != "waiting_receiver_id":
        return

    try:
        receiver_id = int(msg.text.strip())

        # Check if receiver exists in database
        receiver = users_col.find_one({"user_id": receiver_id})
        if not receiver:
            bot.send_message(
                msg.chat.id,
                f"<emoji id=5318828550940293906>🐱</emoji> **❌ ᴜꜱᴇʀ ɪᴅ `{ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}` ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ!\ɴ\ɴᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ:**",
                parse_mode="Markdown"
            )
            return

        # Get receiver's name - properly formatted
        receiver_name = receiver.get("name", "Unknown")
        receiver_username = receiver.get("username", "")

        if receiver_username:
            receiver_display = f"<emoji id=5999340396432333728>☺️</emoji> **{ʀᴇᴄᴇɪᴠᴇʀ_ɴᴀᴍᴇ} (@{ʀᴇᴄᴇɪᴠᴇʀ_ᴜꜱᴇʀɴᴀᴍᴇ})**"
        else:
            receiver_display = receiver_name

        # Store receiver info in user_states
        user_states[user_id] = {
            "receiver_id": receiver_id,
            "receiver_name": receiver_display
        }

        # Move to amount input
        user_stage[user_id] = "waiting_transfer_amount"

        balance = get_balance(user_id)

        message = f"<emoji id=4929483658114368660>💎</emoji> **📤 **ꜱᴇɴᴅ ʙᴀʟᴀɴᴄᴇ - ꜱᴛᴇᴩ 2/2**\ɴ\ɴ**"
        message += f"<emoji id=5899776109548934640>💲</emoji> **👤 ʀᴇᴄᴇɪᴠᴇʀ: {ʀᴇᴄᴇɪᴠᴇʀ_ᴅɪꜱᴩʟᴀʏ}\ɴ**"
        message += f"<emoji id=5998881015320287132>💊</emoji> **🆔 ʀᴇᴄᴇɪᴠᴇʀ ɪᴅ: `{ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}`\ɴ**"
        message += f"<emoji id=6309739370836399696>🌙</emoji> **💰 ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"
        message += f"<emoji id=6001589602085771497>✅</emoji> **ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴛʜᴇ **ᴀᴍᴏᴜɴᴛ** ᴛᴏ ꜱᴇɴᴅ:**"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("<emoji id=6307568836098922002>🌙</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="send_balance_menu"))

        bot.send_message(
            msg.chat.id,
            message,
            parse_mode="Markdown",
            reply_markup=markup
        )

    except ValueError:
        bot.send_message(
            msg.chat.id,
            "<emoji id=5352870513267973607>✨</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ! ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ɴᴜᴍᴇʀɪᴄ ɪᴅ ᴏɴʟʏ:\ɴᴇxᴀᴍᴩʟᴇ: `123456789`**",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"<emoji id=5999270482954691955>🦋</emoji> **ʀᴇᴄᴇɪᴠᴇʀ ɪᴅ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.send_message(msg.chat.id, f"<emoji id=4927247234283603387>🩷</emoji> **❌ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")

# =============================================================
# TRANSFER AMOUNT INPUT HANDLER
# =============================================================

@bot.message_handler(func=lambda m: user_stage.get(m.from_user.id) == "waiting_transfer_amount")
def handle_transfer_amount(msg):
    user_id = msg.from_user.id

    if user_stage.get(user_id) != "waiting_transfer_amount":
        return

    try:
        amount = float(msg.text.strip())

        # Get stored data
        transfer_data = user_states.get(user_id, {})
        receiver_id = transfer_data.get("receiver_id")
        receiver_name = transfer_data.get("receiver_name", f"<emoji id=6123125485661591081>🩷</emoji> **ɪᴅ: {ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}**")

        if not receiver_id:
            bot.send_message(msg.chat.id, "<emoji id=6309709550878463216>🌟</emoji> **❌ ꜱᴇꜱꜱɪᴏɴ ᴇxᴩɪʀᴇᴅ! ᴩʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ᴀɢᴀɪɴ.**")
            user_stage.pop(user_id, None)
            user_states.pop(user_id, None)
            return

        # Validate amount
        if amount <= 0:
            bot.send_message(msg.chat.id, "<emoji id=5998881015320287132>💊</emoji> **❌ ᴀᴍᴏᴜɴᴛ ᴍᴜꜱᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 0!\ɴᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ:**")
            return

        sender_balance = get_balance(user_id)
        if amount > sender_balance:
            bot.send_message(
                msg.chat.id, 
                f"<emoji id=6310022800023229454>✡️</emoji> **❌ ɪɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ ʙᴀʟᴀɴᴄᴇ! ʏᴏᴜ ʜᴀᴠᴇ {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ꜱᴇɴᴅᴇʀ_ʙᴀʟᴀɴᴄᴇ)}\ɴᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ꜱᴍᴀʟʟᴇʀ ᴀᴍᴏᴜɴᴛ:**"
            )
            return

        # Update transfer data with amount
        transfer_data["amount"] = amount
        user_states[user_id] = transfer_data

        # Show confirmation
        confirm_message = f"<emoji id=6309709550878463216>🌟</emoji> **📤 **ᴄᴏɴꜰɪʀᴍ ᴛʀᴀɴꜱꜰᴇʀ**\ɴ\ɴ**"
        confirm_message += f"<emoji id=6309666601205503867>💌</emoji> **👤 ʀᴇᴄᴇɪᴠᴇʀ: {ʀᴇᴄᴇɪᴠᴇʀ_ɴᴀᴍᴇ}\ɴ**"
        confirm_message += f"<emoji id=6154635934135490309>💗</emoji> **🆔 ʀᴇᴄᴇɪᴠᴇʀ ɪᴅ: `{ʀᴇᴄᴇɪᴠᴇʀ_ɪᴅ}`\ɴ**"
        confirm_message += f"<emoji id=6123040393769521180>☄️</emoji> **💰 ᴀᴍᴏᴜɴᴛ ᴛᴏ ꜱᴇɴᴅ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
        confirm_message += f"<emoji id=5041955142060999726>🌈</emoji> **💳 ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ꜱᴇɴᴅᴇʀ_ʙᴀʟᴀɴᴄᴇ)}\ɴ**"
        confirm_message += f"<emoji id=5999210495146465994>💖</emoji> **💳 ʙᴀʟᴀɴᴄᴇ ᴀꜰᴛᴇʀ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ꜱᴇɴᴅᴇʀ_ʙᴀʟᴀɴᴄᴇ - ᴀᴍᴏᴜɴᴛ)}\ɴ\ɴ**"
        confirm_message += f"<emoji id=5352542184493031170>😈</emoji> **ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴩʀᴏᴄᴇᴇᴅ?**"

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("<emoji id=4929483658114368660>💎</emoji> **✅ ᴄᴏɴꜰɪʀᴍ ᴛʀᴀɴꜱꜰᴇʀ**", callback_data="transfer_confirm"),
            InlineKeyboardButton("<emoji id=5352542184493031170>😈</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="balance")
        )

        bot.send_message(
            msg.chat.id,
            confirm_message,
            parse_mode="Markdown",
            reply_markup=markup
        )

        user_stage.pop(user_id, None)

    except ValueError:
        bot.send_message(
            msg.chat.id,
            "<emoji id=6309985824649780135>🌙</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ! ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀꜱ ᴏɴʟʏ:\ɴᴇxᴀᴍᴩʟᴇ: `100`**",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"<emoji id=5281001756057175314>😽</emoji> **ᴛʀᴀɴꜱꜰᴇʀ ᴀᴍᴏᴜɴᴛ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.send_message(msg.chat.id, f"<emoji id=6310022800023229454>✡️</emoji> **❌ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**")

# ---------------------------------------------------------------------
# EDIT PRICE FUNCTIONS
# ---------------------------------------------------------------------

def show_edit_price_country_selection(chat_id, message_id=None):
    if not is_admin(chat_id):
        bot.send_message(chat_id, "<emoji id=5899776109548934640>💲</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    countries = get_all_countries()
    if not countries:
        text = "<emoji id=4929369656797431200>🪐</emoji> **❌ ɴᴏ ᴄᴏᴜɴᴛʀɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴇᴅɪᴛ.**"
        if message_id:
            edit_or_resend(
                chat_id,
                message_id,
                text,
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("<emoji id=5999210495146465994>💖</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="manage_countries")
                )
            )
        else:
            bot.send_message(chat_id, text)
        return

    text = "<emoji id=5040016479722931047>✨</emoji> **✏️ **ᴇᴅɪᴛ ᴄᴏᴜɴᴛʀʏ ᴩʀɪᴄᴇ**\ɴ\ɴꜱᴇʟᴇᴄᴛ ᴀ ᴄᴏᴜɴᴛʀʏ ᴛᴏ ᴇᴅɪᴛ ɪᴛꜱ ᴩʀɪᴄᴇ:**"
    markup = InlineKeyboardMarkup(row_width=2)
    for country in countries:
        markup.add(InlineKeyboardButton(
            f"<emoji id=4929369656797431200>🪐</emoji> **{ᴄᴏᴜɴᴛʀʏ['ɴᴀᴍᴇ']} - {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴏᴜɴᴛʀʏ['ᴩʀɪᴄᴇ'])}**",
            callback_data=f"<emoji id=6309739370836399696>🌙</emoji> **ᴇᴅɪᴛ_ᴩʀɪᴄᴇ_ᴄᴏᴜɴᴛʀʏ_{ᴄᴏᴜɴᴛʀʏ['ɴᴀᴍᴇ']}**"
        ))
    markup.add(InlineKeyboardButton("<emoji id=6309640268761011366>🌙</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="manage_countries"))

    if message_id:
        edit_or_resend(
            chat_id,
            message_id,
            text,
            markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

def show_edit_price_details(chat_id, message_id, country_name):
    if not is_admin(chat_id):
        bot.send_message(chat_id, "<emoji id=6309819721084573392>🌙</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    country = get_country_by_name(country_name)
    if not country:
        edit_or_resend(
            chat_id,
            message_id,
            f"<emoji id=6224236403153179330>🎀</emoji> **❌ ᴄᴏᴜɴᴛʀʏ '{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}' ɴᴏᴛ ꜰᴏᴜɴᴅ.**",
            markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("<emoji id=6298717844804733009>♾</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="edit_price")
            )
        )
        return

    text = f"<emoji id=6309709550878463216>🌟</emoji> **✏️ **ᴇᴅɪᴛ ᴩʀɪᴄᴇ ꜰᴏʀ {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}**\ɴ\ɴ**"
    text += f"<emoji id=6001132493011425597>💖</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}\ɴ**"
    text += f"<emoji id=4929195195225867512>💎</emoji> **💰 ᴄᴜʀʀᴇɴᴛ ᴩʀɪᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴏᴜɴᴛʀʏ['ᴩʀɪᴄᴇ'])}\ɴ**"
    text += f"<emoji id=6307568836098922002>🌙</emoji> **📊 ᴀᴠᴀɪʟᴀʙʟᴇ ᴀᴄᴄᴏᴜɴᴛꜱ: {ɢᴇᴛ_ᴀᴠᴀɪʟᴀʙʟᴇ_ᴀᴄᴄᴏᴜɴᴛꜱ_ᴄᴏᴜɴᴛ(ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ)}\ɴ\ɴ**"
    text += f"<emoji id=5280721097124249567>😽</emoji> **ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴇᴅɪᴛ ᴛʜᴇ ᴩʀɪᴄᴇ:**"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "<emoji id=6111418418424973677>✅</emoji> **✏️ ᴇᴅɪᴛ ᴩʀɪᴄᴇ**",
        callback_data=f"<emoji id=6307569802466563145>🎶</emoji> **ᴇᴅɪᴛ_ᴩʀɪᴄᴇ_ᴄᴏɴꜰɪʀᴍ_{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}**"
    ))
    markup.add(InlineKeyboardButton("<emoji id=5040016479722931047>✨</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_edit_price"))

    edit_or_resend(
        chat_id,
        message_id,
        text,
        markup=markup,
        parse_mode="Markdown"
    )

# ---------------------------------------------------------------------
# MESSAGE HANDLER FOR LOGIN FLOW
# ---------------------------------------------------------------------

@bot.message_handler(func=lambda m: login_states.get(m.from_user.id, {}).get("step") in ["phone", "waiting_otp", "waiting_password"])
def handle_login_flow_messages(msg):
    user_id = msg.from_user.id

    if user_id not in login_states:
        return

    state = login_states[user_id]
    step = state["step"]
    chat_id = state["chat_id"]
    message_id = state["message_id"]

    if step == "phone":
        phone = msg.text.strip()
        if not re.match(r'<emoji id=6310022800023229454>✡️</emoji> **^\+\ᴅ{10,15}$**', phone):
            bot.send_message(chat_id, "<emoji id=5998977626314643141>🦋</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴩʜᴏɴᴇ ɴᴜᴍʙᴇʀ ꜰᴏʀᴍᴀᴛ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ:\ɴᴇxᴀᴍᴩʟᴇ: +919876543210**")
            return

        if not account_manager:
            try:
                bot.edit_message_text(
                    "<emoji id=6152444560216693216>🥰</emoji> **❌ ᴀᴄᴄᴏᴜɴᴛ ᴍᴏᴅᴜʟᴇ ɴᴏᴛ ʟᴏᴀᴅᴇᴅ. ᴩʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ.**",
                    chat_id, message_id
                )
            except:
                pass
            login_states.pop(user_id, None)
            return

        try:
            success, message = account_manager.pyrogram_login_flow_sync(
                login_states, accounts_col, user_id, phone, chat_id, message_id, state["country"]
            )

            if success:
                try:
                    bot.edit_message_text(
                        f"<emoji id=6307553838073124532>✨</emoji> **📱 ᴩʜᴏɴᴇ: {ᴩʜᴏɴᴇ}\ɴ\ɴ**"
                        "<emoji id=5280678521113443426>😽</emoji> **📩 ᴏᴛᴩ ꜱᴇɴᴛ! ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ:**",
                        chat_id, message_id,
                        reply_markup=InlineKeyboardMarkup().add(
                            InlineKeyboardButton("<emoji id=5285100774060227768>😽</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_login")
                        )
                    )
                except:
                    pass
            else:
                try:
                    bot.edit_message_text(
                        f"<emoji id=6307569802466563145>🎶</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇɴᴅ ᴏᴛᴩ: {ᴍᴇꜱꜱᴀɢᴇ}\ɴ\ɴᴩʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.**",
                        chat_id, message_id
                    )
                except:
                    pass
                login_states.pop(user_id, None)

        except Exception as e:
            logger.error(f"<emoji id=6287579968109024771>✅</emoji> **ʟᴏɢɪɴ ꜰʟᴏᴡ ᴇʀʀᴏʀ: {ᴇ}**")
            try:
                bot.edit_message_text(
                    f"<emoji id=6307490397111195260>🦋</emoji> **❌ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}\ɴ\ɴᴩʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.**",
                    chat_id, message_id
                )
            except:
                pass
            login_states.pop(user_id, None)

    elif step == "waiting_otp":
        otp = msg.text.strip()
        if not otp.isdigit() or len(otp) != 5:
            bot.send_message(chat_id, "<emoji id=6307457716705040156>👍</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴏᴛᴩ ꜰᴏʀᴍᴀᴛ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ 5-ᴅɪɢɪᴛ ᴏᴛᴩ:**")
            return

        if not account_manager:
            try:
                bot.edit_message_text(
                    "<emoji id=6111742817304841054>✅</emoji> **❌ ᴀᴄᴄᴏᴜɴᴛ ᴍᴏᴅᴜʟᴇ ɴᴏᴛ ʟᴏᴀᴅᴇᴅ. ᴩʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ.**",
                    chat_id, message_id
                )
            except:
                pass
            login_states.pop(user_id, None)
            return

        try:
            success, message = account_manager.verify_otp_and_save_sync(
                login_states, accounts_col, user_id, otp
            )

            if success:
                country = state["country"]
                phone = state["phone"]
                try:
                    bot.edit_message_text(
                        f"<emoji id=6309666601205503867>💌</emoji> **✅ **ᴀᴄᴄᴏᴜɴᴛ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
                        f"<emoji id=5999210495146465994>💖</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ}\ɴ**"
                        f"<emoji id=5285100774060227768>😽</emoji> **📱 ᴩʜᴏɴᴇ: {ᴩʜᴏɴᴇ}\ɴ**"
                        f"<emoji id=5899776109548934640>💲</emoji> **🔐 ꜱᴇꜱꜱɪᴏɴ: ɢᴇɴᴇʀᴀᴛᴇᴅ\ɴ\ɴ**"
                        f"<emoji id=6151981777490548710>✅</emoji> **ᴀᴄᴄᴏᴜɴᴛ ɪꜱ ɴᴏᴡ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴩᴜʀᴄʜᴀꜱᴇ!**",
                        chat_id, message_id
                    )
                except:
                    pass
                login_states.pop(user_id, None)

            elif message == "password_required":
                try:
                    bot.edit_message_text(
                        f"<emoji id=4927247234283603387>🩷</emoji> **📱 ᴩʜᴏɴᴇ: {ꜱᴛᴀᴛᴇ['ᴩʜᴏɴᴇ']}\ɴ\ɴ**"
                        "<emoji id=6309666601205503867>💌</emoji> **🔐 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ ʀᴇꞯᴜɪʀᴇᴅ!\ɴ**"
                        "<emoji id=5280678521113443426>😽</emoji> **ᴇɴᴛᴇʀ ʏᴏᴜʀ 2-ꜱᴛᴇᴩ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴩᴀꜱꜱᴡᴏʀᴅ:**",
                        chat_id, message_id,
                        reply_markup=InlineKeyboardMarkup().add(
                            InlineKeyboardButton("<emoji id=6307569802466563145>🎶</emoji> **❌ ᴄᴀɴᴄᴇʟ**", callback_data="cancel_login")
                        )
                    )
                except:
                    pass

            else:
                try:
                    bot.edit_message_text(
                        f"<emoji id=6307821174017496029>🔥</emoji> **❌ ᴏᴛᴩ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜰᴀɪʟᴇᴅ: {ᴍᴇꜱꜱᴀɢᴇ}\ɴ\ɴᴩʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.**",
                        chat_id, message_id
                    )
                except:
                    pass
                login_states.pop(user_id, None)

        except Exception as e:
            logger.error(f"<emoji id=5998881015320287132>💊</emoji> **ᴏᴛᴩ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴇʀʀᴏʀ: {ᴇ}**")
            try:
                bot.edit_message_text(
                    f"<emoji id=5235985147265837746>🗒</emoji> **❌ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}\ɴ\ɴᴩʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.**",
                    chat_id, message_id
                )
            except:
                pass
            login_states.pop(user_id, None)

    elif step == "waiting_password":
        password = msg.text.strip()
        if not password:
            bot.send_message(chat_id, "<emoji id=5281001756057175314>😽</emoji> **❌ ᴩᴀꜱꜱᴡᴏʀᴅ ᴄᴀɴɴᴏᴛ ʙᴇ ᴇᴍᴩᴛʏ. ᴇɴᴛᴇʀ 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ:**")
            return

        if not account_manager:
            try:
                bot.edit_message_text(
                    "<emoji id=5040016479722931047>✨</emoji> **❌ ᴀᴄᴄᴏᴜɴᴛ ᴍᴏᴅᴜʟᴇ ɴᴏᴛ ʟᴏᴀᴅᴇᴅ. ᴩʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ.**",
                    chat_id, message_id
                )
            except:
                pass
            login_states.pop(user_id, None)
            return

        try:
            success, message = account_manager.verify_2fa_password_sync(
                login_states, accounts_col, user_id, password
            )

            if success:
                country = state["country"]
                phone = state["phone"]
                try:
                    bot.edit_message_text(
                        f"<emoji id=5235985147265837746>🗒</emoji> **✅ **ᴀᴄᴄᴏᴜɴᴛ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
                        f"<emoji id=6152142357727811958>🦋</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ}\ɴ**"
                        f"<emoji id=5999340396432333728>☺️</emoji> **📱 ᴩʜᴏɴᴇ: {ᴩʜᴏɴᴇ}\ɴ**"
                        f"<emoji id=4927247234283603387>🩷</emoji> **🔐 2ꜰᴀ: ᴇɴᴀʙʟᴇᴅ\ɴ**"
                        f"<emoji id=6307568836098922002>🌙</emoji> **🔐 ꜱᴇꜱꜱɪᴏɴ: ɢᴇɴᴇʀᴀᴛᴇᴅ\ɴ\ɴ**"
                        f"<emoji id=6307447640711763730>💟</emoji> **ᴀᴄᴄᴏᴜɴᴛ ɪꜱ ɴᴏᴡ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴩᴜʀᴄʜᴀꜱᴇ!**",
                        chat_id, message_id
                    )
                except:
                    pass
                login_states.pop(user_id, None)

            else:
                try:
                    bot.edit_message_text(
                        f"<emoji id=5280721097124249567>😽</emoji> **❌ 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ ꜰᴀɪʟᴇᴅ: {ᴍᴇꜱꜱᴀɢᴇ}\ɴ\ɴᴩʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.**",
                        chat_id, message_id
                    )
                except:
                    pass
                login_states.pop(user_id, None)

        except Exception as e:
            logger.error(f"<emoji id=6307605493644793241>📒</emoji> **2ꜰᴀ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴇʀʀᴏʀ: {ᴇ}**")
            try:
                bot.edit_message_text(
                    f"<emoji id=6111778259374971023>🔥</emoji> **❌ ᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}\ɴ\ɴᴩʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.**",
                    chat_id, message_id
                )
            except:
                pass
            login_states.pop(user_id, None)

# ---------------------------------------------------------------------
# EDIT PRICE MESSAGE HANDLER
# ---------------------------------------------------------------------

@bot.message_handler(func=lambda m: edit_price_state.get(m.from_user.id, {}).get("step") == "waiting_price")
def handle_edit_price_input(msg):
    user_id = msg.from_user.id

    if user_id not in edit_price_state or edit_price_state[user_id]["step"] != "waiting_price":
        return

    if not is_admin(user_id):
        bot.send_message(msg.chat.id, "<emoji id=6307568836098922002>🌙</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        edit_price_state.pop(user_id, None)
        return

    try:
        new_price = float(msg.text.strip())
        if new_price <= 0:
            bot.send_message(msg.chat.id, "<emoji id=5235985147265837746>🗒</emoji> **❌ ᴩʀɪᴄᴇ ᴍᴜꜱᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 0. ᴇɴᴛᴇʀ ᴠᴀʟɪᴅ ᴩʀɪᴄᴇ:**")
            return

        country_name = edit_price_state[user_id]["country"]

        result = countries_col.update_one(
            {"name": country_name, "status": "active"},
            {"<emoji id=5235985147265837746>🗒</emoji> **$ꜱᴇᴛ**": {"price": new_price, "updated_at": datetime.utcnow(), "updated_by": user_id}}
        )

        if result.modified_count > 0:
            bot.send_message(
                msg.chat.id,
                f"<emoji id=6111390922044344694>✅</emoji> **✅ ᴩʀɪᴄᴇ ᴜᴩᴅᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!\ɴ\ɴ**"
                f"<emoji id=6111390922044344694>✅</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}\ɴ**"
                f"<emoji id=6298717844804733009>♾</emoji> **💰 ɴᴇᴡ ᴩʀɪᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɴᴇᴡ_ᴩʀɪᴄᴇ)}\ɴ\ɴ**"
                f"<emoji id=5354924568492383911>😈</emoji> **ᴩʀɪᴄᴇ ʜᴀꜱ ʙᴇᴇɴ ᴜᴩᴅᴀᴛᴇᴅ ꜰᴏʀ ᴀʟʟ ᴜꜱᴇʀꜱ.**"
            )
        else:
            bot.send_message(
                msg.chat.id,
                f"<emoji id=6309739370836399696>🌙</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜᴩᴅᴀᴛᴇ ᴩʀɪᴄᴇ. ᴄᴏᴜɴᴛʀʏ '{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}' ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ᴀʟʀᴇᴀᴅʏ ʜᴀꜱ ꜱᴀᴍᴇ ᴩʀɪᴄᴇ.**"
            )

        edit_price_state.pop(user_id, None)
        show_country_management(msg.chat.id)

    except ValueError:
        bot.send_message(msg.chat.id, "<emoji id=6307605493644793241>📒</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴩʀɪᴄᴇ ꜰᴏʀᴍᴀᴛ. ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀꜱ ᴏɴʟʏ (ᴇ.ɢ., 99.99):**")

# ---------------------------------------------------------------------
# REFERRAL SYSTEM FUNCTIONS
# ---------------------------------------------------------------------

def show_referral_info(user_id, chat_id):
    user_data = users_col.find_one({"user_id": user_id}) or {}
    referral_code = user_data.get('referral_code', f'<emoji id=6154635934135490309>💗</emoji> **ʀᴇꜰ{ᴜꜱᴇʀ_ɪᴅ}**')
    total_commission = user_data.get('total_commission_earned', 0)
    total_referrals = user_data.get('total_referrals', 0)

    referral_link = f"<emoji id=5235985147265837746>🗒</emoji> **ʜᴛᴛᴩꜱ://ᴛ.ᴍᴇ/{ʙᴏᴛ.ɢᴇᴛ_ᴍᴇ().ᴜꜱᴇʀɴᴀᴍᴇ}?ꜱᴛᴀʀᴛ={ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴅᴇ}**"

    message = f"<emoji id=5999340396432333728>☺️</emoji> **👥 **ʀᴇꜰᴇʀ & ᴇᴀʀɴ {ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ}% ᴄᴏᴍᴍɪꜱꜱɪᴏɴ!**\ɴ\ɴ**"
    message += f"<emoji id=6307568836098922002>🌙</emoji> **📊 **ʏᴏᴜʀ ꜱᴛᴀᴛꜱ:**\ɴ**"
    message += f"<emoji id=6151981777490548710>✅</emoji> **• ᴛᴏᴛᴀʟ ʀᴇꜰᴇʀʀᴀʟꜱ: {ᴛᴏᴛᴀʟ_ʀᴇꜰᴇʀʀᴀʟꜱ}\ɴ**"
    message += f"<emoji id=6123125485661591081>🩷</emoji> **• ᴛᴏᴛᴀʟ ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ᴇᴀʀɴᴇᴅ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴛᴏᴛᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ)}\ɴ**"
    message += f"<emoji id=6310022800023229454>✡️</emoji> **• ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ʀᴀᴛᴇ: {ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ}% ᴩᴇʀ ʀᴇᴄʜᴀʀɢᴇ\ɴ\ɴ**"
    message += f"<emoji id=6307750079423845494>👑</emoji> **🔗 **ʏᴏᴜʀ ʀᴇꜰᴇʀʀᴀʟ ʟɪɴᴋ:**\ɴ`{ʀᴇꜰᴇʀʀᴀʟ_ʟɪɴᴋ}`\ɴ\ɴ**"
    message += f"<emoji id=5280678521113443426>😽</emoji> **📝 **ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:**\ɴ**"
    message += f"<emoji id=4929369656797431200>🪐</emoji> **1. ꜱʜᴀʀᴇ ʏᴏᴜʀ ʀᴇꜰᴇʀʀᴀʟ ʟɪɴᴋ ᴡɪᴛʜ ꜰʀɪᴇɴᴅꜱ\ɴ**"
    message += f"<emoji id=6307605493644793241>📒</emoji> **2. ᴡʜᴇɴ ᴛʜᴇʏ ᴊᴏɪɴ ᴜꜱɪɴɢ ʏᴏᴜʀ ʟɪɴᴋ\ɴ**"
    message += f"<emoji id=5281001756057175314>😽</emoji> **3. ʏᴏᴜ ᴇᴀʀɴ {ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ}% ᴏꜰ ᴇᴠᴇʀʏ ʀᴇᴄʜᴀʀɢᴇ ᴛʜᴇʏ ᴍᴀᴋᴇ!\ɴ**"
    message += f"<emoji id=5998881015320287132>💊</emoji> **4. ᴄᴏᴍᴍɪꜱꜱɪᴏɴ ᴄʀᴇᴅɪᴛᴇᴅ ɪɴꜱᴛᴀɴᴛʟʏ\ɴ\ɴ**"
    message += f"<emoji id=6152142357727811958>🦋</emoji> **💰 **ᴇxᴀᴍᴩʟᴇ:** ɪꜰ ᴀ ꜰʀɪᴇɴᴅ ʀᴇᴄʜᴀʀɢᴇꜱ ₹1000, ʏᴏᴜ ᴇᴀʀɴ ₹{1000 * ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ / 100}!\ɴ\ɴ**"
    message += f"<emoji id=6287579968109024771>✅</emoji> **ꜱᴛᴀʀᴛ ꜱʜᴀʀɪɴɢ ᴀɴᴅ ᴇᴀʀɴɪɴɢ ᴛᴏᴅᴀʏ! 🎉**"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("<emoji id=5999340396432333728>☺️</emoji> **📤 ꜱʜᴀʀᴇ ʟɪɴᴋ**", url=f"<emoji id=5041955142060999726>🌈</emoji> **ʜᴛᴛᴩꜱ://ᴛ.ᴍᴇ/ꜱʜᴀʀᴇ/ᴜʀʟ?ᴜʀʟ={ʀᴇꜰᴇʀʀᴀʟ_ʟɪɴᴋ}&ᴛᴇxᴛ=ᴊᴏɪɴ%20ɢᴍꜱ%20ᴏᴛᴩ%20ʙᴏᴛ%20%ᴇ2%80%94%20ꜰᴀꜱᴛ%2ᴄ%20ʀᴇʟɪᴀʙʟᴇ%20ᴛᴇʟᴇɢʀᴀᴍ%20ᴀᴄᴄᴏᴜɴᴛ%20ʙᴜʏɪɴɢ!**", style="success"))
    markup.add(InlineKeyboardButton("<emoji id=6111390922044344694>✅</emoji> **🔙 ʙᴀᴄᴋ**", callback_data="back_to_menu", style="primary"))

    sent_msg = bot.send_message(chat_id, message, parse_mode="Markdown", reply_markup=markup)
    user_last_message[user_id] = sent_msg.message_id

# ---------------------------------------------------------------------
# ADMIN MANAGEMENT FUNCTIONS
# ---------------------------------------------------------------------

def show_admin_panel(chat_id):
    user_id = chat_id

    if not is_admin(user_id):
        bot.send_message(chat_id, "<emoji id=6309819721084573392>🌙</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    total_accounts = accounts_col.count_documents({})
    active_accounts = accounts_col.count_documents({"status": "active", "used": False})
    total_users = users_col.count_documents({})
    total_orders = orders_col.count_documents({})
    banned_users = banned_users_col.count_documents({"status": "active"})
    active_countries = countries_col.count_documents({"status": "active"})
    total_admins = get_admin_count()

    text = (
        f"<emoji id=6309640268761011366>🌙</emoji> **⚡ **ɢᴍꜱ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ**\ɴ\ɴ**"
        f"<emoji id=6001132493011425597>💖</emoji> **📊 **ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ:**\ɴ**"
        f"<emoji id=5899776109548934640>💲</emoji> **• 📦 ᴛᴏᴛᴀʟ ᴀᴄᴄᴏᴜɴᴛꜱ: {ᴛᴏᴛᴀʟ_ᴀᴄᴄᴏᴜɴᴛꜱ}\ɴ**"
        f"<emoji id=5354924568492383911>😈</emoji> **• ✅ ᴀᴄᴛɪᴠᴇ ᴀᴄᴄᴏᴜɴᴛꜱ: {ᴀᴄᴛɪᴠᴇ_ᴀᴄᴄᴏᴜɴᴛꜱ}\ɴ**"
        f"<emoji id=5318828550940293906>🐱</emoji> **• 👥 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: {ᴛᴏᴛᴀʟ_ᴜꜱᴇʀꜱ}\ɴ**"
        f"<emoji id=4929369656797431200>🪐</emoji> **• 🛒 ᴛᴏᴛᴀʟ ᴏʀᴅᴇʀꜱ: {ᴛᴏᴛᴀʟ_ᴏʀᴅᴇʀꜱ}\ɴ**"
        f"<emoji id=6123040393769521180>☄️</emoji> **• 🔒 ʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ: {ʙᴀɴɴᴇᴅ_ᴜꜱᴇʀꜱ}\ɴ**"
        f"<emoji id=5899776109548934640>💲</emoji> **• 🌍 ᴀᴄᴛɪᴠᴇ ᴄᴏᴜɴᴛʀɪᴇꜱ: {ᴀᴄᴛɪᴠᴇ_ᴄᴏᴜɴᴛʀɪᴇꜱ}\ɴ**"
        f"<emoji id=4926993814033269936>🖕</emoji> **• 👑 ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴꜱ: {ᴛᴏᴛᴀʟ_ᴀᴅᴍɪɴꜱ}/6\ɴ\ɴ**"
        f"<emoji id=6224236403153179330>🎀</emoji> **🛠️ **ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴛᴏᴏʟꜱ:****"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("<emoji id=6310044717241340733>🔄</emoji> **📲 ᴀᴅᴅ ᴀᴄᴄᴏᴜɴᴛ**", callback_data="add_account", style="success"),
        InlineKeyboardButton("<emoji id=6309985824649780135>🌙</emoji> **📣 ʙʀᴏᴀᴅᴄᴀꜱᴛ**", callback_data="broadcast_menu", style="primary")
    )
    markup.add(
        InlineKeyboardButton("<emoji id=6307457716705040156>👍</emoji> **🔄 ʀᴇꜰᴜɴᴅ**", callback_data="refund_start", style="primary"),
        InlineKeyboardButton("<emoji id=6307643744623531146>🦋</emoji> **🏆 ʀᴀɴᴋɪɴɢ**", callback_data="ranking", style="primary")
    )
    markup.add(
        InlineKeyboardButton("<emoji id=5280678521113443426>😽</emoji> **📨 ᴍᴇꜱꜱᴀɢᴇ ᴜꜱᴇʀ**", callback_data="message_user", style="primary"),
        InlineKeyboardButton("<emoji id=6309666601205503867>💌</emoji> **➖ ᴅᴇᴅᴜᴄᴛ ʙᴀʟᴀɴᴄᴇ**", callback_data="admin_deduct_start", style="danger")
    )
    markup.add(
        InlineKeyboardButton("<emoji id=5280904324724063665>😽</emoji> **🔒 ʙᴀɴ ᴜꜱᴇʀ**", callback_data="ban_user", style="danger"),
        InlineKeyboardButton("<emoji id=5041955142060999726>🌈</emoji> **🔓 ᴜɴʙᴀɴ ᴜꜱᴇʀ**", callback_data="unban_user", style="success")
    )
    markup.add(
        InlineKeyboardButton("<emoji id=4927247234283603387>🩷</emoji> **🗺️ ᴄᴏᴜɴᴛʀɪᴇꜱ**", callback_data="manage_countries", style="primary"),
        InlineKeyboardButton("<emoji id=5899776109548934640>💲</emoji> **🎫 ᴄᴏᴜᴩᴏɴꜱ**", callback_data="admin_coupon_menu", style="success")
    )

    # Show admin list for main admin
    if is_super_admin(user_id):
        admins = get_all_admins()
        admin_text = "<emoji id=5998881015320287132>💊</emoji> **\ɴ\ɴ👥 **ᴄᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴꜱ:**\ɴ**"
        for admin in admins:
            if admin.get("is_super_admin", False):
                admin_text += f"<emoji id=4929195195225867512>💎</emoji> **👑 ᴍᴀɪɴ: `{ᴀᴅᴍɪɴ['ᴜꜱᴇʀ_ɪᴅ']}`\ɴ**"
            else:
                admin_text += f"<emoji id=6309739370836399696>🌙</emoji> **👤 ᴀᴅᴍɪɴ: `{ᴀᴅᴍɪɴ['ᴜꜱᴇʀ_ɪᴅ']}`\ɴ**"
        text += admin_text

    sent_msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    user_last_message[user_id] = sent_msg.message_id

def show_country_management(chat_id):
    if not is_admin(chat_id):
        bot.send_message(chat_id, "<emoji id=5999340396432333728>☺️</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    countries = get_all_countries()
    if not countries:
        text = "<emoji id=6152444560216693216>🥰</emoji> **🌍 **ᴄᴏᴜɴᴛʀʏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**\ɴ\ɴɴᴏ ᴄᴏᴜɴᴛʀɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ. ᴀᴅᴅ ᴀ ᴄᴏᴜɴᴛʀʏ ꜰɪʀꜱᴛ.**"
    else:
        text = "<emoji id=6307490397111195260>🦋</emoji> **🌍 **ᴄᴏᴜɴᴛʀʏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**\ɴ\ɴ**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴜɴᴛʀɪᴇꜱ:**\ɴ**"
        for country in countries:
            accounts_count = get_available_accounts_count(country['name'])
            text += f"<emoji id=5354924568492383911>😈</emoji> **• {ᴄᴏᴜɴᴛʀʏ['ɴᴀᴍᴇ']} - ᴩʀɪᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴏᴜɴᴛʀʏ['ᴩʀɪᴄᴇ'])} - ᴀᴄᴄᴏᴜɴᴛꜱ: {ᴀᴄᴄᴏᴜɴᴛꜱ_ᴄᴏᴜɴᴛ}\ɴ**"

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("<emoji id=6309666601205503867>💌</emoji> **🌐 ᴀᴅᴅ ᴄᴏᴜɴᴛʀʏ**", callback_data="add_country", style="success"),
        InlineKeyboardButton("<emoji id=6309819721084573392>🌙</emoji> **💱 ᴇᴅɪᴛ ᴩʀɪᴄᴇ**", callback_data="edit_price", style="primary")
    )
    markup.add(
        InlineKeyboardButton("<emoji id=5352542184493031170>😈</emoji> **🗑️ ʀᴇᴍᴏᴠᴇ ᴄᴏᴜɴᴛʀʏ**", callback_data="remove_country", style="danger")
    )
    markup.add(InlineKeyboardButton("<emoji id=4929369656797431200>🪐</emoji> **🔙 ʙᴀᴄᴋ ᴛᴏ ᴀᴅᴍɪɴ**", callback_data="admin_panel", style="primary"))

    sent_msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    user_last_message[chat_id] = sent_msg.message_id

def ask_country_name(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "<emoji id=6307569802466563145>🎶</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    country_name = message.text.strip()
    user_states[message.chat.id] = {
        "step": "ask_country_price",
        "country_name": country_name
    }
    bot.send_message(message.chat.id, f"<emoji id=5354924568492383911>😈</emoji> **💰 ᴇɴᴛᴇʀ ᴩʀɪᴄᴇ ꜰᴏʀ {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}:**")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get("step") == "ask_country_price")
def ask_country_price(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "<emoji id=5041955142060999726>🌈</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    try:
        price = float(message.text.strip())
        user_data = user_states.get(message.chat.id)
        country_name = user_data.get("country_name")

        country_data = {
            "name": country_name,
            "price": price,
            "status": "active",
            "created_at": datetime.utcnow(),
            "created_by": message.from_user.id
        }
        countries_col.insert_one(country_data)

        del user_states[message.chat.id]
        bot.send_message(
            message.chat.id,
            f"<emoji id=5040016479722931047>✨</emoji> **✅ **ᴄᴏᴜɴᴛʀʏ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\ɴ\ɴ**"
            f"<emoji id=5999270482954691955>🦋</emoji> **🌍 ᴄᴏᴜɴᴛʀʏ: {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}\ɴ**"
            f"<emoji id=6151981777490548710>✅</emoji> **💰 ᴩʀɪᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴩʀɪᴄᴇ)}\ɴ\ɴ**"
            f"<emoji id=5999151980512024620>🥰</emoji> **ᴄᴏᴜɴᴛʀʏ ɪꜱ ɴᴏᴡ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴜꜱᴇʀꜱ ᴛᴏ ᴩᴜʀᴄʜᴀꜱᴇ ᴀᴄᴄᴏᴜɴᴛꜱ.**"
        )
        show_country_management(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, "<emoji id=6307568836098922002>🌙</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴩʀɪᴄᴇ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ɴᴜᴍʙᴇʀ:**")

def show_country_removal(chat_id):
    if not is_admin(chat_id):
        bot.send_message(chat_id, "<emoji id=5899776109548934640>💲</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    countries = get_all_countries()
    if not countries:
        bot.send_message(chat_id, "<emoji id=4929195195225867512>💎</emoji> **❌ ɴᴏ ᴄᴏᴜɴᴛʀɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ.**")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    for country in countries:
        markup.add(InlineKeyboardButton(
            f"<emoji id=6309985824649780135>🌙</emoji> **❌ {ᴄᴏᴜɴᴛʀʏ['ɴᴀᴍᴇ']}**",
            callback_data=f"<emoji id=5285100774060227768>😽</emoji> **ʀᴇᴍᴏᴠᴇ_ᴄᴏᴜɴᴛʀʏ_{ᴄᴏᴜɴᴛʀʏ['ɴᴀᴍᴇ']}**"
        ))
    markup.add(InlineKeyboardButton("<emoji id=6307447640711763730>💟</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="manage_countries"))

    sent_msg = bot.send_message(
        chat_id,
        "<emoji id=6310044717241340733>🔄</emoji> **🗑️ **ʀᴇᴍᴏᴠᴇ ᴄᴏᴜɴᴛʀʏ**\ɴ\ɴꜱᴇʟᴇᴄᴛ ᴀ ᴄᴏᴜɴᴛʀʏ ᴛᴏ ʀᴇᴍᴏᴠᴇ:**",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    user_last_message[chat_id] = sent_msg.message_id

def remove_country(country_name, chat_id, message_id=None):
    if not is_admin(chat_id):
        return "<emoji id=5999041732996504081>✨</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**"

    try:
        result = countries_col.update_one(
            {"name": country_name, "status": "active"},
            {"<emoji id=6123125485661591081>🩷</emoji> **$ꜱᴇᴛ**": {"status": "inactive", "removed_at": datetime.utcnow()}}
        )

        if result.modified_count > 0:
            accounts_col.delete_many({"country": country_name})

            if message_id:
                try:
                    bot.delete_message(chat_id, message_id)
                except:
                    pass

            bot.send_message(chat_id, f"<emoji id=6309709550878463216>🌟</emoji> **✅ ᴄᴏᴜɴᴛʀʏ '{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}' ᴀɴᴅ ᴀʟʟ ɪᴛꜱ ᴀᴄᴄᴏᴜɴᴛꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.**")
            show_country_management(chat_id)
            return f"<emoji id=5040016479722931047>✨</emoji> **✅ {ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ} ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ**"
        else:
            return f"<emoji id=6307569802466563145>🎶</emoji> **❌ ᴄᴏᴜɴᴛʀʏ '{ᴄᴏᴜɴᴛʀʏ_ɴᴀᴍᴇ}' ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ᴀʟʀᴇᴀᴅʏ ʀᴇᴍᴏᴠᴇᴅ**"
    except Exception as e:
        logger.error(f"<emoji id=5280904324724063665>😽</emoji> **ᴇʀʀᴏʀ ʀᴇᴍᴏᴠɪɴɢ ᴄᴏᴜɴᴛʀʏ: {ᴇ}**")
        return f"<emoji id=5285100774060227768>😽</emoji> **❌ ᴇʀʀᴏʀ ʀᴇᴍᴏᴠɪɴɢ ᴄᴏᴜɴᴛʀʏ: {ꜱᴛʀ(ᴇ)}**"

def ask_ban_user(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "<emoji id=6307553838073124532>✨</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    try:
        user_id_to_ban = int(message.text.strip())

        user = users_col.find_one({"user_id": user_id_to_ban})
        if not user:
            bot.send_message(message.chat.id, "<emoji id=6309739370836399696>🌙</emoji> **❌ ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ.**")
            return

        already_banned = banned_users_col.find_one({"user_id": user_id_to_ban, "status": "active"})
        if already_banned:
            bot.send_message(message.chat.id, "<emoji id=6111390922044344694>✅</emoji> **⚠️ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ.**")
            return

        ban_record = {
            "user_id": user_id_to_ban,
            "banned_by": message.from_user.id,
            "reason": "<emoji id=6307750079423845494>👑</emoji> **ᴀᴅᴍɪɴ ʙᴀɴɴᴇᴅ**",
            "status": "active",
            "banned_at": datetime.utcnow()
        }
        banned_users_col.insert_one(ban_record)

        bot.send_message(message.chat.id, f"<emoji id=4926993814033269936>🖕</emoji> **✅ ᴜꜱᴇʀ {ᴜꜱᴇʀ_ɪᴅ_ᴛᴏ_ʙᴀɴ} ʜᴀꜱ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.**")

        try:
            bot.send_message(
                user_id_to_ban,
                "<emoji id=5899776109548934640>💲</emoji> **🚫 **ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀꜱ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ**\ɴ\ɴ**"
                "<emoji id=6001589602085771497>✅</emoji> **ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.\ɴ**"
                "<emoji id=5999270482954691955>🦋</emoji> **ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ @ᴅʜʀᴜᴠ_ᴩᴀᴩᴀʜᴇʀᴇ ɪꜰ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ.**"
            )
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "<emoji id=5999340396432333728>☺️</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ɴᴜᴍᴇʀɪᴄ ɪᴅ ᴏɴʟʏ.**")

def ask_unban_user(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "<emoji id=4926993814033269936>🖕</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    try:
        user_id_to_unban = int(message.text.strip())

        ban_record = banned_users_col.find_one({"user_id": user_id_to_unban, "status": "active"})
        if not ban_record:
            bot.send_message(message.chat.id, "<emoji id=5354924568492383911>😈</emoji> **⚠️ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ʙᴀɴɴᴇᴅ.**")
            return

        banned_users_col.update_one(
            {"user_id": user_id_to_unban, "status": "active"},
            {"<emoji id=5998977626314643141>🦋</emoji> **$ꜱᴇᴛ**": {"status": "unbanned", "unbanned_at": datetime.utcnow(), "unbanned_by": message.from_user.id}}
        )

        bot.send_message(message.chat.id, f"<emoji id=5998881015320287132>💊</emoji> **✅ ᴜꜱᴇʀ {ᴜꜱᴇʀ_ɪᴅ_ᴛᴏ_ᴜɴʙᴀɴ} ʜᴀꜱ ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ.**")

        try:
            bot.send_message(
                user_id_to_unban,
                "<emoji id=4929483658114368660>💎</emoji> **✅ **ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀꜱ ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ**\ɴ\ɴ**"
                "<emoji id=5318828550940293906>🐱</emoji> **ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴀᴄᴄᴇꜱꜱ ʜᴀꜱ ʙᴇᴇɴ ʀᴇꜱᴛᴏʀᴇᴅ.\ɴ**"
                "<emoji id=6152142357727811958>🦋</emoji> **ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ ɴᴏʀᴍᴀʟʟʏ.**"
            )
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "<emoji id=6287579968109024771>✅</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ɴᴜᴍᴇʀɪᴄ ɪᴅ ᴏɴʟʏ.**")

def show_user_ranking(chat_id):
    if not is_admin(chat_id):
        bot.send_message(chat_id, "<emoji id=6152142357727811958>🦋</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    try:
        users_ranking = []
        all_wallets = wallets_col.find()

        for wallet in all_wallets:
            user_id_rank = wallet.get("user_id")
            balance = float(wallet.get("balance", 0))

            if balance > 0:
                user = users_col.find_one({"user_id": user_id_rank}) or {}
                name = user.get("name", "Unknown")
                username_db = user.get("username")
                users_ranking.append({
                    "user_id": user_id_rank,
                    "balance": balance,
                    "name": name,
                    "username": username_db
                })

        users_ranking.sort(key=lambda x: x["balance"], reverse=True)

        ranking_text = "<emoji id=6309666601205503867>💌</emoji> **📊 **ᴜꜱᴇʀ ʀᴀɴᴋɪɴɢ ʙʏ ᴡᴀʟʟᴇᴛ ʙᴀʟᴀɴᴄᴇ**\ɴ\ɴ**"
        if not users_ranking:
            ranking_text = "<emoji id=6307447640711763730>💟</emoji> **📊 ɴᴏ ᴜꜱᴇʀꜱ ꜰᴏᴜɴᴅ ᴡɪᴛʜ ʙᴀʟᴀɴᴄᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ ᴢᴇʀᴏ.**"
        else:
            for index, user_data in enumerate(users_ranking[:20], 1):
                user_link = f"<emoji id=6307457716705040156>👍</emoji> **<ᴀ ʜʀᴇꜰ='ᴛɢ://ᴜꜱᴇʀ?ɪᴅ={ᴜꜱᴇʀ_ᴅᴀᴛᴀ['ᴜꜱᴇʀ_ɪᴅ']}'>{ᴜꜱᴇʀ_ᴅᴀᴛᴀ['ᴜꜱᴇʀ_ɪᴅ']}</ᴀ>**"
                username_display = f"<emoji id=5285100774060227768>😽</emoji> **@{ᴜꜱᴇʀ_ᴅᴀᴛᴀ['ᴜꜱᴇʀɴᴀᴍᴇ']}**" if user_data['username'] else "<emoji id=6287579968109024771>✅</emoji> **ɴᴏ ᴜꜱᴇʀɴᴀᴍᴇ**"
                ranking_text += f"<emoji id=6111742817304841054>✅</emoji> **{ɪɴᴅᴇx}. {ᴜꜱᴇʀ_ʟɪɴᴋ} - {ᴜꜱᴇʀɴᴀᴍᴇ_ᴅɪꜱᴩʟᴀʏ}\ɴ**"
                ranking_text += f"<emoji id=5998881015320287132>💊</emoji> ** 💰 ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴜꜱᴇʀ_ᴅᴀᴛᴀ['ʙᴀʟᴀɴᴄᴇ'])}\ɴ\ɴ**"

        bot.send_message(chat_id, ranking_text, parse_mode="HTML")
    except Exception as e:
        logger.exception("<emoji id=5999041732996504081>✨</emoji> **ᴇʀʀᴏʀ ɪɴ ʀᴀɴᴋɪɴɢ:**")
        bot.send_message(chat_id, f"<emoji id=5354924568492383911>😈</emoji> **❌ ᴇʀʀᴏʀ ɢᴇɴᴇʀᴀᴛɪɴɢ ʀᴀɴᴋɪɴɢ: {ꜱᴛʀ(ᴇ)}**")

# ---------------------------------------------------------------------
# BROADCAST FUNCTION - PERFECT FORWARD (PURE TELEBOT)
# ---------------------------------------------------------------------

@bot.message_handler(commands=['sendbroadcast'])
def handle_sendbroadcast_command(msg):
    """<emoji id=4927247234283603387>🩷</emoji> **ʜᴀɴᴅʟᴇ /ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴍᴀɴᴅ - ᴇxᴀᴄᴛ ꜰᴏʀᴡᴀʀᴅ**"""
    global IS_BROADCASTING

    if not is_admin(msg.from_user.id):
        bot.send_message(msg.chat.id, "<emoji id=6307490397111195260>🦋</emoji> **❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ**")
        return

    if IS_BROADCASTING:
        bot.send_message(msg.chat.id, "<emoji id=6310044717241340733>🔄</emoji> **⚠️ ᴀɴᴏᴛʜᴇʀ ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴩʀᴏɢʀᴇꜱꜱ. ᴩʟᴇᴀꜱᴇ ᴡᴀɪᴛ...**")
        return

    if not msg.reply_to_message:
        bot.send_message(
            msg.chat.id,
            "<emoji id=5998881015320287132>💊</emoji> **❌ ᴩʟᴇᴀꜱᴇ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ /ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ\ɴ\ɴ**"
            "<emoji id=5352542184493031170>😈</emoji> **📝 **ᴏᴩᴛɪᴏɴꜱ:**\ɴ**"
            "<emoji id=6307643744623531146>🦋</emoji> **• `/ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ` - ɴᴏʀᴍᴀʟ ʙʀᴏᴀᴅᴄᴀꜱᴛ\ɴ**"
            "<emoji id=6307457716705040156>👍</emoji> **• `/ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ -ᴩɪɴ` - ᴀᴜᴛᴏ-ᴩɪɴ (ꜱɪʟᴇɴᴛ)\ɴ**"
            "<emoji id=6309666601205503867>💌</emoji> **• `/ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ -ᴩɪɴʟᴏᴜᴅ` - ᴀᴜᴛᴏ-ᴩɪɴ (ᴡɪᴛʜ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ)\ɴ**"
            "<emoji id=5041955142060999726>🌈</emoji> **• `/ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ -ᴜꜱᴇʀ` - ᴀʟꜱᴏ ꜱᴇɴᴅ ᴛᴏ ᴜꜱᴇʀꜱ\ɴ**"
            "<emoji id=6123040393769521180>☄️</emoji> **• `/ꜱᴇɴᴅʙʀᴏᴀᴅᴄᴀꜱᴛ -ᴩɪɴ -ᴜꜱᴇʀ` - ᴄᴏᴍʙɪɴᴇ ᴏᴩᴛɪᴏɴꜱ**",
            parse_mode="Markdown"
        )
        return

    # Parse options
    cmd_text = msg.text.lower()
    pin_silent = '<emoji id=4926993814033269936>🖕</emoji> **-ᴩɪɴ**' in cmd_text and '<emoji id=5281001756057175314>😽</emoji> **-ᴩɪɴʟᴏᴜᴅ**' not in cmd_text
    pin_loud = '<emoji id=6307821174017496029>🔥</emoji> **-ᴩɪɴʟᴏᴜᴅ**' in cmd_text
    send_to_users = '<emoji id=6111418418424973677>✅</emoji> **-ᴜꜱᴇʀ**' in cmd_text

    source = msg.reply_to_message

    # Send confirmation
    status_msg = bot.send_message(
        msg.chat.id,
        f"<emoji id=6001589602085771497>✅</emoji> **📡 **ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴛᴀʀᴛᴇᴅ**\ɴ\ɴ**"
        f"<emoji id=6310044717241340733>🔄</emoji> **📨 ꜰᴏʀᴡᴀʀᴅɪɴɢ ᴇxᴀᴄᴛ ᴍᴇꜱꜱᴀɢᴇ...\ɴ**"
        f"<emoji id=5999151980512024620>🥰</emoji> **👥 ɢʀᴏᴜᴩꜱ: ʏᴇꜱ\ɴ**"
        f"<emoji id=6307605493644793241>📒</emoji> **👤 ᴜꜱᴇʀꜱ: {'ʏᴇꜱ' ɪꜰ ꜱᴇɴᴅ_ᴛᴏ_ᴜꜱᴇʀꜱ ᴇʟꜱᴇ 'ɴᴏ'}\ɴ**"
        f"<emoji id=5352870513267973607>✨</emoji> **📌 ᴩɪɴ: {'🔊 ʟᴏᴜᴅ' ɪꜰ ᴩɪɴ_ʟᴏᴜᴅ ᴇʟꜱᴇ '🔇 ꜱɪʟᴇɴᴛ' ɪꜰ ᴩɪɴ_ꜱɪʟᴇɴᴛ ᴇʟꜱᴇ '❌ ɴᴏ'}\ɴ\ɴ**"
        f"<emoji id=6309985824649780135>🌙</emoji> **⏳ ᴩʀᴏᴄᴇꜱꜱɪɴɢ...**",
        parse_mode="Markdown"
    )

    IS_BROADCASTING = True

    # Start broadcast thread
    threading.Thread(
        target=broadcast_worker,
        args=(
            source,
            pin_silent,
            pin_loud,
            send_to_users,
            msg.chat.id,
            status_msg.message_id,
            msg.from_user.id
        ),
        daemon=True
    ).start()

def broadcast_worker(source_msg, pin_silent, pin_loud, send_to_users, admin_chat_id, status_msg_id, admin_id):
    """<emoji id=5235985147265837746>🗒</emoji> **ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴡᴏʀᴋᴇʀ - ᴇxᴀᴄᴛ ꜰᴏʀᴡᴀʀᴅ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴩꜱ ᴀɴᴅ ᴜꜱᴇʀꜱ**"""
    global IS_BROADCASTING

    try:
        # Get all unique chat IDs from database
        all_chats = []
        chat_ids = set()

        # 1. Get all users (negative IDs are groups)
        all_users = list(users_col.find())
        for user in all_users:
            uid = user.get("user_id")
            if uid and uid != ADMIN_ID and uid != admin_id:
                chat_ids.add(uid)

        # 2. Get all served chats if collection exists
        try:
            if 'served_chats' in db.list_collection_names():
                served = db['served_chats'].find()
                for chat in served:
                    cid = chat.get("chat_id")
                    if cid:
                        chat_ids.add(cid)
        except:
            pass

        all_chats = list(chat_ids)

        # Separate groups and users
        groups = [cid for cid in all_chats if str(cid).startswith('-')]
        users = [cid for cid in all_chats if not str(cid).startswith('-') and cid != ADMIN_ID and cid != admin_id]

        # Update status
        bot.edit_message_text(
            f"<emoji id=6111418418424973677>✅</emoji> **📡 **ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ ᴛᴏ ɢʀᴏᴜᴩꜱ...**\ɴ\ɴ**"
            f"<emoji id=6111418418424973677>✅</emoji> **👥 ᴛᴏᴛᴀʟ ɢʀᴏᴜᴩꜱ: {ʟᴇɴ(ɢʀᴏᴜᴩꜱ)}**",
            admin_chat_id,
            status_msg_id,
            parse_mode="Markdown"
        )

        # ----- BROADCAST TO GROUPS -----
        groups_sent = 0
        groups_pinned = 0
        groups_failed = 0

        for chat_id in groups:
            try:
                # EXACT FORWARD - Telegram API ka original forward
                forwarded_msg = bot.forward_message(
                    chat_id,
                    source_msg.chat.id,
                    source_msg.message_id
                )
                groups_sent += 1

                # Pin if option enabled
                if pin_silent or pin_loud:
                    try:
                        bot.pin_chat_message(
                            chat_id,
                            forwarded_msg.message_id,
                            disable_notification=(not pin_loud)
                        )
                        groups_pinned += 1
                    except:
                        pass

                # Update progress every 10 messages
                if groups_sent % 10 == 0:
                    bot.edit_message_text(
                        f"<emoji id=6307750079423845494>👑</emoji> **📡 **ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ...**\ɴ\ɴ**"
                        f"<emoji id=6152444560216693216>🥰</emoji> **👥 ɢʀᴏᴜᴩꜱ: {ɢʀᴏᴜᴩꜱ_ꜱᴇɴᴛ}/{ʟᴇɴ(ɢʀᴏᴜᴩꜱ)} ꜱᴇɴᴛ\ɴ**"
                        f"<emoji id=6310044717241340733>🔄</emoji> **📌 ᴩɪɴɴᴇᴅ: {ɢʀᴏᴜᴩꜱ_ᴩɪɴɴᴇᴅ}**",
                        admin_chat_id,
                        status_msg_id,
                        parse_mode="Markdown"
                    )

                time.sleep(0.25)  # Anti-flood

            except Exception as e:
                groups_failed += 1
                logger.error(f"<emoji id=5281001756057175314>😽</emoji> **ɢʀᴏᴜᴩ ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜰᴀɪʟᴇᴅ ꜰᴏʀ {ᴄʜᴀᴛ_ɪᴅ}: {ᴇ}**")
                continue

        # ----- BROADCAST TO USERS (if option enabled) -----
        users_sent = 0
        users_failed = 0

        if send_to_users and users:
            bot.edit_message_text(
                f"<emoji id=5280606902533783431>😽</emoji> **📡 **ɢʀᴏᴜᴩꜱ ᴅᴏɴᴇ: {ɢʀᴏᴜᴩꜱ_ꜱᴇɴᴛ} ꜱᴇɴᴛ**\ɴ\ɴ**"
                f"<emoji id=6310044717241340733>🔄</emoji> **👤 ɴᴏᴡ ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ ᴛᴏ ᴜꜱᴇʀꜱ...\ɴ**"
                f"<emoji id=6001589602085771497>✅</emoji> **👥 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: {ʟᴇɴ(ᴜꜱᴇʀꜱ)}**",
                admin_chat_id,
                status_msg_id,
                parse_mode="Markdown"
            )

            for user_id in users:
                try:
                    # EXACT FORWARD to users
                    bot.forward_message(
                        user_id,
                        source_msg.chat.id,
                        source_msg.message_id
                    )
                    users_sent += 1

                    # Update progress every 20 users
                    if users_sent % 20 == 0:
                        bot.edit_message_text(
                            f"<emoji id=6307553838073124532>✨</emoji> **📡 **ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ ᴛᴏ ᴜꜱᴇʀꜱ...**\ɴ\ɴ**"
                            f"<emoji id=6309640268761011366>🌙</emoji> **👤 ᴜꜱᴇʀꜱ: {ᴜꜱᴇʀꜱ_ꜱᴇɴᴛ}/{ʟᴇɴ(ᴜꜱᴇʀꜱ)} ꜱᴇɴᴛ**",
                            admin_chat_id,
                            status_msg_id,
                            parse_mode="Markdown"
                        )

                    time.sleep(0.2)  # Anti-flood

                except Exception as e:
                    users_failed += 1
                    logger.error(f"<emoji id=6307605493644793241>📒</emoji> **ᴜꜱᴇʀ ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜰᴀɪʟᴇᴅ ꜰᴏʀ {ᴜꜱᴇʀ_ɪᴅ}: {ᴇ}**")
                    continue

        # ----- FINAL REPORT -----
        report = (
            f"<emoji id=5352542184493031170>😈</emoji> **🎯 **ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴩʟᴇᴛᴇᴅ!**\ɴ\ɴ**"
            f"<emoji id=5280606902533783431>😽</emoji> **📊 **ɢʀᴏᴜᴩꜱ:**\ɴ**"
            f"<emoji id=6152444560216693216>🥰</emoji> **✅ ꜱᴇɴᴛ: {ɢʀᴏᴜᴩꜱ_ꜱᴇɴᴛ}\ɴ**"
            f"<emoji id=6309640268761011366>🌙</emoji> **📌 ᴩɪɴɴᴇᴅ: {ɢʀᴏᴜᴩꜱ_ᴩɪɴɴᴇᴅ}\ɴ**"
            f"<emoji id=5040016479722931047>✨</emoji> **❌ ꜰᴀɪʟᴇᴅ: {ɢʀᴏᴜᴩꜱ_ꜰᴀɪʟᴇᴅ}\ɴ**"
            f"<emoji id=6111390922044344694>✅</emoji> **👥 ᴛᴏᴛᴀʟ: {ʟᴇɴ(ɢʀᴏᴜᴩꜱ)}\ɴ\ɴ**"
        )

        if send_to_users:
            report += (
                f"<emoji id=5899776109548934640>💲</emoji> **👤 **ᴜꜱᴇʀꜱ:**\ɴ**"
                f"<emoji id=6307750079423845494>👑</emoji> **✅ ꜱᴇɴᴛ: {ᴜꜱᴇʀꜱ_ꜱᴇɴᴛ}\ɴ**"
                f"<emoji id=4929369656797431200>🪐</emoji> **❌ ꜰᴀɪʟᴇᴅ: {ᴜꜱᴇʀꜱ_ꜰᴀɪʟᴇᴅ}\ɴ**"
                f"<emoji id=6307490397111195260>🦋</emoji> **👥 ᴛᴏᴛᴀʟ: {ʟᴇɴ(ᴜꜱᴇʀꜱ)}\ɴ\ɴ**"
            )

        report += f"<emoji id=6309739370836399696>🌙</emoji> **⏰ ᴛɪᴍᴇ: {ᴅᴀᴛᴇᴛɪᴍᴇ.ɴᴏᴡ().ꜱᴛʀꜰᴛɪᴍᴇ('%ʜ:%ᴍ:%ꜱ')}**"

        bot.edit_message_text(
            report,
            admin_chat_id,
            status_msg_id,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(
            f"<emoji id=6111418418424973677>✅</emoji> **❌ **ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜰᴀɪʟᴇᴅ**\ɴ\ɴᴇʀʀᴏʀ: {ꜱᴛʀ(ᴇ)}**",
            admin_chat_id,
            status_msg_id,
            parse_mode="Markdown"
        )
        logger.error(f"<emoji id=5999210495146465994>💖</emoji> **ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴡᴏʀᴋᴇʀ ᴇʀʀᴏʀ: {ᴇ}**")

    finally:
        IS_BROADCASTING = False

# ---------------------------------------------------------------------
# OTHER FUNCTIONS
# ---------------------------------------------------------------------

def ask_refund_user(message):
    try:
        refund_user_id = int(message.text)
        msg = bot.send_message(message.chat.id, "<emoji id=4927247234283603387>🩷</emoji> **💰 ᴇɴᴛᴇʀ ʀᴇꜰᴜɴᴅ ᴀᴍᴏᴜɴᴛ:**")
        bot.register_next_step_handler(msg, process_refund, refund_user_id)
    except ValueError:
        bot.send_message(message.chat.id, "<emoji id=4929483658114368660>💎</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ɴᴜᴍᴇʀɪᴄ ɪᴅ ᴏɴʟʏ.**")

def process_refund(message, refund_user_id):
    try:
        amount = float(message.text)
        user = users_col.find_one({"user_id": refund_user_id})

        if not user:
            bot.send_message(message.chat.id, "<emoji id=6307605493644793241>📒</emoji> **⚠️ ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ.**")
            return

        add_balance(refund_user_id, amount)
        new_balance = get_balance(refund_user_id)
        bot.send_message(
            message.chat.id,
            f"<emoji id=6307569802466563145>🎶</emoji> **✅ ʀᴇꜰᴜɴᴅᴇᴅ {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)} ᴛᴏ ᴜꜱᴇʀ {ʀᴇꜰᴜɴᴅ_ᴜꜱᴇʀ_ɪᴅ}\ɴ**"
            f"<emoji id=6309985824649780135>🌙</emoji> **💰 ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɴᴇᴡ_ʙᴀʟᴀɴᴄᴇ)}**"
        )

        try:
            bot.send_message(
                refund_user_id,
                f"<emoji id=5318828550940293906>🐱</emoji> **💸 {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)} ʀᴇꜰᴜɴᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴡᴀʟʟᴇᴛ!\ɴ**"
                f"<emoji id=5354924568492383911>😈</emoji> **💰 ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɴᴇᴡ_ʙᴀʟᴀɴᴄᴇ)} ✅**"
            )
        except Exception:
            bot.send_message(message.chat.id, "<emoji id=5285100774060227768>😽</emoji> **⚠️ ᴄᴏᴜʟᴅ ɴᴏᴛ ᴅᴍ ᴛʜᴇ ᴜꜱᴇʀ (ᴍᴀʏʙᴇ ʙʟᴏᴄᴋᴇᴅ).**")
    except ValueError:
        bot.send_message(message.chat.id, "<emoji id=6307643744623531146>🦋</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ ᴇɴᴛᴇʀᴇᴅ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ɴᴜᴍʙᴇʀ.**")
    except Exception as e:
        logger.exception("<emoji id=6307569802466563145>🎶</emoji> **ᴇʀʀᴏʀ ɪɴ ᴩʀᴏᴄᴇꜱꜱ_ʀᴇꜰᴜɴᴅ:**")
        bot.send_message(message.chat.id, f"<emoji id=6111418418424973677>✅</emoji> **ᴇʀʀᴏʀ ᴩʀᴏᴄᴇꜱꜱɪɴɢ ʀᴇꜰᴜɴᴅ: {ᴇ}**")

def ask_message_content(msg):
    try:
        target_user_id = int(msg.text)
        user_exists = users_col.find_one({"user_id": target_user_id})
        if not user_exists:
            bot.send_message(msg.chat.id, "<emoji id=5999270482954691955>🦋</emoji> **❌ ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ.**")
            return

        bot.send_message(msg.chat.id, f"<emoji id=6151981777490548710>✅</emoji> **💬 ɴᴏᴡ ꜱᴇɴᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ (ᴛᴇxᴛ, ᴩʜᴏᴛᴏ, ᴠɪᴅᴇᴏ, ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ) ꜰᴏʀ ᴜꜱᴇʀ {ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}:**")
        bot.register_next_step_handler(msg, process_user_message, target_user_id)
    except ValueError:
        bot.send_message(msg.chat.id, "<emoji id=4929483658114368660>💎</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ. ᴩʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ɴᴜᴍᴇʀɪᴄ ɪᴅ ᴏɴʟʏ.**")

def process_user_message(msg, target_user_id):
    try:
        text = getattr(msg, "text", None) or getattr(msg, "caption", "") or ""
        is_photo = bool(getattr(msg, "photo", None))
        is_video = getattr(msg, "video", None) is not None
        is_document = getattr(msg, "document", None) is not None

        try:
            if is_photo and getattr(msg, "photo", None):
                bot.send_photo(target_user_id, photo=msg.photo[-1].file_id, caption=text or "")
            elif is_video and getattr(msg, "video", None):
                bot.send_video(target_user_id, video=msg.video.file_id, caption=text or "")
            elif is_document and getattr(msg, "document", None):
                bot.send_document(target_user_id, document=msg.document.file_id, caption=text or "")
            else:
                bot.send_message(target_user_id, f"<emoji id=5281001756057175314>😽</emoji> **💌 ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ᴀᴅᴍɪɴ:\ɴ{ᴛᴇxᴛ}**")
            bot.send_message(msg.chat.id, f"<emoji id=6111742817304841054>✅</emoji> **✅ ᴍᴇꜱꜱᴀɢᴇ ꜱᴇɴᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴛᴏ ᴜꜱᴇʀ {ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}**")
        except Exception as e:
            bot.send_message(msg.chat.id, f"<emoji id=6307553838073124532>✨</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴜꜱᴇʀ {ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}. ᴜꜱᴇʀ ᴍᴀʏ ʜᴀᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ.**")
    except Exception as e:
        logger.exception("<emoji id=6151981777490548710>✅</emoji> **ᴇʀʀᴏʀ ɪɴ ᴩʀᴏᴄᴇꜱꜱ_ᴜꜱᴇʀ_ᴍᴇꜱꜱᴀɢᴇ:**")
        bot.send_message(msg.chat.id, f"<emoji id=5899776109548934640>💲</emoji> **ᴇʀʀᴏʀ ꜱᴇɴᴅɪɴɢ ᴍᴇꜱꜱᴀɢᴇ: {ᴇ}**")

# ---------------------------------------------------------------------
# COUNTRY SELECTION FUNCTIONS
# ---------------------------------------------------------------------

def show_countries(chat_id):
    if not has_user_joined_channels(chat_id):
        start(bot.send_message(chat_id, "<emoji id=6111418418424973677>✅</emoji> **/ꜱᴛᴀʀᴛ**"))
        return

    countries = get_all_countries()
    if not countries:
        text = "<emoji id=6001132493011425597>💖</emoji> **🌍 **ꜱᴇʟᴇᴄᴛ ᴄᴏᴜɴᴛʀʏ**\ɴ\ɴ❌ ɴᴏ ᴄᴏᴜɴᴛʀɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ʀɪɢʜᴛ ɴᴏᴡ. ᴩʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʙᴀᴄᴋ ʟᴀᴛᴇʀ.**"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("<emoji id=6111742817304841054>✅</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="back_to_menu"))

        sent_msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
        user_last_message[chat_id] = sent_msg.message_id
        return

    text = "<emoji id=6111418418424973677>✅</emoji> **🌍 **ꜱᴇʟᴇᴄᴛ ᴄᴏᴜɴᴛʀʏ**\ɴ\ɴᴄʜᴏᴏꜱᴇ ʏᴏᴜʀ ᴄᴏᴜɴᴛʀʏ:**"
    markup = InlineKeyboardMarkup(row_width=2)

    row = []
    for i, country in enumerate(countries):
        row.append(InlineKeyboardButton(
            country['name'],
            callback_data=f"<emoji id=6001132493011425597>💖</emoji> **ᴄᴏᴜɴᴛʀʏ_ʀᴀᴡ_{ᴄᴏᴜɴᴛʀʏ['ɴᴀᴍᴇ']}**"
        ))
        if len(row) == 2:
            markup.add(*row)
            row = []

    if row:
        markup.add(*row)

    markup.add(InlineKeyboardButton("<emoji id=6307643744623531146>🦋</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="back_to_menu"))

    sent_msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    user_last_message[chat_id] = sent_msg.message_id

def show_country_details(user_id, country_name, chat_id, message_id, callback_id):
    try:
        country = get_country_by_name(country_name)
        if not country:
            bot.answer_callback_query(callback_id, "<emoji id=6307490397111195260>🦋</emoji> **❌ ᴄᴏᴜɴᴛʀʏ ɴᴏᴛ ꜰᴏᴜɴᴅ**", show_alert=True)
            return

        accounts_count = get_available_accounts_count(country_name)

        # WITH EXPANDABLE BLOCKQUOTE - UI STYLE
        text = f"""⚡ <b>Telegram Account Info</b>

<blockquote>🌍 Country : {country_name}
💸 Price : {format_currency(country['price'])}
📦 Available : {accounts_count}

🔍 Reliable | Affordable | Good Quality

⚠️ Use Telegram X only to login.
🚫 Not responsible for freeze / ban.</blockquote>"""

        markup = InlineKeyboardMarkup(row_width=2)

        if accounts_count > 0:
            accounts = list(accounts_col.find({
                "country": country_name,
                "status": "active",
                "used": False
            }))
            markup.add(InlineKeyboardButton(
                "<emoji id=6111390922044344694>✅</emoji> **🛒 ʙᴜʏ ᴀᴄᴄᴏᴜɴᴛ**",
                callback_data=f"<emoji id=6307821174017496029>🔥</emoji> **ʙᴜʏ_{ᴀᴄᴄᴏᴜɴᴛꜱ[0]['_ɪᴅ']}**" if accounts else "out_of_stock"
            ))
        else:
            markup.add(InlineKeyboardButton(
                "<emoji id=6309640268761011366>🌙</emoji> **🛒 ʙᴜʏ ᴀᴄᴄᴏᴜɴᴛ**",
                callback_data="out_of_stock"
            ))

        markup.add(InlineKeyboardButton("<emoji id=5352542184493031170>😈</emoji> **⬅️ ʙᴀᴄᴋ**", callback_data="back_to_countries"))

        edit_or_resend(
            chat_id,
            message_id,
            text,
            markup=markup,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"<emoji id=4927247234283603387>🩷</emoji> **ᴄᴏᴜɴᴛʀʏ ᴅᴇᴛᴀɪʟꜱ ᴇʀʀᴏʀ: {ᴇ}**")
        bot.answer_callback_query(callback_id, "<emoji id=5999270482954691955>🦋</emoji> **❌ ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴄᴏᴜɴᴛʀʏ ᴅᴇᴛᴀɪʟꜱ**", show_alert=True)

# ---------------------------------------------------------------------
# PROCESS PURCHASE FUNCTION
# ---------------------------------------------------------------------

def process_purchase(user_id, account_id, chat_id, message_id, callback_id):
    try:
        try:
            account = accounts_col.find_one({"_id": ObjectId(account_id)})
        except Exception:
            account = accounts_col.find_one({"_id": account_id})

        if not account:
            bot.answer_callback_query(callback_id, "<emoji id=5280904324724063665>😽</emoji> **❌ ᴀᴄᴄᴏᴜɴᴛ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ**", show_alert=True)
            return

        if account.get('used', False):
            bot.answer_callback_query(callback_id, "<emoji id=5285100774060227768>😽</emoji> **❌ ᴀᴄᴄᴏᴜɴᴛ ᴀʟʀᴇᴀᴅʏ ꜱᴏʟᴅ ᴏᴜᴛ**", show_alert=True)
            try:
                bot.delete_message(chat_id, message_id)
            except:
                pass
            show_countries(chat_id)
            return

        country = get_country_by_name(account['country'])
        if not country:
            bot.answer_callback_query(callback_id, "<emoji id=6310044717241340733>🔄</emoji> **❌ ᴄᴏᴜɴᴛʀʏ ɴᴏᴛ ꜰᴏᴜɴᴅ**", show_alert=True)
            return

        price = country['price']
        balance = get_balance(user_id)

        if balance < price:
            needed = price - balance
            bot.answer_callback_query(
                callback_id,
                f"<emoji id=5998977626314643141>🦋</emoji> **❌ ɪɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ ʙᴀʟᴀɴᴄᴇ!\ɴɴᴇᴇᴅ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴩʀɪᴄᴇ)}\ɴʜᴀᴠᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ʙᴀʟᴀɴᴄᴇ)}\ɴʀᴇꞯᴜɪʀᴇᴅ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɴᴇᴇᴅᴇᴅ)} ᴍᴏʀᴇ**",
                show_alert=True
            )
            return

        deduct_balance(user_id, price)

        try:
            from logs import log_purchase_async
            log_purchase_async(
                user_id=user_id,
                country=account['country'],
                price=price,
                phone=account.get('phone', 'N/A')
            )
        except:
            pass

        session_id = f"<emoji id=6309819721084573392>🌙</emoji> **ᴏᴛᴩ_{ᴜꜱᴇʀ_ɪᴅ}_{ɪɴᴛ(ᴛɪᴍᴇ.ᴛɪᴍᴇ())}**"
        otp_session = {
            "session_id": session_id,
            "user_id": user_id,
            "phone": account['phone'],
            "session_string": account.get('session_string', ''),
            "status": "active",
            "created_at": datetime.utcnow(),
            "account_id": str(account['_id']),
            "has_otp": False,
            "last_otp": None,
            "last_otp_time": None
        }
        otp_sessions_col.insert_one(otp_session)

        order = {
            "user_id": user_id,
            "account_id": str(account.get('_id')),
            "country": account['country'],
            "price": price,
            "phone_number": account.get('phone', 'N/A'),
            "session_id": session_id,
            "status": "waiting_otp",
            "created_at": datetime.utcnow(),
            "monitoring_duration": 1800
        }
        order_id = orders_col.insert_one(order).inserted_id

        try:
            accounts_col.update_one(
                {"_id": account.get('_id')},
                {"<emoji id=5235985147265837746>🗒</emoji> **$ꜱᴇᴛ**": {"used": True, "used_at": datetime.utcnow()}}
            )
        except Exception:
            accounts_col.update_one(
                {"_id": ObjectId(account_id)},
                {"<emoji id=4926993814033269936>🖕</emoji> **$ꜱᴇᴛ**": {"used": True, "used_at": datetime.utcnow()}}
            )

        def start_simple_monitoring():
            try:
                account_manager.start_simple_monitoring_sync(
                    account.get('session_string', ''),
                    session_id,
                    1800
                )
            except Exception as e:
                logger.error(f"<emoji id=5999210495146465994>💖</emoji> **ꜱɪᴍᴩʟᴇ ᴍᴏɴɪᴛᴏʀɪɴɢ ᴇʀʀᴏʀ: {ᴇ}**")

        thread = threading.Thread(target=start_simple_monitoring, daemon=True)
        thread.start()

        account_details = f"""✅ **Purchase Successful!** 

🌍 Country: {account['country']}
💸 Price: {format_currency(price)}
📱 Phone Number: {account.get('phone', 'N/A')}"""

        if account.get('two_step_password'):
            account_details += f"<emoji id=6151981777490548710>✅</emoji> **\ɴ🔒 2ꜰᴀ ᴩᴀꜱꜱᴡᴏʀᴅ: `{ᴀᴄᴄᴏᴜɴᴛ.ɢᴇᴛ('ᴛᴡᴏ_ꜱᴛᴇᴩ_ᴩᴀꜱꜱᴡᴏʀᴅ', 'ɴ/ᴀ')}`**"

        account_details += f"<emoji id=6309985824649780135>🌙</emoji> **\ɴ\ɴ📲 **ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ:**\ɴ**"
        account_details += f"<emoji id=5999151980512024620>🥰</emoji> **1. ᴏᴩᴇɴ ᴛᴇʟᴇɢʀᴀᴍ x ᴀᴩᴩ\ɴ**"
        account_details += f"<emoji id=6111742817304841054>✅</emoji> **2. ᴇɴᴛᴇʀ ᴩʜᴏɴᴇ ɴᴜᴍʙᴇʀ: `{ᴀᴄᴄᴏᴜɴᴛ.ɢᴇᴛ('ᴩʜᴏɴᴇ', 'ɴ/ᴀ')}`\ɴ**"
        account_details += f"<emoji id=5318828550940293906>🐱</emoji> **3. ᴄʟɪᴄᴋ 'ɴᴇxᴛ'\ɴ**"
        account_details += f"<emoji id=6310022800023229454>✡️</emoji> **4. **ᴄʟɪᴄᴋ 'ɢᴇᴛ ᴏᴛᴩ' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴡʜᴇɴ ʏᴏᴜ ɴᴇᴇᴅ ᴏᴛᴩ**\ɴ\ɴ**"
        account_details += f"<emoji id=6123040393769521180>☄️</emoji> **⏳ ᴏᴛᴩ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ 30 ᴍɪɴᴜᴛᴇꜱ**"

        get_otp_markup = InlineKeyboardMarkup()
        get_otp_markup.add(InlineKeyboardButton("<emoji id=6001589602085771497>✅</emoji> **🔢 ɢᴇᴛ ᴏᴛᴩ**", callback_data=f"<emoji id=6001589602085771497>✅</emoji> **ɢᴇᴛ_ᴏᴛᴩ_{ꜱᴇꜱꜱɪᴏɴ_ɪᴅ}**"))

        account_details += f"<emoji id=6123125485661591081>🩷</emoji> **\ɴ💰 ʀᴇᴍᴀɪɴɪɴɢ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɢᴇᴛ_ʙᴀʟᴀɴᴄᴇ(ᴜꜱᴇʀ_ɪᴅ))}**"

        sent_msg = edit_or_resend(
            chat_id,
            message_id,
            account_details,
            markup=get_otp_markup,
            parse_mode="Markdown"
        )

        if sent_msg:
            user_last_message[user_id] = sent_msg.message_id

        bot.answer_callback_query(callback_id, "<emoji id=5280904324724063665>😽</emoji> **✅ ᴩᴜʀᴄʜᴀꜱᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ! ᴄʟɪᴄᴋ ɢᴇᴛ ᴏᴛᴩ ᴡʜᴇɴ ɴᴇᴇᴅᴇᴅ.**", show_alert=True)

    except Exception as e:
        logger.error(f"<emoji id=5285100774060227768>😽</emoji> **ᴩᴜʀᴄʜᴀꜱᴇ ᴇʀʀᴏʀ: {ᴇ}**")
        try:
            bot.answer_callback_query(callback_id, "<emoji id=6309739370836399696>🌙</emoji> **❌ ᴩᴜʀᴄʜᴀꜱᴇ ꜰᴀɪʟᴇᴅ**", show_alert=True)
        except:
            pass

# =============================================================
# RESTART COMMAND (VPS + HEROKU SAFE)
# =============================================================

@bot.message_handler(commands=['restart'])
def restart_bot(message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        bot.reply_to(message, "<emoji id=6152142357727811958>🦋</emoji> **❌ ꜱɪʀꜰ ᴀᴅᴍɪɴ ᴜꜱᴇ ᴋᴀʀ ꜱᴀᴋᴛᴀ ʜᴀɪ!**")
        return

    bot.reply_to(message, "<emoji id=5998881015320287132>💊</emoji> **♻️ ʀᴇꜱᴛᴀʀᴛɪɴɢ ʙᴏᴛ...**")

    logger.info(f"<emoji id=6307821174017496029>🔥</emoji> **ᴀᴅᴍɪɴ {ᴜꜱᴇʀ_ɪᴅ} ᴛʀɪɢɢᴇʀᴇᴅ ʀᴇꜱᴛᴀʀᴛ**")

    time.sleep(1)

    # Clean restart
    os.execv(sys.executable, ['python'] + sys.argv)

# ---------------------------------------------------------------------
# MESSAGE HANDLER FOR ADMIN DEDUCT
# ---------------------------------------------------------------------

@bot.message_handler(func=lambda m: True, content_types=['text','photo','video','document'])
def chat_handler(msg):
    user_id = msg.from_user.id

    # Check if user is in admin add flow
    if user_id in admin_add_state:
        handle_add_admin_userid(msg)
        return

    # Check if user is in admin remove flow
    if user_id in admin_remove_state:
        handle_remove_admin_userid(msg)
        return

    if user_id == ADMIN_ID and user_id in admin_deduct_state:
        pass

    if is_user_banned(user_id):
        return

    ensure_user_exists(
        user_id,
        msg.from_user.first_name or "Unknown",
        msg.from_user.username
    )

    if (
        msg.text and msg.text.startswith('/') and
        not (user_id == ADMIN_ID and user_id in admin_deduct_state)
    ):
        return

    if user_id == ADMIN_ID and user_id in admin_deduct_state:
        state = admin_deduct_state[user_id]

        if state["step"] == "ask_user_id":
            try:
                target_user_id = int(msg.text.strip())
                user_exists = users_col.find_one({"user_id": target_user_id})
                if not user_exists:
                    bot.send_message(ADMIN_ID, "<emoji id=5235985147265837746>🗒</emoji> **❌ ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ. ᴇɴᴛᴇʀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ:**")
                    return

                current_balance = get_balance(target_user_id)
                admin_deduct_state[user_id] = {
                    "step": "ask_amount",
                    "target_user_id": target_user_id,
                    "current_balance": current_balance
                }
                bot.send_message(
                    ADMIN_ID,
                    f"<emoji id=6001589602085771497>✅</emoji> **👤 ᴜꜱᴇʀ ɪᴅ: {ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}\ɴ**"
                    f"<emoji id=5040016479722931047>✨</emoji> **💰 ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴜʀʀᴇɴᴛ_ʙᴀʟᴀɴᴄᴇ)}\ɴ\ɴ**"
                    f"<emoji id=5041955142060999726>🌈</emoji> **💸 ᴇɴᴛᴇʀ ᴀᴍᴏᴜɴᴛ ᴛᴏ ᴅᴇᴅᴜᴄᴛ:**"
                )
                return
            except ValueError:
                bot.send_message(ADMIN_ID, "<emoji id=5318828550940293906>🐱</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ. ᴇɴᴛᴇʀ ɴᴜᴍᴇʀɪᴄ ɪᴅ:**")
                return

        elif state["step"] == "ask_amount":
            try:
                amount = float(msg.text.strip())
                current_balance = state["current_balance"]
                if amount <= 0:
                    bot.send_message(ADMIN_ID, "<emoji id=5280904324724063665>😽</emoji> **❌ ᴀᴍᴏᴜɴᴛ ᴍᴜꜱᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 0:**")
                    return
                if amount > current_balance:
                    bot.send_message(
                        ADMIN_ID,
                        f"<emoji id=6309819721084573392>🌙</emoji> **❌ ᴀᴍᴏᴜɴᴛ ᴇxᴄᴇᴇᴅꜱ ʙᴀʟᴀɴᴄᴇ ({ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴄᴜʀʀᴇɴᴛ_ʙᴀʟᴀɴᴄᴇ)}):**"
                    )
                    return

                admin_deduct_state[user_id] = {
                    "step": "ask_reason",
                    "target_user_id": state["target_user_id"],
                    "amount": amount,
                    "current_balance": current_balance
                }
                bot.send_message(ADMIN_ID, "<emoji id=5318828550940293906>🐱</emoji> **📝 ᴇɴᴛᴇʀ ʀᴇᴀꜱᴏɴ ꜰᴏʀ ᴅᴇᴅᴜᴄᴛɪᴏɴ:**")
                return
            except ValueError:
                bot.send_message(ADMIN_ID, "<emoji id=6298717844804733009>♾</emoji> **❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ. ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ:**")
                return

        elif state["step"] == "ask_reason":
            reason = msg.text.strip()
            if not reason:
                bot.send_message(ADMIN_ID, "<emoji id=6309985824649780135>🌙</emoji> **❌ ʀᴇᴀꜱᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴇᴍᴩᴛʏ:**")
                return

            target_user_id = state["target_user_id"]
            amount = state["amount"]
            old_balance = state["current_balance"]

            deduct_balance(target_user_id, amount)
            new_balance = get_balance(target_user_id)

            transaction_id = f"<emoji id=5281001756057175314>😽</emoji> **ᴅᴇᴅᴜᴄᴛ{ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}{ɪɴᴛ(ᴛɪᴍᴇ.ᴛɪᴍᴇ())}**"
            if 'deductions' not in db.list_collection_names():
                db.create_collection('deductions')
            db['deductions'].insert_one({
                "transaction_id": transaction_id,
                "user_id": target_user_id,
                "amount": amount,
                "reason": reason,
                "admin_id": user_id,
                "old_balance": old_balance,
                "new_balance": new_balance,
                "timestamp": datetime.utcnow()
            })

            bot.send_message(
                ADMIN_ID,
                f"<emoji id=6001132493011425597>💖</emoji> **✅ ʙᴀʟᴀɴᴄᴇ ᴅᴇᴅᴜᴄᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ\ɴ\ɴ**"
                f"<emoji id=5040016479722931047>✨</emoji> **👤 ᴜꜱᴇʀ: {ᴛᴀʀɢᴇᴛ_ᴜꜱᴇʀ_ɪᴅ}\ɴ**"
                f"<emoji id=5280678521113443426>😽</emoji> **💰 ᴀᴍᴏᴜɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
                f"<emoji id=6152444560216693216>🥰</emoji> **📝 ʀᴇᴀꜱᴏɴ: {ʀᴇᴀꜱᴏɴ}\ɴ**"
                f"<emoji id=6001589602085771497>✅</emoji> **📉 ᴏʟᴅ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴏʟᴅ_ʙᴀʟᴀɴᴄᴇ)}\ɴ**"
                f"<emoji id=6307490397111195260>🦋</emoji> **📈 ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɴᴇᴡ_ʙᴀʟᴀɴᴄᴇ)}\ɴ**"
                f"<emoji id=5899776109548934640>💲</emoji> **🆔 ᴛxɴ ɪᴅ: {ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ_ɪᴅ}**"
            )

            try:
                bot.send_message(
                    target_user_id,
                    f"<emoji id=6111742817304841054>✅</emoji> **⚠️ ʙᴀʟᴀɴᴄᴇ ᴅᴇᴅᴜᴄᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ\ɴ\ɴ**"
                    f"<emoji id=6309666601205503867>💌</emoji> **💰 ᴀᴍᴏᴜɴᴛ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ᴀᴍᴏᴜɴᴛ)}\ɴ**"
                    f"<emoji id=5235985147265837746>🗒</emoji> **📝 ʀᴇᴀꜱᴏɴ: {ʀᴇᴀꜱᴏɴ}\ɴ**"
                    f"<emoji id=6307643744623531146>🦋</emoji> **📈 ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: {ꜰᴏʀᴍᴀᴛ_ᴄᴜʀʀᴇɴᴄʏ(ɴᴇᴡ_ʙᴀʟᴀɴᴄᴇ)}\ɴ**"
                    f"<emoji id=5235985147265837746>🗒</emoji> **🆔 ᴛxɴ ɪᴅ: {ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ_ɪᴅ}**"
                )
            except:
                bot.send_message(ADMIN_ID, "<emoji id=6001589602085771497>✅</emoji> **⚠️ ᴜꜱᴇʀ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ ꜰᴀɪʟᴇᴅ (ᴍᴀʏʙᴇ ʙʟᴏᴄᴋᴇᴅ)**")

            del admin_deduct_state[user_id]
            return

    if msg.chat.type == "private":
        bot.send_message(
            user_id,
            "<emoji id=6307821174017496029>🔥</emoji> **⚠️ ᴩʟᴇᴀꜱᴇ ᴜꜱᴇ /ꜱᴛᴀʀᴛ ᴏʀ ʙᴜᴛᴛᴏɴꜱ ꜰʀᴏᴍ ᴛʜᴇ ᴍᴇɴᴜ.**"
        )

# ---------------------------------------------------------------------
# RUN BOT
# ---------------------------------------------------------------------

if __name__ == "__main__":
    logger.info(f"<emoji id=5280904324724063665>😽</emoji> **🤖 ꜰɪxᴇᴅ ᴏᴛᴩ ʙᴏᴛ ꜱᴛᴀʀᴛɪɴɢ...**")
    logger.info(f"<emoji id=5999340396432333728>☺️</emoji> **ᴀᴅᴍɪɴ ɪᴅ: {ᴀᴅᴍɪɴ_ɪᴅ}**")
    logger.info(f"<emoji id=5999151980512024620>🥰</emoji> **ʙᴏᴛ ᴛᴏᴋᴇɴ: {ʙᴏᴛ_ᴛᴏᴋᴇɴ[:10]}...**")
    logger.info(f"<emoji id=6111390922044344694>✅</emoji> **ɢʟᴏʙᴀʟ ᴀᴩɪ ɪᴅ: {ɢʟᴏʙᴀʟ_ᴀᴩɪ_ɪᴅ}**")
    logger.info(f"<emoji id=6123125485661591081>🩷</emoji> **ɢʟᴏʙᴀʟ ᴀᴩɪ ʜᴀꜱʜ: {ɢʟᴏʙᴀʟ_ᴀᴩɪ_ʜᴀꜱʜ[:10]}...**")
    logger.info(f"<emoji id=6307447640711763730>💟</emoji> **ʀᴇꜰᴇʀʀᴀʟ ᴄᴏᴍᴍɪꜱꜱɪᴏɴ: {ʀᴇꜰᴇʀʀᴀʟ_ᴄᴏᴍᴍɪꜱꜱɪᴏɴ}%**")
    logger.info(f"<emoji id=6307568836098922002>🌙</emoji> **ᴍᴜꜱᴛ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 1: {ᴍᴜꜱᴛ_ᴊᴏɪɴ_ᴄʜᴀɴɴᴇʟ_1}**")
    logger.info(f"<emoji id=5352870513267973607>✨</emoji> **ᴍᴜꜱᴛ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 2: {ᴍᴜꜱᴛ_ᴊᴏɪɴ_ᴄʜᴀɴɴᴇʟ_2}**")
    logger.info(f"<emoji id=5280678521113443426>😽</emoji> **ʟᴏɢ ᴄʜᴀɴɴᴇʟ ɪᴅ: {ʟᴏɢ_ᴄʜᴀɴɴᴇʟ_ɪᴅ}**")

    try:
        coupons_col.create_index([("coupon_code", 1)], unique=True)
        coupons_col.create_index([("status", 1)])
        coupons_col.create_index([("created_at", -1)])
        logger.info("<emoji id=6307490397111195260>🦋</emoji> **✅ ᴄᴏᴜᴩᴏɴ ɪɴᴅᴇxᴇꜱ ᴄʀᴇᴀᴛᴇᴅ**")
    except Exception as e:
        logger.error(f"<emoji id=6307569802466563145>🎶</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴄᴏᴜᴩᴏɴ ɪɴᴅᴇxᴇꜱ: {ᴇ}**")

    try:
        admins_col.create_index([("user_id", 1)], unique=True)
        logger.info("<emoji id=6309640268761011366>🌙</emoji> **✅ ᴀᴅᴍɪɴ ɪɴᴅᴇxᴇꜱ ᴄʀᴇᴀᴛᴇᴅ**")
    except Exception as e:
        logger.error(f"<emoji id=6298684666182371615>❤️</emoji> **❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀᴅᴍɪɴ ɪɴᴅᴇxᴇꜱ: {ᴇ}**")

    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        logger.error(f"<emoji id=6154635934135490309>💗</emoji> **ʙᴏᴛ ᴇʀʀᴏʀ: {ᴇ}**")
        time.sleep(30)
        bot.infinity_polling(timeout=60, long_polling_timeout=60)