import os
import asyncio
import aiohttp
import datetime
import pytz
import nest_asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ========= CONFIG =========
BOT_TOKEN = os.getenv('BOT_TOKEN') # Render se aayega
OWNER_ID = 6267722480 # 👑 Owner ID @ZEERYXFFF
ADMIN_IDS = [6267722480] # 👑 Admin IDs
ALLOWED_GROUPS = [-1003472819157] # ✅ Groups jahan bot chalega
ALLOWED_USERS = [6267722480] # ✅ Specific users
DEFAULT_GROUP_ID = -1003912214612 # Main group ID jahan daily report jayegi
DEVELOPER_TAG = "@ZEERYXFF" # ⚡ Owner tag
DEFAULT_API_URL = "https://starstaradmin.vercel.app/like"

# ========= STATE =========
VIP_USERS = {} # tg_id -> set of uids
autolike_tasks = [] # [{uid, region, days, remaining, group_id, user_notify_id, added_by}]
tasks_lock = asyncio.Lock()
custom_time = {"hour": 4, "minute": 0} # Default: 4:00 AM IST
MAINTENANCE_MODE = False
USERNAME_CACHE

# ========= LOGGING ==========
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("AutoLikeBot")

# ========= HELPERS ==========
def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def is_allowed_user(user_id: int) -> bool:
    return user_id in ALLOWED_USERS or is_admin(user_id) or is_owner(user_id)

async def is_allowed_chat(update: Update) -> bool:
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    if chat_type == "private":
        return is_allowed_user(update.effective_user.id)
    return chat_id in ALLOWED_GROUPS

def restrict_access():
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if MAINTENANCE_MODE and not is_admin(update.effective_user.id):
                maintenance_msg = (
                    "🔧 <b>Bot is under maintenance!</b>\n\n"
                    "We're currently performing some updates.\n"
                    "Please try again later.\n\n"
                    f"Contact: {DEVELOPER_TAG}\n"
                    "✨━━━━━━━━━━━━━━━✨"
                )
                return await update.message.reply_text(maintenance_msg, parse_mode="HTML")

            if not await is_allowed_chat(update):
                not_allowed_msg = (
                    "🚫 <b>Access Denied!</b>\n\n"
                    "This bot can only be used by owner.\n"
                    f"Contact {DEVELOPER_TAG} for access.\n"
                    "✨━━━━━━━━━━━━━━━✨"
                )
                return await update.message.reply_text(not_allowed_msg, parse_mode="HTML")
            return await func(update, context)
        return wrapper
    return decorator

def owner_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not is_owner(update.effective_user.id):
            return await update.message.reply_text("⛔ Only owner can use this command!")
        return await func(update, context)
    return wrapper

def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not is_admin(update.effective_user.id):
            return await update.message.reply_text("⛔ You are not authorized!")
        return await func(update, context)
    return wrapper

async def get_username(update: Update) -> str:
    user = update.effective_user
    if user.username:
        username = f"@{user.username}"
    elif user.first_name:
        username = user.first_name
    else:
        username = f"User_{user.id}"
    USERNAME_CACHE[user.id] = username
    return username

def get_username_from_id(user_id: int) -> str:
    if user_id in USERNAME_CACHE:
        return USERNAME_CACHE[user_id]
    return f"User_{user_id}"

def next_run_time(hour: int, minute: int):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= next_run:
        next_run += datetime.timedelta(days=1)
    return next_run, round((next_run - now).total_seconds() / 3600, 1)

def format_schedule_message():
    next_run, hours_wait = next_run_time(custom_time["hour"], custom_time["minute"])
    total_entries = len(autolike_tasks)
    return (
        "✨━━━━━━━━━━━━━━━✨\n"
        "⏰ <b>Next Auto-Like Batch</b>\n"
        f"📅 <b>{next_run.strftime('%d %B %Y %I:%M %p IST')}</b>\n"
        f"⏳ Waiting <b>{hours_wait} hours</b>\n"
        f"📊 Total entries now: <b>{total_entries}</b>\n"
        "✨━━━━━━━━━━━━━━━✨"
    )

# ========= API CALL ==========
async def send_like_request(uid: str, region: str):
    url = f"{DEFAULT_API_URL}?uid={uid}&server_name={region}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "success": True,
                        "likes_given": int(data.get("LikesGivenByAPI", data.get("likesGivenByAPI", 0))),
                        "player": data.get("PlayerNickname", data.get("nickname", "Unknown")),
                        "level": data.get("PlayerLevel", data.get("level", "N/A")),
                        "before": data.get("LikesbeforeCommand", data.get("likesBefore", 0)),
                        "after": data.get("LikesafterCommand", data.get("likesAfter", 0))
                    }
                else:
                    return {"success": False, "error": f"HTTP {resp.status}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========= DAILY TASK ==========
async def daily_autolike_task(application):
    tz = pytz.timezone("Asia/Kolkata")
    while True:
        now = datetime.datetime.now(tz)
        target = now.replace(hour=custom_time["hour"], minute=custom_time["minute"], second=0, microsecond=0)
        if now >= target:
            target += datetime.timedelta(days=1)

        wait_seconds = (target - now).total_seconds()
        log.info(f"Next auto-like run in {wait_seconds/3600:.1f} hours")
        await asyncio.sleep(wait_seconds)

        async with tasks_lock:
            tasks_to_run = autolike_tasks.copy()

        if not tasks_to_run:
            continue

        report = "🌅 <b>DAILY AUTO-LIKE REPORT</b>\n"
        report += f"⏰ {datetime.datetime.now(tz).strftime('%d %b %Y %I:%M %p IST')}\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        success_count = 0
        fail_count = 0

        for task in tasks_to_run:
            uid = task["uid"]
            region = task["region"]
            result = await send_like_request(uid, region)

            if result["success"]:
                success_count += 1
                likes = result["likes_given"]
                report += (
                    f"✅ <b>{result['player']}</b>\n"
                    f"🆔 UID: <code>{uid}</code> | 🌍 {region}\n"
                    f"❤️ Likes: {result['before']} → {result['after']} (+{likes})\n"
                    f"📅 Left: {task['remaining']-1} days\n\n"
                )
            else:
                fail_count += 1
                report += (
                    f"❌ <b>UID: {uid}</b> | 🌍 {region}\n"
                    f"Error: {result['error']}\n"
                    f"📅 Left: {task['remaining']-1} days\n\n"
                )

            task["remaining"] -= 1
            await asyncio.sleep(2) # Delay to avoid spam

        report += "━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += f"✅ Success: {success_count} | ❌ Failed: {fail_count}\n"
        report += f"⚡ Powered by {DEVELOPER_TAG}"

        # Send to group
        try:
            await application.bot.send_message(chat_id=DEFAULT_GROUP_ID, text=report, parse_mode="HTML")
        except Exception as e:
            log.error(f"Failed to send group report: {e}")

        # Remove expired tasks
        async with tasks_lock:
            autolike_tasks[:] = [t for t in autolike_tasks if t["remaining"] > 0]

# ========= COMMANDS ==========
@restrict_access()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = await get_username(update)
    role = "👑 Owner" if is_owner(user.id) else "⚡ Admin" if is_admin(user.id) else ""

    welcome_text = (
        "✨━━━━━━━━━━━━━━━✨\n"
        "🎉 <b>ZEERYX AUTO-LIKE BOT</b> 🎉\n"
        "✨━━━━━━━━━━━━━━━✨\n\n"
        f"Hello, <b>{user.first_name}</b>! 👋\n"
        f"Username: {username}\n"
        f"User ID: <code>{user.id}</code>\n"
        f"{role}\n\n"
        f"Daily auto-likes at {custom_time['hour']:02d}:{custom_time['minute']:02d} AM IST\n\n"
        "💰 <b>PRICING</b>:\n"
        "• 60 Rs - 30 days\n"
        "• 120 Rs - 60 days\n"
        "• 180 Rs - 90 days\n"
        "• 240 Rs - 120 days\n\n"
        f"📞 <b>Contact:</b> {DEVELOPER_TAG}\n"
        "✨━━━━━━━━━━━━━━━✨"
    )
    keyboard = [[InlineKeyboardButton("📢 Updates", url="https://t.me/zeeryxff")]]
    await update.message.reply_text(welcome_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

@owner_only
async def autolike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        return await update.message.reply_text("⚙️ Usage: /autolike <region> <uid1> <uid2>... <days>")

    region = context.args[0]
    *uids, days_str = context.args[1:]
    try:
        days = int(days_str)
    except ValueError:
        return await update.message.reply_text("⚠️ <days> must be numeric.")

    added_by = update.effective_user.id
    added_by_name = get_username_from_id(added_by)
    group_id = DEFAULT_GROUP_ID

    async with tasks_lock:
        for uid in uids:
            if any(t["uid"] == str(uid) for t in autolike_tasks):
                await update.message.reply_text(f"🚫 UID {uid} already active.")
                continue
            task = {
                "region": region,
                "uid": str(uid),
                "days": days,
                "remaining": days,
                "group_id": group_id,
                "user_notify_id": added_by,
                "added_by": added_by,
                "added_by_name": added_by_name,
                "added_date": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            autolike_tasks.append(task)

    # Test send once
    for uid in uids:
        result = await send_like_request(uid, region)
        if result["success"]:
            msg = (
                "✅ AUTO-LIKE ACTIVATED ✅\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 Player: {result['player']}\n"
                f"🆔 UID: {uid}\n"
                f"🌍 Region: {region}\n"
                f"🎯 Level: {result['level']}\n"
                f"❤️ Likes Given: {result['likes_given']}\n"
                f"📈 Before: {result['before']} | After: {result['after']}\n"
                f"📅 Days: {days}\n"
                f"➕ Added by: {added_by_name}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⚡ Daily at {custom_time['hour']:02d}:{custom_time['minute']:02d} AM IST"
            )
        else:
            msg = f"❌ Failed to add UID {uid}: {result['error']}"
        await update.message.reply_text(msg)

    await update.message.reply_text(format_schedule_message(), parse_mode="HTML")

@owner_only
async def removelike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)!= 1:
        return await update.message.reply_text("⚙️ Usage: /removelike <uid>")
    uid = context.args[0]
    async with tasks_lock:
        initial_len = len(autolike_tasks)
        autolike_tasks[:] = [t for t in autolike_tasks if t["uid"]!= uid]
        removed = initial_len - len(autolike_tasks)
    if removed > 0:
        await update.message.reply_text(f"✅ Removed UID: {uid}")
    else:
        await update.message.reply_text(f"❌ UID {uid} not found.")

@owner_only
async def likelist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autolike_tasks:
        return await update.message.reply_text("❌ No active UIDs.")
    msg = "📋 <b>ACTIVE AUTO-LIKE LIST</b>\n━━━━━━━━━━━━━━━━━━\n"
    for i, t in enumerate(autolike_tasks, 1):
        msg += (
            f"<b>{i}.</b> UID: <code>{t['uid']}</code>\n"
            f"🌍 Region: {t['region']}\n"
            f"📅 Days: {t['remaining']}/{t['days']}\n"
            f"➕ Added by: {t.get('added_by_name', 'Unknown')}\n"
            f"📅 Added: {t.get('added_date', 'N/A')}\n\n"
        )
    msg += f"━━━━━━━━━━━━━━━━━━\n<b>Total:</b> {len(autolike_tasks)} UIDs"
    msg += f"\n⏰ Daily: {custom_time['hour']:02d}:{custom_time['minute']:02d} AM IST"
    await update.message.reply_text(msg, parse_mode="HTML")

@owner_only
async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)!= 1 or ":" not in context.args[0]:
        return await update.message.reply_text("⚙️ Usage: /settime <HH:MM>")
    try:
        hour, minute = map(int, context.args[0].split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError
    except ValueError:
        return await update.message.reply_text("⚠️ Invalid time. Example: /settime 04:00")
    custom_time["hour"], custom_time["minute"] = hour, minute
    next_run, hours_wait = next_run_time(hour, minute)
    await update.message.reply_text(
        f"✅ AutoLike time set to <b>{hour:02d}:{minute:02d} IST</b>\n"
        f"Next run: <b>{next_run.strftime('%d %B %Y %I:%M %p')}</b>\n"
        f"(~{hours_wait} hours from now)",
        parse_mode="HTML"
    )

@owner_only
async def extenduid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)!= 2:
        return await update.message.reply_text("⚙️ Usage: /extenduid <uid> <days>")
    uid, add_days_str = context.args
    try:
        add_days = int(add_days_str)
    except ValueError:
        return await update.message.reply_text("⚠️ Days must be numeric.")
    for task in autolike_tasks:
        if task["uid"] == uid:
            old_days = task["days"]
            task["days"] += add_days
            task["remaining"] += add_days
            msg = (
                f"✅ UID EXTENDED\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"UID: {uid}\n"
                f"Region: {task['region']}\n"
                f"Old Days: {old_days}\n"
                f"Added: {add_days}\n"
                f"New Total: {task['days']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━"
            )
            return await update.message.reply_text(msg)
    await update.message.reply_text(f"❌ UID {uid} not found.")

@owner_only
async def addadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)!= 1:
        return await update.message.reply_text("⚙️ Usage: /addadmin <telegram_id>")
    try:
        new_admin_id = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("⚠️ ID must be numeric.")
    if new_admin_id in ADMIN_IDS:
        return await update.message.reply_text("⚠️ Already admin.")
    ADMIN_IDS.append(new_admin_id)
    if new_admin_id not in ALLOWED_USERS:
        ALLOWED_USERS.append(new_admin_id)
    await update.message.reply_text(f"✅ Added {new_admin_id} as admin.\nTotal admins: {len(ADMIN_IDS)}")

@owner_only
async def removeadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)!= 1:
        return await update.message.reply_text("⚙️ Usage: /removeadmin <telegram_id>")
    try:
        admin_id = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("⚠️ ID must be numeric.")
    if admin_id == OWNER_ID:
        return await update.message.reply_text("⚠️ Cannot remove owner!")
    if admin_id in ADMIN_IDS:
        ADMIN_IDS.remove(admin_id)
        await update.message.reply_text(f"✅ Removed {admin_id} from admins.")
    else:
        await update.message.reply_text("❌ Admin not found.")

@owner_only
async def adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "👑 ADMIN LIST 👑\n━━━━━━━━━━━━━━━━━\n"
    msg += f"Owner: {OWNER_ID}\n\nAdmins:\n"
    for i, admin_id in enumerate(ADMIN_IDS, 1):
        username = get_username_from_id(admin_id)
        msg += f"{i}. {username} (ID: {admin_id})\n"
    msg += f"\n━━━━━━━━━━━━━━━━━\nTotal: {len(ADMIN_IDS)}"
    await update.message.reply_text(msg)

@owner_only
async def maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MAINTENANCE_MODE
    if len(context.args) > 0 and context.args[0].lower() == "on":
        MAINTENANCE_MODE = True
        status = "ON 🔧"
    elif len(context.args) > 0 and context.args[0].lower() == "off":
        MAINTENANCE_MODE = False
        status = "OFF ✅"
    else:
        MAINTENANCE_MODE = not MAINTENANCE_MODE
        status = "ON 🔧" if MAINTENANCE_MODE else "OFF ✅"
    await update.message.reply_text(f"Maintenance mode: {status}")

@owner_only
async def allowuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)!= 1:
        return await update.message.reply_text("⚙️ Usage: /allowuser <telegram_id>")
    try:
        user_id = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("⚠️ ID must be numeric.")
    if user_id in ALLOWED_USERS:
        return await update.message.reply_text("⚠️ Already allowed.")
    ALLOWED_USERS.append(user_id)
    await update.message.reply_text(f"✅ User {user_id} allowed.")

@owner_only
async def allowgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)!= 1:
        return await update.message.reply_text("⚙️ Usage: /allowgroup <group_id>")
    try:
        group_id = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("⚠️ ID must be numeric.")
    if group_id in ALLOWED_GROUPS:
        return await update.message.reply_text("⚠️ Already allowed.")
    ALLOWED_GROUPS.append(group_id)
    await update.message.reply_text(f"✅ Group {group_id} allowed.")

@owner_only
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 <b>BOT STATISTICS</b>\n━━━━━━━━━━━━━━━━━━\n"
    msg += f"👥 Active Auto-Likes: {len(autolike_tasks)}\n"
    msg += f"👑 Admins: {len(ADMIN_IDS)}\n"
    msg += f"✅ Allowed Users: {len(ALLOWED_USERS)}\n"
    msg += f"✅ Allowed Groups: {len(ALLOWED_GROUPS)}\n"
    msg += f"⏰ Daily Time: {custom_time['hour']:02d}:{custom_time['minute']:02d} IST\n"
    msg += f"🔧 Maintenance: {'ON' if MAINTENANCE_MODE else 'OFF'}\n"
    msg += "━━━━━━━━━━━━━━━━━━"
    await update.message.reply_text(msg, parse_mode="HTML")

# ========= MAIN ==========
def main():
    nest_asyncio.apply()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("autolike", autolike))
    app.add_handler(CommandHandler("removelike", removelike))
    app.add_handler(CommandHandler("likelist", likelist))
    app.add_handler(CommandHandler("settime", settime))
    app.add_handler(CommandHandler("extenduid", extenduid))
    app.add_handler(CommandHandler("addadmin", addadmin))
    app.add_handler(CommandHandler("removeadmin", removeadmin))
    app.add_handler(CommandHandler("adminlist", adminlist))
    app.add_handler(CommandHandler("maintenance", maintenance))
    app.add_handler(CommandHandler("allowuser", allowuser))
    app.add_handler(CommandHandler("allowgroup", allowgroup))
    app.add_handler(CommandHandler("stats", stats))

    # Start daily task
    loop = asyncio.get_event_loop()
    loop.create_task(daily_autolike_task(app))

    print("🚀 ZEERYX Auto-Like Bot Started!")
    print(f"⏰ Daily auto-like at {custom_time['hour']:02d}:{custom_time['minute']:02d} AM IST")
    app.run_polling()

if __name__ == "__main__":
    main()