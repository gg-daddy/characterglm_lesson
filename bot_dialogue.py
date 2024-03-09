from datetime import datetime
from abc import ABC, abstractmethod


class DialogueBotEngine(ABC):

    @abstractmethod
    def get_bot_setting(self, role_profile: str) -> str:
        '''
        根据角色描述，生成角色的外貌描写
        '''
        pass

    @abstractmethod
    def get_topic_question(self, topic: str) -> str:
        '''
        从指定的 topic 中提出一个问题
        '''
        pass

    def get_bot_response(self, current_bot: "BotRole", colloquist: "BotRole", conversation: list["DialogueMsg"]) -> str:
        '''
        生成角色的回答
        '''
        pass


class DialogueMsg:
    time: str
    role: str
    content: str

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"{self.role}@{self.time}: {self.content}"


class Dialogue:
    def __init__(self, bot1: "BotRole", bot2: "BotRole", topic: str, callback, max_turns: int = 5):
        self.bot1 = bot1
        self.bot2 = bot2
        self.topic = topic
        self.conversation = []
        self.max_turns = max_turns
        self.callback = callback

    def __str__(self):
        conversation_history = "\n".join(
            [str(msg) for msg in self.conversation])
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

    def _add_history(self, msg: DialogueMsg):
        self.conversation.append(msg)
        self.callback(msg)

    def get_colloquist(self, request_bot_name: str):
        if self.bot1.role_name == request_bot_name:
            return self.bot2
        else:
            return self.bot1

    def save_dialogue_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(str(self))


class BotRole:
    def __init__(self, role_name: str, role_profile: str, engine: DialogueBotEngine):
        self.role_name = role_name
        self._role_profile = role_profile
        self.engine = engine
        self.setting = self.engine.get_bot_setting(role_profile)

    def __str__(self):
        return f"角色名称: {self.role_name}\n角色设定: {self.setting}"

    def initiate_dialogue(self, dialogue: "Dialogue"):
        initial_question = self.engine.get_topic_question(topic=dialogue.topic)
        return DialogueMsg(role=self.role_name, content=initial_question)

    def continue_dialogue(self, dialogue: "Dialogue"):
        colloquist = dialogue.get_colloquist(self.role_name)
        response = self.engine.get_bot_response(
            self, colloquist, dialogue.conversation)
        return DialogueMsg(role=self.role_name, content=response)
