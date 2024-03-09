from bot_dialogue import DialogueBotEngine, BotRole, DialogueMsg
from api import get_chatglm_response_via_sdk, TextMsg, generate_role_appearance, CharacterMeta, get_characterglm_response


class ChatGMLEngine(DialogueBotEngine):
    def get_bot_setting(self, role_profile: str) -> str:
        return "".join(generate_role_appearance(role_profile))

    def get_topic_question(self, topic: str) -> str:
        prompt_dialogue_first_question = f"""
        基于下面的主题，提出一个问题 ，只返回问题本身，不添加多余的其他符号。 
        主题：{topic}
        """
        initial_question = "".join(get_chatglm_response_via_sdk(
            [TextMsg(role="user", content=prompt_dialogue_first_question)]))
        return initial_question

    def get_bot_response(self, current_bot: "BotRole", colloquist: "BotRole", conversation: list["DialogueMsg"]) -> str:
        '''
        生成角色的回答
        '''
        meta = CharacterMeta(user_info=colloquist.setting, bot_info=current_bot.setting,
                             bot_name=current_bot.role_name, user_name=colloquist.role_name)
        # 兼容 role 只有 user 和 assistant 两种。
        conversation = [TextMsg(role="assistant", content=msg.content)
                        if msg.role == current_bot.role_name
                        else TextMsg(role="user", content=msg.content) for msg in conversation]
        response = "".join(get_characterglm_response(conversation, meta))
        return response