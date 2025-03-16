# Pomodoro Timer

## ファイル構造

```:bash
POMODORO
│  directory_tree.txt
│  docker-compose.yml
│  Dockerfile
│  PomodoroApp.spec
│  pomodorotimer.toml
│  README.md
│  requirements.txt
│
├─.github
│  └─workflows
│          build.yml
│
└─app
    │  main.py
    │
    ├─assets
    │      end_sound.mp3
    │
    ├─components
    │  │  timer_logic.py
    │  │
    │  └─__pycache__
    │          timer_logic.cpython-39.pyc
    │
    ├─screens
    │  │  settings_screens.py
    │  │  timer_screens.py
    │  │
    │  └─__pycache__
    │          settings_screens.cpython-39.pyc
    │          timer_screens.cpython-39.pyc
    │
    └─storage
        ├─data
        └─temp
```

## 技術

Python（Flet）
Github Actionsで各OS毎にパッケージ化

## 機能

設定された作業時間と小休憩を繰り返す
一定回数繰り返すと、大休憩がスタート
その後カウントを初期化して、再スタート
（デフォルトでは、各ステップが終了すると次のステップが自動でスタートする）

## 設定内容

1. 作業時間の設定
2. 小休憩時間の設定
3. 大休憩時間の設定
4. タイマー終了後の自動スタート
5. 通知音のオフ

