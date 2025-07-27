from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
import math
import base64
import io
from PIL import Image as PILImage

class CalculatorScreen(MDScreen):
    """প্রথম স্ক্রিন - ক্যালকুলেটর"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "calculator"
        
        # ক্যালকুলেটর ভেরিয়েবল
        self.current_input = ""
        self.operator = ""
        self.first_number = 0
        self.waiting_for_operand = False
        self.history = []
        
        self.build_calculator()
    
    def build_calculator(self):
        """ক্যালকুলেটর UI তৈরি করা"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            adaptive_height=True,
            padding="20dp"
        )
        
        # টপ অ্যাপ বার
        toolbar = MDTopAppBar(
            title="উন্নত ক্যালকুলেটর",
            right_action_items=[
                ["arrow-right", lambda x: self.go_to_image_screen()]
            ]
        )
        main_layout.add_widget(toolbar)
        
        # ডিসপ্লে
        self.display = MDTextField(
            text="0",
            font_size="24sp",
            readonly=True,
            multiline=False,
            size_hint_y=None,
            height="60dp"
        )
        main_layout.add_widget(self.display)
        
        # বাটন গ্রিড
        button_grid = MDGridLayout(
            cols=4,
            spacing="5dp",
            size_hint_y=None,
            height="400dp"
        )
        
        # বাটন তালিকা
        buttons = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "√"],
            ["sin", "cos", "tan", "log"],
            ["x²", "x³", "xʸ", "ln"]
        ]
        
        for row in buttons:
            for button_text in row:
                btn = MDRaisedButton(
                    text=button_text,
                    size_hint=(None, None),
                    size=("80dp", "50dp"),
                    on_release=lambda x, text=button_text: self.button_pressed(text)
                )
                
                # বাটনের রঙ সেট করা
                if button_text in ["C", "±", "%", "÷", "×", "-", "+", "="]:
                    btn.md_bg_color = (1, 0.6, 0, 1)  # কমলা
                elif button_text in ["√", "sin", "cos", "tan", "log", "x²", "x³", "xʸ", "ln"]:
                    btn.md_bg_color = (0.7, 0.7, 0.7, 1)  # ধূসর
                else:
                    btn.md_bg_color = (0.2, 0.2, 0.2, 1)  # গাঢ় ধূসর
                
                button_grid.add_widget(btn)
        
        main_layout.add_widget(button_grid)
        
        # ইতিহাস
        history_label = MDLabel(
            text="সাম্প্রতিক গণনা:",
            size_hint_y=None,
            height="30dp",
            theme_text_color="Primary"
        )
        main_layout.add_widget(history_label)
        
        # ইতিহাস স্ক্রল ভিউ
        scroll = MDScrollView(size_hint_y=None, height="100dp")
        self.history_label = MDLabel(
            text="",
            text_size=(None, None),
            halign="left",
            theme_text_color="Secondary"
        )
        scroll.add_widget(self.history_label)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def button_pressed(self, value):
        """বাটন প্রেস হ্যান্ডলার"""
        current = self.display.text
        
        if value == "C":
            self.display.text = "0"
            self.current_input = ""
            self.operator = ""
            self.first_number = 0
            self.waiting_for_operand = False
            
        elif value == "=":
            try:
                if self.operator and not self.waiting_for_operand:
                    second_number = float(current)
                    result = self.calculate(self.first_number, second_number, self.operator)
                    self.display.text = str(result)
                    self.add_to_history(f"{self.first_number} {self.operator} {second_number} = {result}")
                    self.operator = ""
                    self.waiting_for_operand = True
            except:
                self.display.text = "Error"
                
        elif value in ["+", "-", "×", "÷"]:
            if not self.waiting_for_operand and self.operator:
                # চেইন ক্যালকুলেশন
                second_number = float(current)
                result = self.calculate(self.first_number, second_number, self.operator)
                self.display.text = str(result)
                self.first_number = result
            else:
                self.first_number = float(current)
            
            self.operator = value
            self.waiting_for_operand = True
            
        elif value == "√":
            try:
                number = float(current)
                if number >= 0:
                    result = math.sqrt(number)
                    self.display.text = str(result)
                    self.add_to_history(f"√{number} = {result}")
                else:
                    self.display.text = "Error"
            except:
                self.display.text = "Error"
                
        elif value in ["sin", "cos", "tan"]:
            try:
                number = float(current)
                radians = math.radians(number)
                if value == "sin":
                    result = math.sin(radians)
                elif value == "cos":
                    result = math.cos(radians)
                else:  # tan
                    result = math.tan(radians)
                
                self.display.text = str(round(result, 10))
                self.add_to_history(f"{value}({number}°) = {round(result, 10)}")
            except:
                self.display.text = "Error"
                
        elif value == "log":
            try:
                number = float(current)
                if number > 0:
                    result = math.log10(number)
                    self.display.text = str(result)
                    self.add_to_history(f"log({number}) = {result}")
                else:
                    self.display.text = "Error"
            except:
                self.display.text = "Error"
                
        elif value == "ln":
            try:
                number = float(current)
                if number > 0:
                    result = math.log(number)
                    self.display.text = str(result)
                    self.add_to_history(f"ln({number}) = {result}")
                else:
                    self.display.text = "Error"
            except:
                self.display.text = "Error"
                
        elif value == "x²":
            try:
                number = float(current)
                result = number ** 2
                self.display.text = str(result)
                self.add_to_history(f"{number}² = {result}")
            except:
                self.display.text = "Error"
                
        elif value == "x³":
            try:
                number = float(current)
                result = number ** 3
                self.display.text = str(result)
                self.add_to_history(f"{number}³ = {result}")
            except:
                self.display.text = "Error"
                
        elif value == "xʸ":
            # পাওয়ার অপারেশনের জন্য
            self.first_number = float(current)
            self.operator = "**"
            self.waiting_for_operand = True
            
        elif value == "±":
            try:
                number = float(current)
                result = -number
                self.display.text = str(result)
            except:
                pass
                
        elif value == "%":
            try:
                number = float(current)
                result = number / 100
                self.display.text = str(result)
            except:
                self.display.text = "Error"
                
        else:  # সংখ্যা এবং দশমিক বিন্দু
            if self.waiting_for_operand:
                self.display.text = value if value != "." else "0."
                self.waiting_for_operand = False
            else:
                if current == "0" and value != ".":
                    self.display.text = value
                else:
                    if value == "." and "." in current:
                        return  # একাধিক দশমিক বিন্দু প্রতিরোধ
                    self.display.text = current + value
    
    def calculate(self, first, second, operator):
        """গণনা করা"""
        if operator == "+":
            return first + second
        elif operator == "-":
            return first - second
        elif operator == "×":
            return first * second
        elif operator == "÷":
            if second != 0:
                return first / second
            else:
                raise ValueError("Division by zero")
        elif operator == "**":
            return first ** second
    
    def add_to_history(self, calculation):
        """ইতিহাসে যোগ করা"""
        self.history.append(calculation)
        if len(self.history) > 10:  # সর্বোচ্চ ১০টি এন্ট্রি রাখা
            self.history.pop(0)
        
        self.history_label.text = "\n".join(self.history)
    
    def go_to_image_screen(self):
        """দ্বিতীয় স্ক্রিনে যাওয়া"""
        self.manager.current = "image"


class ImageScreen(MDScreen):
    """দ্বিতীয় স্ক্রিন - ছবি এবং তারিখ"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "image"
        self.build_image_screen()
    
    def build_image_screen(self):
        """ইমেজ স্ক্রিন UI তৈরি করা"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp"
        )
        
        # টপ অ্যাপ বার
        toolbar = MDTopAppBar(
            title="ছবি ও তারিখ",
            left_action_items=[
                ["arrow-left", lambda x: self.go_to_calculator_screen()]
            ]
        )
        main_layout.add_widget(toolbar)
        
        # তারিখ লেবেল
        date_label = MDLabel(
            text="03/07/2025",
            font_style="Caption",
            theme_text_color="Secondary",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        main_layout.add_widget(date_label)
        
        # ইমেজ কার্ড
        image_card = MDCard(
            size_hint=(None, None),
            size=("300dp", "200dp"),
            pos_hint={"center_x": 0.5},
            elevation=3,
            padding="10dp"
        )
        
        # ইমেজ প্লেসহোল্ডার
        image_label = MDLabel(
            text="[একটি সুন্দর প্রাকৃতিক দৃশ্যের ছবি]",
            halign="center",
            theme_text_color="Secondary"
        )
        image_card.add_widget(image_label)
        
        main_layout.add_widget(image_card)
        
        # বিবরণ
        description_label = MDLabel(
            text="এটি একটি সুন্দর প্রাকৃতিক দৃশ্য",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(description_label)
        
        self.add_widget(main_layout)
    
    def go_to_calculator_screen(self):
        """ক্যালকুলেটর স্ক্রিনে ফিরে যাওয়া"""
        self.manager.current = "calculator"


class CalculatorApp(MDApp):
    """মূল অ্যাপ্লিকেশন ক্লাস"""
    
    def build(self):
        """অ্যাপ্লিকেশন তৈরি করা"""
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        # স্ক্রিন ম্যানেজার
        sm = MDScreenManager()
        
        # স্ক্রিন যোগ করা
        calculator_screen = CalculatorScreen()
        image_screen = ImageScreen()
        
        sm.add_widget(calculator_screen)
        sm.add_widget(image_screen)
        
        # প্রথম স্ক্রিন সেট করা
        sm.current = "calculator"
        
        return sm


if __name__ == "__main__":
    CalculatorApp().run()



