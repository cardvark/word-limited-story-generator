from openai import OpenAI

def generate_content(client, message, verbose):

    system_prompt = """
    You are a storytelling agent, designed to help people learn Chinese.
    """

    response = client.responses.create(
    extra_body={},
    model="qwen/qwen3-14b:free",
    # reasoning = {
    #     "effort": "low"
    # },

    input=[
                {
                    "role": "user",
                    "content": message,
                }
    ],
    instructions=system_prompt,
    )

    if verbose:
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        print(f"Input tokens used: {input_tokens}")
        print(f"Output tokens used: {output_tokens}")

    print("\n\nPrinting response.output[0]")
    print(response.output[0].content[0].text)
    print("\n\nPrinting response.output[1]")
    print(response.output[1].content[0].text)