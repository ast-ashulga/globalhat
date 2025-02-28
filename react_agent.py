import os
import pickle
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt.chat_agent_executor import create_react_agent, AgentState
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langmem import create_manage_memory_tool, create_search_memory_tool

# Load environment variables from .env file
load_dotenv()

# Ensure API key is set
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"Successfully loaded API key from .env file: {api_key[:5]}...")
else:
    raise ValueError("Please set your OpenAI API key in the .env file.")

# Define a simple calculator tool using LangChain's @tool decorator
@tool("calculator", return_direct=True)  # return_direct=True to return result without additional formatting
def calculator(expression: str) -> str:
    """Evaluate a math expression and return the result as a string."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Create a file-based persistent memory saver
class FilePersistentMemorySaver(MemorySaver):
    def __init__(self, file_path="memory_checkpoints.pkl"):
        super().__init__()
        self.file_path = file_path
        # Load existing data if available
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    self._checkpoints = pickle.load(f)
                print(f"Loaded {len(self._checkpoints)} checkpoints from {file_path}")
            except Exception as e:
                print(f"Error loading checkpoints: {e}")
    
    def put(self, config, checkpoint):
        result = super().put(config, checkpoint)
        # Save to file after each update
        try:
            with open(self.file_path, "wb") as f:
                pickle.dump(self._checkpoints, f)
        except Exception as e:
            print(f"Error saving checkpoints: {e}")
        return result

# Create a file-based checkpointer
checkpointer = FilePersistentMemorySaver()

# Initialize the LLM
llm = ChatOpenAI(model="o3-mini", reasoning_effort='low')

# Create memory tools for storing and searching memories
manage_memory_tool = create_manage_memory_tool(namespace=("memories",))
search_memory_tool = create_search_memory_tool(namespace=("memories",))

# Create the agent with memory tools and the file-based checkpointer
agent_with_memory = create_react_agent(
    llm, 
    tools=[
        calculator, 
        manage_memory_tool, 
        search_memory_tool
    ],
    checkpointer=checkpointer
)

# Example usage
agent_with_memory.invoke({"messages": [
    {"role": "user", "content": "Remember that I prefer dark mode."}
]})

result = agent_with_memory.invoke({"messages": [
    {"role": "user", "content": "What are my lighting preferences?"}
]})
answer = result["messages"][-1].content
print("Agent recalls preference:", answer)

# Uncomment to test the calculator functionality
# user_question = {
#     "messages": [(
#         "user", "What is 12 * 7 minus 5?"
#     )]
# }
# 
# for s in agent_with_memory.stream(user_question, stream_mode="values"):
#     print(s["messages"][-1])
# 
# print(f'Answer: {s["messages"][-1].content}')
