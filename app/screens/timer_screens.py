# timer screen
import flet as ft
from components import timer_logic

work_time = 25 * 60

def timer_view(page: ft.Page):
    global work_time
    if page.session.get("work_time") == None:
        work_time = 25 * 60
    else:
        work_time = page.session.get("work_time") * 60
    page.title = "Pomodoro Timer by Flet"
    if page.session.get("required_cycle") == None:
        required_cycle = 4
    else:
        required_cycle = page.session.get("required_cycle")
    max_cycle = ft.Text(str(required_cycle), size=40, color=ft.Colors.RED_400)
    timer_display = ft.Text(timer_logic.format_duration(work_time), size=80)
    cycle_count_display = ft.Text(value="0", size=40, color=ft.Colors.RED_400)

    # progress_canvas = ft.Canvas(width=200, height=200)

    start_icon = ft.Icons.PLAY_ARROW
    stop_icon = ft.Icons.STOP
    reset_icon = ft.Icons.REPLAY

    start_button = ft.ElevatedButton("Start", on_click=lambda e: timer_logic.start_timer(page, timer_display, cycle_count_display), icon=start_icon)
    stop_button = ft.ElevatedButton("Stop", on_click=lambda e: timer_logic.stop_timer(page), icon=stop_icon)
    reset_button = ft.ElevatedButton("Reset", on_click=lambda e: timer_logic.reset_timer(page, timer_display, cycle_count_display), icon=reset_icon)
    
    setting_icon =ft.Icons.SETTINGS
    to_settings_button = ft.ElevatedButton("Settings Page", on_click=lambda e: page.go("/settings"), icon=setting_icon)
    layout = ft.Column(
        controls=[
            ft.Row(
                controls=[to_settings_button],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[timer_display],
                            alignment=ft.MainAxisAlignment.CENTER  # 横中央揃え
                        ),
                        ft.Row(
                            controls=[ft.Text("Pomodoro:", size=20), cycle_count_display, ft.Text("/", size=40), max_cycle],
                            alignment=ft.MainAxisAlignment.CENTER  # 横中央揃え
                        ),
                        ft.Row(
                            controls=[start_button, stop_button, reset_button],
                            alignment=ft.MainAxisAlignment.CENTER  # ボタンを中央揃え
                        ),
                    ],
                ),
            ),
        ],
    )

    return layout