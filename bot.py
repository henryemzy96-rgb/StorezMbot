import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN set in environment")

# Your Mini App URL (set in BotFather)
MINI_APP_URL = "https://t.me/StorezMbot/StorezMminiapp"  # or the direct WebApp URL if you prefer
WEBSITE_URL = "https://storesm.net"
SUPPORT_CHANNEL = "https://t.me/ForexMarketBrief"  # or a dedicated support channel

# --- Helper functions ---

def get_main_keyboard():
    """Return the inline keyboard with Open App and Visit Website buttons."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🛍 Open STORESM",
                web_app={"url": MINI_APP_URL}   # Launches mini app
            ),
            InlineKeyboardButton(
                text="🌐 Visit Website",
                url=WEBSITE_URL
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_app_only_keyboard():
    """Return a keyboard with only the Open App button (for /app)."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🛍 Open STORESM",
                web_app={"url": MINI_APP_URL}
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_categories_keyboard():
    """Return a keyboard with category buttons that open the app with start_param."""
    categories = [
        ("Social Media", "social_media"),
        ("Marketing Tools", "marketing_tools"),
        ("Digital Resources", "digital_resources"),
        ("Online Services", "online_services"),
    ]
    keyboard = []
    for label, param in categories:
        # Deep link: when user taps, the app opens with startapp=category=...
        deep_link = f"{MINI_APP_URL}?startapp=category={param}"
        keyboard.append([InlineKeyboardButton(label, web_app={"url": deep_link})])
    # Add a general "Open App" button
    keyboard.append([InlineKeyboardButton("🛍 Open STORESM", web_app={"url": MINI_APP_URL})])
    return InlineKeyboardMarkup(keyboard)

# --- Command handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = (
        f"👋 Welcome to STORESM, {user.first_name}!\n\n"
        "Your place to explore digital resources, marketing tools, "
        "social media solutions and online services.\n\n"
        "🔎 Browse available resources\n"
        "📂 Explore different categories\n"
        "🚀 Discover useful services\n"
        "🌐 Access the STORESM marketplace\n\n"
        "Ready to explore? 👇 Tap the button below to open STORESM."
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the Open App button."""
    await update.message.reply_text(
        "🛍 Tap the button below to open the STORESM Mini App.",
        reply_markup=get_app_only_keyboard()
    )

async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show categories with deep‑linked buttons to open the app filtered."""
    text = (
        "📂 Explore our main categories:\n\n"
        "• Social Media\n"
        "• Marketing Tools\n"
        "• Digital Resources\n"
        "• Online Services\n\n"
        "Tap a category below to open the app and see relevant resources."
    )
    await update.message.reply_text(
        text,
        reply_markup=get_categories_keyboard()
    )

async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the website link."""
    await update.message.reply_text(
        f"🌐 Visit our official website: {WEBSITE_URL}"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explain bot commands."""
    help_text = (
        "🤖 *STORESM Bot Commands*\n\n"
        "/start – Welcome message & Open Mini App\n"
        "/app – Open STORESM Mini App\n"
        "/categories – Browse product categories\n"
        "/website – Visit storesm.net\n"
        "/help – Show this help message\n"
        "/support – Get support contact\n\n"
        "Need more? Just ask!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide support contact."""
    support_text = (
        "📞 For support, please reach out through:\n\n"
        f"• Telegram Channel: {SUPPORT_CHANNEL}\n"
        "• Or visit our website for contact options."
    )
    await update.message.reply_text(support_text)

# --- Error handler ---
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Oops, something went wrong. Please try again later."
        )

# --- Main ---
def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("app", app_command))
    application.add_handler(CommandHandler("categories", categories_command))
    application.add_handler(CommandHandler("website", website_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("support", support_command))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start polling (or use webhook)
    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
