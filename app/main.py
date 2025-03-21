# entrypoint
import flet as ft
from screens import settings_screens, timer_screens

def route_change(page: ft.Page):
    
    page.views.clear()

    if page.route == "/settings":
        page.views.append(
            ft.View(
                route="/settings",
                controls=[settings_screens.setting_view(page)]
            )
        )
    elif page.route == "/" or page.route == "/timer":
        page.views.append(
            ft.View(
                route="/timer",
                controls=[timer_screens.timer_view(page)]
            )
        )
    
    page.update()

def main(page: ft.Page):
    page.title = "Pomodoro Timer App"

    page.audio = ft.Audio(autoplay=False)
    page.add(page.audio)

    page.on_route_change = lambda e: route_change(page)

    page.go("/timer")

if __name__ == "__main__":
    ft.app(main)