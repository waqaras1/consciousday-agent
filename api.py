import openai

client = openai.OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="mistralai/mixtral-8x7b-instruct",
    messages=[{"role": "user", "content": "Hello from OpenRouter and Mixtral 8x7B Instruct!"}]
)
print(response.choices[0].message.content)