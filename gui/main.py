import flet as ft
from models.SD import SDModel
import io
import base64
import pickle

model = SDModel()



def render(page: ft.Page):
    text_input1 = ft.TextField(hint_text="Prompt", multiline=True)
    text_input2 = ft.TextField(hint_text="Negative prompt", multiline=True)
    send_button = ft.ElevatedButton(text="Generate")
    progress_ring = ft.ProgressRing(visible=False)



    image_container = ft.Stack([ft.Container(progress_ring, alignment=ft.alignment.center)], width=512, height=512)

    input_container = ft.Container(ft.Column([text_input1, text_input2, send_button]), padding=100)

    def send_click(e):
        progress_ring.visible = True
        page.update()

        
        img = model.query(text_input1.value, text_input2.value)

        img_byte_arr = io.BytesIO()
        img.save("test.jpg")
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img_base64 = base64.b64encode(img_byte_arr).decode()
        
        progress_ring.visible = False
        image_container.controls.append(ft.Image(src_base64=img_base64, width=512, height=512))

        page.update(image_container)

    send_button.on_click = send_click

    container = ft.Row([
        input_container,
        image_container
        
    ])

    page.add(container)

def startapp():
    ft.app(target=render, view=ft.AppView.WEB_BROWSER)
