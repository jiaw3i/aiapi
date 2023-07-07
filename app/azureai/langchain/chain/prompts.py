from langchain import PromptTemplate

message_prompt = PromptTemplate(
    template="{message}",
    input_variables=["message"],
)
