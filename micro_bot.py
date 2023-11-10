import asyncio

from aiogram import Bot

import tokenfile as tf

TOKEN = tf.TOKEN
OWNER_CHAT_ID = tf.OWNER_CHAT_ID
OWNER_CHANNEL_NAME = tf.OWNER_CHANNEL_NAME
OWNER_GROUP_NAME = tf.OWNER_GROUP_NAME


async def main():
    bot = Bot(token=TOKEN)
    # Чтобы отправить сообщение в чат, бот должен найти его.
    # Личку с юзером бот может найти только по ID, группы и каналы - по имени, и только если они публичные.
    await bot.send_message(chat_id=OWNER_CHAT_ID, text='Я родился!')

    await bot.send_message(chat_id=OWNER_GROUP_NAME, text='Привет, группа!')
    admins_in_group = await bot.get_chat_administrators(chat_id=OWNER_GROUP_NAME)
    admins = {admin.user.first_name for admin in admins_in_group}
    print(f'Список админов чата {OWNER_GROUP_NAME}: {admins}')

    await bot.send_message(chat_id=OWNER_CHANNEL_NAME, text='Привет, канал!')
    admins_in_channel = await bot.get_chat_administrators(chat_id=OWNER_CHANNEL_NAME)
    admins = {admin.user.first_name for admin in admins_in_channel}
    print(f'Список админов чата {OWNER_CHANNEL_NAME}: {admins}')

    # если не используется диспетчер, то хорошим тоном считает закрывать сессию бота с сервером
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
