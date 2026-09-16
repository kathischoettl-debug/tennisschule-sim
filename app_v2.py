import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tennisschule Business Simulator v2", layout="wide")

st.title("🎾 Tennisschule Business Simulator v2 – Interaktive Case Study")

# --- INITIALISIERUNG DES SPEICHERS ---
if "runde" not in st.session_state:
    st.session_state.runde = 1
    st.session_state.kapital = 30000.0
    st.session_state.kundenstamm = 120
    st.session_state.image_score = 50
    st.session_state.has_bespannmaschine = False
    st.session_state.historie = []

EVENTS = {
    1: "🌱 **Jahr 1 – Marktstart:** Baue deine Tennisschule auf. Balance zwischen Breitensport, Leistungssport und Shop-Risiko finden.",
    2: "🎒 **Jahr 2 – Schulreform (G8/G9):** Mehr Nachmittagsunterricht! Hoher Einteilungs- und Koordinationsaufwand für passende Zeiten.",
    3: "🏆 **Jahr 3 – Turniersieg & Boom:** Ein Nachwuchstalent gewinnt die Bezirksmeisterschaft! Image steigt, Ausrüster-Interesse wächst.",
    4: "⚡ **Jahr 4 – Energiekrise & Kollektionswechsel:** Die Hallenheizkosten steigen extrem. Zudem wechselt der Ausrüster die Kollektion – Restware verliert an Wert!",
    5: "🏬 **Jahr 5 – Konkurrenz:** Ein Discounter eröffnet in der Nähe. Nur hohe Zufriedenheit hält Kunden trotz hoher Preise."
}

# --- STATUS-LEISTE ---
st.markdown("### 📌 Status der Tennisschule")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Aktuelles Jahr", f"Jahr {st.session_state.runde} / 5")
m2.metric("Bankguthaben", f"{st.session_state.kapital:,.0f} €")
m3.metric("Kundenstamm", f"{st.session_state.kundenstamm} Schüler")
m4.metric("Image / Sponsoren", f"{st.session_state.image_score} / 100")

if st.session_state.runde <= 5:
    st.info(EVENTS.get(st.session_state.runde, "Standard-Geschäftsjahr"))

if st.session_state.runde > 5:
    st.balloons()
    st.success(f"🏆 **Simulation beendet!** Endkapital: **{st.session_state.kapital:,.0f} €** | Kunden: **{st.session_state.kundenstamm}**.")
    if st.button("🔄 Neu starten"):
        st.session_state.runde = 1
        st.session_state.kapital = 30000.0
        st.session_state.kundenstamm = 120
        st.session_state.image_score = 50
        st.session_state.has_bespannmaschine = False
        st.session_state.historie = []
        st.rerun()
    st.stop()

st.markdown("---")
st.subheader(f"⚙️ Entscheidungen für Jahr {st.session_state.runde}")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("#### 1. Kursstruktur & Einteilung")
    gruppengroesse = st.slider("Ziel-Gruppengröße", 1, 5, 3, help="Kleine Gruppen = Hohe Qualität, aber extrem hoher Koordinationsaufwand & Ausfallrisiko!")
    einteilungs_fokus = st.select_slider("Einteilungs-Sorgfalt", options=["Pragmatisch (Wenig Aufwand)", "Mittel", "Perfekt Homogen (Hohe Kosten)"])
    preis_stunde = st.slider("Preis pro Schüler/Stunde (€)", 15, 60, 30)

with col2:
    st.write("#### 2. Trainer-Team & Marketing")
    anteil_nachwuchs = st.slider("Anteil Nachwuchs/Assistenten (%)", 0, 80, 25)
    misch_lohn = (1 - anteil_nachwuchs/100) * 55 + (anteil_nachwuchs/100) * 20
    st.caption(f"Mittlerer Trainerlohn: **{misch_lohn:.1f} €/h**")
    marketing = st.slider("Marketing & Events (€)", 0, 5000, 1000)

with col3:
    st.write("#### 3. Shop & Besaitungsservice")
    has_shop = st.checkbox("Tennisshop betreiben", value=False)
    vororder_volumen = st.slider("Shop Vororder-Volumen (€)", 1000, 10000, 3000) if has_shop else 0
    
    has_besaitung = st.checkbox("Besaitungs-Service anbieten", value=False)
    if has_besaitung and not st.session_state.has_bespannmaschine:
        st.warning("⚠️ Erstinvestition: Professionelle Besaitungsmaschine kostet einmalig **1.800 €**.")

# --- SIMULATION BEFEHL ---
if st.button(f"⏩ Jahr {st.session_state.runde} simulieren"):
    
    investitionen = 0
    if has_besaitung and not st.session_state.has_bespannmaschine:
        investitionen += 1800
        st.session_state.has_bespannmaschine = True

    # 1. KOORDINATION & EINZELEFFEKT
    koordinations_kosten = 500
    if einteilungs_fokus == "Perfekt Homogen (Hohe Kosten)":
        koordinations_kosten = 2500  # Hoher zeitlicher / organisatorischer Aufwand
        homogenitaets_bonus = 15
    elif einteilungs_fokus == "Mittel":
        koordinations_kosten = 1200
        homogenitaets_bonus = 5
    else:
        homogenitaets_bonus = -10  # Unzufriedenheit durch bunt gemischte Gruppen
        
    # 2. QUALITÄT & ZUFRIEDENHEIT
    homogenitaets_abzug = (gruppengroesse - 2) * 8
    qualitaets_abzug = (anteil_nachwuchs / 100) * 20
    
    zufriedenheit = 100 - homogenitaets_abzug - qualitaets_abzug + homogenitaets_bonus
    if has_shop: zufriedenheit += 5  # Shop wird als Service empfunden
    zufriedenheit = max(10, min(100, zufriedenheit))
    
    # 3. SHOP & RISIKO (Ladenhüter / Vororder)
    shop_einnahmen = 0
    shop_kosten = 0
    if has_shop:
        verkaufs_quote = min(1.0, (st.session_state.kundenstamm / 150) * (zufriedenheit / 80))
        if st.session_state.runde == 4: verkaufs_quote *= 0.6  # Kollektionswechsel-Schock!
        
        shop_einnahmen = vororder_volumen * 1.4 * verkaufs_quote
        shop_kosten = vororder_volumen + 1200  # Miete/Lager
        
    # 4. FINANZBERECHNUNG
    stunden_pro_schueler = 30
    gesamte_gruppenstunden = (st.session_state.kundenstamm * stunden_pro_schueler) / max(1, gruppengroesse)
    
    einnahmen_kurse = st.session_state.kundenstamm * stunden_pro_schueler * preis_stunde
    einnahmen_besaitung = 2200 if has_besaitung else 0
    sponsoring = (st.session_state.image_score / 100) * 3500
    
    einnahmen_ges = einnahmen_kurse + shop_einnahmen + einnahmen_besaitung + sponsoring
    
    kosten_trainer = gesamte_gruppenstunden * misch_lohn
    kosten_hallen = gesamte_gruppenstunden * (30 if st.session_state.runde == 4 else 22)
    kosten_ges = kosten_trainer + kosten_hallen + shop_kosten + koordinations_kosten + marketing + investitionen
    
    gewinn = einnahmen_ges - kosten_ges
    st.session_state.kapital += gewinn
    
    # 5. KUNDENSTAMM FLUKTUATION
    if zufriedenheit >= 75:
        kunden_diff = int(st.session_state.kundenstamm * 0.12)
    elif zufriedenheit <= 50:
        kunden_diff = -int(st.session_state.kundenstamm * 0.18)
    else:
        kunden_diff = 0
        
    st.session_state.historie.append({
        "Jahr": f"Jahr {st.session_state.runde}",
        "Schüler": st.session_state.kundenstamm,
        "Zufriedenheit": f"{int(zufriedenheit)}%",
        "Gewinn (€)": round(gewinn),
        "Bankguthaben (€)": round(st.session_state.kapital)
    })
    
    st.session_state.kundenstamm = max(20, st.session_state.kundenstamm + kunden_diff)
    st.session_state.runde += 1
    st.rerun()

# --- HISTORIE ---
if len(st.session_state.historie) > 0:
    st.markdown("---")
    st.subheader("📊 Verlauf deiner Tennisschule")
    df_h = pd.DataFrame(st.session_state.historie)
    
    c_h1, c_h2 = st.columns([1, 1])
    with c_h1:
        st.dataframe(df_h, use_container_width=True)
    with c_h2:
        st.line_chart(df_h.set_index("Jahr")[["Bankguthaben (€)", "Gewinn (€)"]])
