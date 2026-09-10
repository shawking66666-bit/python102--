import streamlit as st
import os
from openai import OpenAI

st.title("AI智能伴侣")
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)
#初始化消息
if 'messages' not in st.session_state:
    st.session_state.messages = []

#遍历列表中的消息并展示出来
for messages in st.session_state.messages:#数据格式：{"role": "user", "content": "用户消息"}
    st.chat_message(messages["role"]).write(messages["content"])
    #if messages["role"] == "user":
    #    st.chat_message("user").write(messages["content"])
    #else:
    #    st.chat_message("assistant").write(messages["content"])



system_prompt = ("You are a helpful assistant. ")
prompt = st.chat_input("请输入内容")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    #接入大模型api
    client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    #接收大模型返回结果数据
    st.chat_message("assistant").write(response.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)




