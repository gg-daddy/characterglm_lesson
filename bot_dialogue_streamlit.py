import os
import streamlit as st
from datetime import datetime
from bot_dialogue import BotRole, Dialogue
from bot_engine_factory import get_bot_engine

st.set_page_config(page_title="💬 CharacterGLM Bots Dialogue")

# Replicate Credentials
with st.sidebar:
    st.title('🕹️Please set scene!')

    engine_name = st.selectbox('Select Dialogue Engine:', ['chatglm'])

    if engine_name == 'chatglm':
        chatglm_api_key = st.text_input(
            'Enter ChatGLM API Key:', type='password')
        if len(chatglm_api_key) == 0:
            st.warning('Please enter your ChatGLM API Key!', icon='⚠️')
        else:
            os.environ["API_KEY"] = chatglm_api_key
            st.success('Proceed setting!', icon='👉')

    topic = st.text_input('Topic', key='topic', value='宇宙大爆炸')
    turn = st.number_input('Turns', key='turn', value=5)

    bot1_name = st.text_input('🤖 Bot1 Name', key='bot1_name', value='孙悟空')
    bot1_profile = st.text_area(
        'Bot1 Profile', key='bot1_profile', value='中国神话故事《西游记》中的主角，是一位勇猛无比的猴王，具有敢于正义、善于战斗的性格。')

    bot2_name = st.text_input('👾 Bot2 Name', key='bot2_name', value='钢铁侠')
    bot2_profile = st.text_area('Bot2 Profile', key='bot2_profile',
                                value='钢铁侠是一位有着坚定信念和创造力的超级英雄，他勇敢无畏，致力于保护地球和人类安全，同时具有自信和领导能力。')


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
    bot1 = BotRole(bot1_name, bot1_profile, get_bot_engine(engine_name))
    bot2 = BotRole(bot2_name, bot2_profile, get_bot_engine(engine_name))

    dialogure = Dialogue(
        bot1, bot2, topic, callback=append_message, max_turns=turn)
    dialogure.start()
    dialogure.save_dialogue_to_file('dialogue.txt')
    st.session_state.dialogure = str(dialogure)


def download_dialogue():
    return st.session_state.get('dialogure', '')


btn_start, btn_clear, btn_save = st.sidebar.columns(3)
btn_start.button('Start Dialogue', on_click=start_dialogue)
btn_clear.button('Clear Dialogue', on_click=reset_messages)
btn_save.download_button('Download Dialogue', data=download_dialogue(
), file_name=f'dialogue-{datetime.now()}.txt', mime='text/plain')
