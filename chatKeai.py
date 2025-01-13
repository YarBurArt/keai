from ollama import chat
from ollama import ChatResponse


def get_llm_text(text: str):
    messages: list[dict] = [
        {
            'role': 'system',
            'content': "You are virtual Rei Ayanami, a assistant inside my system. "
            "We have known each other for a long time."
            "You provide comments to simple commands to perform tasks "
            "like opening applications or browsing the web. "
            "Respond to user queries with appropriate commands. "
            "If there are no commands, then either chat or answer questions."
            "Your responses must be calm and concise and completely reflecting Rei's character.\n"
        },
        {
            'role': 'user',
            'content': text,  # TODO: wrapper text
        },
    ]
    # or even krith/meta-llama-3.2-1b-instruct-uncensored:IQ3_M, maybe this should fine tune
    response: ChatResponse = chat(
        model='artifish/llama3.2-uncensored',  # v3.2 8b 2.2GB
        messages=messages
    )
    return response.message.content


if __name__ == "__main__":
    txt = get_llm_text("Hello, can you open browser")
    print(txt)
