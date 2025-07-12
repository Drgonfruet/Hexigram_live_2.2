import tkinter as tk
from tkinter import ttk, scrolledtext
import datetime
import math
import constants
import webbrowser
import os

class GUIManager:
    def __init__(self, sound_manager, hexagram_calculator, vrchat_manager):
        self.sound_manager = sound_manager
        self.hexagram_calculator = hexagram_calculator
        self.vrchat_manager = vrchat_manager
        self.calculator_window = None
        self.sound_menu_window = None
        self.zero_datetime = datetime.datetime(2055, 7, 16)  # Default zero date
        self.audio_playback_allowed = False
        self.hexagram_images = {}  # Store loaded images
        self.hexagram_labels = {}  # Store image labels
        self.output_labels = []  # Store labels for the main display
        self.level6_moving_line_days = None
        self.level6_moving_line_num = None
        self.setup_main_window()

    def setup_main_window(self):
        self.root = tk.Tk()
        self.root.title("Hexagrams Live 2.0")
        
        # Set taskbar icon
        try:
            icon_path = os.path.join(constants.IMAGES_DIR, 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                icon_path = os.path.join(constants.IMAGES_DIR, 'icon.png')
                if os.path.exists(icon_path):
                    icon_image = tk.PhotoImage(file=icon_path)
                    self.root.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Failed to set window icon: {e}")
        
        self.root.configure(background=constants.DARK_THEME['background'])
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create main content frame
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top controls frame
        self.top_controls = ttk.Frame(self.content_frame)
        self.top_controls.pack(fill=tk.X, padx=10, pady=5)
        
        # Create zero date section in top controls
        self.zero_date_frame = ttk.Frame(self.top_controls)
        self.zero_date_frame.pack(side=tk.LEFT)
        
        # Create buttons frame in top controls
        self.buttons_frame = ttk.Frame(self.top_controls)
        self.buttons_frame.pack(side=tk.RIGHT)
        
        # Add button to open browser
        self.browser_button = ttk.Button(
            self.buttons_frame,
            text="Open Hexagram Reference",
            command=lambda: webbrowser.open("https://www.jamesdekorne.com/GBCh/hex1.htm")
        )
        self.browser_button.pack(side=tk.RIGHT, padx=5)

        self.setup_style()
        self.create_widgets()
        self.root.after(1000, self.enable_audio_playback)
        
        # Set initial window size and position
        initial_width = 1280
        initial_height = 820
        self.root.minsize(800, 600)
        self.root.geometry(f"{initial_width}x{initial_height}")
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - initial_width) // 2
        y = (screen_height - initial_height) // 2
        self.root.geometry(f"{initial_width}x{initial_height}+{x}+{y}")

    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.apply_theme(constants.DARK_THEME)

    def apply_theme(self, theme):
        self.style.configure('TLabel', background=theme['background'], foreground=theme['foreground'])
        self.style.configure('TEntry', fieldbackground=theme['entry_bg'], foreground=theme['foreground'])
        self.style.configure('TButton', background=theme['button_bg'], foreground=theme['foreground'])
        self.style.configure('TFrame', background=theme['background'])
        self.style.configure('TText', background=theme['text_bg'], foreground=theme['foreground'])
        self.style.configure('TScrollbar', background=theme['button_bg'], foreground=theme['foreground'])
        self.root.configure(background=theme['background'])

    def create_widgets(self):
        self.create_zero_date_section()
        self.create_display_area()
        self.create_control_buttons()
        self.create_check_section()

    def create_zero_date_section(self):
        self.zero_date_label = ttk.Label(self.zero_date_frame, text="Zero Date (YYYY-MM-DD):")
        self.zero_date_label.pack(side=tk.LEFT, padx=5)
        
        self.zero_date_entry = ttk.Entry(self.zero_date_frame)
        self.zero_date_entry.pack(side=tk.LEFT, padx=5)
        self.zero_date_entry.insert(0, "2055-07-16")
        
        self.update_button = ttk.Button(self.zero_date_frame, text="Update", command=self.update_zero_datetime)
        self.update_button.pack(side=tk.LEFT, padx=5)

    def load_hexagram_image(self, number):
        image_path = os.path.join(constants.IMAGES_DIR, f'hexagram{number:02d}.gif')
        if number not in self.hexagram_images and os.path.exists(image_path):
            try:
                photo = tk.PhotoImage(file=image_path)
                self.hexagram_images[number] = photo.subsample(2, 2)
            except tk.TclError:
                print(f"Error loading image: {image_path}")
                return None
        return self.hexagram_images.get(number)

    def create_display_area(self):
        self.display_frame = ttk.Frame(self.content_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.hexagram_frame = ttk.Frame(self.display_frame)
        self.hexagram_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        for level in range(1, 7):
            level_frame = ttk.Frame(self.hexagram_frame)
            level_frame.pack(pady=5)
            level_label = ttk.Label(level_frame, text=f"Level {level}", width=8)
            level_label.pack(side=tk.LEFT, padx=(0, 5))
            label = ttk.Label(level_frame)
            label.pack(side=tk.LEFT)
            self.hexagram_labels[level] = label
        
        self.output_frame = ttk.Frame(self.display_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        
        for i in range(21):
            label = ttk.Label(self.output_frame, text="", anchor="w", justify="left", font=("Courier", 10))
            label.pack(fill=tk.X, pady=0)
            self.output_labels.append(label)

    def create_control_buttons(self):
        self.control_buttons = ttk.Frame(self.buttons_frame)
        self.control_buttons.pack(side=tk.RIGHT, padx=5)

        self.send_to_vrchat_button = ttk.Button(
            self.control_buttons,
            text="Send to VRChat: ON" if constants.SEND_TO_VRCHAT_ENABLED else "Send to VRChat: OFF",
            command=self.toggle_send_to_vrchat
        )
        self.send_to_vrchat_button.pack(side=tk.LEFT, padx=5)

        self.page_button = ttk.Button(self.control_buttons, text=f"Page {constants.CURRENT_PAGE}", command=self.toggle_page)
        self.page_button.pack(side=tk.LEFT, padx=5)

        self.sound_menu_button = ttk.Button(self.control_buttons, text="Sound Menu", command=self.open_sound_menu)
        self.sound_menu_button.pack(side=tk.LEFT, padx=5)

        self.calculator_button = ttk.Button(self.control_buttons, text="Zero Date Calculator", command=self.open_calculator)
        self.calculator_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = ttk.Button(self.control_buttons, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=5)

    def create_check_section(self):
        self.check_panel = ttk.Frame(self.content_frame)
        self.check_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.input_frame = ttk.Frame(self.check_panel)
        self.input_frame.pack(fill=tk.X, pady=5)

        self.date_label = ttk.Label(self.input_frame, text="Date (YYYY-MM-DD):")
        self.date_label.pack(side=tk.LEFT, padx=5)
        self.date_entry = ttk.Entry(self.input_frame)
        self.date_entry.pack(side=tk.LEFT, padx=5)

        self.time_label = ttk.Label(self.input_frame, text="Time (HH:MM:SS):")
        self.time_label.pack(side=tk.LEFT, padx=5)
        self.time_entry = ttk.Entry(self.input_frame)
        self.time_entry.pack(side=tk.LEFT, padx=5)

        self.check_button = ttk.Button(self.input_frame, text="Check Hexagrams", command=self.check_hexagrams)
        self.check_button.pack(side=tk.LEFT, padx=5)

        self.check_display_frame = ttk.Frame(self.check_panel)
        self.check_display_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.check_hexagram_frame = ttk.Frame(self.check_display_frame)
        self.check_hexagram_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.check_hexagram_labels = {}
        for level in range(1, 7):
            level_frame = ttk.Frame(self.check_hexagram_frame)
            level_frame.pack(pady=5)
            level_label = ttk.Label(level_frame, text=f"Level {level}", width=8)
            level_label.pack(side=tk.LEFT, padx=(0, 5))
            label = ttk.Label(level_frame)
            label.pack(side=tk.LEFT)
            self.check_hexagram_labels[level] = label

        self.check_text = scrolledtext.ScrolledText(
            self.check_display_frame, width=60, height=20,
            background=constants.DARK_THEME['text_bg'],
            foreground=constants.DARK_THEME['foreground']
        )
        self.check_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.check_text.configure(state='disabled')

    def copy_to_clipboard(self):
        content = "\n".join(label.cget("text") for label in self.output_labels if label.cget("text"))
        self.root.clipboard_clear()
        self.root.clipboard_append(content)

    def update_display(self, hexagrams, time_to_zero, text_widget=None, input_datetime=None):
        if text_widget is None:
            self.update_main_display(hexagrams, time_to_zero, input_datetime)
        else:
            self.update_check_display(hexagrams, time_to_zero, text_widget, input_datetime)

    def update_main_display(self, hexagrams, time_to_zero, input_datetime=None):
        for hexagram in hexagrams:
            level, _, _, hexagram_number, _, _ = hexagram
            image = self.load_hexagram_image(hexagram_number)
            if image and level in self.hexagram_labels:
                self.hexagram_labels[level].configure(image=image)
                self.hexagram_labels[level].image = image
        
        message_lines = []
        if not hexagrams:
            message_lines.append("No hexagrams found for the current date.")
        else:
            current_date = input_datetime.date() if input_datetime else datetime.datetime.now().date()
            current_time = input_datetime.time() if input_datetime else datetime.datetime.now().time()
            days_to_zero = round(time_to_zero.total_seconds() / 86400, 4)
            message_lines.append(f"Hexagrams for: {current_date} - {current_time}")
            message_lines.append(f"Days to 0: {days_to_zero}")
            message_lines.append(f"Zero Date: {constants.ZERO_DATETIME}")
            
            for level, cycle_length, _, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
                moving_line = int((time_since_last_change // (cycle_length.total_seconds() / 6)) + 1)
                time_until_next_hexagram_change = time_since_last_change % cycle_length.total_seconds()
                line_change_interval = cycle_length.total_seconds() / 6
                time_until_next_line_change = time_since_last_change % line_change_interval
                
                if level == 1:
                    milliseconds = int(time_until_next_hexagram_change * 1000)
                    hex_timer = f"{milliseconds:03d}ms"
                    line_milliseconds = int(time_until_next_line_change * 1000)
                    line_timer = f"{line_milliseconds:03d}ms"
                    message_lines.append(f"Level {level}: {cycle_length.total_seconds():.4f} s, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level 1 changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                    if constants.previous_hexagrams.get(f'level_{level}') != hexagram_number and constants.PLAY_AUDIO_LEVEL_1_ENABLED:
                        constants.previous_hexagrams[f'level_{level}'] = hexagram_number
                        self.sound_manager.play_level_sound(1)
                    if constants.previous_hexagrams.get(f'level_{level}_line') != moving_line and constants.PLAY_AUDIO_LEVEL_1_LINE_ENABLED:
                        constants.previous_hexagrams[f'level_{level}_line'] = moving_line
                        self.sound_manager.play_line_sound(1)
                elif level == 2:
                    seconds = int(time_until_next_hexagram_change)
                    hex_timer = f"{seconds:02d}s"
                    line_seconds = int(time_until_next_line_change)
                    line_timer = f"{line_seconds:02d}s"
                    message_lines.append(f"Level {level}: {cycle_length.total_seconds()} s, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level 2 changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                    if constants.previous_hexagrams.get(f'level_{level}') != hexagram_number and constants.PLAY_AUDIO_LEVEL_2_ENABLED:
                        constants.previous_hexagrams[f'level_{level}'] = hexagram_number
                        self.sound_manager.play_level_sound(2)
                    if constants.previous_hexagrams.get(f'level_{level}_line') != moving_line and constants.PLAY_AUDIO_LEVEL_2_LINE_ENABLED:
                        constants.previous_hexagrams[f'level_{level}_line'] = moving_line
                        self.sound_manager.play_line_sound(2)
                elif level == 3:
                    total_seconds = time_until_next_hexagram_change
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_minutes = int(line_total_seconds // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 3600:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} h, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level 3 changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                    if constants.previous_hexagrams.get(f'level_{level}') != hexagram_number and constants.PLAY_AUDIO_LEVEL_3_ENABLED:
                        constants.previous_hexagrams[f'level_{level}'] = hexagram_number
                        self.sound_manager.play_level_sound(3)
                    if constants.previous_hexagrams.get(f'level_{level}_line') != moving_line and constants.PLAY_AUDIO_LEVEL_3_LINE_ENABLED:
                        constants.previous_hexagrams[f'level_{level}_line'] = moving_line
                        self.sound_manager.play_line_sound(3)
                elif level == 4:
                    total_seconds = time_until_next_hexagram_change
                    days = int(total_seconds // 86400)
                    hours = int((total_seconds % 86400) // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{days:02d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_days = int(line_total_seconds // 86400)
                    line_hours = int((line_total_seconds % 86400) // 3600)
                    line_minutes = int((line_total_seconds % 3600) // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_days:02d}d {line_hours:02d}:{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level {level} changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                    if constants.previous_hexagrams.get(f'level_{level}') != hexagram_number and constants.PLAY_AUDIO_LEVEL_4_ENABLED:
                        constants.previous_hexagrams[f'level_{level}'] = hexagram_number
                        self.sound_manager.play_level_sound(4)
                    if constants.previous_hexagrams.get(f'level_{level}_line') != moving_line and constants.PLAY_AUDIO_LEVEL_4_LINE_ENABLED:
                        constants.previous_hexagrams[f'level_{level}_line'] = moving_line
                        self.sound_manager.play_line_sound(4)
                elif level == 5:
                    total_seconds = time_until_next_hexagram_change
                    days = int(total_seconds // 86400)
                    hours = int((total_seconds % 86400) // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{days:02d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_days = int(line_total_seconds // 86400)
                    line_hours = int((line_total_seconds % 86400) // 3600)
                    line_minutes = int((line_total_seconds % 3600) // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_days:02d}d {line_hours:02d}:{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level {level} changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                    if constants.previous_hexagrams.get(f'level_{level}') != hexagram_number and constants.PLAY_AUDIO_LEVEL_5_ENABLED:
                        constants.previous_hexagrams[f'level_{level}'] = hexagram_number
                        self.sound_manager.play_level_sound(5)
                    if constants.previous_hexagrams.get(f'level_{level}_line') != moving_line and constants.PLAY_AUDIO_LEVEL_5_LINE_ENABLED:
                        constants.previous_hexagrams[f'level_{level}_line'] = moving_line
                        self.sound_manager.play_line_sound(5)
                elif level == 6:
                    total_seconds = time_until_next_hexagram_change
                    days = int(total_seconds // 86400)
                    hours = int((total_seconds % 86400) // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{days:02d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_days = int(line_total_seconds // 86400)
                    line_hours = int((line_total_seconds % 86400) // 3600)
                    line_minutes = int((line_total_seconds % 3600) // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_days:02d}d {line_hours:02d}:{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level {level} changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                    # Store for VRChat sync
                    self.level6_moving_line_days = line_days
                    self.level6_moving_line_num = moving_line
                    if constants.previous_hexagrams.get(f'level_{level}') != hexagram_number and constants.PLAY_AUDIO_LEVEL_6_ENABLED:
                        constants.previous_hexagrams[f'level_{level}'] = hexagram_number
                        self.sound_manager.play_level_sound(6)
                    if constants.previous_hexagrams.get(f'level_{level}_line') != moving_line and constants.PLAY_AUDIO_LEVEL_6_LINE_ENABLED:
                        constants.previous_hexagrams[f'level_{level}_line'] = moving_line
                        self.sound_manager.play_line_sound(6)

        for i, line in enumerate(message_lines[:len(self.output_labels)]):
            if self.output_labels[i].cget("text") != line:
                self.output_labels[i].config(text=line)
        for i in range(len(message_lines), len(self.output_labels)):
            if self.output_labels[i].cget("text") != "":
                self.output_labels[i].config(text="")

    def update_check_display(self, hexagrams, time_to_zero, text_widget, input_datetime=None):
        message_lines = []
        if not hexagrams:
            message_lines.append("No hexagrams found for the specified date.")
        else:
            current_date = input_datetime.date() if input_datetime else datetime.datetime.now().date()
            current_time = input_datetime.time() if input_datetime else datetime.datetime.now().time()
            days_to_zero = round(time_to_zero.total_seconds() / 86400, 4)
            message_lines.append(f"Hexagrams for: {current_date} - {current_time}")
            message_lines.append(f"Days to 0: {days_to_zero}")
            message_lines.append(f"Zero Date: {constants.ZERO_DATETIME}")
            
            for level, cycle_length, _, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
                moving_line = int((time_since_last_change // (cycle_length.total_seconds() / 6)) + 1)
                time_until_next_hexagram_change = time_since_last_change % cycle_length.total_seconds()
                line_change_interval = cycle_length.total_seconds() / 6
                time_until_next_line_change = time_since_last_change % line_change_interval
                
                if level == 1:
                    milliseconds = int(time_until_next_hexagram_change * 1000)
                    hex_timer = f"{milliseconds:03d}ms"
                    line_milliseconds = int(time_until_next_line_change * 1000)
                    line_timer = f"{line_milliseconds:03d}ms"
                    message_lines.append(f"Level {level}: {cycle_length.total_seconds():.4f} s, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level 1 changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                elif level == 2:
                    seconds = int(time_until_next_hexagram_change)
                    hex_timer = f"{seconds:02d}s"
                    line_seconds = int(time_until_next_line_change)
                    line_timer = f"{line_seconds:02d}s"
                    message_lines.append(f"Level {level}: {cycle_length.total_seconds()} s, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level 2 changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                elif level == 3:
                    total_seconds = time_until_next_hexagram_change
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_minutes = int(line_total_seconds // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 3600:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} h, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level 3 changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                elif level == 4:
                    total_seconds = time_until_next_hexagram_change
                    days = int(total_seconds // 86400)
                    hours = int((total_seconds % 86400) // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{days:02d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_days = int(line_total_seconds // 86400)
                    line_hours = int((line_total_seconds % 86400) // 3600)
                    line_minutes = int((line_total_seconds % 3600) // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_days:02d}d {line_hours:02d}:{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level {level} changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                elif level == 5:
                    total_seconds = time_until_next_hexagram_change
                    days = int(total_seconds // 86400)
                    hours = int((total_seconds % 86400) // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{days:02d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_days = int(line_total_seconds // 86400)
                    line_hours = int((line_total_seconds % 86400) // 3600)
                    line_minutes = int((line_total_seconds % 3600) // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_days:02d}d {line_hours:02d}:{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level {level} changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
                elif level == 6:
                    total_seconds = time_until_next_hexagram_change
                    days = int(total_seconds // 86400)
                    hours = int((total_seconds % 86400) // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    hex_timer = f"{days:02d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
                    line_total_seconds = time_until_next_line_change
                    line_days = int(line_total_seconds // 86400)
                    line_hours = int((line_total_seconds % 86400) // 3600)
                    line_minutes = int((line_total_seconds % 3600) // 60)
                    line_seconds = int(line_total_seconds % 60)
                    line_timer = f"{line_days:02d}d {line_hours:02d}:{line_minutes:02d}:{line_seconds:02d}"
                    cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
                    message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
                    message_lines.append(f"Level {level} changes in: {hex_timer}")
                    message_lines.append(f"Level {level}: Moving Line = ({moving_line}) Changes in: {line_timer}")
        
        text_widget.configure(state='normal')
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "\n".join(message_lines) + "\n")
        text_widget.configure(state='disabled')
        text_widget.see(tk.END)

    def toggle_send_to_vrchat(self):
        constants.SEND_TO_VRCHAT_ENABLED = not constants.SEND_TO_VRCHAT_ENABLED
        self.send_to_vrchat_button.config(
            text="Send to VRChat: ON" if constants.SEND_TO_VRCHAT_ENABLED else "Send to VRChat: OFF"
        )

    def toggle_page(self):
        constants.CURRENT_PAGE = 2 if constants.CURRENT_PAGE == 1 else 1
        self.page_button.config(text=f"Page {constants.CURRENT_PAGE}")

    def update_zero_datetime(self):
        try:
            date_str = self.zero_date_entry.get()
            new_datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            constants.ZERO_DATETIME = datetime.datetime(new_datetime.year, new_datetime.month, new_datetime.day)
            current_datetime = datetime.datetime.now()
            time_to_zero = constants.ZERO_DATETIME - current_datetime
            hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
            for level in range(1, 7):
                for hexagram in hexagrams:
                    if hexagram[0] == level:
                        constants.previous_hexagrams[f'level_{level}'] = hexagram[3]
                        moving_line = int((hexagram[5] // (hexagram[1].total_seconds() / 6)) + 1)
                        constants.previous_hexagrams[f'level_{level}_line'] = moving_line
            self.audio_playback_allowed = False
            self.update_display(hexagrams, time_to_zero)
            self.root.after(100, self.enable_audio_playback)
        except ValueError:
            print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")

    def check_hexagrams(self):
        date_str = self.date_entry.get()
        time_str = self.time_entry.get()
        try:
            input_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
            time_to_zero = constants.ZERO_DATETIME - input_datetime
            hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
            for hexagram in hexagrams:
                level, _, _, hexagram_number, _, _ = hexagram
                image = self.load_hexagram_image(hexagram_number)
                if image and level in self.check_hexagram_labels:
                    self.check_hexagram_labels[level].configure(image=image)
                    self.check_hexagram_labels[level].image = image
            self.update_display(hexagrams, time_to_zero, self.check_text, input_datetime)
        except ValueError:
            self.check_text.configure(state='normal')
            self.check_text.delete("1.0", tk.END)
            self.check_text.insert(tk.END, "Invalid date or time format.\nPlease enter date as YYYY-MM-DD and time as HH:MM:SS.")
            self.check_text.configure(state='disabled')
            for level in range(1, 7):
                if level in self.check_hexagram_labels:
                    self.check_hexagram_labels[level].configure(image='')

    def enable_audio_playback(self):
        self.audio_playback_allowed = True

    def open_calculator(self):
        if self.calculator_window and tk.Toplevel.winfo_exists(self.calculator_window):
            self.calculator_window.lift()
            return

        def calculate_date():
            try:
                input_date = datetime.datetime.strptime(date_entry.get(), "%Y-%m-%d")
                years_to_add = 67
                days_in_years = years_to_add * 365
                days_to_add = 104
                fractional_days = 0.25
                seconds_to_add = int(math.ceil(fractional_days * 24 * 3600))
                new_date = input_date + datetime.timedelta(days=days_in_years + days_to_add, seconds=seconds_to_add)
                result_label.config(text="The new zero date is:")
                result_entry.config(state="normal")
                result_entry.delete(0, tk.END)
                result_entry.insert(0, new_date.strftime('%Y-%m-%d'))
                result_entry.config(state="readonly")
            except ValueError:
                result_label.config(text="Invalid date format. Please enter a date in YYYY-MM-DD format.")
                result_entry.config(state="normal")
                result_entry.delete(0, tk.END)
                result_entry.config(state="readonly")

        self.calculator_window = tk.Toplevel(self.root)
        self.calculator_window.title("Zero Date Calculator 1.1")
        self.calculator_window.configure(background=constants.DARK_THEME['background'])
        
        frame = ttk.Frame(self.calculator_window)
        frame.pack(padx=20, pady=20)

        description_label = ttk.Label(frame, text="This program will add 67 years and 104.25 days to the entered date")
        description_label.pack(pady=10)

        date_label = ttk.Label(frame, text="Enter a date (YYYY-MM-DD):")
        date_label.pack(pady=5)
        date_entry = ttk.Entry(frame)
        date_entry.pack(pady=5)

        calculate_button = ttk.Button(frame, text="Calculate", command=calculate_date)
        calculate_button.pack(pady=10)

        result_label = ttk.Label(frame, text="")
        result_label.pack(pady=5)
        result_entry = ttk.Entry(frame, state="readonly")
        result_entry.pack(pady=5)

    def open_sound_menu(self):
        if self.sound_menu_window and tk.Toplevel.winfo_exists(self.sound_menu_window):
            self.sound_menu_window.lift()
            return

        self.sound_menu_window = tk.Toplevel(self.root)
        self.sound_menu_window.title("Sound Menu")
        self.sound_menu_window.configure(background=constants.DARK_THEME['background'])

        for level in range(1, 7):
            level_enabled = getattr(constants, f'PLAY_AUDIO_LEVEL_{level}_ENABLED')
            level_button = ttk.Button(
                self.sound_menu_window,
                text=f"Play Audio Level {level}: {'ON' if level_enabled else 'OFF'}",
                command=lambda l=level: self.toggle_level_sound(l)
            )
            level_button.grid(row=level-1, column=0, padx=10, pady=5, sticky="e")
            setattr(self, f'level_{level}_button', level_button)

            line_enabled = getattr(constants, f'PLAY_AUDIO_LEVEL_{level}_LINE_ENABLED')
            line_button = ttk.Button(
                self.sound_menu_window,
                text=f"Level {level} Moving Line Audio: {'ON' if line_enabled else 'OFF'}",
                command=lambda l=level: self.toggle_line_sound(l)
            )
            line_button.grid(row=level-1, column=1, padx=10, pady=5, sticky="e")
            setattr(self, f'level_{level}_line_button', line_button)

    def toggle_level_sound(self, level):
        attr_name = f'PLAY_AUDIO_LEVEL_{level}_ENABLED'
        current_state = getattr(constants, attr_name)
        setattr(constants, attr_name, not current_state)
        button = getattr(self, f'level_{level}_button')
        button.config(text=f"Play Audio Level {level}: {'ON' if not current_state else 'OFF'}")

    def toggle_line_sound(self, level):
        attr_name = f'PLAY_AUDIO_LEVEL_{level}_LINE_ENABLED'
        current_state = getattr(constants, attr_name)
        setattr(constants, attr_name, not current_state)
        button = getattr(self, f'level_{level}_line_button')
        button.config(text=f"Level {level} Moving Line Audio: {'ON' if not current_state else 'OFF'}")

    def run(self):
        self.root.mainloop()

    def cleanup(self):
        """
        Gracefully destroy the Tkinter root window and perform any additional cleanup if needed.
        """
        if self.root:
            self.root.destroy()