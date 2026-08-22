import os
import flet as ft
from google import genai

# Initialize the Gemini Client
client = genai.Client(api_key="AQ.Ab8RN6IxpFR5ilSn1AqRkwNvY9hhybqQv_9Q9wqPtEVp9nM_TQ")

def main(page: ft.Page):
    # --- Page Setup ---
    page.title = "Prosper AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.vertical_alignment = ft.MainAxisAlignment.END

    # --- UI Components ---
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    user_input = ft.TextField(
        hint_text="Type a message...",
        expand=True,
        border_radius=20,
        shift_enter=True,
        on_submit=lambda e: send_message(e)
    )

    def send_message(e):
        prompt = user_input.value.strip()
        if not prompt:
            return

        # Display User Message
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(prompt, color=ft.Colors.WHITE),
                alignment=ft.Alignment(1, 0),
                bgcolor=ft.Colors.BLUE_GREY_800,
                padding=10,
                border_radius=10,
            )
        )
        user_input.value = ""
        page.update()

        try:
            # Generate AI Response
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )

            # Display AI Message
            chat_list.controls.append(
                ft.Container(
                    content=ft.Text(response.text, color=ft.Colors.WHITE),
                    alignment=ft.Alignment(-1, 0),
                    bgcolor=ft.Colors.BLUE_900,
                    padding=10,
                    border_radius=10,
                )
            )
        except Exception as err:
            chat_list.controls.append(
                ft.Container(
                    content=ft.Text(f"Error: {str(err)}", color=ft.Colors.RED_400),
                    alignment=ft.Alignment(-1, 0),
                    padding=10,
                )
            )

        page.update()

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.BLUE_400,
        on_click=send_message
    )

    # --- Layout ---
    page.add(
        chat_list,
        ft.Row(
            controls=[user_input, send_button],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)
