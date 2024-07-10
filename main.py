import argparse
import json
from TaskGenerator import Generator


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--scenario", type=str, default="Appointment & Reminders")
    argparser.add_argument("--assistant_name", type=str, default="Alexa")
    argparser.add_argument("--n_reply", type=int, default=10)
    args = argparser.parse_args()
    
    scenario = args.scenario
    assistant_name = args.assistant_name
    n_reply = args.n_reply
    
    generator = Generator(config_path_or_env="OAI_CONFIG_LIST_TBI")
    res = generator.generate(scenario, n_reply=n_reply, assistant_name=assistant_name)
    json.dump(res, open(f"{assistant_name.lower()}_{scenario.lower().replace(' ', '_')}_{n_reply}.json", "w"), indent=4)
    