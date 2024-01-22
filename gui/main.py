import flet as ft
from models.SD import SDModel


model = SDModel()

def main(page: ft.Page):
    text_input1 = ft.TextField(hint_text="Prompt", multiline=True)
    text_input2 = ft.TextField(hint_text="Negative prompt", multiline=True)
    send_button = ft.ElevatedButton(text="Generate")

    def send_click(e):
        with open('result.jpg', 'wb') as f:
            img = model.query(text_input1.value, text_input2.value)
            f.write(img)
        

    send_button.on_click = send_click

    image = ft.Image(src="/images/placeholder.svg", width=512, height=512)
    input_container = ft.Container(ft.Column([text_input1, text_input2, send_button]), padding=100)
    

    container = ft.Row([
        input_container,
        image
        
    ])

    page.add(container)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)