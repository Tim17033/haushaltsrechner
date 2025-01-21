import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Tabelle der Lebenshaltungspauschalen laden und bereinigen
pauschalen_data = {
    "Nettoeinkommen": [
        "bis 500", "bis 750", "bis 1000", "bis 1250", "bis 1500", "bis 1750", "bis 2000", "bis 2250", "bis 2500", "bis 2750", "bis 3000", "bis 3250", "bis 3500", "bis 3750", "bis 4000", "bis 4250", "bis 4500", "bis 4750", "bis 5000", "ab 5000"
    ],
    "1 Person": [573, 573, 577, 582, 587, 591, 598, 598, 598, 598, 598, 598, 598, 598, 598, 598, 598, 598, 598, 598],
    "2 Personen": [1022, 1022, 1026, 1031, 1036, 1040, 1045, 1055, 1055, 1071, 1071, 1071, 1071, 1071, 1071, 1071, 1071, 1071, 1071, 1071],
    "3 Personen": [1412, 1412, 1416, 1421, 1426, 1430, 1435, 1445, 1445, 1467, 1467, 1467, 1467, 1467, 1467, 1467, 1467, 1467, 1467, 1467],
    "4 Personen": [1802, 1802, 1806, 1811, 1816, 1820, 1825, 1835, 1835, 1863, 1863, 1863, 1863, 1863, 1863, 1863, 1863, 1863, 1863, 1863],
    "5 Personen": [2192, 2192, 2196, 2201, 2206, 2210, 2215, 2225, 2225, 2259, 2259, 2259, 2259, 2259, 2259, 2259, 2259, 2259, 2259, 2259],
    "6 Personen": [2582, 2582, 2586, 2591, 2596, 2600, 2605, 2615, 2615, 2655, 2655, 2655, 2655, 2655, 2655, 2655, 2655, 2655, 2655, 2655],
    "7 Personen": [2972, 2972, 2976, 2981, 2986, 2990, 2995, 3005, 3005, 3051, 3051, 3051, 3051, 3051, 3051, 3051, 3051, 3051, 3051, 3051]
}
pauschalen_df = pd.DataFrame(pauschalen_data)

# Hilfsfunktion zur Berechnung der Lebenshaltungspauschale

def berechne_pauschale(nettoeinkommen, personen):
    for index, row in pauschalen_df.iterrows():
        grenze = row["Nettoeinkommen"].split("bis ")[-1]
        if grenze == "5000":
            if nettoeinkommen > 5000:
                return row[f"{personen} Personen"]
        elif nettoeinkommen <= float(grenze.replace(".", "")):
            return row[f"{personen} Personen"]
    return pauschalen_df.iloc[-1][f"{personen} Personen"]

# Haushaltsrechner App
st.title("\ud83c\udfe0 Haushaltsrechner f\u00fcr Kredit- und Baufinanzierung")
st.write("Herzlich Willkommen! Beantworten Sie die folgenden Fragen Schritt f\u00fcr Schritt. Klicken Sie abschlie\u00dfend auf 'Ergebnisse anzeigen', um Ihre Analyse zu erhalten.")

# Eingaben
kreditnehmer = st.radio(
    "Wird der Kredit von einer alleinstehenden Person oder einem Ehepaar aufgenommen?",
    ("Alleinstehend", "Ehepaar"),
    help="W\u00e4hlen Sie die passende Option aus, um die Einkommenssituation richtig zu erfassen."
)

kinder = st.number_input(
    "Wie viele Kinder leben im Haushalt?",
    min_value=0, max_value=10, step=1,
    help="Geben Sie die Anzahl der Kinder an, da diese die Lebenshaltungskosten beeinflussen."
)

if kreditnehmer == "Alleinstehend":
    nettoeinkommen = st.number_input(
        "Nettoeinkommen der alleinstehenden Person (\u20ac):",
        min_value=0.0, step=100.0,
        help="Tragen Sie das monatliche Nettoeinkommen ein."
    )
else:
    nettoeinkommen = st.number_input(
        "Gemeinsames Nettoeinkommen des Ehepaares (\u20ac):",
        min_value=0.0, step=100.0,
        help="Tragen Sie das gemeinsame monatliche Nettoeinkommen ein."
    )

zusatz_einkommen = st.number_input(
    "Gibt es andere Einkommen (z.B. aus Vermietung und Verpachtung)? (\u20ac):",
    min_value=0.0, step=50.0,
    help="Zus\u00e4tzliche monatliche Einnahmen neben dem Nettoeinkommen."
)

# Automatische Lebenshaltungspauschale
if kreditnehmer and kinder is not None and nettoeinkommen:
    personen = 1 if kreditnehmer == "Alleinstehend" else 2
    personen += kinder
    lebenshaltungspauschale = berechne_pauschale(nettoeinkommen, personen)
    lebenshaltungspauschale = st.number_input(
        "Wie hoch ist die Lebenshaltungspauschale? (\u20ac):",
        value=lebenshaltungspauschale,
        step=50.0,
        help="Dieser Wert wurde basierend auf Ihren Angaben automatisch berechnet. Sie k\u00f6nnen ihn anpassen."
    )

autos = st.number_input(
    "Wie viele Autos gibt es im Haushalt?",
    min_value=0, max_value=5, step=1,
    help="F\u00fcr jedes Auto setzen wir pauschal 250\u20ac an."
)
auto_kosten = autos * 250

versicherungen = st.number_input(
    "Monatliche Kosten f\u00fcr Lebens-, Unfallversicherungen oder Unterhaltszahlungen (\u20ac):",
    min_value=0.0, step=50.0,
    help="Geben Sie die Gesamtkosten an, die f\u00fcr solche Verpflichtungen monatlich anfallen."
)

kredite_sparraten = st.number_input(
    "Gibt es bestehende Kredite oder Sparraten? (\u20ac):",
    min_value=0.0, step=50.0,
    help="Geben Sie die Gesamtkosten f\u00fcr bestehende Kredite oder Sparvertr\u00e4ge an."
)

andere_ausgaben = st.number_input(
    "Andere \u00fcberm\u00e4\u00dfige Ausgaben (z.B. teurer Kindergarten, Mitgliedschaften)? (\u20ac):",
    min_value=0.0, step=50.0,
    help="Tragen Sie besondere monatliche Ausgaben ein, die \u00fcber die normalen Kosten hinausgehen."
)

wohnsituation = st.radio(
    "Wohnen Sie zur Miete oder haben Sie Eigentum?",
    ("Miete", "Eigentum"),
    help="Die Wohnsituation beeinflusst die monatlichen Kosten."
)

if wohnsituation == "Miete":
    warmmiete = st.number_input(
        "Wie hoch ist die monatliche Warmmiete? (\u20ac):",
        min_value=0.0, step=50.0,
        help="Die Warmmiete umfasst Miete, Betriebskosten und Heizkosten."
    )
    wohnkosten = warmmiete
else:
    eigentum_typ = st.radio(
        "Ist es ein Haus oder eine Wohnung?",
        ("Haus", "Wohnung"),
        help="Die Bewirtschaftungskosten variieren je nach Immobilientyp."
    )
    qm = st.number_input(
        f"Wie viele Quadratmeter hat das {eigentum_typ}?",
        min_value=20, max_value=500, step=10,
        help="Die Bewirtschaftungskosten werden pro Quadratmeter berechnet."
    )
    bewirtschaftungskosten = qm * 3.5
    if eigentum_typ == "Wohnung":
        hausgeld = st.number_input(
            "Wie hoch ist das Hausgeld? (\u20ac):",
            min_value=0.0, step=50.0,
            help="Das Hausgeld umfasst Betriebskosten, R\u00fccklagen und Verwaltungsgeb\u00fchren."
        )
        wohnkosten = bewirtschaftungskosten + hausgeld
    else:
        wohnkosten = bewirtschaftungskosten

# Ergebnisse anzeigen
if st.button("Ergebnisse anzeigen"):
    monatl_gesamtausgaben = (
        lebenshaltungspauschale + auto_kosten + versicherungen +
        kredite_sparraten + andere_ausgaben + wohnkosten
    )
    monatl_einkommen = nettoeinkommen + zusatz_einkommen
    kapitaldienst = monatl_einkommen - monatl_gesamtausgaben

    st.markdown("## Ergebnisse")
    st.markdown(
        f"""
        ### Monatliche Ausgaben
        - Gesamte Lebenshaltungskosten: **{lebenshaltungspauschale + auto_kosten:,.2f} \u20ac**
        - Versicherungen und Unterhaltszahlungen: **{versicherungen:,.2f} \u20ac**
        - Kredite und Sparraten: **{kredite_sparraten:,.2f} \u20ac**
        - Wohnkosten: **{wohnkosten:,.2f} \u20ac**
        - Zus\u00e4tzliche Ausgaben: **{andere_ausgaben:,.2f} \u20ac**

        ### Monatliches Einkommen
        - Gesamteinkommen: **{monatl_einkommen:,.2f} \u20ac**

        ### Kapitaldienst
        - Verf\u00fcgbarer Betrag f\u00fcr den Kredit: **{kapitaldienst:,.2f} \u20ac**
        """
    )

    if kapitaldienst > 0:
        fig, ax = plt.subplots()
        labels = ["Verf\u00fcgbar f\u00fcr Kredit", "Gesamtausgaben"]
        data = [kapitaldienst, monatl_gesamtausgaben]
        ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        plt.title("Kapitaldienstaufteilung")
        st.pyplot(fig)
    else:
        st.warning("Der verf\u00fcgbare Betrag f\u00fcr den Kredit ist 0 \u20ac. Es kann kein Diagramm erstellt werden.")
