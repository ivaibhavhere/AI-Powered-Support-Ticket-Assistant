import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "sqlite:///tickets.db"

def get_llm():
    if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model="models/gemma-4-31b-it", temperature=0)
    else:
        raise ValueError("No valid API key found. Please set GEMINI_API_KEY or GOOGLE_API_KEY in .env")

def get_sql_agent():
    """
    Creates and returns a LangChain SQL agent connected to the tickets DB.
    """
    db = SQLDatabase.from_uri(DB_PATH)
    llm = get_llm()
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm, use_query_checker=False)
    
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor

def query_agent(question: str) -> str:
    """
    Passes a natural language query to the SQL agent and returns the response.
    """
    try:
        agent = get_sql_agent()
        # Ensure the agent focuses on the support_tickets schema
        prompt = f"""
        You are a helpful AI assistant for a customer support team. 
        You have access to a SQLite database containing support tickets.
        The table is called 'tickets'.
        
        Answer the following question based on the data:
        {question}
        """
        response = agent.invoke({"input": prompt})
        return response.get("output", "Sorry, I couldn't find an answer to that.")
    except Exception as e:
        return f"Error executing query: {str(e)}"

if __name__ == "__main__":
    # For testing
    print(query_agent("How many tickets are currently open?"))
