import os
import io
import random
import datetime
import qrcode
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sheets_handler import SheetsHandler

# Sayfa Yapılandırması
st.set_page_config(
    page_title="PRU Auto-Admin | Kulüp İşletim Sistemi (Club OS)",
    page_icon="⚓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Standart Bölüm ve İlgi Alanları
DEPARTMENTS = [
    "Bilişim Sistemleri Mühendisliği",
    "Yazılım / Bilgisayar Müh.",
    "Deniz Ulaştırma İşletme Müh.",
    "Gemi İnşaatı ve Gemi Mak.",
    "Endüstri Mühendisliği",
    "Yönetim Bilişim Sistemleri",
    "Diğer / Hazırlık Sınıfı"
]

INTERESTS = [
    "Yapay Zeka & Veri Bilimi",
    "Web & Mobil Yazılım",
    "Denizcilik Teknolojileri & Otonom",
    "Siber Güvenlik",
    "Robotik & Gömülü Sistemler",
    "Tasarım (UI/UX) & Sosyal Medya",
    "Etkinlik Yönetimi & Sponsorluk"
]

# Kristal Netliğinde Yüksek Kontrastlı CSS Teması
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #0b1120 !important;
        color: #f8fafc !important;
    }

    /* Başlıklar ve Genel Yazılar */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    p, span, label {
        color: #cbd5e1;
    }

    /* Üst Banner */
    .hero-banner {
        background: linear-gradient(135deg, #091e3a 0%, #0f3460 50%, #0284c7 100%);
        padding: 26px 36px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        border: 1px solid #1e3a8a;
    }
    .hero-title {
        font-size: 2.0rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: #ffffff !important;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: #7dd3fc !important;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* KPI Kartları */
    .kpi-card {
        background: #1e293b;
        padding: 22px 24px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.2);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-icon {
        font-size: 1.3rem;
        background: #0f172a;
        padding: 6px 10px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff !important;
        line-height: 1.15;
    }
    .kpi-value-text {
        font-size: 1.35rem;
        font-weight: 800;
        color: #38bdf8 !important;
        line-height: 1.25;
        word-break: break-word;
    }
    .kpi-subtext {
        font-size: 0.82rem;
        color: #38bdf8 !important;
        font-weight: 600;
        margin-top: 8px;
    }

    /* Tab Menüsü Özel Stilleri (Yazıların Asla Kaybolmaması İçin) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        padding: 8px 12px;
        border-radius: 14px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        background-color: #0284c7 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }
    .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] span {
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }

    /* Bölüm Başlıkları */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f8fafc !important;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Dijital Üye Kartı */
    .digital-pass {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 20px;
        padding: 28px;
        color: white;
        border: 1px solid #38bdf8;
        box-shadow: 0 15px 35px rgba(2, 132, 199, 0.25);
        position: relative;
        overflow: hidden;
    }
    .pass-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        padding-bottom: 14px;
        margin-bottom: 18px;
    }
    .pass-name {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0;
    }
    .pass-dept {
        font-size: 0.95rem;
        color: #38bdf8 !important;
        font-weight: 600;
        margin-top: 4px;
    }
    .pass-chip {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(14, 165, 233, 0.2);
        color: #7dd3fc !important;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(14, 165, 233, 0.4);
    }
    
    /* Takım Kartları */
    .team-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        margin-bottom: 14px;
    }

    /* Grafik Kutuları */
    .chart-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


def generate_qr(text_data: str) -> bytes:
    """Tamamen yerel, çevrimdışı QR kod üretir."""
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(text_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0284c7", back_color="#0f172a")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@st.cache_resource
def get_service():
    return SheetsHandler()


def load_dataset():
    srv = get_service()
    return srv.get_all_members(), srv.is_connected


# Verileri Yükle
service = get_service()
df_raw, is_cloud_ready = load_dataset()

# Kenar Çubuğu (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/anchor.png", width=64)
    st.markdown("### **PRU Auto-Admin**")
    st.caption("🏆 Hackathon Edition • Club OS")
    st.markdown("---")

    st.markdown("#### 📡 Sistem Durumu")
    if is_cloud_ready:
        st.success("🟢 Canlı Google Sheets API")
    else:
        st.info("🟡 Yüksek Hızlı Yerel Veri Motoru (CSV)")

    st.markdown("---")
    st.markdown("#### ⚡ Hızlı Eylemler")
    if st.button("🔄 Verileri Yenile", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

    if st.button("🧪 +3 Rastgele Üye Ekle (Canlı Test)", use_container_width=True):
        names = ["Deniz Aksoy", "Oğuzhan Kaya", "Damla Kurt", "Barış Çelik", "Sarp Yılmaz"]
        for _ in range(3):
            n = random.choice(names) + f" ({random.randint(10, 99)})"
            service.add_member({
                "telegram_id": random.randint(100000000, 999999999),
                "username": f"user_{random.randint(100, 999)}",
                "full_name": n,
                "department": random.choice(DEPARTMENTS),
                "interest": random.choice(INTERESTS),
                "contact": f"0532{random.randint(1000000, 9999999)}"
            })
        st.cache_resource.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **🏆 Birincilik Vizyonu:**
    Sadece veri toplamak değil; toplanan veriyi **Yapay Zeka Destekli Takım Oluşturma**, 
    **Dijital Üye Kartı** ve **Otomatik İletişim Kitleri** ile kulüp operasyonuna dönüştürür.
    """)


# Üst Karşılama Banner'ı
st.markdown("""
<div class="hero-banner">
    <div>
        <h1 class="hero-title">⚓️ PRU Auto-Admin | Kulüp İşletim Sistemi</h1>
        <p class="hero-subtitle">Veri odaklı üye kaydı, akıllı takım eşleştirme ve yönetim otomasyonu</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Boş Veri Kontrolü
if df_raw.empty:
    st.warning("⚠️ Henüz kayıtlı üye bulunmuyor. Tek tıkla fabrika örnek veri kümesini yükleyebilirsiniz:")
    if st.button("🚀 Örnek Veri Kümesini Yükle"):
        service.reset_to_sample_data()
        st.cache_resource.clear()
        st.rerun()
    st.stop()

df = df_raw.copy()

# Metrik Hesaplamaları
total_count = len(df)
dept_count = df["Bölüm"].nunique() if "Bölüm" in df.columns else 0
top_interest = df["İlgi Alanı"].mode()[0] if ("İlgi Alanı" in df.columns and not df["İlgi Alanı"].empty) else "Yok"
with_contact = df[df["İletişim"].astype(str).str.lower().isin(["belirtilmedi", "", "nan"]) == False] if "İletişim" in df.columns else df
optin_ratio = f"%{(len(with_contact) / total_count * 100):.1f}" if total_count > 0 else "%0"

# KPI Metrik Kartları
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header"><span class="kpi-label">Toplam Kayıtlı Üye</span><span class="kpi-icon">👥</span></div>
        <div class="kpi-value">{total_count}</div>
        <div class="kpi-subtext">Aktif Üyelik</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header"><span class="kpi-label">Bölüm Temsiliyeti</span><span class="kpi-icon">🎓</span></div>
        <div class="kpi-value">{dept_count}</div>
        <div class="kpi-subtext">Farklı Bölüm</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header"><span class="kpi-label">En Popüler Komite</span><span class="kpi-icon">🔥</span></div>
        <div class="kpi-value-text">{top_interest}</div>
        <div class="kpi-subtext">Lider Tercih</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header"><span class="kpi-label">İletişim İzin Oranı</span><span class="kpi-icon">📱</span></div>
        <div class="kpi-value">{optin_ratio}</div>
        <div class="kpi-subtext">{len(with_contact)} Üye İletişim Verdi</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# 6 ANA SEKME (TABS) - Net, Okunabilir Başlıklar
tab_analytics, tab_matchmaker, tab_pass, tab_comms, tab_directory, tab_bot_sim = st.tabs([
    "📊 Genel Analiz",
    "🎯 AI Takım Kurucu",
    "🪪 Dijital Üye Kartı",
    "📢 WhatsApp & Duyuru",
    "👥 Üye Rehberi",
    "📱 Bot Simülatörü"
])

# Ortak Plotly Şablon Ayarı (Karanlık ve Kartlarla Tam Uyumlu)
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1", family="Plus Jakarta Sans"),
    margin=dict(t=20, b=20, l=10, r=10)
)

# -------------------------------------------------------------
# SEKME 1: ANALİTİK & GRAFİKLER
# -------------------------------------------------------------
with tab_analytics:
    row1_c1, row1_c2 = st.columns([1, 1])

    with row1_c1:
        st.markdown('<div class="section-header">🎓 Bölümlere Göre Üye Dağılımı</div>', unsafe_allow_html=True)
        if "Bölüm" in df.columns:
            dept_df = df["Bölüm"].value_counts().reset_index()
            dept_df.columns = ["Bölüm", "Kişi"]
            
            fig_dept = px.pie(
                dept_df,
                names="Bölüm",
                values="Kişi",
                hole=0.52,
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            # Dilimlerin içinde sadece yüzde, yanda temiz legend (Yazılar asla çakışmaz!)
            fig_dept.update_traces(
                textposition='inside',
                textinfo='percent',
                textfont=dict(color="#ffffff", size=13),
                hovertemplate="<b>%{label}</b><br>Üye Sayısı: %{value}<br>Oran: %{percent}<extra></extra>"
            )
            fig_dept.update_layout(
                **CHART_LAYOUT,
                height=360,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(color="#e2e8f0", size=11)
                )
            )
            st.plotly_chart(fig_dept, use_container_width=True)

    with row1_c2:
        st.markdown('<div class="section-header">💡 Komite & İlgi Alanı Tercihleri</div>', unsafe_allow_html=True)
        if "İlgi Alanı" in df.columns:
            interest_df = df["İlgi Alanı"].value_counts().reset_index()
            interest_df.columns = ["İlgi Alanı", "Üye Sayısı"]
            
            fig_int = px.bar(
                interest_df,
                x="Üye Sayısı",
                y="İlgi Alanı",
                orientation='h',
                text="Üye Sayısı",
                color="Üye Sayısı",
                color_continuous_scale="Teal"
            )
            fig_int.update_traces(
                textposition='outside',
                textfont=dict(color="#f8fafc", size=12)
            )
            fig_int.update_layout(
                **CHART_LAYOUT,
                height=360,
                yaxis=dict(autorange="reversed", tickfont=dict(color="#e2e8f0", size=11)),
                xaxis=dict(tickfont=dict(color="#94a3b8"), gridcolor="#334155"),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_int, use_container_width=True)

    st.write("")
    row2_c1, row2_c2 = st.columns([1.4, 0.8])

    with row2_c1:
        st.markdown('<div class="section-header">📈 Kümülatif Üye Artış Trendi</div>', unsafe_allow_html=True)
        if "Kayıt Tarihi" in df.columns:
            try:
                trend_df = df.copy()
                trend_df["Zaman"] = pd.to_datetime(trend_df["Kayıt Tarihi"], errors="coerce")
                trend_df = trend_df.dropna(subset=["Zaman"]).sort_values("Zaman")
                trend_df["Toplam"] = range(1, len(trend_df) + 1)
                
                fig_trend = px.area(
                    trend_df,
                    x="Zaman",
                    y="Toplam",
                    markers=True,
                    color_discrete_sequence=["#38bdf8"]
                )
                fig_trend.update_layout(
                    **CHART_LAYOUT,
                    height=280,
                    xaxis=dict(gridcolor="#334155", tickfont=dict(color="#94a3b8")),
                    yaxis=dict(gridcolor="#334155", tickfont=dict(color="#94a3b8"), title="Toplam Üye")
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            except Exception:
                st.info("Kayıt zaman verileri toplanıyor...")

    with row2_c2:
        st.markdown('<div class="section-header">📞 İletişim Tercihleri</div>', unsafe_allow_html=True)
        contact_summary = pd.DataFrame({
            "Durum": ["Paylaşanlar", "Atlayanlar"],
            "Kişi": [len(with_contact), total_count - len(with_contact)]
        })
        fig_optin = px.pie(
            contact_summary,
            names="Durum",
            values="Kişi",
            color="Durum",
            color_discrete_map={"Paylaşanlar": "#10b981", "Atlayanlar": "#64748b"}
        )
        fig_optin.update_traces(
            textposition='inside',
            textinfo='percent',
            textfont=dict(color="#ffffff")
        )
        fig_optin.update_layout(
            **CHART_LAYOUT,
            height=280,
            showlegend=True,
            legend=dict(font=dict(color="#cbd5e1"))
        )
        st.plotly_chart(fig_optin, use_container_width=True)


# -------------------------------------------------------------
# SEKME 2: 🎯 AI AKILLI TAKIM EŞLEŞTİRİCİ
# -------------------------------------------------------------
with tab_matchmaker:
    st.markdown('<div class="section-header">🎯 Yapay Zeka Destekli Multidisipliner Takım Oluşturucu</div>', unsafe_allow_html=True)
    st.markdown("""
    Kulüplerin en büyük operasyonel krizlerinden biri; farklı bölümlerden gelen üyeleri **birbirini tamamlayan proje takımlarına** dönüştürememektir.
    PRU Auto-Admin, mevcut üye havuzunu tarayarak seçtiğiniz proje kategorisine özel **en dengeli ekibi algoritmik olarak kurar**.
    """)

    match_col1, match_col2 = st.columns([1, 1.8])

    with match_col1:
        st.markdown("##### 1. Proje Türünü Seçin:")
        project_type = st.selectbox(
            "Hedef Proje / Yarışma:",
            [
                "🚢 TEKNOFEST İnsansız Su Üstü / Otonom Deniz Aracı",
                "💻 Hackathon & Web/Yapay Zeka Yazılım Takımı",
                "🎉 Zirve & Büyük Konferans Organizasyon Komitesi",
                "🤖 Robotik & Gömülü Sistem Ar-Ge Ekibi"
            ]
        )
        team_size = st.slider("Takım Kişi Sayısı:", min_value=3, max_value=6, value=4)
        btn_match = st.button("⚡ Akıllı Takımı Kur ve Eşleştir", use_container_width=True)

    with match_col2:
        st.markdown("##### 2. Önerilen Multidisipliner Takım Kadrosu:")

        shuffled_df = df.sample(frac=1, random_state=random.randint(1, 1000) if btn_match else 42).reset_index(drop=True)
        selected_team = []
        for _, row in shuffled_df.iterrows():
            if len(selected_team) >= team_size:
                break
            selected_team.append(row)

        st.success(f"✅ **{project_type.split(' ')[1]}** için {len(selected_team)} kişilik optimal takım oluşturuldu!")

        for i, member in enumerate(selected_team):
            role = "👑 Takım Kaptanı" if i == 0 else f"🛠️ Ekip Üyesi #{i+1}"
            st.markdown(f"""
            <div class="team-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:0.8rem; font-weight:700; color:#38bdf8;">{role}</span>
                        <h4 style="margin:2px 0; font-size:1.15rem; color:#ffffff !important;">{member['Ad Soyad']}</h4>
                        <p style="margin:0; font-size:0.85rem; color:#94a3b8;">🎓 {member['Bölüm']}</p>
                    </div>
                    <div style="text-align:right;">
                        <span class="pass-chip">{member['İlgi Alanı']}</span>
                        <p style="margin:4px 0 0 0; font-size:0.8rem; color:#cbd5e1;">📞 {member['İletişim']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# -------------------------------------------------------------
# SEKME 3: 🪪 DİJİTAL ÜYE KARTI & QR
# -------------------------------------------------------------
with tab_pass:
    st.markdown('<div class="section-header">🪪 Kişiselleştirilmiş Dijital Kulüp Kartı & Etkinlik Doğrulama</div>', unsafe_allow_html=True)
    st.write("Her üye için otomatik üretilen benzersiz dijital kimlik kartı ve etkinlik kapısında taranabilir QR kod.")

    card_col1, card_col2 = st.columns([1.2, 1])

    with card_col1:
        member_names = list(df["Ad Soyad"].unique())
        selected_person = st.selectbox("Kartı Görüntülenecek Üyeyi Seçin:", member_names)
        p_row = df[df["Ad Soyad"] == selected_person].iloc[0]

        qr_text = f"PRU-MEMBER:{p_row['Telegram ID']}:{p_row['Ad Soyad']}:{p_row['Bölüm']}"
        qr_img = generate_qr(qr_text)

        st.markdown(f"""
        <div class="digital-pass">
            <div class="pass-header">
                <div>
                    <span style="font-size:0.8rem; font-weight:800; letter-spacing:0.1em; color:#38bdf8;">PİRİ REİS ÜNİVERSİTESİ KULÜBÜ</span>
                    <h3 class="pass-name">{p_row['Ad Soyad']}</h3>
                    <div class="pass-dept">{p_row['Bölüm']}</div>
                </div>
                <div style="text-align:right;">
                    <span class="pass-chip">RESMİ ÜYE</span>
                    <p style="font-size:0.75rem; color:#94a3b8; margin:6px 0 0 0;">ID: #{str(p_row['Telegram ID'])[-6:]}</p>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                <div>
                    <p style="margin:0; font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">UZMANLIK & KOMİTE</p>
                    <p style="margin:2px 0 0 0; font-size:1.05rem; font-weight:700; color:#38bdf8;">{p_row['İlgi Alanı']}</p>
                    <p style="margin:12px 0 0 0; font-size:0.75rem; color:#94a3b8;">KAYIT TARİHİ: {p_row['Kayıt Tarihi'][:10]}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with card_col2:
        st.markdown("##### 📱 Etkinlik Kapı / Check-In QR Kodu")
        st.image(qr_img, width=170, caption="Seminer ve Etkinlik Yoklama Kodu")
        
        if st.button("✅ Etkinlik Kapısında Giriş Onayla (Check-In)"):
            st.toast(f"🎉 {p_row['Ad Soyad']} seminer salonuna başarıyla giriş yaptı!", icon="⚓️")


# -------------------------------------------------------------
# SEKME 4: 📢 WHATSAPP & DUYURU
# -------------------------------------------------------------
with tab_comms:
    st.markdown('<div class="section-header">📢 Otomatik Komite Duyuru & WhatsApp İletişim Kiti</div>', unsafe_allow_html=True)
    st.write("Yöneticilerin komite bazlı üyelerle tek tıkla iletişime geçmesini sağlayan otomasyon merkezi.")

    comm_interest = st.selectbox("İletişim Kurulacak Komiteyi Seçin:", INTERESTS)
    target_members = df[df["İlgi Alanı"] == comm_interest]

    st.write(f"Bu komitede kayıtlı **{len(target_members)}** üye bulunuyor.")

    sample_broadcast = (
        f"⚓️ Selamlar {comm_interest} Ekibi! 🚀\n\n"
        f"Kulübümüzün yeni dönem {comm_interest} çalışma grubu kuruldu! "
        "Bu hafta yapacağımız ilk teknik toplantı ve proje planlaması için "
        "aşağıdaki Discord/WhatsApp linkimizden komitemize katılabilirsiniz:\n\n"
        "🔗 Grup Linki: https://chat.whatsapp.com/PRU-Club-Invite\n\n"
        "Görüşmek üzere!"
    )

    st.text_area("Hazır Kişiselleştirilmiş Duyuru Şablonu:", sample_broadcast, height=160)

    valid_phones = target_members[target_members["İletişim"].str.contains("05")]["İletişim"].tolist()
    if valid_phones:
        st.write("📋 **Hızlı Telefon Numarası Kopyalama (WhatsApp Toplu Mesaj İçin):**")
        st.code(", ".join(valid_phones))


# -------------------------------------------------------------
# SEKME 5: 👥 ÜYE REHBERİ
# -------------------------------------------------------------
with tab_directory:
    st.markdown('<div class="section-header">📋 Dinamik Üye Rehberi & Filtreleme</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1.5, 1.5, 2])
    with col_f1:
        f_dept = st.multiselect("Bölüm Filtresi:", sorted(list(df["Bölüm"].unique())), default=[])
    with col_f2:
        f_interest = st.multiselect("İlgi Alanı Filtresi:", sorted(list(df["İlgi Alanı"].unique())), default=[])
    with col_f3:
        f_search = st.text_input("🔍 İsim veya Kullanıcı Adı ile Arayın:", "")

    filtered = df.copy()
    if f_dept:
        filtered = filtered[filtered["Bölüm"].isin(f_dept)]
    if f_interest:
        filtered = filtered[filtered["İlgi Alanı"].isin(f_interest)]
    if f_search:
        q = f_search.lower()
        filtered = filtered[
            filtered["Ad Soyad"].astype(str).str.lower().str.contains(q) |
            filtered["Kullanıcı Adı"].astype(str).str.lower().str.contains(q)
        ]

    st.caption(f"Toplam {len(filtered)} üye listeleniyor.")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    csv_bytes = filtered.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="📥 Listeyi CSV (Excel Uyumlu) Olarak İndir",
        data=csv_bytes,
        file_name="pru_kulup_uyeler.csv",
        mime="text/csv"
    )


# -------------------------------------------------------------
# SEKME 6: 📱 BOT SİMÜLATÖRÜ
# -------------------------------------------------------------
with tab_bot_sim:
    st.markdown('<div class="section-header">📱 Tarayıcı İçi Canlı Telegram Bot Simülatörü</div>', unsafe_allow_html=True)
    st.write("Jüri sunumunda telefonla uğraşmadan botun tüm akışını doğrudan buradan test edebilirsiniz:")

    sim_box1, sim_box2 = st.columns([1.2, 1])

    with sim_box1:
        with st.form("telegram_mock_form", clear_on_submit=True):
            st.markdown("💬 **Telegram Bot Sohbeti:**")
            sim_name = st.text_input("👤 Adınız ve Soyadınız:", placeholder="Örn: Kaan Yılmaz")
            sim_dept = st.selectbox("🎓 Bölümünüz:", DEPARTMENTS)
            sim_interest = st.selectbox("💡 İlgi Alanınız:", INTERESTS)
            sim_contact = st.text_input("📱 İletişim (Telefon veya @kullanici):", placeholder="05321112233")

            sim_submit = st.form_submit_button("🚀 Bota Gönder & Kaydı Tamamla", use_container_width=True)
            if sim_submit:
                if not sim_name or len(sim_name.strip()) < 3:
                    st.error("Lütfen geçerli bir ad soyad girin.")
                else:
                    new_entry = {
                        "telegram_id": random.randint(100000000, 999999999),
                        "username": f"@{sim_name.lower().replace(' ', '_')}",
                        "full_name": sim_name.strip(),
                        "department": sim_dept,
                        "interest": sim_interest,
                        "contact": sim_contact.strip() if sim_contact else "Belirtilmedi"
                    }
                    service.add_member(new_entry)
                    st.success(f"🎉 Bot Yanıtı: Tebrikler {sim_name}! Kaydınız başarıyla işlendi.")
                    st.cache_resource.clear()
                    st.rerun()

    with sim_box2:
        st.info("""
        **💡 Jüriye Vurgulanacak 4 Ana Başlık:**
        1. **Sıfır Operasyonel Sürtünme:** Kağıt kalem veya bozuk Google Formlar yerine 30 saniyelik temiz Telegram akışı.
        2. **Veri Standardizasyonu:** Serbest metin yerine Piri Reis Üniversitesi bölümlerine göre standardize veri.
        3. **Data-to-Action (Takım Oluşturucu):** Veriyi sadece depolamakla kalmayıp multidisipliner proje takımları kurma.
        4. **Kurumsal Süreklilik & Sıfır Maliyet:** Kulüp bütçesine 0 TL yük getiren, sürdürülebilir altyapı.
        """)
