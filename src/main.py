import flet as ft
from components import Message, ChatMessage
from ai import AIBot


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = 'Flet Chat Ai'
    page.window.height = 600
    page.window.width = 300
    ai_bot = AIBot()

    def join_chat_click(e):
        if not join_username.value:
            join_username.error_text = 'Nome é obrigatório'
            join_username.update()
        else:
            page.session.set('user_name', join_username.value)
            page.dialog.open = False
            new_mansage.prefix = ft.Text(f'{join_username.value}: ')
            page.update()

    def add_message_on_histtory(message: Message):
        m = ChatMessage(message)
        chat.controls.append(m)
        history_messages = page.session.get('history_messages') if page.session.get('history_messages') else []
        history_messages.append(message)
        page.session.set('history_messages', history_messages)
        page.update()

    def send_message_click(e):
        if new_mansage.value != '':
            user_message = new_mansage.value
            add_message_on_histtory(
                Message(
                    user_name=page.session.get('user_name'),
                    text=user_message,
                    user_type='user'
                )
            )
            new_mansage.value = ''
            page.update()

            ai_response = ai_bot.invoke(
                history_messages = page.session.get('history_messages') if page.session.get('history_messages') else [],
                user_message=user_message,
            )
            add_message_on_histtory(
                Message(
                    user_name='AI',
                    text=ai_response,
                    user_type='ai'
                )
            )
            page.update()
            new_mansage.focus()


    join_username = ft.TextField(
        label='Informe seu nome.',
        autofocus=True,
        on_submit=join_chat_click,
    )

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text('Bem vindo(a)!'),
        content=ft.Column([join_username], width=200, height=70, tight=True),
        actions=[ft.ElevatedButton(text='Começar', on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    app_bar  = ft.AppBar(
        leading=ft.Icon(ft.Icons.ASSISTANT),
        leading_width=40,
        title=ft.Text('AI Chat'),
        bgcolor=ft.Colors.SURFACE,

    )

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    
    new_mansage = ft.TextField(
        hint_text= 'Em que posso ajudar?',
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=3,
        filled=True,
        expand=True,
        on_submit=send_message_click
    )

    page.add(
        app_bar,
        ft.Container(
            content= chat,
            border_radius=5,
            padding=10,
            expand=True,

        ),

        ft.Row(
            {
                new_mansage,
                ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    tooltip='Enviar',
                    on_click=send_message_click
                )
            }

        ),
    )

    page.update()

ft.app(main)
