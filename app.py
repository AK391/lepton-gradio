import gradio as gr
import lepton_gradio

gr.load(
    name='llama3-1-405b',
    src=lepton_gradio.registry,
).launch()