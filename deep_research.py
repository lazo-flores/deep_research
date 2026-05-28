import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from email_agent import set_recipient_email, is_valid_email

load_dotenv(override=True)


async def run(query: str, email: str = ""):
    # Set recipient email if provided and valid
    if email and email.strip():
        if is_valid_email(email):
            set_recipient_email(email.strip())
        else:
            set_recipient_email(None)
    else:
        set_recipient_email(None)

    async for chunk in ResearchManager().run(query):
        yield chunk


def clear_fields():
    """Clear input fields only."""
    return "", ""


def check_if_fields_have_input(query: str, email: str):
    """Check if either field has input to enable/disable clear button."""
    has_input = bool(query.strip() or email.strip())
    return gr.update(interactive=has_input)


with gr.Blocks() as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(
        label="I am your research assistant. What topic would you like to research?",
        placeholder="e.g. 'Posibilily of extraterrestrial life'"
    )
    email_textbox = gr.Textbox(
        label="OPTIONAL: Enter your email if you want to get a copy of the report emailed to you.",
        placeholder="your.email@example.com"
    )

    with gr.Row():
        run_button = gr.Button("Run", variant="primary")
        clear_button = gr.Button("Clear", interactive=False)

    report = gr.Markdown(label="Report")

    # Run button and submit functionality
    run_button.click(fn=run, inputs=[query_textbox, email_textbox], outputs=report)
    query_textbox.submit(fn=run, inputs=[query_textbox, email_textbox], outputs=report)

    # Clear button functionality
    clear_button.click(
        fn=clear_fields,
        inputs=[],
        outputs=[query_textbox, email_textbox]
    )

    # Enable/disable clear button based on input
    query_textbox.change(
        fn=check_if_fields_have_input,
        inputs=[query_textbox, email_textbox],
        outputs=clear_button
    )
    email_textbox.change(
        fn=check_if_fields_have_input,
        inputs=[query_textbox, email_textbox],
        outputs=clear_button
    )

ui.launch(share=True, inbrowser=True, theme=gr.themes.Glass(primary_hue="indigo"))
