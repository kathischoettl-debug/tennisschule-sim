import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tennisschule Simulator", layout="wide")

st.title("🎾 Tennisschule Business Simulator")
st.markdown("Simuliere die Wirtschaftlichkeit deiner Tennisschule basierend auf Region, Trainerkosten, Trainingsformaten & Zusatzangeboten.")

# --- SIDEBAR: EINSTELLUNGEN & STANDORT ---
st.sidebar.header("1. Standort & Region")
region = st.sidebar.selectbox("Region / Kaufkraft", ["München & Umgebung (Hohe Preise/Kosten)", "Durchschnittliche Region", "Ländlich / Niedrige Preise"])

if "München" in region:
    mult_cost = 1.4
    mult_price = 1.4
elif "Ländlich" in region:
    mult_cost = 0.7
    mult_price = 0.7
else:
    mult_cost = 1.0
    mult_price = 1.0

st.sidebar.header("2. Strategische Ausrichtung")
fokus = st.sidebar.radio("Fokus der Tennisschule", ["Breitensport (Höhere Skalierbarkeit)", "Leistungssport (Besseres Image, schwankende Auslastung)"])
anstallungsverhaeltnis = st.sidebar.radio("Trainer-Anstellung", ["Freiberufler", "Festangestellt (inkl. 20% Sozialabgaben)"])

# --- TAB-STRUKTUR ---
tab1, tab2, tab3, tab4 = st.tabs(["👥 Trainer & Kapazität", "🎾 Angebote & Kurse", "🛒 Shop & Besaitung", "📊 Finanzauswertung"])

with tab1:
    st.header("Trainer-Team & Stundensätze")
    col1, col2 = st.columns(2)
    
    with col1:
        anz_a = st.number_input("Anzahl A-Trainer", 0, 10, 1)
        anz_b = st.number_input("Anzahl B-Trainer", 0, 10, 2)
        anz_c = st.number_input("Anzahl C-Trainer", 0, 10, 2)
        anz_nachwuchs = st.number_input("Anzahl Nachwuchs / Assistenten", 0, 10, 3)
    
    with col2:
        cost_a = st.slider("Stundensatz A-Trainer (€/h)", 40, 90, int(75 * mult_cost))
        cost_b = st.slider("Stundensatz B-Trainer (€/h)", 30, 65, int(50 * mult_cost))
        cost_c = st.slider("Stundensatz C-Trainer (€/h)", 20, 40, int(32 * mult_cost))
        cost_nachwuchs = st.slider("Stundensatz Nachwuchs (€/h)", 12, 25, int(18 * mult_cost))

    st.subheader("Wöchentliche Arbeitsstunden im Schnitt")
    std_pro_trainer = st.slider("Trainingsstunden pro Trainer / Woche", 5, 40, 20)

with tab2:
    st.header("Trainingsangebote & Preise")
    c1, c2 = st.columns(2)
    
    with c1:
        preis_einzel = st.slider("Preis Einzelstunde (€/h für Kunde)", 30, 100, int(60 * mult_price))
        platz_preis_sommer = st.slider("Platzmiete Sommer (€/h)", 10, 30, 20)
        platz_preis_winter = st.slider("Platzmiete Halle Winter (€/h)", 25, 60, 40)
        stunden_sommer = st.slider("Stunden im Sommer-Halbjahr (26 Wochen)", 100, 2000, 800)
        stunden_winter = st.slider("Stunden im Winter-Halbjahr (26 Wochen)", 100, 2000, 600)
        
    with c2:
        st.subheader("Feriencamps")
        anz_camps = st.slider("Anzahl Feriencamps pro Jahr", 0, 10, 4)
        teilnehmer_camp = st.slider("Teilnehmer pro Camp", 10, 60, 35)
        preis_camp = st.slider("Preis pro Teilnehmendem (€)", 150, 450, 320)
        gastro_kosten_camp = st.slider("Verpflegungskosten pro Teilnehmendem (€)", 30, 100, 50)

with tab3:
    st.header("Zusatzgeschäfte: Shop & Besaitung")
    sc1, sc2 = st.columns(2)
    
    with sc1:
        st.subheader("Tennisshop")
        has_shop = st.checkbox("Tennisshop betreiben", value=True)
        lager_miete = st.number_input("Monatliche Shop-/Lagerkosten (€)", 0, 1000, 200) if has_shop else 0
        shop_umsatz = st.number_input("Geschätzter Jahresumsatz Shop (€)", 0, 50000, 8000) if has_shop else 0
        shop_marge = st.slider("Marge im Shop (%)", 10, 50, 25) if has_shop else 0
        
    with sc2:
        st.subheader("Besaitungsservice")
        has_besaitung = st.checkbox("Besaitungsservice anbieten", value=True)
        schlaeger_jahr = st.slider("Besaitete Schläger pro Jahr", 0, 1000, 250) if has_besaitung else 0
        preis_besaitung = st.slider("Preis pro Besaitung für Kunde (€)", 10, 35, 22) if has_besaitung else 0
        lohn_besaiter = st.slider("Lohn Besaiter pro Schläger (€)", 5, 20, 12) if has_besaitung else 0

with tab4:
    st.header("📊 Finanzielles Ergebnis (Jahresübersicht)")
    
    # BERECHNUNGEN
    # 1. Trainerkosten
    stunden_gesamtes_jahr = stunden_sommer + stunden_winter
    gehalt_faktor = 1.2 if anstallungsverhaeltnis == "Festangestellt (inkl. 20% Sozialabgaben)" else 1.0
    
    tot_trainer_kosten = (
        (anz_a * cost_a + anz_b * cost_b + anz_c * cost_c + anz_nachwuchs * cost_nachwuchs)
        / max(1, (anz_a + anz_b + anz_c + anz_nachwuchs))
    ) * stunden_gesamtes_jahr * gehalt_faktor
    
    # 2. Einnahmen Kurse & Plätze
    einnahmen_kurse = stunden_gesamtes_jahr * preis_einzel
    platzkosten = (stunden_sommer * platz_preis_sommer) + (stunden_winter * platz_preis_winter)
    
    # 3. Camps
    einnahmen_camps = anz_camps * teilnehmer_camp * preis_camp
    kosten_camps = anz_camps * teilnehmer_camp * gastro_kosten_camp + (anz_camps * 30 * cost_nachwuchs * 2) # 30h Camp-Dauer
    marge_camps = einnahmen_camps - kosten_camps
    
    # 4. Shop & Besaitung
    gewinn_shop = (shop_umsatz * (shop_marge / 100.0)) - (lager_miete * 12) if has_shop else 0
    gewinn_besaitung = schlaeger_jahr * (preis_besaitung - lohn_besaiter) if has_besaitung else 0
    
    # Image/Ausrüster-Bonus
    ausruester_bonus = 2000 if (fokus == "Leistungssport (Besseres Image, schwankende Auslastung)" and stunden_gesamtes_jahr > 1000) else 500
    
    # Gesamtrechnung
    gesamteinnahmen = einnahmen_kurse + einnahmen_camps + shop_umsatz + (schlaeger_jahr * preis_besaitung) + ausruester_bonus
    gesamtausgaben = tot_trainer_kosten + platzkosten + kosten_camps + (shop_umsatz * (1 - shop_marge/100.0)) + (lager_miete * 12) + (schlaeger_jahr * lohn_besaiter)
    gewinn = gesamteinnahmen - gesamtausgaben
    
    # METRIKEN ANZEIGEN
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gesamteinnahmen", f"{gesamteinnahmen:,.0f} €")
    m2.metric("Gesamtausgaben", f"{gesamtausgaben:,.0f} €")
    m3.metric("Jahresgewinn / Verlust", f"{gewinn:,.0f} €", delta_color="normal")
    m4.metric("Ausrüster-Sponsoring", f"{ausruester_bonus:,.0f} €")
    
    st.subheader("Detailrechnung")
    df = pd.DataFrame({
        "Kategorie": ["Trainingsbetrieb (Stunden)", "Feriencamps", "Tennisshop", "Besaitungsservice", "Platzmieten (Kosten)"],
        "Einnahmen (€)": [einnahmen_kurse, einnahmen_camps, shop_umsatz, schlaeger_jahr * preis_besaitung, 0],
        "Kosten (€)": [tot_trainer_kosten, kosten_camps, shop_umsatz * (1 - shop_marge/100.0) + (lager_miete * 12), schlaeger_jahr * lohn_besaiter, platzkosten]
    })
    st.dataframe(df, use_container_width=True)
    
    if gewinn > 0:
        st.success("🎉 Die Tennisschule arbeitet profitabel!")
    else:
        st.error("⚠️ Die Tennisschule macht Verlust. Passe Stundensätze, Gruppengrößen oder Trainerkosten an.")
