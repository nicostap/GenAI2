import streamlit as st
import base64
from backend import process_request
from io import BytesIO
from PIL import Image
from frontend import output_frontend
from database import run_migrations
from ollama import generate

st.set_page_config(
    page_title="QueryBot",
)
st.title("QueryBot")

if "db_status" not in st.session_state:
    print("Setting up SQLite database...")
    run_migrations()
    print("Setting up finished")
    st.session_state.db_status = "ready"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! What can I help you do today?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?", accept_file=True, file_type=["png", "jpg"]):
    with st.chat_message("user"):
        st.markdown(prompt.text)

    st.session_state.messages.append({"role": "user", "content": prompt.text})

    with st.chat_message("assistant"):
        image_input = ''
        if len(prompt.files) > 0:
            image = Image.open(prompt.files[0])
            image_bytes = BytesIO()
            image.save(image_bytes, format=image.format)
            image_bytes.seek(0)
            for response in generate(model='llava:13b-v1.6',
                                     prompt="""
                                     Describe the content of this image in detail.
                                     Include information about objects, colors, and any visible text or patterns.
                                     """,
                                     images=[image_bytes],
                                     stream=True):
                image_input += response['response']
        with st.spinner("Running query..."):
            text_input = f"""
                # image_input:
                { 'No image input' if len(image_input) == 0 else image_input  }

                # Request:
                {prompt.text}
            """
            data = process_request(text_input)
        with st.spinner("Building HTML..."):
            raw_html = output_frontend(data, prompt.text)
            raw_html = raw_html.replace("```html", "").replace("```", "")
            html_bytes = BytesIO(raw_html.encode())
            base64_html = base64.b64encode(html_bytes.getvalue()).decode()
            iframe_html = f'<iframe src="data:text/html;base64,{base64_html}" width="100%" height="300"></iframe>'
        st.session_state.messages.append({"role": "assistant", "content": iframe_html})
        st.rerun()