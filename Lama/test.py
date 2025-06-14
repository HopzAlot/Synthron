import ollama

client= ollama.Client()

model="llama3.2"
prompt="what is an llm?"

response= client.generate(model=model , prompt= prompt)

print("Response from ollama:\n")
print(response)
