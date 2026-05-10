import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if database configuration exists
db_configured = all([
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_NAME")
])

config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "water_quality")
}

def connect_to_database():
    if not db_configured:
        return None
    try:
        db = mysql.connector.connect(**config)
        return db
    except mysql.connector.Error as err:
        # Silently fail - error will be handled by calling functions
        return None
        return None



def create_database():
    if not db_configured:
        return
    try:
        db = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"]
        )
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS WaterQualityMonitoringSystem")
        cursor.close()
        db.close()
    except Exception as e:
        st.warning(f"Could not create database: {e}")

def create_user_table(current_username):
    if not db_configured:
        return
    db = connect_to_database()
    if db is None:
        return
    try:
        cursor = db.cursor()
        cursor.execute("USE WaterQualityMonitoringSystem")
        create_user_table_query = f"""
        CREATE TABLE IF NOT EXISTS {current_username}_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            aluminium FLOAT,
            ammonia FLOAT,
            arsenic FLOAT,
            barium FLOAT,
            cadmium FLOAT,
            chloramine FLOAT,
            chromium FLOAT,
            copper FLOAT,
            flouride FLOAT,
            bacteria FLOAT,
            viruses FLOAT,
            `lead` FLOAT,
            nitrates FLOAT,
            nitrites FLOAT,
            mercury FLOAT,
            perchlorate FLOAT,
            radium FLOAT,
            selenium FLOAT,
            silver FLOAT,
            uranium FLOAT,
            is_safe INT
        )
        """
        cursor.execute(create_user_table_query)
        db.commit()
    except Exception as e:
        st.warning(f"Could not create user table: {e}")
    finally:
        if db:
            cursor.close()
            db.close()
    # st.write(f'{current_username}_data table was created')

def insert_user_inputs(current_username, aluminium, ammonia, arsenic, barium, cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, lead, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium, is_safe):
    if not db_configured:
        st.info("Database not configured. Prediction saved locally only.")
        return
    db = connect_to_database()
    if db is None:
        st.warning("Could not save to database.")
        return
    try:
        cursor = db.cursor()
        cursor.execute("USE WaterQualityMonitoringSystem")
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        insert_new_data_query = f"""
        INSERT INTO {current_username}_data (timestamp, aluminium, ammonia, arsenic, barium, cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, `lead`, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium, is_safe)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        insert_new_data = (current_timestamp, aluminium, ammonia, arsenic, barium, cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, lead, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium, is_safe)
        cursor.execute(insert_new_data_query, insert_new_data)
        db.commit()
        st.write("Record has been saved successfully.")
    except Exception as e:
        st.warning(f"Could not save record: {e}")
    finally:
        if db:
            cursor.close()
            db.close()
    


def show_user_table(current_username):
    if not db_configured:
        st.info("Database not configured. Cannot display user history.")
        return
    db = connect_to_database()
    if db is None:
        return
    try:
        cursor = db.cursor()

        cursor.execute("USE WaterQualityMonitoringSystem")
        select_query = f"SELECT * FROM {current_username}_data"
        cursor.execute(select_query)
        records = cursor.fetchall()

        if records:
            df = pd.DataFrame(records, columns=['id','timestamp', 'aluminium', 'ammonia', 'arsenic', 'barium', 'cadmium', 'chloramine', 'chromium', 'copper', 'flouride', 'bacteria', 'viruses', 'lead', 'nitrates', 'nitrites', 'mercury', 'perchlorate', 'radium', 'selenium', 'silver', 'uranium','is_safe'])
            with st.expander('🔎 Personal Feed - Database'):
                st.data_editor(df,hide_index=True, disabled=("id","timestamp","is_safe"))
        else:
            st.write("No Feed is recorded yet... Go and use Predicting Model for personal feed.")
    except Exception as e:
        st.warning(f"Could not retrieve records: {e}")
    finally:
        if db:
            cursor.close()
            db.close()
    
    


def get_database(current_username):
    if not db_configured:
        return None
    db = connect_to_database()
    if db is None:
        return None
    try:
        cursor = db.cursor()

        cursor.execute("USE WaterQualityMonitoringSystem")
        select_query = f"SELECT * FROM {current_username}_data"
        cursor.execute(select_query)
        records = cursor.fetchall()

        if records:
            df = pd.DataFrame(records, columns=['id','timestamp', 'aluminium', 'ammonia', 'arsenic', 'barium', 'cadmium', 'chloramine', 'chromium', 'copper', 'flouride', 'bacteria', 'viruses', 'lead', 'nitrates', 'nitrites', 'mercury', 'perchlorate', 'radium', 'selenium', 'silver', 'uranium','is_safe'])
            return df
        return None
    except Exception as e:
        st.warning(f"Could not get database: {e}")
        return None
    finally:
        if db:
            cursor.close()
            db.close()
