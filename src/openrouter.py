from openai import OpenAI
import json

def generate_content(client, messages, verbose=False):

    system_prompt = """
    You are a storytelling agent, designed to help people learn Chinese.
    """

    response = client.responses.create(
    extra_body={},
    model="qwen/qwen3-14b:free",
    # model = "qwen/qwen3-235b-a22b:free",
    input=messages,
    instructions=system_prompt,
    )

    if verbose:
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        print(f"Input tokens used: {input_tokens}")
        print(f"Output tokens used: {output_tokens}")

    print(json.dumps(response.model_dump(), indent=4))
    print("\n\nPrinting response.output[0]")
    print(response.output[0].content[0].text)
    print("\n\nPrinting response.output[1]")
    print(response.output[1].content[0].text)

    response_text = response.output[1].content[0].text

    messages.append({
        "role": "assistant",
        "content": response_text,
    })

    return response.output[1].content[0].text