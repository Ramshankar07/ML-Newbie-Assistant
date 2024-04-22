import pandas as pd
import os
from crewai import Crew
from langchain_groq import ChatGroq
from dotenv import load_dotenv

oad_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def main():
    # Setting the title and description 
    st.title("Machine Learning Newbie Assistant")
    multiline_text = """
    This Machine Learning Assistant is designed to guide users through the process of defining, assessing, and solving machine learning problems. It leverages a team of AI agents, each with a specific role, to clarify the problem, evaluate the data, recommend suitable models, and generate starter Python code. 
    """
    st.markdown(multiline_text, unsafe_allow_html=True)
    
    # Sidebar customization for models
    st.sidebar.title('Customization')
    model = st.sidebar.selectbox(
        'Choose a Model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )
    temprature = st.sidebar.slider('Model Temprature', 0.0, 1.0, 0.0)
    
    # Initialize the ChatGroq model
    llm = ChatGroq(
        api_key=groq_api_key,
        model=model,
        temperature=temprature
    )
    