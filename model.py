from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1")

template = (
    "You are tasked with extracting specific information from the following text content: {content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {user_prompt}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def llm_parse(chunks, user_prompt):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    res = []

    for i, chunk in enumerate(chunks, start=0):
        response = chain.invoke({"content": chunk, "user_prompt": user_prompt})
        res.append(response)
    
    return "\n".join(res) 