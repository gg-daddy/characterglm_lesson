import streamlit as st
from datetime import datetime
from bot_dialogue import BotRole, Dialogue, DialogueMsg

st.set_page_config(page_title="💬 CharacterGLM Bots Dialogue")

# Replicate Credentials
with st.sidebar:
    st.title('🕹️对话设置')
    
    st.write('🤼‍♀️ 请设定主题')
    topic = st.text_input('主题', key='topic', label_visibility='collapsed',value='宇宙大爆炸')
    
    st.write('🎲 对话轮次')
    turn = st.number_input('轮次', key='turn', label_visibility='collapsed',value=5)
    
    st.write('😎 角色1')
    bot1_name = st.text_input('名称', key='bot1_name',label_visibility='collapsed', value='孙悟空')
    bot1_profile = st.text_area('角色设定', key='bot1_profile',label_visibility='collapsed', value='中国神话故事《西游记》中的主角，是一位勇猛无比的猴王，具有敢于正义、善于战斗的性格。')
    
    st.write('🤖 角色2')
    bot2_name = st.text_input('名称', key='bot2_name', label_visibility='collapsed', value='钢铁侠')
    bot2_profile = st.text_area('角色设定', key='bot2_profile', label_visibility='collapsed', value='钢铁侠是一位有着坚定信念和创造力的超级英雄，他勇敢无畏，致力于保护地球和人类安全，同时具有自信和领导能力。')

def reset_messages():
    st.session_state.messages = []
        
if "messages" not in st.session_state.keys():
    reset_messages()

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.write(message.content)

def append_message(message):
    print(message)
    with st.chat_message(message.role):        
        st.write(message.content)
    
def start_dialogue():
    bot1 = BotRole(bot1_name, bot1_profile)
    bot2 = BotRole(bot2_name, bot2_profile)

    dialogure= Dialogue(bot1, bot2, topic, callback= append_message ,max_turns=turn)
    dialogure.start()
    dialogure.save_dialogue_to_file('dialogue.txt')
    st.session_state.dialogure = str(dialogure)
    
def download_dialogue():
    return st.session_state.get('dialogure', '')

btn_start, btn_clear, btn_save = st.sidebar.columns(3)
btn_start.button('开始对话', on_click=start_dialogue)
btn_clear.button('清空对话', on_click=reset_messages)
btn_save.download_button('保存对话', data=download_dialogue(), file_name=f'dialogue-{datetime.now()}.txt', mime='text/plain')