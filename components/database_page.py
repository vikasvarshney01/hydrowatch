import streamlit as st
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
# Try to import pygwalker Streamlit renderer; degrade gracefully if unavailable
try:
    from pygwalker.api.streamlit import StreamlitRenderer
    pygwalker_available = True
except Exception:
    pygwalker_available = False


warnings.filterwarnings('ignore')


def database():
    st.toast("Explore the model building",icon=':material/model_training:')
    st.title('Data Exploration')
    st.write("## Dataset used to train this Model")
    st.toast(":blue[Please wait for sometime, Graphs are loading in the background]",icon=":material/run_circle:")
    
    @st.cache_data
    def load_data():
        original_data = pd.read_csv("waterQualityPrediction.csv")
        cleaned_data = pd.read_csv("output_file.csv")
        return original_data, cleaned_data
    
    original_data, cleaned_data = load_data()
    with st.expander('🔎 Original Dataframe Preview',icon=':material/expand_all:'):
        st.write(original_data)
    
        
    with st.expander('🔎 Cleaned Data Preview',icon=':material/expand_all:'):
        st.write(cleaned_data)  
        
        
    with st.container(border=True):
       
        st.title("EDA Report")
        st.divider()
        
        histogram, boxplot, heatmap = st.tabs(['Histrogram Distribution','Box Plots','Correlation-Heatmap'])
        
        
        with histogram:
            with st.status(label="Visualizing",state='running',expanded=False) as status:
                c1,c2 =st.columns(2)
                with c1:
                    # Display histograms for each numeric variable
                    st.header("Distribution of  Original Data",divider='grey')
                    original_data = original_data[original_data['ammonia'] != '#NUM!']
                    original_data['ammonia'] = original_data['ammonia'].astype('float')
                    original_data['is_safe'] = original_data['is_safe'].astype('int64')
                    for column in original_data.columns:
                        if original_data[column].dtype in ['float64', 'int64']:
                            plt.figure(figsize=(10, 4))
                            sns.histplot(original_data[column], kde=True, color='#1995ad')
                            plt.title(f'Histogram of {column}')
                            st.pyplot(plt)
                            plt.clf()
                              
                with c2:       
                    # Display histograms for each numeric variable
                    st.header("Distribution of Cleaned data",divider='grey')
                    for column in cleaned_data.columns:
                        if cleaned_data[column].dtype in ['float64', 'int64']:
                            plt.figure(figsize=(10, 4))
                            sns.histplot(cleaned_data[column], kde=True,color='#1195ad')
                            plt.title(f'Histogram of {column}')
                            st.pyplot(plt)
                            plt.clf()
                st.info("Don't worry about imbalanced data. I used SMOTE technique to balance it, while creating model", icon=':material/circle_notifications:')
                status.update(label="Visualization of Histogram", state='complete',expanded=True)
        with boxplot:
            with st.status(label="Visualizing",state='running',expanded=False) as status:
                c1, c2 = st.columns(2)
                with c1:
                    st.header("Box Plots of Original Data", divider='grey')
                    for column in original_data.columns:
                        if original_data[column].dtype in ['float64', 'int64']:
                            plt.figure(figsize=(10, 4))
                            sns.boxplot(x=original_data[column],color='#1995ad')
                            plt.title(f'Box Plot of {column}')
                            st.pyplot(plt)
                            plt.clf()

                with c2:
                    st.header("Box Plots of Cleaned data",divider='grey')
                    for column in cleaned_data.columns:
                        if cleaned_data[column].dtype in ['float64', 'int64']:
                            plt.figure(figsize=(10, 4))
                            sns.boxplot(x=cleaned_data[column],color='#1995ad')
                            plt.title(f'Box Plot of {column}')
                            st.pyplot(plt)
                            plt.clf()
                status.update(label="Visualization of Boxplots", state='complete',expanded=True)

        with heatmap:
            with st.status(label="Visualizing",state='running',expanded=False) as status:
                c1,c2 =st.columns(2)
                with c1:          
                    st.header("Correlation Heatmap of original data",divider='grey')
                    plt.figure(figsize=(14, 10))
                    correlation_matrix = cleaned_data.corr()
                    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
                    plt.title("Correlation Heatmap")
                    st.pyplot(plt)

                with c2:
                    st.header("Correlation Heatmap of cleaned data",divider='grey')
                    plt.figure(figsize=(14, 10))
                    correlation_matrix = original_data.corr()
                    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
                    plt.title("Correlation Heatmap")
                    st.pyplot(plt)
                status.update(label="Visualization of Histogram", state='complete',expanded=True)
            

    st.header("Try out...new interactive visualization with your own ideas",divider='rainbow')
    
    with st.status("Rendering Tableau in Streamlit",state='running',expanded=False) as status_2:
        if pygwalker_available:
            pyg_app = StreamlitRenderer(dataset= cleaned_data,appearance='light')
            pyg_app.explorer(default_tab='data')
        else:
            st.info("Interactive explorer (pygwalker) is not available in this environment.")
        status_2.update(label='Tableau in Streamlit', state='complete',expanded=True)