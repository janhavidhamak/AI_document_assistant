import gradio as gr

def create_ui(process_fn, answer_fn):
    """
    Builds and returns the Gradio UI.
    """
    with gr.Blocks(title="AI Document Assistant") as demo:
        gr.Markdown("<h1 style='text-align: center;'>AI Document Assistant</h1>")
        
        with gr.Row():
            with gr.Column():
                pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"], type="filepath")
                status_output = gr.Textbox(label="Status", interactive=False)
            
            with gr.Column():
                question_input = gr.Textbox(label="Ask a Question")
                ask_btn = gr.Button("Get Answer", variant="primary")
                answer_output = gr.Textbox(label="Answer", interactive=False, lines=5)
                page_output = gr.Textbox(label="Source Page Number", interactive=False)
        
        # Connect the UI components to the functions
        # Trigger process_fn when a file is uploaded
        pdf_input.upload(fn=process_fn, inputs=pdf_input, outputs=status_output)
        
        # Trigger answer_fn when button is clicked or enter is pressed
        ask_btn.click(fn=answer_fn, inputs=question_input, outputs=[answer_output, page_output])
        question_input.submit(fn=answer_fn, inputs=question_input, outputs=[answer_output, page_output])
        
    return demo
