from datetime import datetime
import os
from dotenv import load_dotenv
from bot_engine_factory import get_bot_engine
from bot_dialogue import Dialogue, BotRole

load_dotenv()


if __name__ == "__main__":
    print("Testing BotRole and Dialogue classes")

    bot1 = BotRole(
        "孙悟空", "中国神话故事《西游记》中的主角，是一位勇猛无比的猴王，具有敢于正义、善于战斗的性格。", get_bot_engine("chatglm"))
    bot2 = BotRole(
        "钢铁侠", "钢铁侠是一位有着坚定信念和创造力的超级英雄，他勇敢无畏，致力于保护地球和人类安全，同时具有自信和领导能力。", get_bot_engine("chatglm"))

    dialogure = Dialogue(bot1, bot2, "英雄的宿命",
                         callback=lambda msg: print(msg), max_turns=20)
    dialogure.start()
    current_directory = os.getcwd()
    file_name = f".dialogue-{datetime.now()}.txt"
    file_path = os.path.join(current_directory, file_name)
    dialogure.save_dialogue_to_file(file_path)
