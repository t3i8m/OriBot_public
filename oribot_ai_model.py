import openai

def generated_answer(message):
    if ("oribot" in [n.lower() for n in message.split()]) or "орибот" in [n.lower() for n in message.split()]:
        return "OriBot is cool!"
    else:
        openai.api_key = "PASSWORD"
        # openai.api_key = "PASSWORD"
        try:
            model_engine = "gpt-3.5-turbo"
            prompt = [{"role":"user",
                   "content":message}]

            completion = openai.ChatCompletion.create(
                model=model_engine,
                messages = prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.9
            )
            # print(completion.choices[0].message.content)
            response = completion.choices[0].message.content
            print("chat-gpt-3.5")
            return response
        except Exception as ex:
            print("text-davinci-003")

            model_engine = "text-davinci-003"
            prompt = message

            completion = openai.Completion.create(
                engine=model_engine,
                prompt = prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.9
            )
            response = completion.choices[0].text
            return response
