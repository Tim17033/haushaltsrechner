import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Tabelle der Lebenshaltungspauschalen laden und bereinigen
pauschalen_data = {
    "Nettoeinkommen": [
        "bis 500", "bis 750", "bis 1000", "bis 1250", "bis 1500", "bis 1750", "bis 2000", "bis 2250", "bis 2500", "bis 2750", "bis 3000", "bis 3250", "bis 3500", "bis 3750", "bis 4000", "bis 4250", "bis 4500", "bis 4750", "bis 5000", "ab 5000"
    ],
    "1 Person": [573, 573, 577, 582, 587, 591, 591, 598, 672, 718, 790, 862, 934, 943, 1010, 1076, 1144, 1211, 1278, 1285],
    "2 Personen": [1022, 1022, 1026, 1031, 1036, 1040, 1050, 1055, 1060, 1071, 1071, 1071, 1104, 1113, 1180, 1246, 1314, 1381, 1448, 1455],
    "3 Personen": [1412, 1412, 1416, 1421, 1426, 1430, 1440, 1445, 1450, 1461, 1467, 1473, 1473, 1473, 1473, 1473, 1484, 1551, 1618, 1625],
    "4 Personen": [1802, 1802, 1806, 1811, 1816, 1820, 1830, 1835, 1840, 1851, 1857, 1863, 1869, 1874, 1880, 1885, 1885, 1885, 1885, 1885],
    "5 Personen": [2192, 2192, 2196, 2201, 2206, 2210, 2220, 2225, 2230, 2241, 2247, 2253, 2259, 2264, 2270, 2275, 2281, 2287, 2287, 2287],
    "6 Personen": [2582, 2582, 2586, 2591, 2596, 2600, 2610, 2615, 2620, 2631, 2637, 2643, 2649, 2654, 2660, 2665, 2671, 2677, 2683, 2691],
    "7 Personen": [2972, 2972, 2976, 2981, 2986, 2990, 3000, 3005, 3010, 3021, 3027, 3033, 3039, 3044, 3050, 3055, 3061, 3067, 3073, 3081]
}
pauschalen_df = pd.DataFrame(pauschalen_data)

# Hilfsfunktion zur Berechnung der Lebenshaltungspauschale

def berechne_pauschale(nettoeinkommen, personen):
    personen = min(personen, 7)  # Maximal 7 Personen berücksichtigen
    for index, row in pauschalen_df.iterrows():
        grenze = row["Nettoeinkommen"].split("bis ")[-1]
        try:
            grenze = float(grenze.replace(".", ""))
        except ValueError:
            grenze = float("inf")  # Für "ab 5000" setzen wir eine sehr hohe Grenze
        if nettoeinkommen <= grenze:
            return row[f"{personen} Personen"]
    return pauschalen_df.iloc[-1][f"{personen} Personen"]

# Haushaltsrechner App
st.title("🏠 Haushaltsrechner für Kredit- und Baufinanzierung")
st.markdown(
    """
    **Willkommen zum Haushaltsrechner!**
    Beantworten Sie Schritt für Schritt die folgenden Fragen, um Ihre monatlichen Ausgaben und Ihr verfügbares Einkommen zu analysieren.
    """
)

# Eingaben
st.markdown("### Informationen zum Kreditnehmer")
kreditnehmer = st.radio(
    "Wird der Kredit von einer alleinstehenden Person oder einem Ehepaar aufgenommen?",
    ("Alleinstehend", "Ehepaar")
)
st.caption("Wählen Sie die passende Option, um die Einkommenssituation richtig zu erfassen.")

kinder = st.number_input(
    "Wie viele Kinder leben im Haushalt?",
    min_value=0, max_value=10, step=1
)
st.caption("Geben Sie die Anzahl der Kinder an, da diese die Lebenshaltungskosten beeinflussen.")

st.markdown("### Einkommensangaben")
if kreditnehmer == "Alleinstehend":
    nettoeinkommen = st.number_input(
        "Nettoeinkommen der alleinstehenden Person (€):",
        min_value=0.0, step=100.0
    )
st.caption("Tragen Sie das monatliche Nettoeinkommen ein.")
else:
    nettoeinkommen = st.number_input(
        "Gemeinsames Nettoeinkommen des Ehepaares (€):",
        min_value=0.0, step=100.0
    )
st.caption("Tragen Sie das gemeinsame monatliche Nettoeinkommen ein.")

zusatz_einkommen = st.number_input(
    "Gibt es andere Einkommen (z.B. aus Vermietung und Verpachtung)? (€):",
    min_value=0.0, step=50.0
)
st.caption("Zusätzliche monatliche Einnahmen neben dem Nettoeinkommen.")

# Nettohaushaltseinkommen berechnen
nettohaushaltseinkommen = nettoeinkommen + zusatz_einkommen

# Automatische Lebenshaltungspauschale
if kreditnehmer and kinder is not None and nettohaushaltseinkommen:
    personen = 1 if kreditnehmer == "Alleinstehend" else 2
    personen += kinder
    lebenshaltungspauschale = berechne_pauschale(nettohaushaltseinkommen, personen)
    st.markdown(f"### Lebenshaltungspauschale: **{lebenshaltungspauschale:.2f} €**")
st.caption("Dieser Wert wurde basierend auf Ihren Angaben automatisch berechnet.")

st.markdown("### Haushaltskosten")
autos = st.number_input(
    "Wie viele Autos gibt es im Haushalt?",
    min_value=0, max_value=5, step=1
)
st.caption("Für jedes Auto setzen wir pauschal 250€ an.")
auto_kosten = autos * 250

versicherungen = st.number_input(
    "Monatliche Kosten für Lebens-, Unfallversicherungen oder Unterhaltszahlungen (€):",
    min_value=0.0, step=50.0
)
st.caption("Geben Sie die Gesamtkosten an, die für solche Verpflichtungen monatlich anfallen.")

kredite_sparraten = st.number_input(
    "Gibt es bestehende Kredite oder Sparraten? (€):",
    min_value=0.0, step=50.0
)
st.caption("Geben Sie die Gesamtkosten für bestehende Kredite oder Sparverträge an.")

andere_ausgaben = st.number_input(
    "Andere übermäßige Ausgaben (z.B. teurer Kindergarten, Mitgliedschaften)? (€):",
    min_value=0.0, step=50.0
)
st.caption("Tragen Sie besondere monatliche Ausgaben ein, die über die normalen Kosten hinausgehen.")

st.markdown("### Wohnsituation")
wohnsituation = st.radio(
    "Wohnen Sie zur Miete oder haben Sie Eigentum?",
    ("Miete", "Eigentum")
)
st.caption("Die Wohnsituation beeinflusst die monatlichen Kosten.")

if wohnsituation == "Miete":
    warmmiete = st.number_input(
        "Wie hoch ist die monatliche Warmmiete? (€):",
        min_value=0.0, step=50.0
    )
st.caption("Die Warmmiete umfasst Miete, Betriebskosten und Heizkosten.")
    wohnkosten = warmmiete
else:
    eigentum_typ = st.radio(
        "Ist es ein Haus oder eine Wohnung?",
        ("Haus", "Wohnung")
    )
st.caption("Die Bewirtschaftungskosten variieren je nach Immobilientyp.")
    qm = st.number_input(
        f"Wie viele Quadratmeter hat das {eigentum_typ}?",
        min_value=20, max_value=500, step=10
    )
st.caption("Die Bewirtschaftungskosten werden pro Quadratmeter berechnet.")
    bewirtschaftungskosten = qm * 3.5
    if eigentum_typ == "Wohnung":
        hausgeld = st.number_input(
            "Wie hoch ist das Hausgeld? (€):",
            min_value=0.0, step=50.0
        )
st.caption("Das Hausgeld umfasst Betriebskosten, Rücklagen und Verwaltungsgebühren.")
        wohnkosten = bewirtschaftungskosten + hausgeld
    else:
        wohnkosten = bewirtschaftungskosten

# Ergebnisse anzeigen
if st.button("Ergebnisse anzeigen"):
    monatl_gesamtausgaben = (
        lebenshaltungspauschale + auto_kosten + versicherungen +
        kredite_sparraten + andere_ausgaben + wohnkosten
    )
    monatl_einkommen = nettohaushaltseinkommen
    kapitaldienst = monatl_einkommen - monatl_gesamtausgaben

    st.markdown("## Ergebnisse")
    st.markdown(
        f"""
        ### Monatliche Ausgaben
        - Gesamte Lebenshaltungskosten: **{lebenshaltungspauschale + auto_kosten:,.2f} €**
        - Versicherungen und Unterhaltszahlungen: **{versicherungen:,.2f} €**
        - Kredite und Sparraten: **{kredite_sparraten:,.2f} €**
        - Wohnkosten: **{wohnkosten:,.2f} €**
        - Zusätzliche Ausgaben: **{andere_ausgaben:,.2f} €**

        ### Monatliches Einkommen
        - Gesamteinkommen: **{monatl_einkommen:,.2f} €**

        ### Kapitaldienst
        - Verfügbarer Betrag für den Kredit: **{kapitaldienst:,.2f} €**
        """
    )

    if kapitaldienst > 0:
        fig, ax = plt.subplots()
        labels = ["Verfügbar für Kredit", "Gesamtausgaben"]
        data = [kapitaldienst, monatl_gesamtausgaben]
        ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        plt.title("Kapitaldienstaufteilung")
        st.pyplot(fig)
    else:
        st.warning("Der verfügbare Betrag für den Kredit ist 0 €. Es kann kein Diagramm erstellt werden.")




