import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
from PIL import Image
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

# Importa le funzioni per la gestione del roster
from roster import create_table, add_giocatore, mostra_roster

# Crea la tabella del roster se non esiste
create_table()

st.title("Gestione Sessione di Tiro")
st.sidebar.title("Menu")
pagina = st.sidebar.radio("Scegli una sezione", ["Roster", "Sessione di Tiro", "Report"])

# ------------------ SEZIONE ROSTER ------------------
if pagina == "Roster":
    st.header("Gestione Roster")
    with st.form("aggiungi_giocatore"):
        nome = st.text_input("Nome")
        cognome = st.text_input("Cognome")
        numero = st.number_input("Numero", min_value=0, step=1)
        ruolo = st.text_input("Ruolo")
        submitted = st.form_submit_button("Aggiungi giocatore")
        if submitted:
            add_giocatore(nome, cognome, numero, ruolo)
            st.success("Giocatore aggiunto!")
    st.subheader("Roster")
    roster = mostra_roster()
    st.table(roster)

# ------------------ SEZIONE SESSIONE DI TIRO ------------------
elif pagina == "Sessione di Tiro":
    st.header("Inserimento Sessione di Tiro")
    
    # Recupera il roster dal database
    roster = mostra_roster()
    if not roster:
        st.warning("Il roster è vuoto. Aggiungi almeno un giocatore nella sezione 'Roster'.")
    else:
        # Crea una lista formattata per la selezione dei giocatori
        giocatori_lista = [f"{g[1]} {g[2]} (#{g[3]})" for g in roster]
        mapping_giocatori = {f"{g[1]} {g[2]} (#{g[3]})": g[0] for g in roster}
        
        with st.form("form_sessione"):
            # Data della sessione
            data_sessione = st.date_input("Data della Sessione", value=datetime.date.today())
            
            # Selezione giocatori
            giocatori_selezionati = st.multiselect("Seleziona i giocatori della sessione:", options=giocatori_lista)
            
            # Selezione della tipologia di tiro
            tipologia_tiro = st.selectbox("Tipologia del Tiro", options=["3 punti", "Media distanza", "Colpo a canestro"])
            
            # Inserimento dei dati dei tiri
            tiri_tentati = st.number_input("Numero di Tiri Tentati", min_value=0, value=0, step=1)
            tiri_realizzati = st.number_input("Numero di Tiri Realizzati", min_value=0, value=0, step=1)
            
            if tiri_realizzati > tiri_tentati:
                st.error("I tiri realizzati non possono essere maggiori di quelli tentati.")
            
            # Sezione per selezionare le posizioni dei tiri sul campo
            st.markdown("### Seleziona la posizione dei tiri sul campo")
            st.info("Clicca sull'immagine per registrare le coordinate (x, y) da cui sono stati effettuati i tiri.")
            
            # Carica l'immagine del campo
            try:
                court_image = Image.open("court.jpg")
            except Exception as e:
                st.error("Immagine del campo non trovata. Assicurati di avere 'court.png' nella cartella del progetto.")
                st.stop()
            
            # Dimensioni standard del campo (ad es. 94x50 piedi)
            court_width, court_height = 94, 50
            fig = go.Figure()
            fig.add_layout_image(
                dict(
                    source=court_image,
                    xref="x",
                    yref="y",
                    x=0,
                    y=court_height,  # l'immagine parte dall'angolo in alto
                    sizex=court_width,
                    sizey=court_height,
                    sizing="stretch",
                    opacity=0.8,
                    layer="below"
                )
            )
            # Imposta gli assi
            fig.update_xaxes(range=[0, court_width], showgrid=False, zeroline=False)
            fig.update_yaxes(range=[0, court_height], showgrid=False, zeroline=False, scaleanchor="x", scaleratio=1)
            fig.update_layout(
                width=600,
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                clickmode="event+select"
            )
            
            # Cattura i click sul grafico
            selected_points = plotly_events(fig, click_event=True)
            
            # Mostra il grafico aggiornato con eventuali marker
            if selected_points:
                # Aggiungi marker per ciascun click e mostra le coordinate selezionate
                for point in selected_points:
                    x = point.get("x")
                    y = point.get("y")
                    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color="red", size=12)))
                st.write("Coordinate selezionate:")
                st.write(selected_points)
            
            st.plotly_chart(fig)
            
            # Pulsante per invio del form
            submitted = st.form_submit_button("Salva Sessione")
            
            if submitted:
                if tiri_realizzati > tiri_tentati:
                    st.error("I tiri realizzati non possono essere maggiori di quelli tentati.")
                elif not giocatori_selezionati:
                    st.error("Seleziona almeno un giocatore per la sessione.")
                elif not selected_points:
                    st.error("Seleziona almeno una posizione sul campo.")
                else:
                    sessione = {
                        "data": data_sessione,
                        "giocatori": [mapping_giocatori[g] for g in giocatori_selezionati],
                        "tipologia_tiro": tipologia_tiro,
                        "tiri_tentati": tiri_tentati,
                        "tiri_realizzati": tiri_realizzati,
                        "posizioni": selected_points
                    }
                    # Qui potresti salvare la sessione su un database o file.
                    st.success("Sessione salvata correttamente!")
                    st.write("Dettagli della sessione:")
                    st.json(sessione)

# ------------------ SEZIONE REPORT ------------------
elif pagina == "Report":
    st.header("Report e Statistiche")
    st.info("Sezione report da implementare")