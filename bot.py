import os
import telebot
from telebot import types
from sheets_handler import SheetsHandler

# Ortam değişkenlerini yükle
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "BURAYA_BOT_TOKEN_GELECEK")
if not BOT_TOKEN or BOT_TOKEN == "BURAYA_BOT_TOKEN_GELECEK":
    print("[UYARI] TELEGRAM_BOT_TOKEN henüz ayarlanmadı! Lütfen .env dosyasını güncelleyin.")

bot = telebot.TeleBot(BOT_TOKEN)
sheets_service = SheetsHandler()

# Geçici oturum verileri
user_sessions = {}

# Piri Reis Üniversitesi bölümleri ve popüler komiteler
DEPARTMENTS = [
    ["Bilişim Sistemleri Mühendisliği", "Yazılım / Bilgisayar Müh."],
    ["Deniz Ulaştırma İşletme Müh.", "Gemi İnşaatı ve Gemi Mak."],
    ["Endüstri Mühendisliği", "Yönetim Bilişim Sistemleri"],
    ["Diğer / Hazırlık Sınıfı"]
]

INTERESTS = [
    ["Yapay Zeka & Veri Bilimi", "Web & Mobil Yazılım"],
    ["Denizcilik Teknolojileri & Otonom", "Siber Güvenlik"],
    ["Robotik & Gömülü Sistemler", "Tasarım (UI/UX) & Sosyal Medya"],
    ["Etkinlik Yönetimi & Sponsorluk"]
]


def create_keyboard(options_list):
    """Listeden tek tıkla seçilebilecek özel Telegram klavyesi üretir."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for row in options_list:
        markup.row(*[types.KeyboardButton(btn) for btn in row])
    return markup


@bot.message_handler(commands=['iptal', 'cancel'])
def cmd_cancel(message):
    """Devam eden herhangi bir işlemi sıfırlar."""
    user_id = message.from_user.id
    if user_id in user_sessions:
        user_sessions.pop(user_id, None)
    bot.send_message(
        message.chat.id,
        "❌ İşlem iptal edildi. Dilediğiniz zaman /start yazarak yeniden başlayabilirsiniz.",
        reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(commands=['start', 'kayit'])
def cmd_start(message):
    """Kayıt akışını başlatan karşılama fonksiyonu."""
    user_id = message.from_user.id
    username = message.from_user.username or ""
    
    # Kullanıcı oturumunu sıfırla
    user_sessions[user_id] = {
        "telegram_id": user_id,
        "username": username,
        "full_name": "",
        "department": "",
        "interest": "",
        "contact": ""
    }

    welcome_text = (
        "⚓️ *PRU Auto-Admin | Kulüp Üyelik Kayıt Asistanı* 🚀\n\n"
        "Piri Reis Üniversitesi Kulüp Ailemize hoş geldiniz!\n"
        "Yeni dönem workshopları, teknik projeler ve etkinliklerden haberdar olmak için "
        "30 saniyede resmi üye kaydınızı yapabilirsiniz.\n\n"
        "*(İstediğiniz an /iptal yazabilirsiniz)*\n\n"
        "👉 *Lütfen Adınızı ve Soyadınızı yazınız:*"
    )
    sent_msg = bot.send_message(
        message.chat.id, 
        welcome_text, 
        parse_mode="Markdown", 
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(sent_msg, process_step_name)


def process_step_name(message):
    """Ad-Soyad bilgisini alır ve Bölüm seçimine yönlendirir."""
    if message.text and message.text.startswith('/'):
        return  # Komut geldiyse akıştan çık

    user_id = message.from_user.id
    name = message.text.strip()

    if len(name) < 3:
        sent_msg = bot.reply_to(message, "⚠️ Lütfen geçerli bir Ad ve Soyad giriniz:")
        bot.register_next_step_handler(sent_msg, process_step_name)
        return

    if user_id not in user_sessions:
        user_sessions[user_id] = {"telegram_id": user_id, "username": message.from_user.username or ""}
    
    user_sessions[user_id]["full_name"] = name

    dept_text = (
        f"Memnun olduk, *{name}*! 🎓\n\n"
        "Lütfen okuduğunuz bölümü aşağıdaki butonlardan seçin ya da doğrudan yazın:"
    )
    sent_msg = bot.send_message(
        message.chat.id, 
        dept_text, 
        parse_mode="Markdown", 
        reply_markup=create_keyboard(DEPARTMENTS)
    )
    bot.register_next_step_handler(sent_msg, process_step_department)


def process_step_department(message):
    """Bölüm bilgisini alır ve İlgi Alanı seçimine yönlendirir."""
    if message.text and message.text.startswith('/'):
        return

    user_id = message.from_user.id
    if user_id not in user_sessions:
        bot.send_message(message.chat.id, "⚠️ Oturum süresi doldu. Lütfen /start yazarak tekrar başlayın.")
        return

    user_sessions[user_id]["department"] = message.text.strip()

    interest_text = (
        "Harika! Şimdi kulüp içerisinde en çok hangi alanda aktif olmak istersin?\n\n"
        "Aşağıdaki alanlardan birini seçebilir veya kendi uzmanlığını yazabilirsin:"
    )
    sent_msg = bot.send_message(
        message.chat.id, 
        interest_text, 
        reply_markup=create_keyboard(INTERESTS)
    )
    bot.register_next_step_handler(sent_msg, process_step_interest)


def process_step_interest(message):
    """İlgi alanı bilgisini alır ve isteğe bağlı iletişim bilgisi sorar."""
    if message.text and message.text.startswith('/'):
        return

    user_id = message.from_user.id
    if user_id not in user_sessions:
        bot.send_message(message.chat.id, "⚠️ Oturum süresi doldu. Lütfen /start yazarak tekrar başlayın.")
        return

    user_sessions[user_id]["interest"] = message.text.strip()

    contact_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_markup.row(types.KeyboardButton("⏭ Bu Adımı Atla"))

    contact_text = (
        "Son adım! 📱 Kulüp WhatsApp duyuru grubu ve acil etkinlik bildirimleri için "
        "isteğe bağlı olarak telefon numaranı veya e-posta adresini paylaşabilirsin.\n\n"
        "*(Paylaşmak istemiyorsan aşağıdaki 'Atla' butonuna basabilirsin.)*"
    )
    sent_msg = bot.send_message(
        message.chat.id, 
        contact_text, 
        parse_mode="Markdown", 
        reply_markup=contact_markup
    )
    bot.register_next_step_handler(sent_msg, process_step_final)


def process_step_final(message):
    """Verileri işler, kaydeder ve kullanıcıya onay özeti döner."""
    if message.text and message.text.startswith('/'):
        return

    user_id = message.from_user.id
    if user_id not in user_sessions:
        bot.send_message(message.chat.id, "⚠️ Oturum süresi doldu. Lütfen /start yazarak tekrar başlayın.")
        return

    contact = message.text.strip()
    if contact == "⏭ Bu Adımı Atla":
        contact = "Belirtilmedi"
    
    user_sessions[user_id]["contact"] = contact
    data = user_sessions[user_id]

    bot.send_chat_action(message.chat.id, 'typing')
    success = sheets_service.add_member(data)

    hide_markup = types.ReplyKeyboardRemove()

    if success:
        summary_msg = (
            "🎉 *Tebrikler! Kulüp Üyelik Kaydınız Başarıyla Alındı.* ✅\n\n"
            "📋 *Kayıt Detayları:*\n"
            f"• 👤 *İsim:* {data['full_name']}\n"
            f"• 🎓 *Bölüm:* {data['department']}\n"
            f"• 💡 *İlgi Alanı:* {data['interest']}\n"
            f"• 📞 *İletişim:* {data['contact']}\n\n"
            "Verileriniz merkezi yönetim sistemine (Google Sheets & Dashboard) başarıyla işlendi. "
            "Aramıza hoş geldin! Tanışma toplantısında görüşmek üzere! ⚓️🔥"
        )
        bot.send_message(message.chat.id, summary_msg, parse_mode="Markdown", reply_markup=hide_markup)
    else:
        bot.send_message(
            message.chat.id, 
            "⚠️ Kaydınız işlenirken geçici bir hata oluştu. Lütfen birazdan tekrar /start yazarak deneyin.",
            reply_markup=hide_markup
        )

    user_sessions.pop(user_id, None)


@bot.message_handler(commands=['durum', 'status', 'ozet'])
def cmd_status(message):
    """Anlık üye sayısını ve sistem modunu gösterir."""
    try:
        df = sheets_service.get_all_members()
        count = len(df)
        mode = "🟢 Canlı Google Sheets" if sheets_service.is_connected else "🟡 Yerel Güvenli Veri Deposu (CSV)"
        top_interest = df["İlgi Alanı"].mode()[0] if ("İlgi Alanı" in df.columns and not df.empty) else "-"
        msg = (
            "📊 *PRU Auto-Admin Canlı Raporu:*\n\n"
            f"• 📡 Veritabanı: `{mode}`\n"
            f"• 👥 Toplam Kayıtlı Üye: *{count}*\n"
            f"• 🔥 En Popüler Komite: *{top_interest}*\n"
            f"• 🖥️ Yönetim Dashboard'u: Yayında"
        )
    except Exception as e:
        msg = f"Rapor alınamadı: {e}"
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")


@bot.message_handler(commands=['yardim', 'help'])
def cmd_help(message):
    help_text = (
        "🤖 *PRU Auto-Admin Komut Rehberi:*\n\n"
        "• `/start` veya `/kayit` - Yeni üyelik kaydı başlatır.\n"
        "• `/durum` veya `/ozet` - Canlı üye ve komite istatistiklerini getirir.\n"
        "• `/iptal` - Devam eden kayıt akışını iptal eder.\n"
        "• `/yardim` - Bu yardım menüsünü açar."
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


if __name__ == "__main__":
    print("[BAŞLADI] PRU Auto-Admin Telegram Botu Dinlemede...")
    bot.infinity_polling(skip_pending=True)
