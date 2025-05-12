from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.user_states import AnsMessage
from core.init_bot import bot
from keyboards.user_kbs import start_kb, back_kb, answer_kb
from config import BOT_USERNAME, IMG_URL
from database.cruds import add_user_if_not_exists


user_router = Router() 


@user_router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await add_user_if_not_exists(message.from_user.id)
    if message.text != '/start':
        receiver_id = message.text[7:]
        if int(receiver_id) == message.from_user.id:
            await message.answer('<b>Вы не можете отправить сообщение самому себе</b>')
            return
        await message.answer('<b>✍️ Напишите что-нибудь для человека, который дал эту ссылку</b>',
                                reply_markup=back_kb)
        await state.update_data(receiver_id=receiver_id)
        await state.set_state(AnsMessage.writing)
        return
    await message.answer(f'<b>👋 Добро пожаловать в бота для отправки и получения анонимных сообщений! Вот ваша ссылка, перейдя по ней, человек сможет прислать вам сообщение. Помимо текстовых сообщений поддерживаются: кружки, голосовые, изображения, видео, стикеры и гифки\n\n🔗 https://t.me/{BOT_USERNAME}?start={message.from_user.id}</b>',
                            reply_markup=start_kb, disable_web_page_preview=True)

@user_router.callback_query(F.data.startswith('answer_'))
async def start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    if callback.message.text != '/start':
        receiver_id = int(callback.data.split('_')[1])
        await callback.message.answer('<b>✍️ Напишите что-нибудь для человека, который дал эту ссылку</b>',
                                reply_markup=back_kb)
        await state.update_data(receiver_id=receiver_id)
        await state.set_state(AnsMessage.writing)
        return

@user_router.message(AnsMessage.writing)
async def send_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    receiver_id = int(data.get('receiver_id'))
    sender_id = message.from_user.id
    try:
        if message.content_type == ContentType.TEXT:
            await bot.send_message(receiver_id, f"<b>📩 Получено новое сообщение от пользователя!</b>\n\n«{message.text.replace('<', '&lt;').replace('>', '&gt;')}»", reply_markup=answer_kb(sender_id))
        elif message.content_type == ContentType.PHOTO:
            message_text = f"«{message.caption.replace('<', '&lt;').replace('>', '&gt;')}»" if message.caption else ''
            await bot.send_photo(receiver_id, photo=message.photo[-1].file_id, caption=f'<b>📩 Получено новое сообщение от пользователя!</b>\n\n{message_text}', reply_markup=answer_kb(sender_id))
        elif message.content_type == ContentType.VIDEO:
            message_text = f"«{message.caption.replace('<', '&lt;').replace('>', '&gt;')}»" if message.caption else ''
            await bot.send_video(receiver_id, video=message.video.file_id, caption=f'<b>📩 Получено новое сообщение от пользователя!</b>\n\n{message_text}', reply_markup=answer_kb(sender_id))
        elif message.content_type == ContentType.ANIMATION:
            message_text = f"«{message.caption.replace('<', '&lt;').replace('>', '&gt;')}»" if message.caption else ''
            await bot.send_animation(receiver_id, animation=message.animation.file_id, caption=f'<b>📩 Получено новое сообщение от пользователя!</b>\n\n{message_text}' ,reply_markup=answer_kb(sender_id))
        elif message.content_type == ContentType.VOICE:
            message_text = f"«{message.caption.replace('<', '&lt;').replace('>', '&gt;')}»" if message.caption else ''
            await bot.send_voice(receiver_id, voice=message.voice.file_id, caption=f'<b>📩 Получено новое сообщение от пользователя!</b>\n\n{message_text}', reply_markup=answer_kb(sender_id))
        elif message.content_type == ContentType.VIDEO_NOTE:
            answer_message = await bot.send_video_note(receiver_id, video_note=message.video_note.file_id, reply_markup=answer_kb(sender_id))
            await bot.send_message(receiver_id, f'<b>📩 Получено новое сообщение от пользователя! ☝🏼</b>', reply_to_message_id=answer_message.message_id)
        elif message.content_type == ContentType.STICKER:
            answer_message = await bot.send_sticker(receiver_id, sticker=message.sticker.file_id, reply_markup=answer_kb(sender_id))
            await bot.send_message(receiver_id, f'<b>📩 Получено новое сообщение от пользователя! ☝🏼</b>', reply_to_message_id=answer_message.message_id)
        else:
            await message.answer('<b>❌ Неподдерживаемый тип сообщения, попробуйте еще раз</b>')
            return
        await message.answer('<b>✅ Сообщение отправлено</b>')
    except:
        await message.answer('<b>❌ Пользователь не найден</b>')
    await state.clear()

@user_router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    if callback.message.content_type == ContentType.PHOTO:
        await callback.message.answer(f'<b>👋 Добро пожаловать в бота для отправки и получения анонимных сообщений! Вот ваша ссылка, перейдя по ней, человек сможет прислать вам сообщение. Помимо текстовых сообщений поддерживаются: кружки, голосовые, изображения, видео, стикеры и гифки\n\n🔗 https://t.me/{BOT_USERNAME}?start={callback.message.chat.id}</b>',
                                            reply_markup=start_kb, disable_web_page_preview=True)
    else:
        await callback.message.edit_text(f'<b>👋 Добро пожаловать в бота для отправки и получения анонимных сообщений! Вот ваша ссылка, перейдя по ней, человек сможет прислать вам сообщение. Помимо текстовых сообщений поддерживаются: кружки, голосовые, изображения, видео, стикеры и гифки\n\n🔗 https://t.me/{BOT_USERNAME}?start={callback.message.chat.id}</b>',
                                            reply_markup=start_kb, disable_web_page_preview=True)
    await state.clear()

@user_router.callback_query(F.data == 'info')
async def info(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer_photo(IMG_URL, caption=f'<b>Выставь эту ссылку к себе в канал или в описание профиля, и любой человек сможет написать тебе анонимное сообщение 💬\n\nТвоя ссылка: <code>https://t.me/{BOT_USERNAME}?start={callback.message.chat.id}</code></b>',
                                        reply_markup=back_kb)

@user_router.message(Command('info'))
async def info(message: Message) -> None:
    await message.answer_photo(IMG_URL, caption=f'<b>Выставь эту ссылку к себе в канал или в описание профиля, и любой человек сможет написать тебе анонимное сообщение 💬\n\nТвоя ссылка: <code>https://t.me/{BOT_USERNAME}?start={message.chat.id}</code></b>',
                                reply_markup=back_kb)

@user_router.message()
async def echo(message: Message) -> None:
    await message.answer('<b>❌ Вы ввели неверную команду</b>')