import streamlit as st
import plotly.graph_objects as go # pip install plotly
from Data.DatabaseProcess import DatabaseProcess

databaseProcess = DatabaseProcess("Database.db")

if st.session_state['loggedIn']:

    def LoggedOut_Clicked():
        st.session_state['username'] = ""
        st.session_state['user_id'] = ""
        st.session_state['loggedIn'] = False


    st.sidebar.text("Bienvenue " + st.session_state['username'])
    st.sidebar.button("Deconnexion",  on_click=LoggedOut_Clicked)

    st.title('Résultats: ')

    st.subheader("Historique des analyses ")

    # Get User resuts
    resuls = databaseProcess.getUserResults(st.session_state['user_id'])
    resuls.reverse()

    date            = []
    heure           = []
    bilan           = []
    prediction      = []

    for value in resuls:
        date.append(value[0])
        heure.append(value[1])
        bilan.append(value[2])
        prediction.append(value[3])

    # st.write(resuls)

    fig = go.Figure(data=go.Table(
        header=dict(values=["<b>Date</b>", "<b>Heure</b>", "<b>Bilan</b>", "<b>Prediction</b>"],
                    font=dict(color='black', size=12),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[date, heure, bilan, prediction], align='left'))

    )
    fig.update_layout(margin=dict(l=5,r=5,b=10,t=10), width=1300, height=500)
    st.write(fig)

else:
    st.subheader("Vous devez vous connecter pour avoir accès à cette page.")