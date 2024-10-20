# `lepton-gradio`

is a Python package that makes it very easy for developers to create machine learning apps that are powered by Lepton AI's API.

# Installation

1. Clone this repo: `git clone https://github.com/leptonai/lepton-gradio.git`
2. Navigate into the folder that you cloned this repo into: `cd lepton-gradio`
3. Install this package: `pip install -e .`

<!-- ```bash
pip install lepton-gradio
``` -->

That's it! 

# Basic Usage

Just like if you were to use the `leptonai` API, you should first save your Lepton AI API key to this environment variable:

```
export LEPTON_API_TOKEN=<your token>
```

Then in a Python file, write:

```python
import gradio as gr
import lepton_gradio

gr.load(
    name='lepton-chat-model',
    src=lepton_gradio.registry,
).launch()
```

Run the Python file, and you should see a Gradio Interface connected to the model on Lepton AI!

![ChatInterface](chatinterface.png)

# Customization 

Once you can create a Gradio UI from a Lepton AI endpoint, you can customize it by setting your own input and output components, or any other arguments to `gr.Interface`. For example:

```py
import gradio as gr
import lepton_gradio

gr.load(
    name='lepton-chat-model',
    src=lepton_gradio.registry,
    title='Lepton AI-Gradio Integration',
    description="Chat with Lepton AI's chat model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()
```

![CustomizedInterface](custom_chat_lepton.png)

# Composition

Or use your loaded Interface within larger Gradio Web UIs, e.g.

```python
import gradio as gr
import lepton_gradio

with gr.Blocks() as demo:
    with gr.Tab("Lepton Chat Model"):
        gr.load('lepton-chat-model', src=lepton_gradio.registry)
    with gr.Tab("Lepton Other Model"):
        gr.load('lepton-other-model', src=lepton_gradio.registry)

demo.launch()
```

# Under the Hood

The `lepton-gradio` Python library has two dependencies: `leptonai` and `gradio`. It defines a "registry" function `lepton_gradio.registry`, which takes in a model name and returns a Gradio app.

# Supported Models in Lepton AI

All chat API models supported by Lepton AI are compatible with this integration. For a comprehensive list of available models and their specifications, please refer to the Lepton AI documentation.

-------

Note: if you are getting an authentication error, then the Lepton AI API Client is not able to get the API token from the environment variable. This happened to me as well, in which case save it in your Python session, like this:

```py
import os

os.environ["LEPTON_API_TOKEN"] = ...
```
