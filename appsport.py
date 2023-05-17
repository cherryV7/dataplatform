import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

# --- USER AUTHENTICATION ---
names = ["Przemysław Zych", "Szymon Winiewski"]
usernames = ["pzych", "swisniewski"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "legia", "lab", cookie_expiry_days=0)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- READ EXCEL ----

        # Załadowanie danych
    data = pd.read_csv('..\data_s&c4.csv')
    data['Data'] = pd.to_datetime(data['Data'])  # Konwersja kolumny Data na typ daty


        # Tytuł aplikacji)
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Witaj {name}")
    st.title('Porównanie wyników zawodników')

    # Wybór zawodników do porównania
    players = st.multiselect('Wybierz zawodników', data['Zawodnik'].unique())

    # Wybór wartości do porównania
    values = st.selectbox('Wybierz wartość', data.columns[4:])

    # Wybór przedziału czasowego
    dates = sorted(data['Data'].dt.date.unique())  # Unikalne daty
    start_date = st.selectbox('Wybierz datę początkową', dates)
    end_date = st.selectbox('Wybierz datę końcową', dates)

    # Filtracja danych dla wybranych zawodników i przedziału czasowego
    filtered_data = data[data['Zawodnik'].isin(players)]
    filtered_data = filtered_data[(filtered_data['Data'].dt.date >= start_date) & (filtered_data['Data'].dt.date <= end_date)]

    # Wykres interaktywny
    fig = px.line(filtered_data, x='Data', y=values, color='Zawodnik', title='Porównanie wyników zawodników',
                text=values)  # Dodanie etykiet wyników
    fig.update_traces(textposition='top center')  # Umieszczenie etykiet na górze punktów

    # Konfiguracja osi X
    fig.update_xaxes(title_text='Data')

    # Konfiguracja osi Y
    fig.update_yaxes(title_text='Wynik')

    st.plotly_chart(fig)
