import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("8309959181:AAEZx-Ueh2xmVDjl2ASvb_UGv4efPb53x_s")
ADMIN_CHAT_ID = -1003637925360

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# ===== ARIZA ID =====
def get_next_id():
    try:
        with open("last_id.txt", "r") as f:
            last = int(f.read())
    except:
        last = 0
    new = last + 1
    with open("last_id.txt", "w") as f:
        f.write(str(new))
    return new

# ===== HOLATLAR =====
class Form(StatesGroup):
    fish = State()
    phone = State()
    ip_phone = State()
    ish_joyi = State()
    depart_tarmoq = State()
    jarayon = State()
    turi = State()
    boshqa_turi = State()
    muammo = State()
    taklif = State()
    prioritet = State()

# ===== KLAVIATURALAR =====
ishjoy_kb = ReplyKeyboardMarkup(resize_keyboard=True)
ishjoy_kb.add("Bosh ofis", "BXO/BXM/Markaz")

turi_kb = ReplyKeyboardMarkup(resize_keyboard=True)
turi_kb.add("Avtomatlashtirish", "Optimallashtirish", "Robot qo'yish", "Boshqa")

prior_kb = ReplyKeyboardMarkup(resize_keyboard=True)
prior_kb.add("Yuqori", "O‘rtacha", "Past")

new_app_kb = ReplyKeyboardMarkup(resize_keyboard=True)
new_app_kb.add("🆕 Yangi ariza yaratish")

# ===== START =====
@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("F.I.Sh kiriting:")
    await Form.fish.set()

# 🆕 YANGI ARIZA
@dp.message_handler(lambda message: message.text == "🆕 Yangi ariza yaratish")
async def new_application(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("F.I.Sh kiriting:")
    await Form.fish.set()

# ===== FISH =====
@dp.message_handler(state=Form.fish)
async def fish(message: types.Message, state: FSMContext):
    await state.update_data(fish=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await Form.phone.set()

# ===== TELEFON =====
@dp.message_handler(state=Form.phone)
async def phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("IP telefon raqamingizni kiriting:")
    await Form.ip_phone.set()

# ===== IP TELEFON =====
@dp.message_handler(state=Form.ip_phone)
async def ip_phone(message: types.Message, state: FSMContext):
    await state.update_data(ip_phone=message.text)
    await message.answer("Ish joyini tanlang:", reply_markup=ishjoy_kb)
    await Form.ish_joyi.set()

# ===== ISH JOYI =====
@dp.message_handler(state=Form.ish_joyi)
async def ishjoy(message: types.Message, state: FSMContext):
    await state.update_data(ish_joyi=message.text)

    if message.text == "Bosh ofis":
        await message.answer("Departament nomini kiriting:")
    else:
        await message.answer("Filial / tarmoq nomini kiriting:")

    await Form.depart_tarmoq.set()

# ===== DEPART/TARMOQ =====
@dp.message_handler(state=Form.depart_tarmoq)
async def depart(message: types.Message, state: FSMContext):
    await state.update_data(depart=message.text)
    await message.answer("Kamchiligi mavjud bo'lgan jarayon nomini yozing:")
    await Form.jarayon.set()

# ===== JARAYON =====
@dp.message_handler(state=Form.jarayon)
async def jarayon(message: types.Message, state: FSMContext):
    await state.update_data(jarayon=message.text)
    await message.answer("Turini tanlang:", reply_markup=turi_kb)
    await Form.turi.set()

# ===== TURI =====
@dp.message_handler(state=Form.turi)
async def turi(message: types.Message, state: FSMContext):
    if message.text == "Boshqa":
        await message.answer("Turini yozib kiriting:")
        await Form.boshqa_turi.set()
    else:
        await state.update_data(turi=message.text)
        await message.answer("Jarayondagi muammoni yozing:")
        await Form.muammo.set()

# ===== BOSHQA TURI =====
@dp.message_handler(state=Form.boshqa_turi)
async def boshqa(message: types.Message, state: FSMContext):
    await state.update_data(turi=message.text)
    await message.answer("Jarayondagi muammoni yozing:")
    await Form.muammo.set()

# ===== MUAMMO =====
@dp.message_handler(state=Form.muammo)
async def muammo(message: types.Message, state: FSMContext):
    await state.update_data(muammo=message.text)
    await message.answer("Taklifingizni yozing:")
    await Form.taklif.set()

# ===== TAKLIF =====
@dp.message_handler(state=Form.taklif)
async def taklif(message: types.Message, state: FSMContext):
    await state.update_data(taklif=message.text)
    await message.answer("Prioritetni tanlang:", reply_markup=prior_kb)
    await Form.prioritet.set()

# ===== YAKUN =====
@dp.message_handler(state=Form.prioritet)
async def finish(message: types.Message, state: FSMContext):
    await state.update_data(prioritet=message.text)
    data = await state.get_data()

    app_id = get_next_id()

    text = f"""
🆕 Yangi murojaat №{app_id}

👤 FISH: {data['fish']}
📱 Telefon: {data['phone']}
☎️ IP telefon: {data['ip_phone']}

🏢 Ish joyi: {data['ish_joyi']}
📍 Depart/Tarmoq: {data['depart']}

⚙️ Jarayon: {data['jarayon']}
🔧 Turi: {data['turi']}

❗ Muammo:
{data['muammo']}

💡 Taklif:
{data['taklif']}

🔥 Prioritet: {data['prioritet']}
"""

    await bot.send_message(ADMIN_CHAT_ID, text)

    await message.answer(
        f"Murojaatingiz qabul qilindi ✅\nAriza raqami: №{app_id}",
        reply_markup=new_app_kb
    )

    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

