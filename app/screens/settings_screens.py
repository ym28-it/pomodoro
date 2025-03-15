# user setting screen
import flet as ft
from components import timer_logic

def setting_view(page: ft.Page):
    work_time_value = page.session.get("work_time")
    short_break_value = page.session.get("short_break")
    long_break_value = page.session.get("long_break")
    required_cycle_value = page.session.get("required_cycle")
    auto_start_value = page.session.get("auto_start")
    mute_setting_value = page.session.get("mute_setting")

    # None の場合にデフォルト値を適用
    if work_time_value is None:
        work_time_value = 25
    if short_break_value is None:
        short_break_value = 5
    if long_break_value is None:
        long_break_value = 20
    if required_cycle_value is None:
        required_cycle_value = 4
    if auto_start_value is None:
        auto_start_value = True
    if mute_setting_value is None:
        mute_setting_value = False

    # 取得した値を TextField にセット
    work_time = ft.TextField(label="作業時間(分)", value=str(work_time_value))
    short_break = ft.TextField(label="小休憩時間(分)", value=str(short_break_value))
    long_break = ft.TextField(label="大休憩時間(分)", value=str(long_break_value))
    required_cycle = ft.TextField(label="大休憩のスパン(回)", value=str(required_cycle_value))
    auto_start = ft.Checkbox(label="自動スタート", value=auto_start_value)
    mute_setting = ft.Checkbox(label="通知音のミュート", value=mute_setting_value)

    def save_settings(e):
        page.session.set("work_time", int(work_time.value))
        page.session.set("short_break", int(short_break.value))
        page.session.set("long_break", int(long_break.value))
        page.session.set("required_cycle", int(required_cycle.value))
        page.session.set("auto_start", auto_start.value)
        page.session.set("mute_setting", mute_setting.value)
        timer_logic.set_durations(page)
        page.go("/timer")
    
    timer_icon = ft.Icons.TIMER_SHARP
    save_icon = ft.Icons.SAVE
    save_button = ft.ElevatedButton("Save", on_click=save_settings, icon=save_icon)
    to_timer_button = ft.ElevatedButton("Timer Page", on_click=lambda e: page.go("/timer"), icon=timer_icon)

    return ft.Column(controls=[
        ft.Row(
                controls=[to_timer_button],
                alignment=ft.MainAxisAlignment.END
            ),
        ft.Divider(),
        work_time,
        short_break,
        long_break,
        required_cycle,
        auto_start,
        mute_setting,
        ft.Row(
                controls=[save_button],
                alignment=ft.MainAxisAlignment.END
            )
    ])