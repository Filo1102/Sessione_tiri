# roster.py

import sqlite3
import streamlit as st

def create_table():
    conn = sqlite3.connect("basket_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS giocatori (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cognome TEXT,
            numero INT,
            ruolo TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_giocatore(nome, cognome, numero, ruolo):
    conn = sqlite3.connect("basket_data.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO giocatori (nome, cognome, numero, ruolo)
        VALUES (?, ?, ?, ?)
    ''', (nome, cognome, numero, ruolo))
    conn.commit()
    conn.close()
    st.success("Giocatore aggiunto con successo!")

def mostra_roster():
    conn = sqlite3.connect("basket_data.db")
    c = conn.cursor()
    c.execute("SELECT id, nome, cognome, numero, ruolo FROM giocatori")
    roster = c.fetchall()
    conn.close()
    return roster
