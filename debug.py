# pylint: disable-all
#
# This file serves as a convenient debug entry point.
# Do whatever you want with it.
#
# from openssm import LlamaIndexSSM
from openssm import GPT4LlamaIndexSSM
# from openssm import LeptonSLM, LeptonSSM
# from openssm import logger, mlogger

# Configure logging for some informative output
# mlogger.setLevel(logger.DEBUG)
# logger.setLevel(logger.DEBUG)

"""
ssm = LlamaIndexSSM(storage_dir="/Users/ctn/Downloads/802.11standardsAllMxL/test")
ssm.read_directory()
print(ssm.discuss("What are the standards being discussed?"))
"""

# ssm = LlamaIndexSSM(storage_dir="./examples/integrations/.openssm/phu")
ssm = GPT4LlamaIndexSSM(storage_dir="./examples/integrations/.openssm/phu")
ssm.read_directory(re_index=True)
print(ssm.discuss("Who is Phu Hoang?"))


"""
ssm = LlamaIndexSSM(storage_dir="./examples/integrations/.openssm/ylecun")
ssm.read_directory(re_index=True)
print(ssm.discuss("Who is Yann LeCun?"))
print(ssm.discuss("Who is Christopher Nguyen?"))
print(ssm.discuss("What is OpenSSM?"))
"""

# ssm = LeptonSSM()
# ssm = LlamaIndexSSM(name="eos", slm=LeptonSLM(), storage_dir="./examples/integrations/.openssm/eos")
# ssm = LlamaIndexSSM(name="ylecun", storage_dir="./examples/integrations/.openssm/ylecun")

# ssm.read_directory(use_existing_index=True)
# ssm.save()
# ssm = LlamaIndexSSM()
# ssm.discuss("What is the E290? How is it different from the E490?")
# print(ssm.discuss("Who is Yann LeCun?"))

"""
ssm = LlamaIndexSSM(name="avv", storage_dir="./examples/integrations/.openssm/avv")
ssm.read_website([
    "https://www.avv.co/",
    "https://www.avv.co/porfolio/",
    "https://www.avv.co/team/",
    "https://www.avv.co/about-us/",
    "https://www.avv.co/careers/"
],
    re_index=True)
# ssm.save()
print(ssm.discuss("What is AVV?"))
"""

# from tests.core.ssm.test_base_ssm import TestBaseSSM
# from tests.integrations.test_openai import TestGPT3CompletionSLM
# from tests.integrations.test_lepton_ai import TestSSM, TestRAGSSM
# test.test_constructor_default_values()
# test.test_call_lm_api()
# test.test_constructor_default_values()

# from tests.core.ssm.test_base_ssm import TestBaseSSM
# test = TestBaseSSM()
# test.setUp()
# test.test_conversation_history()

# from tests.integrations.test_openai import TestGPT4ChatCompletionSLM
# test = TestGPT4ChatCompletionSLM()
# test.test_constructor_default_values()
# test.test_call_lm_api()

# from openssm import GPT4ChatCompletionSSM
# ssm = GPT4ChatCompletionSSM()
# print(ssm.discuss("I am CTN. I am a robot."))
# print(ssm.discuss("What is my name? What am I?"))
