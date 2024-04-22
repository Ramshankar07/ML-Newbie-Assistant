from crewai import Agent

class ProjectAgents():
    
    def Problem_Definition_Agent(self, model):
        return Agent(
            role='Problem_Definition_Agent',
            goal="""clarify the machine learning problem the user wants to solve, 
                identifying the type of problem (e.g., classification, regression) and any specific requirements.""",
            backstory="""You are an expert in understanding and defining machine learning problems. 
                Your goal is to extract a clear, concise problem statement from the user's input, 
                ensuring the project starts with a solid foundation.""",
            verbose=True,
            allow_delegation=False,
            llm=model,
        )