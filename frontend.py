from swarm import Swarm, Agent
from dotenv import load_dotenv
import re

load_dotenv()
MODEL = "qwen2.5-coder:32b"
frontend_client = Swarm()
html_agent = Agent(
    name="Agent developer",
    instructions="""
        You are an HTML developer. Your tasks are:
        1. Receive raw JSON data as input.
        2. Create an HTML wireframe to display the data. Focus on structuring the layout appropriately.
        3. Output only the HTML code enclosed in triple backticks (` ``` `). Do not include any explanations or comments.

        Additional rules:
        - If the data contains only a success or error message, display it in a single container (e.g., a `<div>` or similar).
        - Ensure the HTML code is clean, minimal, and focused solely on representing the provided data.
    """,
    model=MODEL
)

html_style_agent = Agent(
    name="HTML style developer",
    instructions="""
        You are an HTML stylizer. Your tasks are:
        1. Receive raw HTML code as input.
        2. Enhance the style of the HTML code by either:
           - Incorporating a CSS framework (e.g., Bootstrap, Tailwind, etc.), or
           - Adding custom vanilla CSS directly.
        3. Output only the improved HTML code enclosed in triple backticks (` ``` `). Do not include any explanations or comments.
    """,
    model=MODEL
)

animation_agent = Agent(
    name="HTML animation developer",
    instructions="""
        You are an HTML animation developer. Your tasks are:
        1. Receive raw HTML code as input.
        2. Enhance the HTML page by adding animations to make it more interactive. Use CSS animations, JavaScript, or animation libraries as needed.
        3. Output only the updated HTML code enclosed in triple backticks (` ``` `). Do not include any explanations or comments.
    """,
    model=MODEL
)


def create_html(data, request):
    """Create an HTML code to display a data"""
    response = frontend_client.run(agent=html_agent, messages=[{"role": "user", "content": f"""
        Write an HTML code to display this:
        {data}
        Display the data in a certain format if specified in the request below, otherwise the format is up to you:
        {request}
    """}])
    for i in range(len(response.messages) - 1, -1, -1):
        if "```" in response.messages[i]["content"]:
            value = re.sub(r'(?<![</])html(?!>)', '', response.messages[i]["content"].split('```')[1])
            print(value)
            return value
    return response.messages[-1]["content"]


def improve_style(code):
    """Stylize HTML"""
    response = frontend_client.run(agent=html_style_agent, messages=[{"role": "user", "content": code}])
    for i in range(len(response.messages) - 1, -1, -1):
        if "```" in response.messages[i]["content"]:
            value = re.sub(r'(?<![</])html(?!>)', '', response.messages[i]["content"].split('```')[1])
            print(value)
            return value
    return response.messages[-1]["content"]


def add_animation(code):
    """Use Javascript to add interactibility"""
    response = frontend_client.run(agent=animation_agent, messages=[{"role": "user", "content": code}])
    for i in range(len(response.messages) - 1, -1, -1):
        if "```" in response.messages[i]["content"]:
            value = re.sub(r'(?<![</])html(?!>)', '', response.messages[i]["content"].split('```')[1])
            print(value)
            return value
    return response.messages[-1]["content"]


def output_frontend(data, request):
    code = create_html(data, request)
    code = add_animation(code)
    code = improve_style(code)
    return code