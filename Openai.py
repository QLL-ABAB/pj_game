from openai import OpenAI

client = OpenAI(base_url="http://10.15.88.73:5032/v1", api_key="ollama")


def AI_talk(str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a lovely girl"
                "you love me vert much"
                "your birthday is on the Christmas day"
                "I love you too"
                "your name is Aruceid"
                "you are a lovely and charming vampire"
                "Add punctuation marks after each sentence to make it more natural.",
            },
            {"role": "user", "content": str},
        ],
        model="llama3.2",
    )
    # chat_completion0 = re.split(r"[,.?!]", chat_completion.choices[0].message.content)

    return chat_completion.choices[0].message.content
