import streamlit as st
from Data.DatabaseProcess import DatabaseProcess

databaseProcess = DatabaseProcess("Database.db")

st.set_page_config(
 page_title="Diabete App",
 layout="wide",
 initial_sidebar_state="expanded",
)

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

def show_main_page():
    with mainSection:
        st.image("images/1.jpg")


def LoggedOut_Clicked():
    st.session_state['username'] = ""
    st.session_state['user_id'] = ""
    st.session_state['loggedIn'] = False


def login(userName, password):
    id = databaseProcess.getUsersId(userName, password)
    if id != None:
        st.session_state['user_id'] = id[0]
        st.session_state['username'] = userName
        return True
    else:
        return False

def sigin(userName, email, password):
    if userName == "" or email == "" or password == "":
        st.warning("veuillez remplir le formulaire")
    else:
        # Create user
        if ("@" in email) and ("." in email):
            try :
                databaseProcess.createUser(userName, email, password)
                id = databaseProcess.getUsersId(userName, password) # (1,)
                st.session_state['user_id'] = id[0]
                st.session_state['username'] = userName

                st.success("Bienvenue " + userName)
                st.session_state['loggedIn'] = True
            except:
                st.error("le nom d'utilisateur / email existe; veuillez entrer un autre")
        else:
            st.error("veuillez verifier vos infos")

def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Nom d'utilisateur ou mot de passe invalide")

def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            userName = st.text_input (label="", value="", placeholder="Nom d'utilisateur")
            password = st.text_input (label="", value="",placeholder="Mot de passe", type="password")
            st.button ("Connexion", on_click=LoggedIn_Clicked, args= (userName, password))


def show_sigin_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            col1, col2= st.columns(2)
            with col1:
                st.image("images/4.png")
            with col2:
                userName = st.text_input (label="Nom d'utilisateur", value="", placeholder="Nom d'utilisateur")
                email = st.text_input (label="Email", value="", placeholder="Email")
                password = st.text_input (label="Mot de passe", value="",placeholder="Mot de passe", type="password")
                st.button ("S'inscrire", on_click=sigin, args= (userName, email, password))

def formConnect():
    st.title("Diabete Application")
    menu = ["Connexion","Inscription"]
    choix = st.selectbox("Quel est votre choix ? Connexion / Inscription ",menu)

    if choix == "Connexion":
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        st.session_state['loggedIn'] = False
        show_sigin_page()

with headerSection:
    if 'loggedIn' not in st.session_state:
        formConnect()
    else:
        if st.session_state['loggedIn']:
            # show_logout_page()
            st.sidebar.text("Bienvenue " + st.session_state['username'])
            st.sidebar.button("Deconnexion",  on_click=LoggedOut_Clicked)
            # st.balloons()
            show_main_page()
        else:
            formConnect()
