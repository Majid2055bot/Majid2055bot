import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8321227911:AAHW7Vd-EUnHpodyn51dl2f9wEu_xPvghg4")
OWNER_ID = 8653460899
OWNER_USERNAME = "Mhyvc"

def home():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 حسابي", callback_data="profile"),
         InlineKeyboardButton("🔢 لوحة الأرقام", callback_data="numbers")],
        [InlineKeyboardButton("📋 الأوامر", callback_data="commands"),
         InlineKeyboardButton("ℹ️ عن البوت", callback_data="about")],
        [InlineKeyboardButton("👑 لوحة المالك", callback_data="admin")]
    ])

def back():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 الرئيسية", callback_data="home")]])

def numbers():
    rows=[]
    for a,b,c in [(1,2,3),(4,5,6),(7,8,9)]:
        rows.append([InlineKeyboardButton(str(x), callback_data=f"n{x}") for x in (a,b,c)])
    rows.append([InlineKeyboardButton("0", callback_data="n0")])
    rows.append([InlineKeyboardButton("🔙 الرئيسية", callback_data="home")])
    return InlineKeyboardMarkup(rows)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"مرحباً {update.effective_user.first_name} 👋\n\n"
        "🤖 أهلاً بك في البوت.\nاختر من لوحة التحكم:",
        reply_markup=home())

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 لوحة البوت:", reply_markup=home())

async def uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 ID: `{update.effective_user.id}`", parse_mode="Markdown")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 الأوامر:\n/start\n/menu\n/id\n/help\n/owner\n\n"
        "استخدم /menu للوصول إلى جميع الأزرار.")

async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ هذا الأمر للمالك فقط.")
        return
    await update.message.reply_text(
        "👑 لوحة المالك\n\n"
        "الحالة: يعمل ✅\n"
        f"المالك: @{OWNER_USERNAME}\n"
        f"ID: {OWNER_ID}")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    d=q.data
    u=q.from_user

    if d=="home":
        await q.edit_message_text("🏠 لوحة البوت:", reply_markup=home())
    elif d=="profile":
        await q.edit_message_text(
            f"👤 حسابك\n\nالاسم: {u.first_name}\n"
            f"المستخدم: @{u.username or 'غير متوفر'}\n"
            f"🆔 ID: `{u.id}`",
            parse_mode="Markdown", reply_markup=back())
    elif d=="numbers":
        await q.edit_message_text("🔢 لوحة الأرقام\nاختر رقماً:", reply_markup=numbers())
    elif d.startswith("n"):
        await q.answer(f"تم اختيار الرقم {d[1:]}")
    elif d=="commands":
        await q.edit_message_text(
            "📋 الأوامر:\n\n/start تشغيل\n/menu القائمة\n/id عرض ID\n"
            "/help المساعدة\n/owner لوحة المالك", reply_markup=back())
    elif d=="about":
        await q.edit_message_text(
            "ℹ️ بوت Telegram متكامل بواجهة أزرار ولوحة أرقام "
            "وصلاحيات للمالك، وقابل لإضافة خدمات وقواعد بيانات لاحقاً.",
            reply_markup=back())
    elif d=="admin":
        if u.id != OWNER_ID:
            await q.answer("⛔ للمالك فقط", show_alert=True)
            return
        await q.edit_message_text(
            "👑 لوحة المالك\n\n"
            "🟢 البوت يعمل\n"
            "📊 الإحصائيات المتقدمة يمكن ربطها بقاعدة بيانات.\n"
            "📢 يمكن إضافة Broadcast لاحقاً.",
            reply_markup=back())

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📩 تم استلام رسالتك.\nاستخدم /menu لفتح اللوحة.",
        reply_markup=home())

def main():
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("id", uid))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("owner", owner))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    app.run_polling()

if __name__=="__main__":
    main()
