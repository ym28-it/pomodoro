import time
import flet as ft
from enum import Enum
import asyncio
import threading

class TimerState(Enum):
    WORK = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3
    STOPPED = 4

_global_loop = asyncio.new_event_loop()
threading.Thread(target=lambda: _global_loop.run_forever(), daemon=True).start()

current_state = TimerState.STOPPED
start_time = None
elapsed_time = 0

work_duration = 25 * 60
short_break_duration = 5 * 60
long_break_duration = 20 * 60
required_cycle = 4
current_cycle_count = 0
auto_start = True
mute_setting = False

current_duration = work_duration
stop_flag = False
state_before_stop = TimerState.WORK


def set_durations(page: ft.Page):
    global current_state, work_duration, short_break_duration, long_break_duration, required_cycle, current_duration, auto_start, mute_setting

    work_duration = page.session.get("work_time") * 60
    short_break_duration = page.session.get("short_break") * 60
    long_break_duration = page.session.get("long_break") * 60
    required_cycle = page.session.get("required_cycle")
    auto_start = page.session.get("auto_start")
    mute_setting = page.session.get("mute_setting")

    current_state = TimerState.STOPPED

def start_timer(page: ft.Page, timer_display: ft.Text, cycle_count_display: ft.Text):
    global start_time, current_state, elapsed_time, stop_flag, current_duration, reset_flag, state_before_stop

    if current_state == TimerState.STOPPED:
        if stop_flag:
            stop_flag = False
            current_state = state_before_stop
        else:
            current_duration = work_duration
            current_state = TimerState.WORK
        start_time = time.time()
        
        asyncio.run_coroutine_threadsafe(_run_timer(page, timer_display, cycle_count_display), _global_loop)

async def _run_timer(page: ft.Page, timer_display: ft.Text, cycle_count_display: ft.Text):
    global start_time, elapsed_time, current_state, stop_flag, auto_start

    while True:
        if current_state == TimerState.STOPPED or stop_flag:
            await asyncio.sleep(0.05)
            continue

        current_time = time.time()

        elapsed_time = current_time - start_time

        remaining = current_duration - elapsed_time

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        milliseconds = int((remaining - int(remaining)) * 1000)

        timer_display.value = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        page.update()

        if remaining <= 0:
            _handle_state_transition(page, timer_display, cycle_count_display)
            if auto_start == False:
                current_state = TimerState.STOPPED
            break
        
        await asyncio.sleep(0.05)

def reset_timer(page: ft.Page, timer_display: ft.Text, cycle_count_display: ft.Text):
    global current_state, current_cycle_count, work_duration
    current_cycle_count = 0
    cycle_count_display.value = "0"
    timer_display.value = format_duration(work_duration)
    timer_display.color = ft.Colors.BLACK
    current_state = TimerState.STOPPED
    page.update()

def stop_timer(page: ft.Page):
    global current_state, stop_flag, current_duration, start_time, state_before_stop
    stop_flag = True
    current_duration = current_duration - (time.time() - start_time)
    state_before_stop = current_state
    current_state = TimerState.STOPPED

def format_duration(duration):
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    milliseconds = int((duration - int(duration)) * 1000)
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def _handle_state_transition(page: ft.Page, timer_display: ft.Text, cycle_count_display: ft.Text):
    global current_state, start_time, current_cycle_count, current_duration, work_duration, short_break_duration, long_break_duration, stop_flag, mute_setting, state_before_stop

    if current_state == TimerState.WORK:
        current_cycle_count += 1
        if current_cycle_count >= required_cycle:
            current_state = TimerState.LONG_BREAK
            timer_display.color = ft.Colors.LIGHT_BLUE_ACCENT_400
            current_duration = long_break_duration
        else:
            current_duration = short_break_duration
            current_state = TimerState.SHORT_BREAK
            timer_display.color = ft.Colors.GREEN_ACCENT_400

    else:
        if current_state == TimerState.LONG_BREAK:
            current_cycle_count = 0

        current_duration = work_duration
        current_state = TimerState.WORK
        timer_display.color = ft.Colors.BLACK
    
    cycle_count_display.value = f"{current_cycle_count}"

    if mute_setting == False:
        _play_notification_sound()

    if not auto_start:
        stop_flag = True
        state_before_stop = current_state
        current_state = TimerState.STOPPED
        timer_display.value = format_duration(current_duration)
        page.update()
        return

    start_time = time.time()
    asyncio.run_coroutine_threadsafe(_run_timer(page, timer_display, cycle_count_display), _global_loop)

def _play_notification_sound(page: ft.Page):
    try:
        page.audio.src = "assets/end_sound.mp3"

        page.audio.play()
        page.update()
    except Exception as e:
        print("Sound Error:", e)

