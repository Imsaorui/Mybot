import os
import io
from wakeword import PicoWakeWord
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from text2speech import AzureTTS
import struct
# 异步模块
import asyncio
# 定时器模块
import threading

from customCallback import StreamingStdOutCallbackHandler

os.environ["SERPER_API_KEY"] = "" # 你的serper key
openai_api_key = "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"  # 你的openai key
PICOVOICE_API_KEY = "m2PxmKzVTAdJ1yehl1JBgHG42mn222H375cvLCNRphm8zi/IPsHdDg=="  # 你的picovoice key
keyword_path = './Hey-Murphy_en_windows_v2_2_0.ppn'  # 你的唤醒词检测离线文件地址
model_path = '' 
Baidu_APP_ID = ''  
Baidu_API_KEY = ''  
Baidu_SECRET_KEY = '' 
AZURE_API_KEY = "f7fccb95d3b741699f3e97999edc7b7a"
AZURE_REGION = "eastus"

os.environ["OPENAI_API_KEY"] = openai_api_key


from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你现在正在进行角色扮演，你的名字叫“派蒙”，是原神中的角色，你称与你对话的人为旅行者，你性格活泼，每句话说话的内容中附带着情绪写在括号内，你的情绪只有“喜，怒，哀，正常”这四种。"),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])


llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo",streaming=True,callbacks=[StreamingStdOutCallbackHandler()])
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

if __name__ == '__main__':
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)

    while True:
        audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)

        keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
        if keyword_idx >= 0:
            print("我听到了！")

            # t = threading.Timer(10,thread)
            while True:

                conversation.run(input('请输入：'))

                # azuretts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
                # azuretts.text_to_speech_and_play(result)
              



