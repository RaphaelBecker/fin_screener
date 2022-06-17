import streamlit as st
from PIL import Image

st.write("# This is your Trading-Journal")

st.sidebar.success("Success rate: 65%. OK")

# Set up sections of web page
header = st.container()
checklist_and_create = st.container()
journal_list = st.container()

with header:
    with st.expander("Why should you use a trading journal?"):
        st.markdown(
            """
        Das Trading-Journal (auch Trading- oder Tradertagebuch) wird als Hilfsmittel zur Selbstkontrolle beim Handel mit Wertpapieren (im Fachjargon: Trading) eingesetzt (siehe auch Trader).
    
        Üblicherweise besteht ein Trading-Journal aus zwei Teilen. Der erste Teil der Aufzeichnungen enthält die wesentlichen Fakten zu einem Wertpapiergeschäft (Trade) wie zum Beispiel Name und Kennung des gehandelten Wertpapiers, An- und Verkaufspreis, Datum, Stückzahl, Gebühren, gegebenenfalls auch Kurscharts, Pressemitteilungen und Geschäftsberichte. Der andere Teil wird von jedem Trader frei bestimmt – es gibt jedoch Vorschläge von erfahrenen Tradern. Demnach werden in der Regel eigene Zielsetzungen, Einschätzungen oder Prognosen sowie Regeln und Notizen über deren Einhaltung als zu erfassende Daten vorgeschlagen. Des Weiteren wird häufig empfohlen, seine Gefühle vor, während und nach Durchführung eines Trades festzuhalten, wie zum Beispiel:
    
        Erwartungsvolle Aufmerksamkeit, Euphorie (vor der Eröffnung eines Trades)
        Negierung, Zorn, Feilschen, Akzeptanz (bei im Verlust befindlicher Position)
        Bestätigung, Prestige, Übertragung auf Ego (bei im Gewinn befindlicher Position)
        Außerdem wird oft empfohlen dem Trading-Journal einen Plan beizulegen, welcher die Schritte beschreibt, die zum Ausführen der jeweiligen Strategie notwendig sind.
    
        Zweck eines Trading-Journals ist es, Selbsterkenntnis, Selbstkontrolle und Disziplin im Hinblick auf das Trading zu verbessern:
    
        **Selbsterkenntnis**
        Die Erkenntnis, einen Fehler begangen zu haben, ist die Voraussetzung, um den Fehler in der Zukunft vermeiden zu können.
    
        **Selbstkontrolle**
        Disziplin setzt voraus, sich über sein Handeln im Klaren zu sein.
    
        **Disziplin**
        Aufgestellte Regeln und Pläne erzielen nur dann einen Nutzen, wenn sie diszipliniert umgesetzt werden.
        """
        )

with checklist_and_create:
    with st.expander("Trading Checklist"):
        if st.checkbox('Is the market in a trading range or trending?'):
            if st.checkbox('Is a support or resistance level nearby?'):
                if st.checkbox('Is the price action confirmed by indicators?'):
                    if st.checkbox('What is my risk and reward ratio?'):
                        if st.checkbox('How much captial am I risking?'):
                            if st.checkbox('Are there any significant economical releases?'):
                                if st.checkbox('What is my exit strategy?'):
                                    if st.checkbox('Am I following my trading plan?'):
                                        st.button('create trading journal entry')

with journal_list:
    for i in range(0,2,1):
        st.markdown(
            """
        **Beispieleintrag xy**
        | Trade   |      0      |  
        |----------|:-------------:|
        | Datum |  15. Dezember - 19.10 Uhr |
        | Ziel |    30 Pips   |   
        | Einstieg |  Long Trade (1 Lot) bei 1,32254 |   
        | Einstieg Stragie  | Bullische Einstiegsanforderungen der dreifach Moving Average Crossover Strategie erfüllt  |   
        | Ausstieg | Handel bei 1,32504 (20:30) beendet |   
        | Gewinn | 25 Pips  |  
        | Ausstieg Stategie | Es war ein ruhiger Tag, ich saß vor dem Terminal und überwachte den Handel in seiner Gesamtheit. Beendete den Handel kurz vor dem Zielniveau, basierend auf der Angst, die bereits gewonnenen Pips zu verlieren, und nicht aufgrund von Analysen oder Marktsignalen. |    
        | Post Beobachtungen | GBPUSD stieg nach dem Verkauf weiter und durchbrach das ursprüngliche Zielniveau | 
        
        """
        )

        image = Image.open('mocks/example_trade.png')
        st.image(image, caption='Apple trade 0')