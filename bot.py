from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ▶️ Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "PrivateVPN работает на личном сервере в Нидерландах и открывает безопасный доступ к зарубежным интернет-ресурсам"

    keyboard = [
        [InlineKeyboardButton("Подключить VPN", callback_data="connect_vpn")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ▶️ Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 🔹 Шаг 1 — выбор устройств
    if query.data == "connect_vpn":
        keyboard = [
            [InlineKeyboardButton("1 устройство", callback_data="dev_1")],
            [InlineKeyboardButton("2 устройства", callback_data="dev_2")],
            [InlineKeyboardButton("5 устройств", callback_data="dev_5")],
        ]

        await query.edit_message_text(
            "Выберите количество устройств",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 🔹 Шаг 2 — выбор оплаты
    elif query.data in ["dev_1", "dev_2", "dev_5"]:
        context.user_data["devices"] = query.data

        keyboard = [
            [InlineKeyboardButton("Бесплатно 3 суток", callback_data="free_trial")]
        ]

        await query.edit_message_text(
            "Выберите тип оплаты",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 🔹 Шаг 3 — отправка заявки админу
    elif query.data == "free_trial":
        user = query.from_user

        username = f"@{user.username}" if user.username else "нет username"

        text_to_admin = (
            f"🔥 Новый запрос на VPN\n\n"
            f"👤 Имя: {user.first_name}\n"
            f"📎 Username: {username}\n"
            f"🆔 ID: {user.id}\n"
            f"📱 Устройства: {context.user_data.get('devices')}"
        )

        try:
            # 👉 отправка ТЕБЕ в личку
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=text_to_admin
            )
        except Exception as e:
            print("Ошибка отправки админитратору:", e)

        # 👉 ответ пользователю
        await query.edit_message_text(
            "Заявка отправлена. Администратор скоро свяжется с вами в личных сообщениях 🦄"
        )


# ▶️ Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
