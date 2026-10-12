# ⚓️ PRU Auto-Admin: Kulüp İşletim Sistemi (Club OS) & Veri Otomasyonu

PRU Auto-Admin; üniversite kulüplerinin standlarda ve dağınık formlarda yaşadığı üye kayıt ve yönetim kaosunu ortadan kaldıran; Telegram botu üzerinden verileri toplayıp Google Sheets'e anlık işleyen ve yöneticilere **Yapay Zeka Destekli Takım Oluşturma**, **Dijital Üye Kartı (QR)** ve **Otomatik İletişim Kitleri** sunan uçtan uca modern bir Kulüp İşletim Sistemidir (Club OS).

---

## 1. Problem
Üniversite kulüplerinde her dönem başında yaşanan temel operasyonel krizler şunlardır:
- **Manuel ve Dağınık Kayıt Süreci:** Üye kayıtlarının standlarda kağıt-kalemle veya farklı Google Form linkleriyle toplanması sonucu veriler kaybolmakta, mükerrer kayıtlar oluşmakta ve iletişim bilgileri standart dışı kalmaktadır.
- **Veri Standardizasyonu Eksikliği:** Öğrencilerin bölüm adlarını farklı yazması ve ilgi alanlarının serbest metin bırakılması sebebiyle yönetim veri analizi yapamamaktadır.
- **Multidisipliner Takım Kurma Felci:** Kulüplerin en büyük sorunu yüzlerce üyeyi TEKNOFEST, Hackathon veya proje takımlarına dengeli şekilde (mühendislik + denizcilik + tasarım) dağıtamamasıdır.
- **Geciken Karar Alma ve Sürtünme:** Yönetim kurulu demografik içgörüye sahip olmadığı için etkinlik ve sponsorluk planlamalarını hissi kararlarla yapmaktadır.

---

## 2. Çözüm
- **Tek Cümlelik Özet:** *PRU Auto-Admin, yeni üyelerin kayıtlarını 30 saniyelik interaktif bir Telegram botuyla toplayıp Google Sheets ile buluta senkronize eden; yönetim kuruluna ise anlık analitik, yapay zeka destekli takım eşleştirme ve dijital QR üye kartları sunan kapsamlı bir kulüp işletim sistemidir.*
- **Ana Kullanıcı Akışı:**
  1. **Öğrenci:** Standdaki Telegram bağlantısına tıklar -> `/start` ile botu başlatır -> Ad-Soyad girer -> Piri Reis Üniversitesi bölümlerini ve ilgi alanlarını tek tıkla butonlardan seçer -> Anında onay ve dijital kayıt bilgisi alır.
  2. **Veri Motoru:** Bot verileri anlık olarak Google Sheets API (`gspread`) ve yerel yedek motoruna işler.
  3. **Yönetim Konsolu (Dashboard):** Kulüp yönetimi canlı Streamlit panelinden demografiyi inceler, TEKNOFEST/Hackathon için tek tıkla multidisipliner takımlar kurar, üyelere QR dijital kimlik kartı üretir ve komiteye özel WhatsApp duyuruları oluşturur.

---

## 3. Kim kullanacak?
1. **Kulüp Üyeleri ve Aday Öğrenciler (Son Kullanıcı):**
   - **Kullanım Amacı:** Kulübe resmi kayıt yaptırmak, komite tercihlerini iletmek ve etkinliklere girmek.
   - **Sıklık:** Dönem başında 1 kez (~30 saniye).
2. **Kulüp Yönetim Kurulu & Takım Liderleri (Yönetici):**
   - **Kullanım Amacı:** Bölüm ve üye dağılımını izlemek, yarışma takımları kurmak, etkinlik kapısında QR check-in yapmak ve sponsorlara demografik rapor sunmak.
   - **Sıklık:** Günlük ve haftalık düzenli operasyon.

---

## 4. Özellikler

### ✅ Çalışanlar (Tamamlanan Özellikler)
- **Adım Adım Telegram Bot Akışı:** Kullanıcıyı yönlendiren, kullanıcı girdilerini doğrulayan modern durum yönetimi (`register_next_step_handler`).
- **Piri Reis Üniversitesi Özel Klavye Menüleri:** Bölüm ve komiteler için tek tıkla seçim, sıfır yazım hatası.
- **Google Sheets API & Yerel Fail-Safe Modu:** API veya internet kesintilerinde otomatik yerel CSV (`data/members_backup.csv`) yedeğine geçiş.
- **🎯 AI & Kural Tabanlı Multidisipliner Takım Eşleştirici:** TEKNOFEST, Hackathon ve Zirve organizasyonları için üyelerin yeteneklerine göre dengeli (kaptan + mühendis + tasarımcı) takımlar kurma.
- **🪪 Dijital Üye Kartı & Çevrimdışı QR Check-In:** Her üye için dinamik kartvizit ve etkinlik yoklaması için anlık QR kod üretimi.
- **📢 WhatsApp & İletişim Otomasyon Kiti:** Komitelere özel tek tıkla kopyalanabilir duyuru şablonları ve telefon listeleri.
- **📱 Tarayıcı İçi Canlı Bot Simülatörü:** Jüri sunumunda telefon bağlantısına gerek kalmadan bota kayıt simülasyonu yapabilme.
- **📊 Gelişmiş Plotly Grafikleri & KPI Kartları:** Bölüm dağılımı (Donut), komite talepleri (Bar), kümülatif büyüme (Area) ve iletişim izin oranı (Pie).
- **📥 Excel/CSV Çıktı Motoru:** Filtrelenmiş üye listesini tek tıkla `utf-8-sig` formatında dışa aktarma.

### 🟡 Yarım Kalanlar (MVP Kapsamında Sınırlandırılanlar)
- **Doğrudan Telegram Üzerinden Toplu Mesaj (Broadcast):** Telegram Bot spam kuralları ve güvenlik sebebiyle toplu duyurular WhatsApp kiti üzerinden yürütülmektedir.

### 🚀 Planlananlar (Gelecek Yol Haritası)
- **Fakülte Dekanlığı İçin Tek Tıkla PDF Faaliyet Raporu:** Dönem sonu resmi faaliyet raporunu PDF formatında indirme.
- **Discord / GitHub Rol Senkronizasyonu:** Teknik komiteye kaydolan üyeye otomatik Discord rolü ve GitHub organizasyon daveti.

---

## 5. Teknik yapı
- **Programlama Dili:** Python 3.10+
- **Bot Katmanı:** `pyTelegramBotAPI` (Event-driven, conversational state machine)
- **Veri Depolama & API:** `Google Sheets API` (`gspread`, `google-auth`), Yerel `pandas` CSV Storage Engine
- **Web Yönetim Konsolu:** `Streamlit`
- **Veri Görselleştirme:** `Plotly Express & Graph Objects`
- **QR Kod Motoru:** `qrcode` (Tamamen çevrimdışı, harici API bağımlılığı sıfır)
- **Ortam Değişkenleri:** `python-dotenv`

---

## 6. Kurulum ve çalıştırma
Sistemi sıfırdan bir bilgisayarda **10 dakika içinde** ayağa kaldırmak için:

```bash
# 1. Proje dizinine geçin ve sanal ortamı kurun
git clone <repo-url>
cd pru-auto-admin
python -m venv venv
venv\Scripts\activate   # Windows

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Ortam dosyasını oluşturun (.env)
copy .env.example .env
# .env dosyasına TELEGRAM_BOT_TOKEN ekleyin (Google Cloud opsiyoneldir)

# 4. Çalıştırın:
# Terminal 1 (Bot):
python bot.py

# Terminal 2 (Dashboard):
streamlit run dashboard.py
```
*(Windows kullanıcıları doğrudan `run_dashboard.bat` ve `run_bot.bat` dosyalarına çift tıklayabilir).*

---

## 7. Onchain kısım (varsa)
**Yoktur.**

Hackathon şartnamesinde açıkça belirtildiği üzere: *"Onchain olmak zorunlu değildir; çalışan ve gerçekten kulübün işine yarayan bir ürün en yüksek puanı alır."*

Kulüp operasyonlarının çözülmesi gereken temel meselesi mutabakat (consensus) veya kripto transferi değil; **veri standardizasyonu, operasyonel iş gücü israfı ve yetenek eşleştirmesidir.** Üniversite kulüp standında yeni öğrencilere cüzdan açtırmaya çalışmak ve gas fee ödetmek katılımı felç eder. Projemiz bilinçli bir mühendislik kararıyla sıfır sürtünmeli, ücretsiz ve sürdürülebilir Web2 verimlilik standartlarına sadık kalmıştır.

---

## 8. Kulüp bunu nasıl devralır?
- **Yayına Alma (Deployment):**
  - **Dashboard:** [Streamlit Community Cloud](https://streamlit.io/cloud) üzerine ücretsiz tek tıkla deploy edilir.
  - **Telegram Bot:** [Render](https://render.com) veya üniversite sunucusunda 7/24 ücretsiz background daemon olarak çalıştırılır.
- **Sürdürülebilirlik:** Kod tamamen modülerdir; yeni dönemde sadece Google Sheets tablosu güncellenir.
- **Maliyet:** **0 TL (Tamamen Ücretsiz).**

---

## 9. Hazır kullanılanlar ve yapay zeka kullanımı
- **Kütüphaneler:** `pyTelegramBotAPI`, `gspread`, `google-auth`, `pandas`, `streamlit`, `plotly`, `qrcode`, `Pillow`, `python-dotenv`.
- **Yapay Zeka (AI) Kullanımı:** Veri modelleme mimarisi, Piri Reis Üniversitesi bölümlerine göre kural tabanlı takım eşleştirme algoritması ve çok sekmeli SaaS arayüz tasarımında pair-programming asistanı olarak yapay zekadan faydalanılmıştır.

---

## 10. Takım
- **Full-Stack & Veri Mühendisi:** Bot durum yönetimi, Google Sheets API entegrasyonu, veri mimarisi ve hata toleransı.
- **Veri Analisti & UI/UX Geliştirici:** Streamlit analitik paneli tasarımı, Plotly görselleştirmeleri, akıllı takım eşleştirici ve kullanıcı deneyimi.
