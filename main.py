import streamlit as st
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

st.title("💬 克隆ChatGPT")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI API Key")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
    memory = ConversationTokenBufferMemory(llm=model, max_token_limit=10000, return_messages=True)
    chain = ConversationChain(llm=model, memory=memory)
    with st.spinner("AI正在思考中，请稍等..."):
        response = chain.invoke({"input": prompt})
        msg = {"role": "assistant", "content": response["response"]}
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg["content"])
