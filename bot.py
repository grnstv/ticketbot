import os
import datetime
import motor.motor_asyncio

from telegram import Update, BotCommand, User, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, ApplicationBuilder, CommandHandler, ContextTypes

"""
TODO:
1. Регистрировать новых пользователей
2. Выводить справочную информацию
3. Статистику
"""

class UserRepository:
    def __init__(self, mongodb_url: str = os.environ["MONGODB_URL"],
                 database: str = "users",
                 collection: str = "user_profile"):

        self._db_client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
        self._collection = self._db_client[database][collection]

    def close(self):
        self._db_client.close()

    async def get_user(self, id: str) -> User | None:
        return await self._collection.find_one({"telegram_id": id})

    async def about_service(self):
        return await self._collection.aggregate([
            {
                "$group": {
                    "_id": None,
                    "total_users": {
                        "$sum": 1
                    },
                    "first_user_registered": {
                        "$first": "$created_at"
                    },
                    "last_user_seen": {
                        "$last": "$last_seen"
                    }
                }
            }
        ]).next()

    async def create_user(self, user) -> User | None:
        return await self._collection.insert_one({
            "first_name": user.first_name,
            "last_name": user.last_name if user.last_name else "",
            "username": user.username if user.username else "",
            "telegram_id": user.id,
            "visits": 1,
            "created_at": datetime.datetime.now(tz=datetime.timezone.utc),
            "last_seen": datetime.datetime.now(tz=datetime.timezone.utc)
        })

    async def increment_user_stats(self, user_id: str) -> None:
        await self._collection.update_one(
            {"telegram_id": user_id},
            {"$inc": {"visits": 1},
             "$set": {
                 "last_seen": datetime.datetime.now(tz=datetime.timezone.utc)
             }}
        )

class SimpleBot:
    def __init__(self, api_token: str = os.environ["TELEGRAM_API_KEY"]):
        self._user_repository = UserRepository()

        self._app = (ApplicationBuilder()
                     .token(api_token)
                     .post_init(self._commands("post_init"))
                     .build())
        self._app.add_handler(CommandHandler("start", self._commands("start")))
        self._app.add_handler(CallbackQueryHandler(self._commands("button_callback")))

    def _commands(self, command):
        async def post_init(application: Application) -> None:
            await application.bot.set_my_commands([('start', 'Starts the bot')])
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            user = await self._user_repository.get_user(id=update.effective_user.id)

            welcome_message = f"Привет, {update.effective_user.first_name}!"
            keyboard = [
                [
                    InlineKeyboardButton("О сервисе", callback_data="3"),
                ],
                [InlineKeyboardButton("Погода в Москве", callback_data="4")],
            ]

            if user:
                welcome_message += f"\n\nРады видеть тебя снова!"
                keyboard[0].insert(0,
                                   InlineKeyboardButton("Моя статистика", callback_data="2"))

                await self._user_repository.increment_user_stats(user["telegram_id"])
            else:
                welcome_message += f"\n\nТы еще не зарегистрирован, давай сделаем тебе аккаунт"
                keyboard[0].insert(0,
                                   InlineKeyboardButton("Зарегистрироваться", callback_data="1"))

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(welcome_message, reply_markup=reply_markup)

        async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            query = update.callback_query
            await query.answer()

            if query.data == "1":
                await self._user_repository.create_user(query.from_user)
                await query.message.reply_text("Отлично, зарегистрировались")

            elif query.data == "2":
                user = await self._user_repository.get_user(query.from_user.id)
                await query.message.reply_text(f"""{user['first_name']} {user['last_name']}
        @{user['username']} зарегистрирован {user['created_at'].strftime('%d %b %Y')},
        Нажимал /start {user['visits']} раз, последний раз {user['last_seen'].strftime('%d %b %Y')}""")

            elif query.data == "3":
                stats = await self._user_repository.about_service()
                await query.message.reply_text(f"""Всего пользователей: {stats['total_users']}
        Первый пользователь зарегистрировался: {stats['first_user_registered'].strftime('%d %b %Y')}
        Последний раз заходили: {stats['last_user_seen'].strftime('%d %b %Y')}""")

            elif query.data == "4":
                # import requests, parse yandex weather etc
                # or just:
                await query.message.reply_text("В Москве +15, солнечно ☀️")

            else:
                await query.message.reply_text("unknown button")

        if command == "start":
            return start_command
        if command == "button_callback":
            return button
        if command == "post_init":
            return post_init

    def run(self):
        try:
            self._app.run_polling(allowed_updates=Update.ALL_TYPES)
        finally:
            self._user_repository.close()

if __name__ == "__main__":
    bot = SimpleBot()
    bot.run()