# This file is used to handle the azure ai chatbot
import asyncio
import multiprocessing
from queue import Queue

from flask import Blueprint, request, Response
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from flask_sse import sse
import os
import threading

from langchain.llms import AzureOpenAI
from langchain.schema import HumanMessage, SystemMessage

from app.azureai.handler.stream_handler import QueueCallbackHandler

azure_ai = Blueprint('azure_ai', __name__)
os.environ['OPENAI_API_TYPE'] = "azure"
os.environ['OPENAI_API_BASE'] = 'https://jiawei.openai.azure.com/'
# os.environ['OPENAI_API_VERSION'] = "2022-12-01"
os.environ['OPENAI_API_VERSION'] = "2023-03-15-preview"
os.environ['OPENAI_API_KEY'] = '8f1fdaec3eca44df865368bbbee2761c'

ai = AzureChatOpenAI(
    deployment_name='gpt-35-turbo',
    model_name='gpt-35-turbo',
    streaming=True,
    temperature=0.9,
)


def dochat(input_text, q):
    ai.streaming = True
    ai(
        messages=[
            SystemMessage(content="You're an assistant."),
            HumanMessage(content=input_text),
        ],
        callbacks=[QueueCallbackHandler(q)]
    )


def llm_thread(input_text, q):
    ai(
        messages=[
            SystemMessage(content="You're an assistant."),
            HumanMessage(content=input_text),
        ],
        callbacks=[QueueCallbackHandler(q)]
    )


def stream(input_text, q):
    threading.Thread(target=llm_thread, args=(input_text, q)).start()
    while True:
        message = q.get()
        print(message)
        yield f'data: %s\n\n' % message


@azure_ai.route('/chat', methods=['GET', 'POST'])
def chat():
    q = Queue()
    if request.method == 'POST':
        data = request.get_json()
        input_text = data['message']
        # asyncio.run(dochat(input_text, q))
        return Response(stream(input_text, q), mimetype='text/event-stream')
    else:
        return Response(None, mimetype='text/event-stream')
