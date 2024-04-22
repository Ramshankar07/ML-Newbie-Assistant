import pandas as pd
import os
import streamlit as st
from crewai import Crew
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from tasks import ProjectTasks
from agents import ProjectAgents

load_dotenv()
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
    tasks = ProjectTasks()
    agents = ProjectAgents()
    
    # Create agents
    Problem_Definition_Agent = agents.Problem_Definition_Agent(model=llm)
    Data_Assessment_Agent = agents.Data_Assessment_Agent(model=llm)
    Model_Recommendation_Agent = agents.Model_Recommendation_Agent(model=llm)
    Starter_Code_Generator_Agent = agents.Starter_Code_Generator_Agent(model=llm)
    
    # User input
    user_question = st.text_area("Describe your ML Doubt:")
    st.info("Please select the steps you would like to include in the workflow along with Starting Code:")
    task1 = st.checkbox("Problem Definition")
    task2 = st.checkbox("Data Assessment")
    task3 = st.checkbox("Model Recommendation")
    submit_button = st.button("Submit")
    data_upload = False    
            
# Building the CrewAI workflow
    if submit_button and user_question:
        
        task_define_problem = tasks.task_define_problem(agent=Problem_Definition_Agent, user_question=user_question)
        
        # Choose the appropriate task based on whether data was uploaded
        if data_upload:
            task_assess_data = tasks.task_assess_data_1(agent=Data_Assessment_Agent, df=df, uploaded_file=uploaded_file.name)
        else:
            task_assess_data = tasks.task_access_data_2(agent=Data_Assessment_Agent)
            
        task_recommend_model = tasks.task_recommend_model(agent=Model_Recommendation_Agent)
        
        task_generate_code = tasks.task_generate_code(agent=Starter_Code_Generator_Agent)

        
        crew = Crew(
            agents=[Problem_Definition_Agent, Data_Assessment_Agent, Model_Recommendation_Agent, Starter_Code_Generator_Agent],
            tasks=[task_define_problem, task_assess_data, task_recommend_model,  task_generate_code],
            verbose=2
        )
        
        # Run the CrewAI workflow
        result = crew.kickoff()
        
        # Display the final output
        if task1:
            st.chat_message(name="ai", avatar="🤖").write(task_define_problem.output.result)
        if task2:
            st.chat_message(name="ai", avatar="🤖").write(task_assess_data.output.result)
        if task3:
            st.chat_message(name="ai", avatar="🤖").write(task_recommend_model.output.result)
        st.chat_message(name="ai", avatar="🤖").write(result)
    

if __name__ == '__main__':
    main()


    