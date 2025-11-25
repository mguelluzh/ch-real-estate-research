from datetime import date
from openai import OpenAI

# Client liest den OPENAI_API_KEY aus den GitHub Secrets / Umgebungsvariablen
client = OpenAI()

MASTER_PROMPT = """
Du bist ein*e leitende*r Schweizer Immobilien-Research-Analyst*in
mit Expertise in:
- Markt-, Preis- & Transaktionsanalysen
- Raumplanung (RPG, Richtpläne, Sondernutzungs- und Gestaltungspläne)
- kommunalen Bau- und Zonenordnungen (BZO)
- Projektentwicklungen & Baubewilligungen
- politischen Prozessen (Initiativen, Referenden, Abstimmungen)
- finanzwirtschaftlichen Rahmenbedingungen (SNB, Hypotheken, Kapitalmärkte)

Erstelle einen umfassenden, tiefgründigen und professionellen Monatsbericht,
ideal für Investor:innen, Asset Manager, Developer, Banken, Beratungen
und institutionelle Marktteilnehmer.

ANTWORTSTRUKTUR (immer genau so):

1. Executive Summary (10–15 prägnante Kernpunkte)

2. Markt- & Transaktionslage Schweiz
   - Miet- & Kaufpreisbewegungen
   - Zinsumfeld (SNB, Hypotheken)
   - Segmente: Wohnen, Büro, Retail, Logistik
   - Top-Transaktionen (ab ca. CHF 10–20 Mio.)
   - zentrale Branchenreports (Wüest Partner, FPRE, IAZI, UBS, CS etc.)
   - makroökonomische Rahmenbedingungen

3. Politik, Gesetzgebung & Abstimmungen
   - nationale, kantonale und kommunale Vorlagen mit Immobilienbezug
   - Initiativen und Referenden inkl. Status (eingereicht / zustande gekommen / in Prüfung / zur Abstimmung / angenommen / abgelehnt)
   - Auswirkungen auf Mieten, Eigentum, Investitionen, Bauträger, Renditen
   - juristisch saubere Einordnung nach RPG, ZGB, OR und kantonalem Bau- und Planungsrecht

4. Raumplanung, BZO, Nutzungsplanung & Bewilligungen
   - laufende und anstehende Revisionen (BZO, Gestaltungspläne, Sondernutzungspläne)
   - Richtplan-Anpassungen (kantonal/kommunal)
   - Ein- und Auszonungen, Verdichtungsstrategien
   - Baubewilligungen, öffentliche Auflagen, Mitwirkungsverfahren
   - Einspracheverfahren, wichtige Gerichtsentscheide (insb. Bundesgericht, Verwaltungsgerichte)
   - Bedeutung für Dichte, Ausnutzungsziffern, Bauvolumen und Entwicklungspotenziale

5. Projektentwicklungen & Bautätigkeit
   - grosse Projekte (Kostenordnung, Projektphasen, Bewilligungsstatus)
   - neue Baugesuche und Baubewilligungen
   - Fertigstellungen und Vermietungsstand (falls verfügbar)
   - Relevanz für Investor:innen und Marktstruktur

6. Strategischer Ausblick (1–3 Monate)
   - erwartete Zins- und Marktentwicklungen
   - wichtige politische Termine und Abstimmungen
   - relevante Fristen in Raumplanung und Bauverfahren
   - Chancen- und Risikoanalyse
   - (optional) kurze Handlungsempfehlungen für professionelle Marktteilnehmer:innen

Antwortstil:
- akademisch, präzise, sachlich und schweizerisch-formal
- juristisch korrekt und faktenbasiert
- klar gegliedert, keine Wiederholungen, kein Fülltext
- Fokus auf Relevanz für professionelle Anwender:innen im Immobilien- und Finanzbereich
"""


def build_prompt(region: str, topics: str | None = None, output_length: str = "ausführlich") -> str:
    today = date.today().isoformat()

    extra_topics = topics.strip() if topics else "Keine speziellen Zusatzschwerpunkte."
    length_note = {
        "kurz": "Halte dich eher knapp, aber trotzdem strukturiert.",
        "sehr ausführlich": "Gehe in allen Teilen besonders tief ins Detail.",
        "ausführlich": "Normale ausführliche Tiefe, wie für ein professionelles Research-Dossier.",
    }.get(output_length, "Normale ausführliche Tiefe, wie für ein professionelles Research-Dossier.")

    return f"""
{MASTER_PROMPT}

Rahmenbedingungen für diesen Lauf:
- Stichtag: {today}
- Betrachteter Zeitraum: letzte 4–6 Wochen (falls sinnvoll, auch leicht darüber hinaus)
- Region / Kanton / Gemeinde: {region}
- Besondere Themen / Vertiefungen: {extra_topics}
- Gewünschte Output-Länge: {output_length} ({length_note})

Bitte halte dich strikt an die oben definierte Struktur (Punkte 1–6)
und arbeite alle Teile sauber gegliedert ab.
"""


def run_research(region: str, topics: str | None = None, output_length: str = "ausführlich") -> str:
    prompt = build_prompt(region=region, topics=topics, output_length=output_length)

    response = client.responses.create(
        model="gpt-5.1",  # ggf. anderes Modell wählen, falls nötig
        input=prompt,
    )

    return response.output[0].content[0].text


if __name__ == "__main__":
    region = "Kanton Zürich"
    topics = "Fokus auf BZO-Revisionen, grössere Entwicklungsareale und politische Vorlagen mit Immobilienbezug."
    output_length = "ausführlich"

    report = run_research(region=region, topics=topics, output_length=output_length)
    print(report)
