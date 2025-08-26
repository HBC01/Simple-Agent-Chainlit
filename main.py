import os
from agents import Agent,OpenAIChatCompletionsModel,AsyncOpenAI,Runner,RunConfig
import chainlit as cl
from dotenv import load_dotenv
load_dotenv()
Gemini_Key=os.getenv("Gemini_Api_Key")
if not Gemini_Key:
    raise ValueError("Gemini key not found in .env")
extra_client=AsyncOpenAI(api_key=Gemini_Key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
gemini_model =OpenAIChatCompletionsModel(openai_client=extra_client,model="gemini-2.0-flash")
simple_agent=Agent(name="Simple Agent",instructions="you are a Helpful Agent to user,also answer the user quiries")
my_config=RunConfig(model=gemini_model,model_provider=extra_client,tracing_disabled=True)
@cl.on_chat_start
async def start():
    
    await  cl.Message(content="**Simple Agent** 👋🥀👋 \n I am Glad to help you in your queries? \n Ask anything?").send()

@cl.on_message
async def main(msg :cl.Message):
    result =Runner.run_sync(simple_agent,msg.content,run_config=my_config)
    await cl.Message(result.final_output).send()

if __name__ == "__main__":
    main()
