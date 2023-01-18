
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import logging

from custom_handlers import WhitelistHandler
import processing
import config


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def bad_command(update: Update):
    await update.message.reply_text("Bad Command!! 🤨")
    await update.message.reply_text("😡")
    await update.message.reply_text("Try again 🤔")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()} -> {user.id}!",
        reply_markup=ForceReply(selective=True),
    )
    await update.message.reply_text('Use /help to see commands!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""Commands:
/graph: moisture data for graph, number of datapoints can be supplied after command, default 36
/recent: get recent datapoints as text, number of datapoints can be supplied after command, default 4
""")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def graph(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args: list[str] = context.args # type: ignore
    limit = None
    if args:
        limit = int(args[0])
        if len(args) > 1 or int(args[0]) > 50:
            await bad_command(update)
            return
    await update.message.reply_text("Hol up ✋")
    await update.message.reply_text("⌛️")
    if limit:
        path_to_image = processing.generate_graph(limit)
    else:
        path_to_image = processing.generate_graph()
    await update.message.reply_text("Processed 👍\nSending... 🤌")
    await update.message.reply_photo(path_to_image)
    processing.delete_graph_img(path_to_image)

async def recent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args: list[str] = context.args # type: ignore 
    limit = None
    if args:
        limit = int(args[0])
        if len(args) > 1 or int(args[0]) > 50:
            await bad_command(update)
            return
    await update.message.reply_text("Processing...")
    if limit:
        message = processing.get_recent_entries(limit)
    else:
        message = processing.get_recent_entries()
    await update.message.reply_text(message)
    


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config.token).build()

    application.add_handler(WhitelistHandler())
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("graph", graph))
    application.add_handler(CommandHandler("recent", recent))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()