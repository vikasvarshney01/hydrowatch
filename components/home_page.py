import streamlit as st
import json
from streamlit_lottie import st_lottie


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
 
lottie_water_plant = load_lottiefile('lottiefiles/water_plant.json')

def home():
    st.toast("꧁ ༺ 𝐖𝐄𝐋𝐂🌏𝐌𝐄 ༻ ꧂",icon='🙏')
    
    st.markdown("""<h1 style=' text-align: center; color: #1995AD; font-size: 90px;'>
    <span style='color:#00131a; font-weight: bold; text-shadow: 4px 2px #888888; font-family:Gill Sans, sans-serif'>HydroWatch </span>
                : Water Quality Monitoring and Prediction System</h1>""", unsafe_allow_html=True)
    st_lottie(lottie_water_plant,speed=1, loop=True,quality='medium',reverse=False,)
    st.markdown("""<marquee behavior='scroll' direction='left' scrollamount='10' style='color: #1995AD ; font-size: 50px'>Welcome to 
                <span style='color: black; text-shadow: 4px 1px #888888'>HydroWatch</sapn></marquee>""", unsafe_allow_html=True)
    st.markdown("""
        <p style='font-size: 20px'>HydroWatch is a water quality monitoring system that helps you assess the quality of your water based on various parameters.
        Whether you're a homeowner, a researcher, or a water treatment professional, HydroWatch provides valuable insights into the health of your water.</p>

        ## About HydroWatch
        <p style='font-size: 20px'>HydroWatch uses machine learning models to predict water quality based on factors such as <span style='font-size: 20px;
        color: #1995AD; font-weight: bold'>Bacteria, Viruses, Chloramine, Chromium</span> and <span style='font-size: 20px; color: #1995AD; font-weight: bold'>more</span>.
        You can either get a one-time prediction as a guest user or register to get personalized predictions and store your data for future analysis.</p>

        ## Features
        <ul style='font-size: 20px'>
        <li style='font-size: 20px'><span style ='font-weight: bold'>Prediction Model</span>: Predict water quality based on input parameters.</li>
        <li style='font-size: 20px'><span style ='font-weight: bold'>Database</span>: Explore the data used to train the prediction model.</li>
        <li style='font-size: 20px'><span style ='font-weight: bold'>Account</span>: View your account details and water quality analysis.</li>
        <li style='font-size: 20px'><span style ='font-weight: bold'>User Data</span>: View the data you've entered.</li>
        </ul>

        ## How to Use
        <ol>
        <li style='font-size: 20px'>Select the desired page from the sidebar menu.</li>
        <li style='font-size: 20px'>Follow the instructions on each page to interact with the app.</li>
        </ol>

        ## About Developer
        <p style='font-size: 20px'>HydroWatch is developed by a student(Satwik Uppada) of Lovely Professional University with a passion for making clean water accessible to all
        . If you have any questions or feedback, feel free to reach out to us.</p> 

        <p style='font-size: 20px; color: #1995AD; font-weight: bold'>Thank you for using HydroWatch!</p>
    """,unsafe_allow_html=True)