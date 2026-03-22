# -----> Required libraries 
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import requests
import json
import os
from dotenv import load_dotenv
import components.database_creation as database_creation
from streamlit_lottie import st_lottie

# Load environment variables from .env file
load_dotenv()

def lottie_files(filepath: str):
    with open(filepath,'r') as f:
        return json.load(f)

login_lottie_file = lottie_files("lottiefiles/login.json")

fb_credentials = os.getenv("FIREBASE_CREDENTIALS")

# Initialize Firebase only if credentials are available
firebase_initialized = False
if fb_credentials and not firebase_admin._apps:
    try:
        cred = credentials.Certificate(fb_credentials)
        firebase_admin.initialize_app(cred)
        firebase_initialized = True
    except Exception as e:
        st.warning(f"Firebase initialization failed: {e}")
        firebase_initialized = False

# Note: Session state initialization is now done in app.py


def app():
    
    # Check if Firebase is configured
    if not firebase_initialized:
        st.error("🔧 Firebase Authentication Not Configured")
        st.info("""
        Firebase credentials are not set up. To enable user authentication:
        
        1. Set up a Firebase project at https://firebase.google.com
        2. Download your Firebase credentials JSON file
        3. Set the FIREBASE_CREDENTIALS environment variable to point to your credentials file
        
        For now, you can use Guest Mode in the Prediction Model page.
        """)
        return
    
    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):  
        try:
            # Validate email format
            email = email.strip()  # Remove whitespace
            if not email or '@' not in email or '.' not in email:
                st.error("Please enter a valid email address")
                return None
            
            # Validate password
            if not password or len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return None
            
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            # -----> make sure you insert your firebase passkey here 
            r = requests.post(rest_api_url, params={"key": "AIzaSyAPKhhz8TSHOPW9mXl7JEm_Cnj3Ms9X-T8"}, data=payload)
            
            response_data = r.json()
            
            # Check for errors
            if 'error' in response_data:
                error_message = response_data['error'].get('message', 'Unknown error')
                if error_message == 'EMAIL_EXISTS':
                    st.error("This email is already registered. Please login instead.")
                elif error_message == 'INVALID_EMAIL':
                    st.error("Invalid email format. Please enter a valid email address (e.g., user@example.com)")
                elif error_message == 'WEAK_PASSWORD':
                    st.error("Password is too weak. Please use at least 6 characters.")
                else:
                    st.error(f"Signup failed: {error_message}")
                return None
            
            return response_data.get('email')
        except Exception as e:
            st.error(f'Signup failed: {e}')
            return None

    def sign_in_with_email_and_password(email, password, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            # Validate inputs
            email = email.strip() if email else ""
            
            if not email:
                st.error("Please enter your email address")
                return None
            
            if not password:
                st.error("Please enter your password")
                return None
            
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token,
            }
           
            payload = json.dumps(payload)
            # -----> make sure you insert your firebase passkey here 
            r = requests.post(rest_api_url, params={"key": "AIzaSyAPKhhz8TSHOPW9mXl7JEm_Cnj3Ms9X-T8"}, data=payload)
            
            data = r.json()
            
            # Check for errors
            if 'error' in data:
                error_message = data['error'].get('message', 'Unknown error')
                if error_message == 'EMAIL_NOT_FOUND':
                    st.error("Email not found. Please sign up first.")
                elif error_message == 'INVALID_PASSWORD':
                    st.error("Invalid password. Please try again.")
                elif error_message == 'INVALID_EMAIL':
                    st.error("Invalid email format.")
                elif error_message == 'USER_DISABLED':
                    st.error("This account has been disabled.")
                else:
                    st.error(f"Sign-in failed: {error_message}")
                return None
            
            user_info = {
                'email': data['email'],
                'username': data.get('displayName')  # Retrieve username if available
            }
            return user_info
            
        except Exception as e:
            st.error(f'Sign-in failed: {e}')
            return None

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            # -----> make sure you insert your firebase passkey here 
            r = requests.post(rest_api_url, params={"key": "AIzaSyAPKhhz8TSHOPW9mXl7JEm_Cnj3Ms9X-T8"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)
          
    def authentication():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            
            if userinfo:  # Check if login was successful
                st.session_state.username = userinfo['username'] if userinfo['username'] else userinfo['email'].split('@')[0]
                st.session_state.useremail = userinfo['email']

                global Usernm
                Usernm = st.session_state.username

                st.session_state.signedout = True
                st.session_state.signout = True
            else:
                st.error("Login failed. Please check your credentials.")
        except Exception as e:
            st.error(f"Login Failed: {e}")
           
    def signout():
        st.session_state.signedout = False
        st.session_state.signout = False
        st.session_state.username = ''       
                           
                                            
    def forget():
        st.subheader("Forgot Password...❓",divider='gray')
        email = st.text_input('Email')
        if st.button("Send Link"):
            try:
                success, message = reset_password(email)
                if success:
                    st.success("Password reset email sent successfully.")
                else:
                    st.warning(f"Password reset failed: {message}")
            except:
                st.warning("Process Failed.....")
                
    def analysis():
        st.markdown(
            f"""
            <style>
            .analysis {{
                font-size: 2em;
                font-weight: bold;
                color: grey ;
                background: #f0f0f0;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 2px 2px 12px #aaaaaa;
                margin: 0px 0px 8px 0px;
            }}
            </style>
            <div class="analysis">
                Analysis Report
            </div>
            """,
            unsafe_allow_html=True
        )              
        st.subheader("Personal Data :open_file_folder:",divider='rainbow')
        
        # Check if database is configured
        if not database_creation.db_configured:
            st.info("""
            📊 **Database Storage Not Configured**
            
            Your prediction results are currently not being saved to a database.
            
            **To enable data storage and history:**
            1. Install MySQL on your system
            2. Configure the database credentials in `.env` file:
               ```
               DB_HOST=localhost
               DB_PORT=3306
               DB_USER=your_username
               DB_PASSWORD=your_password
               DB_NAME=water_quality
               ```
            3. Restart the application
            
            For now, you can still use **Registered Mode** for predictions - they just won't be saved permanently.
            """)
            return
        
        try:
            database_creation.show_user_table(current_username= st.session_state.username)
            data = database_creation.get_database(st.session_state.username)
            
            if data is None or len(data) == 0:
                st.info("No prediction history yet. Go to the Prediction Model page to make your first prediction!")
                return
            
            with st.container(border=True):
                st.header("EDA Report",divider='grey')
                c1,c2,c3 =st.columns(3)
                with c1:
                   st.line_chart(data,x='timestamp',y='aluminium',color='#1995ad')
                   st.line_chart(data,x='timestamp',y='ammonia',color='#1995ad')
                   st.line_chart(data,x='timestamp',y='arsenic',color='#1995ad')
                   st.line_chart(data,x='timestamp',y='barium',color="#1995ad") 
                   st.line_chart(data,x='timestamp',y='cadmium',color="#1995ad") 
                   st.line_chart(data,x='timestamp',y='chloramine',color="#1995ad")
                   st.line_chart(data,x='timestamp',y='chromium',color="#1995ad")
                 
                with c2:
                    st.line_chart(data,x='timestamp',y='copper',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='flouride',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='bacteria',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='viruses',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='lead',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='nitrates',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='nitrites',color="#1995ad")
                		
                with c3:
                    st.line_chart(data,x='timestamp',y='mercury',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='perchlorate',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='radium',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='selenium',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='silver',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='uranium',color="#1995ad")
                    st.bar_chart(data,x='timestamp',y='is_safe',color="#1995ad")
        except Exception as e:
            st.error(f"Error loading analysis data: {e}")
            st.info("If you just made your first prediction, try refreshing the page.")
    
    # if the state is signed out means not sign in till now
    if  not st.session_state["signedout"]:
        st.toast("Please login for Personalized analysis",icon=":material/login:")
        # only show if the state is False, hence the button has never been clicked
        
        with st.container(border=True):
            c1,c2 = st.columns(2,vertical_alignment='center',gap='medium')
            with c1:
                st_lottie(login_lottie_file,speed=1,reverse=False,loop=True,quality='high',height=585)
            with c2:
                
                # Set default to Login if signup was successful
                default_choice = 0 if st.session_state.show_signup_success else 1
                choice = st.selectbox('Login/Signup',['Login','Sign up'], index=default_choice)
                
                # Show success message if signup just completed
                if st.session_state.show_signup_success and choice == 'Login':
                    st.success('✅ Account created successfully! Please login below.')
                    st.session_state.show_signup_success = False
                
                with st.container(border=True):
                    if choice == 'Sign up':
                        st.info("📧 Please use a valid email format (e.g., user@example.com)")
                        email = st.text_input('Email Address', placeholder="user@example.com")
                        password = st.text_input('Password (min 6 characters)',type='password', placeholder="Min 6 characters")
                        username = st.text_input("Enter your unique username", placeholder="Your display name")
                        
                        if st.button('Create my account',type='primary'):
                            # Validate inputs before submission
                            if not email:
                                st.error("Please enter an email address")
                            elif not password:
                                st.error("Please enter a password")
                            elif not username:
                                st.error("Please enter a username")
                            else:
                                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                                if user:
                                    st.session_state.show_signup_success = True
                                    st.balloons()
                                    st.rerun()
                    else:
                        st.markdown(f"""
                            <style>
                            .greeting {{
                                font-size: 2em;
                                font-weight: bold;
                                color:black;
                                padding: 10px;
                                border-radius: 10px;
                                text-align: center
                            }}
                            .messages {{
                                font-weight: bold;
                                text-align: center;
                            }}
                            </style>

                            <div class='greeting'>
                                Welcome Back
                            </div>
                            <div class='messages'>
                                Enter your credentials
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.info("Please press :red-background[ENTER] once you enter the details to apply the updated values.")
                        email = st.text_input('Email Address')
                        password = st.text_input('Password',type='password')
                        st.session_state.email_input = email
                        st.session_state.password_input = password
                        st.button('Login', on_click= authentication,type='primary')
                        st.write("---")
                        with st.expander("Forgot Password",icon="❓️",expanded=False):
                            forget()
        
        

    
            
                                                                       
    if st.session_state.signout:
        # Assuming username and useremail are stored in session_state
        st.toast("Thanks for logging in ",icon="🙏")
        if 'username' in st.session_state and 'useremail' in st.session_state:
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
                    Account Information
                </div>
                """,
                unsafe_allow_html=True
            )              
            
            st.markdown(
                f"""
                <style>
                .information {{
                    font-size: 2em;
                    font-weight: bold;
                    color:#1995ad;
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 10px;
                    text-align:left ;
                    box-shadow: 2px 2px 12px #aaaaaa;
                    margin: 0px 0px 8px 0px;
                    display: flex;
                    justify-content: space-between
                }}
                </style>
                <div class="information">
                    <div style='color: #1995AD; font-size: large' ><b style='color: black; font-size:20px' >Name:</b> {st.session_state.username}</div>
                    <div style='color: #1995AD; font-size: large'><b style='color: black; font-size:20px' >Email id:</b> {st.session_state.useremail}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
                  
        # col1, col8 = st.columns(spec=[8,5], gap="large")
        st.button('Sign Out', on_click=signout,type='primary')
        st.write("---")
        analysis()
                     
def credentials():
    if not firebase_initialized:
        return ""
    # Check if username exists in session state and is not empty
    if 'username' in st.session_state and st.session_state.username:
        return st.session_state.username
    return ""
