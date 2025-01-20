import streamlit as st
import matplotlib.pyplot as plt

# Haushaltsrechner App
st.title("🏠 Haushaltsrechner für Kredit- und Baufinanzierung")
st.write("Herzlich Willkommen! Beantworten Sie die folgenden Fragen Schritt für Schritt. Wir helfen Ihnen, Ihre finanzielle Situation zu analysieren.")

# Schritt 1: Kreditnehmer
kreditnehmer = st.radio(
    "Wird der Kredit von einer alleinstehenden Person oder einem Ehepaar aufgenommen?",
    ("Alleinstehend", "Ehepaar"),
    help="Wählen Sie die passende Option aus, um die Einkommenssituation richtig zu erfassen."
)

# Schritt 2: Kinder im Haushalt
kinder = st.number_input(
    "Wie viele Kinder leben im Haushalt?",
    min_value=0, max_value=10, step=1,
    help="Geben Sie die Anzahl der Kinder an, da diese die Lebenshaltungskosten beeinflussen."
)

# Schritt 3: Nettoeinkommen
if kreditnehmer == "Alleinstehend":
    nettoeinkommen = st.number_input(
        "Nettoeinkommen der alleinstehenden Person (€):",
        min_value=0.0, step=100.0,
        help="Tragen Sie das monatliche Nettoeinkommen ein."
    )
else:
    nettoeinkommen = st.number_input(
        "Gemeinsames Nettoeinkommen des Ehepaares (€):",
        min_value=0.0, step=100.0,
        help="Tragen Sie das gemeinsame monatliche Nettoeinkommen ein."
    )

# Schritt 4: Zusätzliche Einkommen
zusatz_einkommen = st.number_input(
    "Gibt es andere Einkommen (z.B. aus Vermietung und Verpachtung)? (€):",
    min_value=0.0, step=50.0,
    help="Zusätzliche monatliche Einnahmen neben dem Nettoeinkommen."
)

# Schritt 5: Lebenshaltungspauschale
lebenshaltungspauschale = st.number_input(
    "Wie hoch ist die Lebenshaltungspauschale? (€):",
    min_value=0.0, step=50.0,
    help="Diese Pauschale deckt die geschätzten monatlichen Lebenshaltungskosten ab."
)

# Schritt 6: Autos im Haushalt
autos = st.number_input(
    "Wie viele Autos gibt es im Haushalt?",
    min_value=0, max_value=5, step=1,
    help="Für jedes Auto setzen wir pauschal 250€ an."
)
auto_kosten = autos * 250

# Schritt 7: Versicherungen und Unterhaltszahlungen
versicherungen = st.number_input(
    "Monatliche Kosten für Lebens-, Unfallversicherungen oder Unterhaltszahlungen (€):",
    min_value=0.0, step=50.0,
    help="Geben Sie die Gesamtkosten an, die für solche Verpflichtungen monatlich anfallen."
)

# Schritt 8: Kredite und Sparraten
kredite_sparraten = st.number_input(
    "Gibt es bestehende Kredite oder Sparraten? (€):",
    min_value=0.0, step=50.0,
    help="Geben Sie die Gesamtkosten für bestehende Kredite oder Sparverträge an."
)

# Schritt 9: Zusätzliche Ausgaben
andere_ausgaben = st.number_input(
    "Andere übermäßige Ausgaben (z.B. teurer Kindergarten, Mitgliedschaften)? (€):",
    min_value=0.0, step=50.0,
    help="Tragen Sie besondere monatliche Ausgaben ein, die über die normalen Kosten hinausgehen."
)

# Schritt 10: Wohnsituation
wohnsituation = st.radio(
    "Wohnen Sie zur Miete oder haben Sie Eigentum?",
    ("Miete", "Eigentum"),
    help="Die Wohnsituation beeinflusst die monatlichen Kosten."
)

if wohnsituation == "Miete":
    warmmiete = st.number_input(
        "Wie hoch ist die monatliche Warmmiete? (€):",
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
            "Wie hoch ist das Hausgeld? (€):",
            min_value=0.0, step=50.0,
            help="Das Hausgeld umfasst Betriebskosten, Rücklagen und Verwaltungsgebühren."
        )
        wohnkosten = bewirtschaftungskosten + hausgeld
    else:
        wohnkosten = bewirtschaftungskosten

# Gesamtausgaben berechnen
monatl_gesamtausgaben = (
    lebenshaltungspauschale + auto_kosten + versicherungen + kredite_sparraten + 
    andere_ausgaben + wohnkosten
)

# Kapitaldienst berechnen
monatl_einkommen = nettoeinkommen + zusatz_einkommen
kapitaldienst = monatl_einkommen - monatl_gesamtausgaben

# Ergebnisse anzeigen
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

# Kapitaldienstgrafik
fig, ax = plt.subplots()
labels = ["Verfügbar für Kredit", "Gesamtausgaben"]
data = [kapitaldienst, monatl_gesamtausgaben]
colors = ["#76c7c0", "#ff6f61"]
ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
ax.axis("equal")
plt.title("Kapitaldienstaufteilung")
st.pyplot(fig)
