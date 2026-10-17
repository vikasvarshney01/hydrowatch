import streamlit as st
import pickle
import components.account_page as account_page
import components.database_creation as database_creation
from streamlit_lottie import st_lottie_spinner
import json
from streamlit_lottie import st_lottie
import time
import pandas as pd
import re

def lottie_files(filepath: str):
    with open(filepath,'r') as f:
        return json.load(f)

predict_lottie_file = lottie_files("lottiefiles/water_drop.json")

@st.cache_data
def load_training_data():
    """Load the training dataset for sample selection."""
    return pd.read_csv("waterQualityPrediction.csv")

def get_parameter_columns():
    """Return the list of parameter column names in order."""
    return ['aluminium', 'ammonia', 'arsenic', 'barium', 'cadmium', 
            'chloramine', 'chromium', 'copper', 'flouride', 'bacteria',
            'viruses', 'lead', 'nitrates', 'nitrites', 'mercury',
            'perchlorate', 'radium', 'selenium', 'silver', 'uranium']

def form():
    with st.form(key='water_quality_form'):
        st.subheader("Enter Parameter Values:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            aluminium = st.text_input("Aluminium (mg/L)", key='aluminium')
            ammonia = st.text_input("Ammonia (mg/L)", key='ammonia')
            arsenic = st.text_input("Arsenic (mg/L)", key='arsenic')
            barium = st.text_input("Barium (mg/L)", key='barium')
            cadmium = st.text_input("Cadmium (mg/L)", key='cadmium')
        with col2:
            chloramine = st.text_input("Chloramine (mg/L)", key='chloramine')
            chromium = st.text_input("Chromium (mg/L)", key='chromium')
            copper = st.text_input("Copper (mg/L)", key='copper')
            flouride = st.text_input("Flouride (mg/L)", key='flouride')
            bacteria = st.text_input("Bacteria (index 0-1)", key='bacteria')
        with col3:
            viruses = st.text_input("Viruses (index 0-1)", key='viruses')
            lead = st.text_input("Lead (mg/L)", key='lead')
            nitrates = st.text_input("Nitrates (mg/L)", key='nitrates')
            nitrites = st.text_input("Nitrites (mg/L)", key='nitrites')
            mercury = st.text_input("Mercury (mg/L)", key='mercury')
        with col4:
            perchlorate = st.text_input("Perchlorate (mg/L)", key='perchlorate')
            radium = st.text_input("Radium (pCi/L)", key='radium')
            selenium = st.text_input("Selenium (mg/L)", key='selenium')
            silver = st.text_input("Silver (mg/L)", key='silver')
            uranium = st.text_input("Uranium (mg/L)", key='uranium')
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(label='Predict',type='primary')
        user_data = [aluminium , ammonia, arsenic, barium , cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, lead, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium]
        
        # Convert string inputs to floats
        try:
            x = [float(val) for val in user_data]
        except ValueError:
            st.error("Please enter valid numeric values for all parameters")
            x = [0.0] * len(user_data)
        
    return submit_button, x


def apply_uploaded_csv(uploaded_file):
    """Read a one-row CSV file and store the values in session state."""
    try:
        uploaded_data = pd.read_csv(uploaded_file)
    except Exception:
        st.error("Could not read the CSV file. Please upload a valid CSV file.")
        return False

    params = get_parameter_columns()
    missing_columns = [column for column in params if column not in uploaded_data.columns]
    if missing_columns:
        st.error(f"Missing columns in CSV: {', '.join(missing_columns)}")
        return False

    if len(uploaded_data) < 1:
        st.error("The uploaded CSV must contain at least one row.")
        return False

    row = uploaded_data.iloc[0]
    for column in params:
        st.session_state[column] = str(row[column])

    st.success("CSV loaded successfully. The first row has been copied into the parameters form.")
    return True


def apply_pasted_values(raw_values):
    """Parse pasted values and copy them into parameter fields."""
    params = get_parameter_columns()
    tokens = [token.strip() for token in re.split(r"[,\n\t; ]+", raw_values.strip()) if token.strip()]

    if len(tokens) != len(params):
        st.error(f"Please paste exactly {len(params)} values. You provided {len(tokens)} values.")
        return False

    try:
        numeric_tokens = [float(token) for token in tokens]
    except ValueError:
        st.error("Invalid pasted data. Please paste numeric values only.")
        return False

    for param, value in zip(params, numeric_tokens):
        st.session_state[param] = str(value)

    st.success("Values pasted successfully. Parameters are now auto-filled.")
    return True


def evaluate_rule_based_risk(x):
    """Apply conservative threshold rules for high-risk contamination markers."""
    values = dict(zip(get_parameter_columns(), x))
    threshold_rules = {
        'arsenic': 0.01,
        'lead': 0.015,
        'mercury': 0.002,
        'cadmium': 0.005,
        'chromium': 0.1,
        'flouride': 1.5,
        'nitrates': 10.0,
        'nitrites': 1.0,
        'barium': 2.0,
        'uranium': 0.03,
        'radium': 5.0,
        'selenium': 0.05,
    }

    violations = []
    for parameter, max_value in threshold_rules.items():
        current_value = values[parameter]
        if current_value > max_value:
            violations.append(f"{parameter}={current_value} exceeds {max_value}")

    if values['bacteria'] > 0:
        violations.append(f"bacteria={values['bacteria']} should be 0")
    if values['viruses'] > 0:
        violations.append(f"viruses={values['viruses']} should be 0")

    return violations


def evaluate_hybrid_prediction(x, model_prediction):
    """Combine model output with rule-based checks for final safety decision."""
    model_is_safe = int(model_prediction[0]) == 1
    violations = evaluate_rule_based_risk(x)
    final_is_safe = model_is_safe and len(violations) == 0
    return final_is_safe, model_is_safe, violations


def display_safety_result(final_is_safe, model_is_safe, violations):
    """Render final decision and supporting details in UI."""
    if final_is_safe:
        st.success("Water is Safe")
    else:
        st.warning("Water is Unsafe")

    if not model_is_safe and len(violations) == 0:
        st.info("Model prediction flagged this sample as unsafe.")

    if len(violations) > 0:
        st.error("Rule-based safety checks flagged high-risk values:")
        for violation in violations[:8]:
            st.write(f"- {violation}")
        if len(violations) > 8:
            st.write(f"- ...and {len(violations) - 8} more")


def model():
    st.toast(":rainbow[Please enter the values here]")
    st.title("Water Quality Parameters")
    for param in get_parameter_columns():
        st.session_state.setdefault(param, "0.0")
    
    choice = st.selectbox('Guest Mode/Registered Mode',['Guest','Registered'])
                                                                                                            
    if choice == 'Guest':
        st.markdown("### Paste Values to Auto-Fill")
        st.caption("Paste 20 numeric values separated by comma, space, tab, semicolon, or new line.")
        pasted_values = st.text_area("Paste all parameter values", key="guest_paste_values", height=90)
        if st.button("Apply Pasted Values", use_container_width=True, key="guest_apply_paste"):
            if apply_pasted_values(pasted_values):
                st.rerun()

        st.divider()

        st.markdown("### 📤 Upload CSV to Auto-Fill Parameters")
        st.caption("Upload a CSV file with the same parameter columns. The first row will be used to fill the form.")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="guest_csv_upload")
        if uploaded_file is not None and st.session_state.get("guest_csv_last_name") != uploaded_file.name:
            if apply_uploaded_csv(uploaded_file):
                st.session_state["guest_csv_last_name"] = uploaded_file.name
                st.rerun()

        if st.button("🔄 Clear Values", use_container_width=True):
            params = get_parameter_columns()
            for param in params:
                st.session_state[param] = "0.0"
            st.info("Values cleared!")
            st.rerun()

        st.divider()
        
        submit_button, x = form()
        if submit_button:
            st.write("You are in guest mode")
            with st_lottie_spinner(predict_lottie_file,height=300):
                time.sleep(2)
                with open('Rf_model.pkl', 'rb') as f:
                    loaded_model = pickle.load(f)
                    prediction = loaded_model.predict([x])
                    final_is_safe, model_is_safe, violations = evaluate_hybrid_prediction(x, prediction)
                    display_safety_result(final_is_safe, model_is_safe, violations)
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

            st.markdown("### Paste Values to Auto-Fill")
            st.caption("Paste 20 numeric values separated by comma, space, tab, semicolon, or new line.")
            pasted_values = st.text_area("Paste all parameter values", key="registered_paste_values", height=90)
            if st.button("Apply Pasted Values (Registered)", use_container_width=True, key="registered_apply_paste"):
                if apply_pasted_values(pasted_values):
                    st.rerun()

            st.divider()

            st.markdown("### 📤 Upload CSV to Auto-Fill Parameters")
            st.caption("Upload a CSV file with the same parameter columns. The first row will be used to fill the form.")
            uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="registered_csv_upload")
            if uploaded_file is not None and st.session_state.get("registered_csv_last_name") != uploaded_file.name:
                if apply_uploaded_csv(uploaded_file):
                    st.session_state["registered_csv_last_name"] = uploaded_file.name
                    st.rerun()

            if st.button("🔄 Clear Values (Registered)", use_container_width=True):
                params = get_parameter_columns()
                for param in params:
                    st.session_state[param] = "0.0"
                st.info("Values cleared!")
                st.rerun()

            st.divider()

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
                        final_is_safe, model_is_safe, violations = evaluate_hybrid_prediction(x, prediction)
                        display_safety_result(final_is_safe, model_is_safe, violations)
                    database_creation.insert_user_inputs(current_username=user_name, aluminium = x[0], ammonia=x[1], arsenic=x[2], barium=x[3], cadmium=x[4], chloramine=x[5], chromium=x[6], copper=x[7], flouride=x[8], bacteria=x[9], viruses=x[10], lead=x[11], nitrates=x[12], nitrites=x[13], mercury=x[14], perchlorate=x[15], radium=x[16], selenium=x[17], silver=x[18], uranium=x[19],is_safe=int(final_is_safe))

        else:
            account_page.app()