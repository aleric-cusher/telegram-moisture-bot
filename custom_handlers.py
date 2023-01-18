from telegram.ext import BaseHandler, Updater
import telegram
import config
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class WhitelistHandler(BaseHandler):
    def __init__(self):
        super().__init__(self.cb)

    async def cb(self, update: telegram.Update, context):
        await update.message.reply_text("You are not whitelisted </3 :(")

    def check_update(self, update: telegram.Update):
        mess = update.message
        if mess is None or mess.from_user.id not in config.whitelist:
            logger.info(f"Unknown user: {mess.from_user.full_name}({mess.from_user.id}), message: {mess.text}")
            return True
        logger.info(f"Known user: {mess.from_user.full_name}({mess.from_user.id}), message: {mess.text}")
        return False