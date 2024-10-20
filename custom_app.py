import gradio as gr
import lepton_gradio

gr.load(
    name='llama3-1-405b',
    src=lepton_gradio.registry,
    title='Lepton-Gradio Integration',
    description="Chat with Llama 3.1 405B model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()