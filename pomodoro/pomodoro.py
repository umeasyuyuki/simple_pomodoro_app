import tkinter as tk
from tkinter import font
import math
import datetime
import pygame  # 追加：pygame

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.attributes('-fullscreen', True)  # 全画面表示

        # pygameの初期化
        pygame.mixer.init()  # 音声を扱うための初期化

        # ダークモード配色設定
        self.dark_bg = "#2e2e2e"
        self.dark_fg = "#ffffff"

        # フォント設定
        self.selected_font = "Courier"

        # 背景色とテキスト色をダークモードに設定
        self.root.config(bg=self.dark_bg)

        # タイトルラベルをダークモードで表示（ラベルの色を白色に設定）
        self.label = tk.Label(text="Set your work and break time", fg=self.dark_fg, bg=self.dark_bg, font=("Courier", 30))
        self.label.pack(pady=20)

        # タイマーの数字を最初は非表示
        self.timer_text = tk.Label(fg=self.dark_fg, bg=self.dark_bg, font=(self.selected_font, 380, "bold"))

        # 作業時間と休憩時間の入力フィールド
        self.work_label = tk.Label(text="Work Time (min)", bg=self.dark_bg, fg=self.dark_fg, font=("Courier", 20))
        self.work_label.pack(pady=10)
        self.work_time_input = tk.Entry(width=10, font=("Courier", 40))
        self.work_time_input.pack(pady=10)
        self.work_time_input.insert(0, "25")

        self.break_label = tk.Label(text="Break Time (min)", bg=self.dark_bg, fg=self.dark_fg, font=("Courier", 20))
        self.break_label.pack(pady=10)
        self.break_time_input = tk.Entry(width=10, font=("Courier", 40))
        self.break_time_input.pack(pady=10)
        self.break_time_input.insert(0, "5")

        # Startボタンを入力フォームのすぐ下に配置
        self.start_button = tk.Button(text="Start", highlightbackground=self.dark_bg, font=("Courier", 40), command=self.start_timer)
        self.start_button.pack(pady=20)

        # Timeボタンを追加
        self.time_button = tk.Button(text="Time", highlightbackground=self.dark_bg, font=("Courier", 40), command=self.show_time)
        self.time_button.pack(pady=20)

        # 合計作業時間を表示するラベル（最初は非表示）
        self.total_time_label = tk.Label(fg=self.dark_fg, bg=self.dark_bg, font=("Courier", 60, "bold"))
        self.total_time_label.pack(pady=20)  # Startボタンの下に配置

        # フォント選択メニューを右上に表示
        self.font_var = tk.StringVar(value=self.selected_font)
        self.font_menu = tk.OptionMenu(self.root, self.font_var, "Courier", "Arial", "Times", command=self.change_font)
        self.font_menu.config(bg=self.dark_bg, fg=self.dark_fg)
        self.font_menu.place(x=self.root.winfo_screenwidth() - 200, y=10)

        # ResetボタンとStopボタンを定義（初期は非表示）
        self.reset_button = tk.Button(text="Reset", highlightbackground=self.dark_bg, font=("Courier", 20), command=self.reset_timer)
        self.stop_button = tk.Button(text="Stop", highlightbackground=self.dark_bg, font=("Courier", 20), command=self.stop_timer)

        # Stopボタンが押された時の一時停止状態を管理
        self.timer_paused = False
        self.remaining_time = 0

        # 作業時間のログを記録するリスト
        self.work_log = []
        self.reps = 0
        self.timer = None
        self.work_time = 0
        self.break_time = 0

        # ESCキーで全画面を解除する設定
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Enterキーでホーム画面に戻る設定
        self.root.bind("<Return>", self.return_home)

    def show_time(self):
        """時刻のみを画面いっぱいに表示する"""
        self.clear_screen()  # ホーム画面を非表示にする
        self.time_button.pack_forget()  # Timeボタンを非表示にする
        self.time_label = tk.Label(self.root, fg=self.dark_fg, bg=self.dark_bg, font=(self.selected_font, 240, "bold"))
        self.time_label.pack(expand=True)
        self.update_clock()

    def update_clock(self):
        """現在の時刻を24時間制で表示"""
        now = datetime.datetime.now().strftime("%H:%M:%S")  # 現在の時刻を取得
        self.time_label.config(text=now, font=(self.selected_font, 240, "bold"))  # ラベルに時刻を設定しフォントを反映
        self.root.after(1000, self.update_clock)  # 1秒ごとに時刻を更新

    def return_home(self, event=None):
        """ホーム画面に戻る"""
        if hasattr(self, 'time_label'):
            self.time_label.pack_forget()  # 時刻表示を非表示にする
        self.show_home_screen()

    def clear_screen(self):
        """画面をクリア（ホーム画面を隠す）"""
        self.label.pack_forget()
        self.work_label.pack_forget()
        self.work_time_input.pack_forget()
        self.break_label.pack_forget()
        self.break_time_input.pack_forget()
        self.start_button.pack_forget()
        self.total_time_label.pack_forget()

    def show_home_screen(self):
        """ホーム画面を再表示"""
        self.label.pack(pady=20)
        self.work_label.pack(pady=10)
        self.work_time_input.pack(pady=10)
        self.break_label.pack(pady=10)
        self.break_time_input.pack(pady=10)
        self.start_button.pack(pady=20)
        self.time_button.pack(pady=20)  # Timeボタンを再表示
        self.total_time_label.pack(pady=20)

    def change_font(self, selected_font):
        """タイマーのフォントを変更"""
        self.selected_font = selected_font
        self.timer_text.config(font=(self.selected_font, 380, "bold"))
        self.time_label.config(font=(self.selected_font, 240, "bold"))  # 時刻のフォントも変更

    def reset_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)

        # セッションの合計作業時間を計算して表示
        total_time = sum(self.work_log)
        total_time_minutes = total_time / 60
        self.label.config(text=f"Total Work Time: {total_time_minutes:.2f} min", fg=self.dark_fg)  # 上部のラベルに表示
        self.timer_text.pack_forget()  # タイマーを非表示
        self.reps = 0
        self.work_log.clear()  # 作業ログをリセット

        # リセット後にリセットとストップボタンを非表示にする
        self.reset_button.place_forget()
        self.stop_button.place_forget()

        # 入力フィールドを再表示
        self.work_label.pack(pady=10)
        self.work_time_input.pack(pady=10)
        self.break_label.pack(pady=10)
        self.break_time_input.pack(pady=10)

        # Startボタンを再表示
        self.start_button.pack(pady=20)
        
        # Timeボタンを再表示
        self.time_button.pack(pady=20)

    def stop_timer(self):
        """タイマーを一時停止"""
        if self.timer:
            self.root.after_cancel(self.timer)
        if not self.timer_paused:
            # タイマーが動いている場合、残り時間を保存し、Resumeボタンに変える
            self.timer_paused = True
            self.stop_button.config(text="Resume", command=self.resume_timer)
        else:
            self.stop_button.config(text="Stop", command=self.stop_timer)

    def resume_timer(self):
        """一時停止したタイマーを再開"""
        self.timer_paused = False
        self.count_down(self.remaining_time)
        self.stop_button.config(text="Stop", command=self.stop_timer)

    def start_timer(self):
        """タイマー開始時にTimeボタンを隠す"""
        try:
            self.time_button.pack_forget()  # タイマーが始まるときにTimeボタンを隠す
            work_time_input_value = int(self.work_time_input.get())
            break_time_input_value = int(self.break_time_input.get())

            # 作業時間と休憩時間が60以下かをチェック
            if work_time_input_value > 60 or break_time_input_value > 60:
                raise ValueError("Time should be less than or equal to 60 minutes")

            self.work_time = work_time_input_value * 60  # 作業時間を秒に変換
            self.break_time = break_time_input_value * 60  # 休憩時間を秒に変換

            if self.work_time > 0 and self.break_time > 0:
                # 入力フィールドを非表示にする
                self.work_label.pack_forget()
                self.work_time_input.pack_forget()
                self.break_label.pack_forget()
                self.break_time_input.pack_forget()

                # タイマーを大きく表示
                self.timer_text.config(text="00:00", font=(self.selected_font, 380, "bold"))
                self.timer_text.pack(pady=50)

                # Total Work Time ラベルを非表示にする
                self.total_time_label.pack_forget()

                self.reps += 1
                if self.reps % 2 == 0:
                    self.count_down(self.break_time)
                    self.label.config(text="Break Time...", fg="#ffffff")
                else:
                    start_time = datetime.datetime.now()  # セッション開始時刻を記録
                    self.count_down(self.work_time, start_time)
                    self.label.config(text="Enjoy!", fg="#ffffff")

                # ボタンの配置を再表示（1cm上に、1cm中央寄り）
                self.reset_button.place(x=40, y=self.root.winfo_screenheight() - 150)
                self.stop_button.place(x=self.root.winfo_screenwidth() - 140, y=self.root.winfo_screenheight() - 150)
                self.start_button.pack_forget()
        except ValueError as e:
            self.label.config(text=str(e), fg="red")

    def count_down(self, count, start_time=None):
        """カウントダウン処理"""
        if self.timer_paused:
            self.remaining_time = count
            return

        minutes = math.floor(count / 60)
        seconds = count % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        self.timer_text.config(text=f"{minutes}:{seconds}")

        if count > 0:
            self.remaining_time = count
            self.timer = self.root.after(1000, self.count_down, count - 1, start_time)
        else:
            # セッション終了時間を記録し、作業ログに追加
            if start_time:
                end_time = datetime.datetime.now()
                work_duration = (end_time - start_time).seconds  # 作業時間を秒で取得
                self.work_log.append(work_duration)

            # 作業終了時に鳥の音を再生
            if self.reps % 2 == 0:
                pygame.mixer.music.load('gong.mp3')  # ゴングの音（休憩終了）
            else:
                pygame.mixer.music.load('bird.mp3')  # 鳥の音（作業終了）

            pygame.mixer.music.play()  # 音声を再生
            self.start_timer()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)  # 全画面モードを解除

root = tk.Tk()
pomodoro = PomodoroTimer(root)
root.mainloop()
