import os
import flet as ft
from google import genai
from google.genai import types


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

# Fetch API key safely from GitHub Secrets / Environment Variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. Please set the environment variable."
    )

client = genai.Client(api_key=API_KEY)


# ============================================================
# PROSPER AI PERSONALITY
# ============================================================

SYSTEM_INSTRUCTION = """
You are Prosper AI, an intelligent, helpful, friendly,
and professional AI assistant.

Your creator is Fuwa Prosper Jesufemi.

If the user asks who created you, who built you,
who is your developer, or who made Prosper AI,
say that Prosper AI was created by Fuwa Prosper Jesufemi.

Fuwa Prosper Jesufemi is a young YouTuber, content creator,
gamer, website developer, and technology enthusiast.

His interests include:
- YouTube and content creation
- Gaming
- Website development
- Technology and gadgets
- Entrepreneurship
- Personal development
- Law and legal studies

Be helpful, friendly, and professional.
"""


# ============================================================
# FLET APPLICATION
# ============================================================

def main(page: ft.Page):

    page.title = "Prosper AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    message_input = ft.TextField(
        hint_text="Ask Prosper AI something...",
        expand=True,
        border_radius=20
    )

    def send_message(e):

        user_text = (message_input.value or "").strip()

        if not user_text:
            return

        # Show user message
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(
                    user_text,
                    color=ft.Colors.WHITE
                ),
                alignment=ft.alignment.center_right,
                bgcolor=ft.Colors.BLUE_700,
                padding=12,
                border_radius=15,
                margin=ft.margin.only(left=50)
            )
        )

        message_input.value = ""
        page.update()

        try:
            # Send request using google-genai SDK
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                text=(
                                    SYSTEM_INSTRUCTION
                                    + "\n\nUser message:\n"
                                    + user_text
                                )
                            )
                        ]
                    )
                ]
            )

            bot_reply = response.text

            if not bot_reply:
                bot_reply = "Sorry, I couldn't generate a response."

        except Exception as error:

            print("Gemini error:", error)

            bot_reply = (
                "❌ Gemini connection failed.\n\n"
                "Please check your API configuration "
                "and internet connection."
            )

        # Show AI response
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(
                    bot_reply,
                    color=ft.Colors.WHITE,
                    selectable=True
                ),
                alignment=ft.alignment.center_left,
                bgcolor=ft.Colors.GREY_800,
                padding=12,
                border_radius=15,
                margin=ft.margin.only(right=50)
            )
        )

        page.update()

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.BLUE_400,
        on_click=send_message
    )

    page.add(
        chat_list,
        ft.Row(
            controls=[
                message_input,
                send_button
            ]
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
