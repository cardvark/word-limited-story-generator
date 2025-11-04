from openai import OpenAI

def generate_content(client, message, verbose):

    response = client.responses.create(
    extra_body={},
    model="qwen/qwen3-14b:free",
    input=[
                {
                    "role": "user",
                    "content": message,
                }
                ]
    )

    if verbose:
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        print(f"Input tokens used: {input_tokens}")
        print(f"Output tokens used: {output_tokens}")

    print(response.output[0].content[0].text)

    # print(response.output.content[0].text)


