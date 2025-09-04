import streamlit as st
from openai import OpenAI, AuthenticationError

# ---- Page for Lab 1 ----
def lab1():
    st.title("📄 Document question answering (Lab 1)")
    st.write(
        "Upload a document below and ask a question about it – GPT will answer! "
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    )

    openai_api_key = st.text_input("OpenAI API Key", type="password")

    client = None
    if openai_api_key:
        try:
            client = OpenAI(api_key=openai_api_key)
            client.models.list()
            st.success("✅ API key is valid!")
        except AuthenticationError:
            st.error("❌ Invalid API key. Please check and try again.")
            client = None
        except Exception as e:
            st.error(f"⚠️ Error while validating key: {e}")
            client = None
    else:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")

    if client:
        model = st.selectbox(
            "Choose a model",
            ["gpt-4.1", "gpt-5-chat-latest", "gpt-5-nano"],
            index=0,
        )

        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        question = st.text_area(
            "Now ask a question about the document!",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file,
        )

        if uploaded_file and question:
            document = uploaded_file.read().decode()
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document} \n\n---\n\n {question}",
                }
            ]

            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )

            st.write_stream(stream)


# ---- Page for Lab 2 ----
def lab2():
    st.title("📄 Document question answering (Lab 2)")
    st.write("This is Lab 2 page. The functionality could be different from Lab 1.")


# ---- Main navigation ----
st.set_page_config(page_title="Multi-Page Lab App")

page = st.navigation([
    st.Page(lab2, title="Lab 2"),  # 👉 ставим первой, теперь Lab 2 открывается по умолчанию
    st.Page(lab1, title="Lab 1"),
])
page.run()
