import os
import flet as ft
from google import genai

def main(page: ft.Page):
    page.title = "Gemini AI Chat"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    
    # Initialize Gemini API Client
    # Replace 'YOUR_GEMINI_API_KEY' with your actual key or set GEMINI_API_KEY env variable
    api_key = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Chat messages container
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    # Text input field
    user_input = ft.TextField(
        hint_text="Type a message...",
        expand=True,
        border_radius=20,
        autofocus=True
    )

    def send_message(e):
        prompt = user_input.text.strip()
        if not prompt:
            return

        # 1. Add User Message to Chat
        chat_list.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(prompt, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.BLUE_600,
                        padding=12,
                        border_radius=15,
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        )
        user_input.value = ""
        page.update()

        # 2. Get Response from Gemini
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            reply = response.text
        except Exception as err:
            reply = f"Error: {str(err)}"

        # 3. Add AI Response to Chat
        chat_list.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(reply, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREY_800,
                        padding=12,
                        border_radius=15,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )
        page.update()

    # Send button
    send_btn = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.BLUE_400,
        on_click=send_message
    )

    # App Layout
    page.add(
        ft.AppBar(
            title=ft.Text("Gemini AI Assistant"),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_VARIANT
        ),
        chat_list,
        ft.Row([user_input, send_btn])
    )

ft.app(target=main)
