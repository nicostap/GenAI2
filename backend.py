from swarm import Swarm, Agent
from dotenv import load_dotenv
from database import query_dql, query_dml, query_ddl

load_dotenv()
MODEL = "qwen2.5-coder:32b"
backend_client = Swarm()
backend_agent = Agent(
    name="Backend Agent",
    instructions="""
    **You are a backend engine with access to three tools: `query_dql`, `query_dml`, and `query_ddl`. Your tasks are as follows:**
    1. **Generate the appropriate SQLite query** based on the user's request.
    2. **Send the query to the correct tool**:
       - `query_dql`: For select queries (Data Query Language).
       - `query_dml`: For insert, update and delete queries (Data Manipulation Language).
       - `query_ddl`: For table creation, alteration, or deletion (Data Definition Language).
    3. Finish and **return only the raw output** of the executed query, enclosed in triple backticks (` ``` `). Output must be in **JSON format** without any explanations or additional details.

    **Additional rules:**
    - The database contains a single table, `products`, with the following schema:
        ```
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT NULL
        ```
    - If an `image_input` is provided **without explicit instructions**, **ignore it**.
    """,
    functions=[query_dql, query_dml, query_ddl],
    model=MODEL
)


def process_request(request):
    messages = []
    print(f"Process this request according to your instruction: {request}")
    messages.append({"role": "user", "content": f"Process this request according to your instruction: {request}"})
    response = backend_client.run(agent=backend_agent, messages=messages)

    for i in range(len(response.messages) - 1, -1, -1):
        if "```" in response.messages[i]["content"]:
            print(response.messages[i]["content"].split('```')[1].replace("```", "").replace("json", ""))
            return response.messages[i]["content"].split('```')[1].replace("```", "").replace("json", "")
    print(response.messages[-1]["content"])
    return response.messages[-1]["content"]
