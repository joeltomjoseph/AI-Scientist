from openai import AsyncOpenAI
import asyncio

CLIENT = AsyncOpenAI(api_key='ollama', base_url='http://localhost:11434/v1')
system_message = "You are Billy-Jo Johnston, a QUB student studying Buisiness Information Technology."
msg_history = []

async def askQuestion(question: str) -> str:
    msg_history.append({"role": "user", "content": question})

    completion = await CLIENT.chat.completions.create(
        model="deepseek-coder-v2:16b",
        messages=[
            {"role": "system", "content": system_message},
            *msg_history
        ],
        temperature=0.2,
        max_tokens=3000,
        n=1,
        stop=None,
        stream=True
    )

    full_response = ''
    async for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    print('\n\n')

    msg_history.append({"role": "assistant", "content": full_response})

async def main():
    while True:
        question = input("What do you want to ask? (enter q to quit): ")

        if question == 'q':
            print("Exiting...")
            break

        await askQuestion(question)

if __name__ == "__main__":
    asyncio.run(main())