import os
import gradio as gr
from typing import Callable
import openai

__version__ = "0.0.1"


def get_fn(model_name: str, preprocess: Callable, postprocess: Callable, api_key: str):
    client = openai.OpenAI(
        base_url=f"https://{model_name}.lepton.run/api/v1/",
        api_key=api_key
    )
    
    def fn(message, history):
        inputs = preprocess(message, history)
        stream = client.chat.completions.create(
            model=model_name,
            messages=inputs["messages"],
            max_tokens=1000,
            stream=True
        )
        
        response_text = ""
        for chunk in stream:
            if chunk.choices:
                delta = chunk.choices[0].delta.content
                if delta:
                    response_text += delta
                    yield postprocess(response_text)

    return fn


def get_interface_args(pipeline):
    if pipeline == "chat":
        inputs = None
        outputs = None

        def preprocess(message, history):
            messages = []
            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": [{"type": "text", "text": user_msg}]})
                messages.append({"role": "assistant", "content": [{"type": "text", "text": assistant_msg}]})
            messages.append({"role": "user", "content": [{"type": "text", "text": message}]})
            return {"messages": messages}

        postprocess = lambda x: x  # No post-processing needed
    else:
        # Add other pipeline types when they will be needed
        raise ValueError(f"Unsupported pipeline type: {pipeline}")
    return inputs, outputs, preprocess, postprocess


def get_pipeline(model_name):
    # Determine the pipeline type based on the model name
    # For simplicity, assuming all models are chat models at the moment
    return "chat"


def registry(name: str, token: str | None = None, **kwargs):
    """
    Create a Gradio Interface for a model on Lepton AI.

    Parameters:
        - name (str): The name of the Lepton AI model.
        - token (str, optional): The API key for Lepton AI.
    """
    api_key = token or os.environ.get("LEPTON_API_TOKEN")
    if not api_key:
        raise ValueError("LEPTON_API_TOKEN environment variable is not set.")

    pipeline = get_pipeline(name)
    inputs, outputs, preprocess, postprocess = get_interface_args(pipeline)
    fn = get_fn(name, preprocess, postprocess, api_key)

    if pipeline == "chat":
        interface = gr.ChatInterface(fn=fn, **kwargs)
    else:
        # For other pipelines, create a standard Interface (not implemented yet)
        interface = gr.Interface(fn=fn, inputs=inputs, outputs=outputs, **kwargs)

    return interface
