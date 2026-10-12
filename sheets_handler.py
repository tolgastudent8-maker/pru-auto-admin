import os
import datetime
import pandas as pd
from typing import Dict, Any, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

LOCAL_BACKUP_PATH = os.path.join(os.path.dirname(__file__), "data", "members_backup.csv")
COLUMNS = [
    "Kayıt Tarihi",
    "Telegram ID",
    "Kullanıcı Adı",
    "Ad Soyad",
    "Bölüm",
    "İlgi Alanı",
    "İletişim",
    "Durum"
]

SAMPLE_DATA = [
    ["2026-10-12 10:15:22", "109283741", "@tolga_akgul", "Tolga Akgül", "Bilişim Sistemleri Mühendisliği", "Yapay Zeka & Veri Bilimi", "05551234567", "Onaylandı"],
    ["2026-10-12 10:22:40", "108273645", "@deniz_k", "Deniz Kara", "Deniz Ulaştırma İşletme Müh.", "Denizcilik Teknolojileri & Otonom", "deniz@pru.edu.tr", "Onaylandı"],
    ["2026-10-12 11:05:12", "107382910", "@selin_y", "Selin Yıldız", "Yazılım / Bilgisayar Müh.", "Web & Mobil Yazılım", "05329876543", "Onaylandı"],
    ["2026-10-12 11:40:19", "106492831", "@can_ozturk", "Can Öztürk", "Gemi İnşaatı ve Gemi Mak.", "Robotik & Gömülü Sistemler", "can.ozturk@mail.com", "Onaylandı"],
    ["2026-10-12 12:15:33", "105827192", "@ayse_demir", "Ayşe Demir", "Bilişim Sistemleri Mühendisliği", "Yapay Zeka & Veri Bilimi", "05443332211", "Onaylandı"],
    ["2026-10-12 13:02:45", "104928371", "@mert_kaya", "Mert Kaya", "Yazılım / Bilgisayar Müh.", "Siber Güvenlik", "mert@gmail.com", "Onaylandı"],
    ["2026-10-12 13:45:10", "103827162", "@zeynep_b", "Zeynep Bulut", "Endüstri Mühendisliği", "Etkinlik Yönetimi & Sponsorluk", "05335556677", "Onaylandı"],
    ["2026-10-12 14:10:55", "102738491", "@burak_g", "Burak Güler", "Deniz Ulaştırma İşletme Müh.", "Denizcilik Teknolojileri & Otonom", "Belirtilmedi", "Onaylandı"],
    ["2026-10-12 14:35:18", "101827394", "@irem_celik", "İrem Çelik", "Yönetim Bilişim Sistemleri", "Tasarım (UI/UX) & Sosyal Medya", "irem@pru.edu.tr", "Onaylandı"],
    ["2026-10-12 15:20:04", "100928385", "@emre_t", "Emre Tekin", "Bilişim Sistemleri Mühendisliği", "Web & Mobil Yazılım", "05051112233", "Onaylandı"],
    ["2026-10-12 15:50:31", "100192837", "@alperen_v", "Alperen Vural", "Gemi İnşaatı ve Gemi Mak.", "Robotik & Gömülü Sistemler", "alperen@mail.com", "Onaylandı"],
    ["2026-10-12 16:30:12", "100293847", "@melisa_a", "Melisa Arslan", "Bilişim Sistemleri Mühendisliği", "Yapay Zeka & Veri Bilimi", "05342223344", "Onaylandı"],
    ["2026-10-12 16:45:50", "100382918", "@kaan_y", "Kaan Yılmaz", "Deniz Ulaştırma İşletme Müh.", "Denizcilik Teknolojileri & Otonom", "kaan@pru.edu.tr", "Onaylandı"],
    ["2026-10-12 17:00:15", "100472819", "@ece_s", "Ece Şen", "Yazılım / Bilgisayar Müh.", "Yapay Zeka & Veri Bilimi", "05558887766", "Onaylandı"]
]


class SheetsHandler:
    """
    Google Sheets API (gspread) ile entegrasyonu yöneten servis sınıfı.
    Eğer Google kimlik dosyası (credentials.json) bulunamazsa veya API hatası alınırsa,
    hackathon/demo sırasında sistemin çökmemesi için otomatik olarak yerel CSV moduna geçer.
    """

    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
        self.sheet_name = os.getenv("SPREADSHEET_NAME", "PRU_Auto_Admin_Uyeler")
        self.is_connected = False
        self.worksheet = None

        self._init_connection()

    def _init_connection(self):
        """Google Sheets bağlantısını kurar, yoksa yerel veri deposunu hazırlar."""
        if os.path.exists(self.credentials_path):
            try:
                import gspread
                gc = gspread.service_account(filename=self.credentials_path)
                try:
                    spreadsheet = gc.open(self.sheet_name)
                except gspread.SpreadsheetNotFound:
                    spreadsheet = gc.create(self.sheet_name)
                    print(f"[BİLGİ] '{self.sheet_name}' tablosu Google Drive'da yeni oluşturuldu.")

                self.worksheet = spreadsheet.sheet1
                existing_values = self.worksheet.get_all_values()
                if not existing_values or len(existing_values) == 0:
                    self.worksheet.append_row(COLUMNS)
                
                self.is_connected = True
                print(f"[BAŞARILI] Google Sheets bağlantısı kuruldu: {self.sheet_name}")
                return
            except Exception as e:
                print(f"[UYARI] Google Sheets bağlantı hatası: {e}")
                print("[BİLGİ] Yerel CSV (Demo/Offline) moduna geçiliyor...")
        else:
            print(f"[BİLGİ] '{self.credentials_path}' bulunamadı. Yerel CSV (Demo/Offline) modu devrede.")

        self._ensure_local_backup()

    def _ensure_local_backup(self):
        """Yerel CSV dosyasını ve klasörünü hazırlar. Yoksa örnek verilerle doldurur."""
        os.makedirs(os.path.dirname(LOCAL_BACKUP_PATH), exist_ok=True)
        if not os.path.exists(LOCAL_BACKUP_PATH) or os.path.getsize(LOCAL_BACKUP_PATH) == 0:
            df = pd.DataFrame(SAMPLE_DATA, columns=COLUMNS)
            df.to_csv(LOCAL_BACKUP_PATH, index=False, encoding="utf-8-sig")

    def add_member(self, member_data: Dict[str, Any]) -> bool:
        """Yeni bir üyeyi Google Sheets'e veya yerel CSV'ye ekler."""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = member_data.get("username", "")
        if username and not username.startswith("@"):
            username = f"@{username}"
        elif not username:
            username = "Belirtilmedi"

        row = [
            now_str,
            str(member_data.get("telegram_id", "Web-Panel")),
            username,
            member_data.get("full_name", "İsimsiz Üye"),
            member_data.get("department", "Diğer / Hazırlık Sınıfı"),
            member_data.get("interest", "Genel Katılım"),
            member_data.get("contact", "Belirtilmedi"),
            "Onaylandı"
        ]

        if self.is_connected and self.worksheet:
            try:
                self.worksheet.append_row(row)
                self._append_to_local_csv(row)
                return True
            except Exception as e:
                print(f"[HATA] Google Sheets'e yazılamadı: {e}. Yerel CSV'ye yazılıyor.")

        return self._append_to_local_csv(row)

    def _append_to_local_csv(self, row: List[Any]) -> bool:
        try:
            self._ensure_local_backup()
            df_new = pd.DataFrame([row], columns=COLUMNS)
            df_new.to_csv(LOCAL_BACKUP_PATH, mode="a", header=False, index=False, encoding="utf-8-sig")
            return True
        except Exception as e:
            print(f"[KRİTİK] Yerel CSV yazma hatası: {e}")
            return False

    def get_all_members(self) -> pd.DataFrame:
        """Tüm kayıtları döndürür."""
        if self.is_connected and self.worksheet:
            try:
                records = self.worksheet.get_all_records()
                if records:
                    df = pd.DataFrame(records)
                    return df
            except Exception as e:
                print(f"[UYARI] Google Sheets okunamadı: {e}. Yerel CSV'ye dönülüyor.")

        self._ensure_local_backup()
        try:
            df = pd.read_csv(LOCAL_BACKUP_PATH, encoding="utf-8-sig")
            return df
        except Exception as e:
            print(f"[HATA] Yerel CSV okunamadı: {e}")
            return pd.DataFrame(columns=COLUMNS)

    def reset_to_sample_data(self) -> bool:
        """Demo/Jüri sunumu için verileri örnek sete sıfırlar."""
        try:
            os.makedirs(os.path.dirname(LOCAL_BACKUP_PATH), exist_ok=True)
            df = pd.DataFrame(SAMPLE_DATA, columns=COLUMNS)
            df.to_csv(LOCAL_BACKUP_PATH, index=False, encoding="utf-8-sig")
            return True
        except Exception as e:
            print(f"[HATA] Veri sıfırlama başarısız: {e}")
            return False
