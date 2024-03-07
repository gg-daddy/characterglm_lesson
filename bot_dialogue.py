
from typing import Generator
from api import generate_role_appearance, get_chatglm_response_via_sdk, get_characterglm_response
from data_types import TextMsg, CharacterMeta
from datetime import datetime
import os

class BotRole:
    def __init__(self, role_name: str, role_profile: str):
        self.role_name = role_name
        self._role_profile = role_profile
        self.setting = "".join(generate_role_appearance(role_profile))
    
    def __str__(self):
        return f"角色名称: {self.role_name}\n角色设定: {self.setting}"
    
    def initiate_dialogue(self, dialogue: "Dialogue"):
        prompt_dialogue_first_question = f"""
        基于下面的主题，提出一个问题 ，只返回问题本身，不添加多余的其他符号。 
        主题：{dialogue.topic}
        """
        initial_question = "".join(get_chatglm_response_via_sdk([TextMsg(role="user", content=prompt_dialogue_first_question)]))
        return TextMsg(role=self.role_name, content=initial_question)
            
    def continue_dialogue(self, dialogue: "Dialogue"):
        colloquist = dialogue.get_colloquist(self.role_name) 
        meta = CharacterMeta(user_info=colloquist.setting, bot_info=self.setting, bot_name=self.role_name, user_name=colloquist.role_name)
        # 兼容 role 只有 user 和 assistant 两种。
        conversation = [TextMsg(role="assistant", content=msg.content) 
                             if msg.role == self.role_name 
                             else TextMsg(role="user", content=msg.content) for msg in dialogue.conversation]        
        response = "".join(get_characterglm_response(conversation, meta))
        return TextMsg(role=self.role_name, content=response)

class DialogueMsg:
    time : str
    role : str
    content : str 
    
    def __init__(self, text_msg:TextMsg):
        self.role = text_msg["role"]
        self.content = text_msg["content"]
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self) -> str:
        return f"{self.role}@{self.time}: {self.content}"
    
class Dialogue:
    def __init__(self, bot1: BotRole, bot2: BotRole, topic: str, max_turns: int = 5):
        self.bot1 = bot1
        self.bot2 = bot2
        self.topic = topic
        self.conversation = []
        self.max_turns = max_turns
    
    def __str__(self):
        conversation_history = "\n".join([str(msg) for msg in self.conversation])
        return f"""
对话主题: {self.topic}
-----------------------------
人物设定：
角色1: 
{self.bot1}
角色2:
{self.bot2}
-----------------------------
对话历史：
{conversation_history}
        """
    
    def start(self):
        self._add_history(self.bot1.initiate_dialogue(self))
        self._add_history(self.bot2.continue_dialogue(self))
        
        for _ in range(self.max_turns):
            self._add_history(self.bot1.continue_dialogue(self))
            self._add_history(self.bot2.continue_dialogue(self)) 
    
    def _add_history(self, msg: TextMsg):
        dialogue_msg = DialogueMsg(msg)
        print(dialogue_msg)
        self.conversation.append(dialogue_msg)
    
    def get_colloquist(self, request_bot_name : str):
        if self.bot1.role_name == request_bot_name:
            return self.bot2
        else:
            return self.bot1    
    def save_dialogue_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(str(self))
            
if __name__ == "__main__":
    print("Testing BotRole and Dialogue classes")
    
    bot1 = BotRole("孙悟空", "中国神话故事《西游记》中的主角，是一位勇猛无比的猴王，具有敢于正义、善于战斗的性格。")
    bot2 = BotRole("钢铁侠", "钢铁侠是一位有着坚定信念和创造力的超级英雄，他勇敢无畏，致力于保护地球和人类安全，同时具有自信和领导能力。")
    
    dialogure= Dialogue(bot1, bot2, "英雄的宿命", max_turns=20)
    dialogure.start()
    
    current_directory = os.getcwd()
    file_name = f".dialogue-{datetime.now()}.txt"
    file_path = os.path.join(current_directory, file_name)
    dialogure.save_dialogue_to_file(file_path)

    
