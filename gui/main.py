import flet as ft
from models.SD import SDModel
import base64
from io import BytesIO
from PIL import Image


def render(page: ft.Page):
    text_input1 = ft.TextField(hint_text='Prompt', multiline=True)
    text_input2 = ft.TextField(hint_text='Negative prompt', multiline=True)
    send_button = ft.ElevatedButton(text='Generate')
    progress_ring = ft.ProgressRing(visible=False)
    image = ft.Image(width=512, height=512)
    image.src='/images/placeholder.svg'

    image_container = ft.Stack([image, ft.Container(progress_ring, alignment=ft.alignment.center)],
                               width=512, height=512)
    input_container = ft.Container(ft.Column([text_input1, text_input2, send_button]), padding=100)

    def send_click(e):
        progress_ring.visible = True
        page.update()

        img = model.query(text_input1.value, text_input2.value)

        buffered = BytesIO()
        img.save(buffered, format='JPEG')
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        progress_ring.visible = False
        image.src_base64 = img_base64
        page.update()

    send_button.on_click = send_click

    container = ft.Row([
        input_container,
        image_container
        
    ])
    progress = ft.Column([ft.Text("Model initialization", style="headlineSmall"),
                             ft.Column([ft.Text("Please wait..."), ft.ProgressBar(width=400)])], alignment=ft.alignment.center
                )   
    page.add(progress)
    model = SDModel()
    progress.visible = False
    page.add(container)

def startapp():
    ft.app(target=render, view=ft.AppView.WEB_BROWSER)
