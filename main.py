import flet as ft
import google.generativeai as genai
import os

# ==========================================
# 1. API KEY CONFIGURATION
# ==========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6IW-gEKorUTVuu9iQq8-YiRMy_tlKALEY4EablGqc-oDQ")

genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# 2. PROSPER AI PERSONA & CREATOR BIO
# ==========================================
system_instruction = """
You are Prosper AI, an intelligent, helpful, and professional AI assistant.

CRITICAL CREATOR INFORMATION:
If the user asks "Who created you?", "Who built this app?", "Who is your developer?", or any variation about your creator, you MUST respond with the following details:

FUWA PROSPER JESUFEMI
Date of Birth: July 10, 2010

Fuwa Prosper Jesufemi is a young YouTuber, Content Creator, Gamer, Website Developer, and Tech Enthusiast with a passion for technology, digital creativity, gaming, and innovation.

He creates content focused on technology, gadgets, gaming, lifestyle, and personal growth, while continuously developing his skills in web development and digital media.

Beyond technology and content creation, Prosper is also an aspiring lawyer, currently building the knowledge and discipline needed to pursue a career in law.

Areas of Interest:
- 🎥 YouTube & Content Creation
- 🎮 Gaming
- 💻 Website Development
- 📱 Technology & Gadgets
- ⚖️ Law & Legal Studies
- 🚀 Entrepreneurship & Personal Development

Vision:
To build a strong digital brand, inspire others through content, develop innovative technology solutions, and eventually make an impact in both the technology and legal industries.

“Creating. Building. Learning. Becoming.”

RULES:
- Never say you were created by Google or OpenAI. Always attribute your creation to Fuwa Prosper Jesufemi.
"""

# Initialize Gemini model with System Instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

chat_session = model.start_chat(history=[])
is_owner_mode = False

# ==========================================
# 3. FLET MOBILE UI APPLICATION
# ==========================================
def main(page: ft.Page):
    global is_owner_mode

    page.title = "Prosper AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    # Chat message list
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    # Input text field
    message_input = ft.TextField(
        hint_text="Type a message...",
        expand=True,
        border_radius=20,
        shift_enter=True
    )

    def send_message_click(e):
        global is_owner_mode

        user_text = message_input.value.strip()
        if not user_text:
            return

        # Display user message
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(user_text, color=ft.colors.WHITE),
                alignment=ft.alignment.center_right,
                bgcolor=ft.colors.BLUE_700,
                padding=12,
                border_radius=15,
                margin=ft.margin.only(left=50)
            )
        )
        
        message_input.value = ""
        page.update()

        # Check for Owner Mode trigger
        if user_text == "Fuwa123":
            is_owner_mode = True
            bot_reply = "🔓 **OWNER MODE ACTIVATED.** Welcome back, Creator Fuwa Prosper Jesufemi. Systems fully accessible."
        else:
            try:
                prompt = user_text
                if is_owner_mode:
                    prompt = f"[SYSTEM: User is authenticated as Owner/Creator Fuwa Prosper Jesufemi]. User says: {user_text}"
                
                response = chat_session.send_message(prompt)
                bot_reply = response.text
            except Exception as err:
                bot_reply = f"Error: {str(err)}\nPlease verify your Gemini API key."

        # Display Bot response
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(bot_reply, color=ft.colors.WHITE),
                alignment=ft.alignment.center_left,
                bgcolor=ft.colors.GREY_800,
                padding=12,
                border_radius=15,
                margin=ft.margin.only(right=50)
            )
        )
        page.update()

    # Layout structure
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.BLUE_400,
        on_click=send_message_click
    )

    input_row = ft.Row([message_input, send_button])

    page.add(
        chat_list,
        input_row
    )

ft.app(target=main)
