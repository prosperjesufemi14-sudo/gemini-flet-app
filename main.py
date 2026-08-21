import os
import flet as ft
from google import genai

# Initialize the Gemini Client using the environment variable GEMINI_API_KEY
client = genai.Client()

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
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.BLUE_400,
        tooltip="Send message",
    )

    # --- Event Handlers ---
    def send_message_click(e):
        prompt = user_input.value.strip()
        if not prompt:
            return

        # Clear input field
        user_input.value = ""
        
        # Add User Message to Chat
        chat_list.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(prompt, color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE_800,
                        padding=12,
                        border_radius=15,
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        )
        page.update()

        # Generate Gemini Response
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            bot_text = response.text if response.text else "No response generated."
        except Exception as err:
            bot_text = f"Error: {str(err)}"

        # Add Gemini Response to Chat
        chat_list.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(bot_text, color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREY_800,
                        padding=12,
                        border_radius=15,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )
        page.update()

    # Bind Send Actions
    send_button.on_click = send_message_click
    user_input.on_submit = send_message_click

    # Input Bar Layout
    input_row = ft.Row(
        controls=[
            user_input,
            send_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # --- Add Controls to Page ---
    page.add(
        chat_list,
        input_row,
    )

if __name__ == "__main__":
    ft.app(target=main)
