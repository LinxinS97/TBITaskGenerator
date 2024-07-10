import autogen
import json
from typing import Dict, List
from tqdm import tqdm


class Generator:

    TRANSLATOR_SYS_MSG = """# Your Role
You are a AI assistant ({assistant_name}) command translator. You can translate human's thinking into {assistant_name} command.

# Your task
Reply with the thinking and the corresponding translated command.

## Answer format
Your answer should be in JSON format. For example:
{{
    "thinking": "I want to set a reminder for myself to do something later.",
    "command": "{assistant_name}, set a reminder for (time)"
}}
"""


    OPERATION_GENERATOR = """# Your task
Given a scenario, reply with {n} diverse, distinguishable operations to the AI assistant ({assistant_name}). The operations should related to people's daily life.

# Scenario
{scenario}

# Your Answer
Your answer should be only operations without specific commands.

## Answer format
["operation_1", "operation_2", ...]
"""
    
    def __init__(
            self,
            model_list: List[str] = ["gpt-4-turbo", "gpt-4o"], 
            config_path_or_env: str = "OAI_CONFIG_LIST_TBI",
            llm_config = None,
    ) -> None:
        self.model_list = model_list.copy()
        config_list = autogen.config_list_from_json(config_path_or_env, filter_dict={ "model": model_list })
        if llm_config is None:
            self.llm_config = {
                "temperature": 0,
                "config_list": config_list.copy(),
            }
        else:
            self.llm_config = llm_config.copy()
        
        self.llm_config.update({"cache_seed": None})  # remove cache seed to prevent auto record.
    
    def generate(self, scenario: str, interactive: bool = False, assistant_name: str = "Alexa", n_reply: int = 1):
        res = []
        operations = json.loads(autogen.AssistantAgent(
            name="Operation_generator",
            system_message="",
            llm_config=self.llm_config
        ).generate_oai_reply([{
            "role": "user",
            "content": self.OPERATION_GENERATOR.format(assistant_name=assistant_name, scenario=scenario, n=n_reply)
        }])[1])
        print("Generated operations: ", operations)
        
        
        for ope in tqdm(operations, desc="Generating thinking and command"):
            translator = autogen.AssistantAgent(
                name="Translator",
                system_message=self.TRANSLATOR_SYS_MSG.format(assistant_name=assistant_name),
                llm_config=self.llm_config
            )
            
            res.append(json.loads(translator.generate_oai_reply([{
                "content": f"I want to {ope.lower()}",
                "role": "user"
            }])[1]))
        
        return res

if __name__ == "__main__":
    generator = Generator()
    res = generator.generate("Appointment & Reminders", n_reply=3)
    a = 1
