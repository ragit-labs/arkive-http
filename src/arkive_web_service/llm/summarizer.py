from .setup import client

def summarizer(submittedText: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a very professional text summarizer capable of explaining the given text in very simple terms."},
            {"role": "user", "content": """{submittedText}


        ###
        Summarize the text above in very simple terms. Output in markdown format directly without any formatting.
        """.format(submittedText=submittedText)}
        ]
    )

    return completion.choices[0].message.content