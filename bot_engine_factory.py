from bot_dialogue import DialogueBotEngine, BotRole, Dialogue
from bot_glm_engine_adapter import ChatGMLEngine

BOT_ENGINE = {
    "chatglm": ChatGMLEngine()
}


def get_bot_engine(engine_name: str) -> DialogueBotEngine:
    engine = BOT_ENGINE.get(engine_name)
    if not engine:
        raise ValueError(f"不支持的引擎名称: {engine_name}")
    return engine
