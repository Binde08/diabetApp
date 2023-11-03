import streamlit as st
import os
from datetime import datetime
import joblib
from Data.DatabaseProcess import DatabaseProcess

databaseProcess = DatabaseProcess("Database.db")

if st.session_state['loggedIn']:

    def LoggedOut_Clicked():
        st.session_state['username'] = ""
        st.session_state['user_id'] = ""
        st.session_state['loggedIn'] = False


    st.sidebar.text("Bienvenue " + st.session_state['username'])
    st.sidebar.button("Deconnexion",  on_click=LoggedOut_Clicked)

    st.title('Prédiction: ')

    st.subheader("Veuillez entrer vos informations")

    col1, col2, col3 = st.columns(3)

    with col1:
       # st.header("groupe")
       # st.image("im.jpg")
       # ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
       Pregnancies = st.number_input("Grossesses", key="inpu1", min_value=0.0)
       Glucose = st.number_input("Glucose", key="inpu2", min_value=0.0)
       BloodPressure = st.number_input("Pression Arterielle", key="inpu3", min_value=0.0)

    with col2:
       SkinThickness = st.number_input("Epaisseur de la peau", key="inpu4", min_value=0.0)
       Insulin = st.number_input("Insuline", key="inpu5", min_value=0.0)
       BMI = st.number_input("IMC", key="inpu6", min_value=0.0)

    with col3:
       DiabetesPedigreeFunction = st.number_input("DiabetesPedigreeFonction", key="inpu7", min_value=0.0)
       Age = st.number_input("Age", key="inpu9", min_value=0.0)


    submit = st.button("Predire")

    modele_path = os.path.dirname(os.path.abspath((__file__))) + "/forestmodel.joblib"
    forest_model = joblib.load(modele_path)
    data = [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]

    if submit:
        if (Pregnancies == 0.0 and Glucose == 0.0 and BloodPressure == 0.0 and SkinThickness == 0.0 and Insulin == 0.0 and BMI == 0.0 and DiabetesPedigreeFunction == 0.0 and Age == 0):
            st.warning('Veuillez entrer des valeurs svp')
        elif (Pregnancies >= 0.0 and Glucose >= 0.0 and BloodPressure >= 0.0 and SkinThickness >= 0.0 and Insulin >= 0.0 and BMI >= 0.0 and DiabetesPedigreeFunction >= 0.0 and Age >= 0):

            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            date, time = dt_string.split(" ")[0], dt_string.split(" ")[1]

            en_savoir_plus = ("Etre diabétique: Cela signifie que ton taux de glucose dans le sang est trop élevé. \n"
                                  " Le glucose est un sucre que ton corps utilise comme source d'énergie. \n "
                                  "Il est absorbé par le sang après avoir été ingéré sous forme de glucides. \n "
                                  "Lorsque tu es diabétique, ton corps ne produit pas assez d'insuline ou ne l'utilise pas correctement. \n "
                                  "L'insuline est une hormone qui permet au glucose de pénétrer dans les cellules pour être utilisé comme source d'énergie. \n "
                                  "Le diabète peut avoir des conséquences graves sur la santé, si on ne le contrôle pas. \n "
                                  "Il peut entraîner des complications cardiaques, des accidents vasculaires cérébraux, des problèmes de vision et des problèmes rénaux. \n "
                                  "Il est important de prendre des mesures pour contrôler ton diabète. \n "
                                  "Tu devras suivre un régime alimentaire sain, faire de l'exercice régulièrement et prendre des médicaments, si nécessaire.")
            def morebtn():
                return st.info(en_savoir_plus)

            if forest_model.predict(data)[0] == 1 :
                bilan = "Selon nos analyses vous souffrez du diabete car votre taux insuline est faible (votre organisme n'utilise pas l'insuline produit) et votre concentration sanguine elevé de sucre (glucose)"
                prediction = "Diabétique"
                st.error(bilan)

                st.button ("En savoir plus...", on_click=morebtn)

            else:
                bilan = "Selon nos analyses tout semble normal, vous n'etes pas diabibetique."
                prediction = "Non Diabétique"
                st.success(bilan)

                st.button ("En savoir plus...", on_click=morebtn)

            # insert results
            databaseProcess.createUserResult(date, time, bilan, prediction, st.session_state['user_id'])

else:
    st.subheader("Vous devez vous connecter pour avoir accès à cette page.")
