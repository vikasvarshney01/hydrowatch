import streamlit as st
import pickle
import components.account_page as account_page
import components.database_creation as database_creation
from streamlit_lottie import st_lottie_spinner
import json
from streamlit_lottie import st_lottie
import time

def lottie_files(filepath: str):
    with open(filepath,'r') as f:
        return json.load(f)

predict_lottie_file = lottie_files("lottiefiles/water_drop.json")

def form():
    with st.form(key='water_quality_form'):
        st.subheader("Enter Parameter Values:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            aluminium = st.text_input("Aluminium", value="0.0")
            ammonia = st.text_input("Ammonia", value="0.0")
            arsenic = st.text_input("Arsenic", value="0.0")
            barium = st.text_input("Barium", value="0.0")
            cadmium = st.text_input("Cadmium", value="0.0")
        with col2:
            chloramine = st.text_input("Chloramine", value="0.0")
            chromium = st.text_input("Chromium", value="0.0")
            copper = st.text_input("Copper", value="0.0")
            flouride = st.text_input("Flouride", value="0.0")
            bacteria = st.text_input("Bacteria", value="0.0")
        with col3:
            viruses = st.text_input("Viruses", value="0.0")
            lead = st.text_input("Lead", value="0.0")
            nitrates = st.text_input("Nitrates", value="0.0")
            nitrites = st.text_input("Nitrites", value="0.0")
            mercury = st.text_input("Mercury", value="0.0")
        with col4:
            perchlorate = st.text_input("Perchlorate", value="0.0")
            radium = st.text_input("Radium", value="0.0")
            selenium = st.text_input("Selenium", value="0.0")
            silver = st.text_input("Silver", value="0.0")
            uranium = st.text_input("Uranium", value="0.0")
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(label='Predict',type='primary')
        user_data = [aluminium , ammonia, arsenic, barium , cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, lead, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium]
        x = user_data
        
    return submit_button, x


def model():
    st.toast(":rainbow[Please enter the values here]")
    st.title("Water Quality Parameters")
    
    choice = st.selectbox('Guest Mode/Registered Mode',['Guest','Registered'])
                                                                                                            
    if choice == 'Guest':
        submit_button, x = form()
        if submit_button:
            st.write("You are in guest mode")
            with st_lottie_spinner(predict_lottie_file,height=300):
                time.sleep(2)
                with open('Rf_model.pkl', 'rb') as f:
                    loaded_model = pickle.load(f)
                    prediction = loaded_model.predict([x])
                    if prediction == [0]:
                        st.success("Water is Safe")
                    else:
                        st.warning("Water is Unsafe")
        else:
            st.info("Please enter new values and click the Predict button for your results")
            
    if choice == 'Registered':                                                                                                                                                                                
        if account_page.credentials() != "":
            user_name = account_page.credentials()
        
            st.markdown(
                f"""
                <style>
                .greeting {{
                    font-size: 2em;
                    font-weight: bold;
                    color:#1995ad;
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 2px 2px 12px #aaaaaa;
                    margin: 0px 0px 8px 0px;
                }}
                </style>
                <div class="greeting">
                    Hello, {user_name}!
                </div>
                """,
                unsafe_allow_html=True
            )
            
            submit_button, x = form()
            if submit_button:
                database_creation.connect_to_database()
                database_creation.create_database()
                database_creation.create_user_table(current_username=user_name)
                with st_lottie_spinner(predict_lottie_file,height=300):
                    time.sleep(2)
                    with open('Rf_model.pkl', 'rb') as f:
                        loaded_model = pickle.load(f)
                        prediction = loaded_model.predict([x])
                        if prediction == [0]:
                            st.success("Water is Safe")
                        else:
                            st.warning("Water is Unsafe")
                    database_creation.insert_user_inputs(current_username=user_name, aluminium = x[0], ammonia=x[1], arsenic=x[2], barium=x[3], cadmium=x[4], chloramine=x[5], chromium=x[6], copper=x[7], flouride=x[8], bacteria=x[9], viruses=x[10], lead=x[11], nitrates=x[12], nitrites=x[13], mercury=x[14], perchlorate=x[15], radium=x[16], selenium=x[17], silver=x[18], uranium=x[19],is_safe=int(prediction[0]))

        else:
            account_page.app()