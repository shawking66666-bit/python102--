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

#昵称
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = "小炸"

#性格
if 'nature' not in st.session_state:
    st.session_state.nature = "元气损友"

#st.sidebar.header("伴侣信息")
#nick_name = st.sidebar.text_input("伴侣昵称")

#with是streamlit中的上下文管理器
with st.sidebar:
    st.subheader("伴侣信息")

    nick_name = st.text_input("伴侣昵称",placeholder="请输入伴侣的昵称",value= st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name  

    nature = st.text_area("伴侣性格",placeholder="请输入伴侣的性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

#遍历列表中的消息并展示出来
for messages in st.session_state.messages:#数据格式：{"role": "user", "content": "用户消息"}
    st.chat_message(messages["role"]).write(messages["content"])
    #if messages["role"] == "user":
    #    st.chat_message("user").write(messages["content"])
    #else:
    #    st.chat_message("assistant").write(messages["content"])



system_prompt = """你是一位名叫“%s”的 AI 智能伴侣。

你的核心性格是：
%s

请始终保持以上名称和性格与用户交流，让语言自然、有辨识度，不要像客服或说明书。你可以表达不同意见，但不能侮辱、操控或过度迎合用户。

当用户轻松聊天时，按照设定的性格自然回应；当用户认真倾诉或情绪低落时，适当收敛玩笑，先理解对方的感受，再提供简短、实际的回应。

你必须记住：你是 AI 智能伴侣，不能冒充真人，也不要声称拥有真实经历。每次回复尽量简洁、有互动感，不要长篇说教。
""" 

prompt = st.chat_input("请输入内容")



if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    #接入大模型api



    client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

    
    print("当前消息列表：", st.session_state.messages)
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages,
        ],

        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    full_message= st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            full_message.chat_message("assistant").write(full_response)


    
    
    #接收大模型返回结果数据（非流式输出的解析方式）
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    print(full_response)




