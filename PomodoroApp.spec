# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app/main.py'],            # エントリーポイントの指定
    pathex=['.'],               # プロジェクトルートをパスに含める
    binaries=[],                # 追加のバイナリファイルがあれば指定（今回は不要）
    datas=[('app/assets', 'app/assets')],  # アプリ内のassetsフォルダを同じ階層にコピー
    hiddenimports=[],           # 必要に応じて、動的にインポートされるモジュールを追加
    hookspath=[],               # カスタムフックがあればそのディレクトリを指定
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PomodoroApp',       # 出力される実行ファイル名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                 # UPXによる圧縮（不要な場合はFalse）
    console=False             # GUIアプリの場合はFalse（コンソールウィンドウを非表示）
)
