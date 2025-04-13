import sys
import json
import os
import requests
import io
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QLabel, QSlider, QCheckBox, QPushButton, QComboBox, 
                            QFrame, QGridLayout, QSpacerItem, QSizePolicy, QGroupBox, QStackedWidget)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QSize, QPoint, QByteArray
from PyQt5.QtGui import (QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush, QPen, 
                        QLinearGradient, QFontDatabase, QMovie, QCursor, QRadialGradient)
from PyQt5 import QtSvg

# Cores do tema
PURPLE_PRIMARY = "#6200ED"
PURPLE_LIGHT = "#7A1CF7"
PURPLE_DARK = "#5000C4"
DARK_BG = "#0A0A0A"
CARD_BG = "#121212"
BORDER_COLOR = "#222222"
TEXT_COLOR = "#FFFFFF"
TEXT_SECONDARY = "#AAAAAA"
DISABLED_COLOR = "#444444"
SUCCESS_COLOR = "#00C853"
ERROR_COLOR = "#FF3D00"

# Caminho para recursos
RESOURCES_PATH = "resources/"

class ResourceManager:
    @staticmethod
    def ensure_resources_dir():
        if not os.path.exists(RESOURCES_PATH):
            os.makedirs(RESOURCES_PATH)
    
    @staticmethod
    def download_resource(url, filename):
        ResourceManager.ensure_resources_dir()
        filepath = os.path.join(RESOURCES_PATH, filename)
        
        if not os.path.exists(filepath):
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"Downloaded: {filename}")
                return filepath
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                return None
        return filepath
    
    @staticmethod
    def load_font(url, family_name, filename):
        filepath = ResourceManager.download_resource(url, filename)
        if filepath:
            font_id = QFontDatabase.addApplicationFont(filepath)
            if font_id != -1:
                print(f"Font loaded: {family_name}")
                return QFontDatabase.applicationFontFamilies(font_id)[0]
        return None

    @staticmethod
    def download_icons():
        icons = {
            "aimbot": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/crosshair.svg",
            "slots": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/grid.svg",
            "silent": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/target.svg",
            "visual": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/eye.svg",
            "extra": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/settings.svg",
            "profile": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/user.svg",
            "advanced": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/cpu.svg",
            "check": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/check.svg",
            "refresh": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/refresh-cw.svg",
            "online": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/zap.svg",
            "logo": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/hexagon.svg"
        }
        
        for name, url in icons.items():
            ResourceManager.download_resource(url, f"{name}.svg")

class StyleHelper:
    @staticmethod
    def get_slider_style():
        return """
        QSlider::groove:horizontal {
            border: 1px solid #333333;
            height: 4px;
            background: #333333;
            margin: 2px 0;
            border-radius: 2px;
        }

        QSlider::handle:horizontal {
            background: """ + PURPLE_PRIMARY + """;
            border: 1px solid """ + PURPLE_PRIMARY + """;
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 8px;
        }

        QSlider::sub-page:horizontal {
            background: """ + PURPLE_PRIMARY + """;
            border-radius: 2px;
        }
        """
    
    @staticmethod
    def get_checkbox_style():
        return """
        QCheckBox {
            color: """ + TEXT_COLOR + """;
            font-family: 'Poppins';
            font-weight: 500;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid #555555;
            background: #222222;
        }
        
        QCheckBox::indicator:checked {
            background: """ + PURPLE_PRIMARY + """;
            border: 1px solid """ + PURPLE_PRIMARY + """;
        }
        """
    
    @staticmethod
    def get_button_style():
        return """
        QPushButton {
            background-color: """ + PURPLE_PRIMARY + """;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-family: 'Poppins';
            font-weight: 600;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background-color: """ + PURPLE_LIGHT + """;
        }
        
        QPushButton:pressed {
            background-color: """ + PURPLE_DARK + """;
        }
        
        QPushButton:disabled {
            background-color: #444444;
            color: #888888;
        }
        """
    
    @staticmethod
    def get_keybind_button_style():
        return """
        QPushButton {
            background-color: #222222;
            color: white;
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 4px 8px;
            font-family: 'Poppins';
            font-weight: 500;
            font-size: 12px;
            min-width: 60px;
            text-align: center;
        }
        
        QPushButton:hover {
            background-color: #333333;
            border: 1px solid #444444;
        }
        
        QPushButton:focus {
            border: 1px solid """ + PURPLE_PRIMARY + """;
        }
        """
    
    @staticmethod
    def get_combobox_style():
        return """
        QComboBox {
            background-color: #222222;
            color: white;
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 4px 8px;
            min-width: 6em;
            font-family: 'Poppins';
            font-weight: 500;
            font-size: 12px;
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #444444;
        }
        
        QComboBox QAbstractItemView {
            background-color: #222222;
            color: white;
            selection-background-color: """ + PURPLE_PRIMARY + """;
            border: 1px solid #333333;
            border-radius: 0px;
        }
        """
    
    @staticmethod
    def get_tab_style():
        return """
        QTabWidget::pane {
            border: 1px solid #222222;
            background: """ + CARD_BG + """;
            border-radius: 8px;
            top: -1px;
        }
        
        QTabBar::tab {
            background: #181818;
            color: #888888;
            padding: 8px 12px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-family: 'Poppins';
            font-weight: 500;
            font-size: 12px;
        }
        
        QTabBar::tab:selected {
            background: """ + PURPLE_PRIMARY + """;
            color: white;
        }
        
        QTabBar::tab:hover:!selected {
            background: #222222;
            color: white;
        }
        """
    
    @staticmethod
    def get_separator_style():
        return """
        QFrame[frameShape="4"] {
            color: #222222;
            height: 1px;
        }
        """
    
    @staticmethod
    def get_label_style():
        return """
        QLabel {
            color: """ + TEXT_COLOR + """;
            font-family: 'Poppins';
            font-weight: 500;
            font-size: 13px;
        }
        """
    
    @staticmethod
    def get_value_label_style():
        return """
        QLabel {
            color: """ + TEXT_SECONDARY + """;
            font-family: 'Poppins';
            font-weight: 500;
            font-size: 12px;
        }
        """
    
    @staticmethod
    def get_title_label_style():
        return """
        QLabel {
            color: """ + PURPLE_PRIMARY + """;
            font-family: 'Poppins';
            font-weight: 600;
            font-size: 14px;
        }
        """
    
    @staticmethod
    def get_card_style():
        return """
        QWidget {
            background-color: """ + CARD_BG + """;
            border-radius: 8px;
            border: 1px solid #222222;
        }
        """
    
    @staticmethod
    def get_badge_style(color=PURPLE_PRIMARY):
        return f"""
        QLabel {{
            background-color: {color}33;
            color: {color};
            border: 1px solid {color}66;
            border-radius: 10px;
            padding: 2px 8px;
            font-family: 'Poppins';
            font-weight: 500;
            font-size: 11px;
        }}
        """

class AnimatedToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(38, 22)
        self._bg_color = QColor(DISABLED_COLOR)
        self._circle_color = QColor(TEXT_COLOR)
        self._active_color = QColor(PURPLE_PRIMARY)
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, QByteArray(b"circle_position"), self)
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.stateChanged.connect(self.start_transition)
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def get_circle_position(self):
        return self._circle_position
    
    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    circle_position = pyqtSignal(int)
    
    def start_transition(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 19)
        else:
            self.animation.setEndValue(3)
        self.animation.start()
    
    def hitButton(self, pos):
        return self.contentsRect().contains(pos)
    
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        if self.isChecked():
            p.setBrush(QBrush(self._active_color))
        else:
            p.setBrush(QBrush(self._bg_color))
        
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)
        
        # Draw circle
        p.setBrush(QBrush(self._circle_color))
        p.drawEllipse(self._circle_position, 3, 16, 16)

class KeybindButton(QPushButton):
    keybind_changed = pyqtSignal(str)
    
    def __init__(self, keybind="None", parent=None):
        super().__init__(keybind, parent)
        self.keybind = keybind
        self.listening = False
        self.setStyleSheet(StyleHelper.get_keybind_button_style())
        self.clicked.connect(self.start_listening)
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def start_listening(self):
        self.listening = True
        self.setText("Press Key...")
        self.setFocus()
    
    def keyPressEvent(self, event):
        if self.listening:
            key_text = event.text().upper()
            if key_text:
                self.keybind = key_text
            else:
                key = event.key()
                if key == Qt.Key_Escape:
                    self.keybind = "ESC"
                elif key == Qt.Key_Return or key == Qt.Key_Enter:
                    self.keybind = "ENTER"
                elif key == Qt.Key_Control:
                    self.keybind = "CTRL"
                elif key == Qt.Key_Alt:
                    self.keybind = "ALT"
                elif key == Qt.Key_Shift:
                    self.keybind = "SHIFT"
                elif key == Qt.Key_Tab:
                    self.keybind = "TAB"
                elif key == Qt.Key_Space:
                    self.keybind = "SPACE"
                elif key == Qt.Key_F1:
                    self.keybind = "F1"
                elif key == Qt.Key_F2:
                    self.keybind = "F2"
                elif key == Qt.Key_F3:
                    self.keybind = "F3"
                elif key == Qt.Key_F4:
                    self.keybind = "F4"
                elif key == Qt.Key_F5:
                    self.keybind = "F5"
                elif key == Qt.Key_F6:
                    self.keybind = "F6"
                elif key == Qt.Key_F7:
                    self.keybind = "F7"
                elif key == Qt.Key_F8:
                    self.keybind = "F8"
                elif key == Qt.Key_F9:
                    self.keybind = "F9"
                elif key == Qt.Key_F10:
                    self.keybind = "F10"
                elif key == Qt.Key_F11:
                    self.keybind = "F11"
                elif key == Qt.Key_F12:
                    self.keybind = "F12"
                elif key == Qt.Key_Insert:
                    self.keybind = "INS"
                elif key == Qt.Key_Delete:
                    self.keybind = "DEL"
                elif key == Qt.Key_Home:
                    self.keybind = "HOME"
                elif key == Qt.Key_End:
                    self.keybind = "END"
                elif key == Qt.Key_PageUp:
                    self.keybind = "PGUP"
                elif key == Qt.Key_PageDown:
                    self.keybind = "PGDN"
                elif key == Qt.Key_Left:
                    self.keybind = "LEFT"
                elif key == Qt.Key_Right:
                    self.keybind = "RIGHT"
                elif key == Qt.Key_Up:
                    self.keybind = "UP"
                elif key == Qt.Key_Down:
                    self.keybind = "DOWN"
                elif key == Qt.Key_Backspace:
                    self.keybind = "BKSP"
                elif key == Qt.Key_CapsLock:
                    self.keybind = "CAPS"
                elif key == Qt.Key_NumLock:
                    self.keybind = "NUMLK"
                elif key == Qt.Key_ScrollLock:
                    self.keybind = "SCRLK"
                else:
                    self.keybind = f"KEY_{key}"
            
            self.setText(self.keybind)
            self.listening = False
            self.keybind_changed.emit(self.keybind)
            
    def get_keybind(self):
        return self.keybind
    
    def set_keybind(self, keybind):
        self.keybind = keybind
        self.setText(keybind)

class LabeledSlider(QWidget):
    valueChanged = pyqtSignal(int)
    
    def __init__(self, title, min_val, max_val, value, parent=None, step=1, suffix=""):
        super().__init__(parent)
        self.title = title
        self.suffix = suffix
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(StyleHelper.get_label_style())
        
        self.value_label = QLabel(f"{value}{suffix}")
        self.value_label.setStyleSheet(StyleHelper.get_value_label_style())
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.value_label)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setValue(value)
        self.slider.setSingleStep(step)
        self.slider.setStyleSheet(StyleHelper.get_slider_style())
        self.slider.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.slider.valueChanged.connect(self.on_value_changed)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.slider)
    
    def on_value_changed(self, value):
        self.value_label.setText(f"{value}{self.suffix}")
        self.valueChanged.emit(value)
    
    def value(self):
        return self.slider.value()
    
    def setValue(self, value):
        self.slider.setValue(value)

class IconLabel(QWidget):
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        self.icon = QtSvg.QSvgWidget(icon_path)
        self.icon.setFixedSize(16, 16)
        
        self.label = QLabel(text)
        self.label.setStyleSheet(StyleHelper.get_label_style())
        
        layout.addWidget(self.icon)
        layout.addWidget(self.label)

class TabButton(QPushButton):
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)
        
        self.icon = QtSvg.QSvgWidget(icon_path)
        self.icon.setFixedSize(20, 20)
        
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #888888; font-family: 'Poppins'; font-weight: 500; font-size: 11px;")
        
        layout.addWidget(self.icon, 0, Qt.AlignCenter)
        layout.addWidget(self.label, 0, Qt.AlignCenter)
        
        self.setFixedSize(70, 70)
        self.setStyleSheet("""
            QPushButton {
                background-color: #181818;
                border: none;
                border-radius: 8px;
            }
            
            QPushButton:checked {
                background-color: """ + PURPLE_PRIMARY + """;
            }
            
            QPushButton:checked QLabel {
                color: white;
            }
            
            QPushButton:hover:!checked {
                background-color: #222222;
            }
            
            QPushButton:hover:!checked QLabel {
                color: white;
            }
        """)

class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_direction = Qt.Horizontal
        self.m_speed = 300
        self.m_animationtype = QEasingCurve.OutCubic
        self.m_now = 0
        self.m_next = 0
        self.m_wrap = False
        self.m_pnow = QPoint(0, 0)
        self.m_active = False
    
    def setDirection(self, direction):
        self.m_direction = direction
    
    def setSpeed(self, speed):
        self.m_speed = speed
    
    def setAnimation(self, animationtype):
        self.m_animationtype = animationtype
    
    def setWrap(self, wrap):
        self.m_wrap = wrap
    
    def slideInNext(self):
        self.slideInIdx(self.currentIndex() + 1)
    
    def slideInPrev(self):
        self.slideInIdx(self.currentIndex() - 1)
    
    def slideInIdx(self, idx, direction=None):
        if self.m_active:
            return
        
        self.m_active = True
        
        if direction is None:
            direction = self.m_direction
        
        idx = idx % self.count()
        
        if idx == self.currentIndex():
            self.m_active = False
            return
        
        self.m_next = idx
        
        if self.m_now == self.m_next:
            self.m_active = False
            return
        
        offsetx, offsety = self.frameRect().width(), self.frameRect().height()
        self.widget(self.m_next).setGeometry(self.frameRect())
        
        if direction == Qt.Horizontal:
            if self.m_now < self.m_next:
                offsetx = offsetx
                offsety = 0
            else:
                offsetx = -offsetx
                offsety = 0
        else:
            if self.m_now < self.m_next:
                offsetx = 0
                offsety = offsety
            else:
                offsetx = 0
                offsety = -offsety
        
        pnext = self.widget(self.m_next).pos()
        pnow = self.widget(self.m_now).pos()
        self.m_pnow = pnow
        
        self.widget(self.m_next).move(pnext.x() - offsetx, pnext.y() - offsety)
        self.widget(self.m_next).show()
        self.widget(self.m_next).raise_()
        
        anim_group = QPropertyAnimation(self.widget(self.m_next), b"pos")
        anim_group.setDuration(self.m_speed)
        anim_group.setStartValue(QPoint(pnext.x() - offsetx, pnext.y() - offsety))
        anim_group.setEndValue(QPoint(pnext.x(), pnext.y()))
        anim_group.setEasingCurve(self.m_animationtype)
        
        anim_group_now = QPropertyAnimation(self.widget(self.m_now), b"pos")
        anim_group_now.setDuration(self.m_speed)
        anim_group_now.setStartValue(QPoint(pnow.x(), pnow.y()))
        anim_group_now.setEndValue(QPoint(pnow.x() + offsetx, pnow.y() + offsety))
        anim_group_now.setEasingCurve(self.m_animationtype)
        
        anim_group.start()
        anim_group_now.start()
        
        anim_group.finished.connect(self.animationDoneSlot)
    
    def animationDoneSlot(self):
        self.setCurrentIndex(self.m_next)
        self.widget(self.m_now).hide()
        self.widget(self.m_now).move(self.m_pnow)
        self.m_now = self.m_next
        self.m_active = False

class EternityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ETERNITY SOFTWARES - FORTNITE | V2")
        self.setMinimumSize(900, 650)
        self.setStyleSheet(f"background-color: {DARK_BG}; color: {TEXT_COLOR};")
        
        # Carregar recursos
        self.load_resources()
        
        # Configurações padrão
        self.config = {
            # Aimbot
            "enableAim": False,
            "fovSize": 350,
            "confidence": 75,
            "aimSmooth": 80,
            "maxDetections": 1,
            "aimBone": "Head",
            "smoothingType": "Default",
            "controllerOn": False,
            "keybind": "RMB",
            "keybind2": "P",

            # Slots
            "enableSlots": False,
            "slot1": {"enabled": False, "fov": 800, "key": "1"},
            "slot2": {"enabled": False, "fov": 120, "key": "2"},
            "slot3": {"enabled": False, "fov": 800, "key": "3"},
            "slot4": {"enabled": False, "fov": 120, "key": "4"},
            "slot5": {"enabled": False, "fov": 800, "key": "5"},
            "slot6": {"key": "P"},

            # Silent Aim
            "enableFlickBot": False,
            "flickScopeSens": 50,
            "flickCooldown": 0.25,
            "flickDelay": 0.003,
            "flickbotKeybind": "MMB",

            # Visual
            "showFov": False,
            "showCrosshair": False,
            "showDetections": False,
            "showAimline": False,
            "showFPS": False,
            "useHue": False,
            "boxType": "Regular",

            # Extra
            "cupModeOn": False,
            "enableTriggerBot": False,
            "requireKeybind": False,
            "autoFireFovSize": 20,
            "autoFireConfidence": 60,
            "autoFireKeybind": "RMB",
            "reduceBloom": False,
            "antiRecoilOn": False,
            "requireADS": False,
            "antiRecoilStrength": 1,

            # Advanced
            "useModelClass": True,
            "imgValue": "640",
            "modelFPS": 165,
            "lastModel": "Fortnite.pt",
        }
        
        # Informações do usuário
        self.user_info = {
            "username": "user123*******",
            "purchased": "2 months ago",
            "expiry": "in 10 months",
            "lastLogin": "2 days ago",
        }
        
        self.init_ui()
        self.load_config()
        
        # Efeito de fade-in na inicialização
        self.setWindowOpacity(0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_in_animation.start()
    
    def load_resources(self):
        # Carregar fontes
        self.poppins_font = ResourceManager.load_font(
            "https://fonts.gstatic.com/s/poppins/v20/pxiEyp8kv8JHgFVrJJfecg.woff2",
            "Poppins",
            "poppins-regular.woff2"
        )
        
        self.poppins_medium = ResourceManager.load_font(
            "https://fonts.gstatic.com/s/poppins/v20/pxiByp8kv8JHgFVrLGT9Z1xlFQ.woff2",
            "Poppins Medium",
            "poppins-medium.woff2"
        )
        
        self.poppins_semibold = ResourceManager.load_font(
            "https://fonts.gstatic.com/s/poppins/v20/pxiByp8kv8JHgFVrLEj6Z1xlFQ.woff2",
            "Poppins SemiBold",
            "poppins-semibold.woff2"
        )
        
        self.poppins_bold = ResourceManager.load_font(
            "https://fonts.gstatic.com/s/poppins/v20/pxiByp8kv8JHgFVrLCz7Z1xlFQ.woff2",
            "Poppins Bold",
            "poppins-bold.woff2"
        )
        
        # Baixar ícones
        ResourceManager.download_icons()
    
    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Banner/Logo
        banner = QWidget()
        banner.setFixedHeight(70)
        banner.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5000c4, stop:1 #7a1cf7);
            border-radius: 10px;
        """)
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(15, 10, 15, 10)
        
        # Logo e título
        header_layout = QHBoxLayout()
        
        logo_icon = QtSvg.QSvgWidget(os.path.join(RESOURCES_PATH, "logo.svg"))
        logo_icon.setFixedSize(30, 30)
        logo_icon.setStyleSheet("background-color: transparent;")
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        
        banner_title = QLabel("ETERNITY SOFTWARES")
        banner_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; font-family: 'Poppins';")
        
        banner_subtitle = QLabel("FORTNITE | V2")
        banner_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 12px; font-family: 'Poppins';")
        
        title_layout.addWidget(banner_title)
        title_layout.addWidget(banner_subtitle)
        
        header_layout.addWidget(logo_icon)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        banner_layout.addLayout(header_layout)
        
        main_layout.addWidget(banner)
        
        # Área de navegação e conteúdo
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Navegação (botões de abas)
        nav_widget = QWidget()
        nav_widget.setFixedWidth(80)
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(10)
        nav_layout.setAlignment(Qt.AlignTop)
        
        # Botões de navegação
        self.tab_buttons = []
        
        aimbot_btn = TabButton(os.path.join(RESOURCES_PATH, "aimbot.svg"), "Aimbot")
        slots_btn = TabButton(os.path.join(RESOURCES_PATH, "slots.svg"), "Slots")
        silent_btn = TabButton(os.path.join(RESOURCES_PATH, "silent.svg"), "Silent")
        visual_btn = TabButton(os.path.join(RESOURCES_PATH, "visual.svg"), "Visual")
        extra_btn = TabButton(os.path.join(RESOURCES_PATH, "extra.svg"), "Extra")
        profile_btn = TabButton(os.path.join(RESOURCES_PATH, "profile.svg"), "Profile")
        advanced_btn = TabButton(os.path.join(RESOURCES_PATH, "advanced.svg"), "Model")
        
        self.tab_buttons = [aimbot_btn, slots_btn, silent_btn, visual_btn, extra_btn, profile_btn, advanced_btn]
        
        for btn in self.tab_buttons:
            nav_layout.addWidget(btn)
        
        # Conteúdo (páginas)
        self.content_stack = AnimatedStackedWidget()
        self.content_stack.setSpeed(300)
        
        # Criar páginas
        self.create_aimbot_page()
        self.create_slots_page()
        self.create_silent_aim_page()
        self.create_visual_page()
        self.create_extra_page()
        self.create_profile_page()
        self.create_advanced_page()
        
        # Conectar botões às páginas
        for i, btn in enumerate(self.tab_buttons):
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
        
        # Selecionar primeira aba por padrão
        aimbot_btn.setChecked(True)
        
        content_layout.addWidget(nav_widget)
        content_layout.addWidget(self.content_stack)
        
        main_layout.addLayout(content_layout)
        
        # Barra de status
        status_bar = QWidget()
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(5, 5, 5, 5)
        
        version_label = QLabel("Eternity Softwares v2.0")
        version_label.setStyleSheet("color: #666666; font-size: 11px; font-family: 'Poppins';")
        
        # Badge de status
        status_badge = QLabel()
        status_badge.setText("● Online")
        status_badge.setStyleSheet(StyleHelper.get_badge_style())
        
        # Ícone para o badge
        online_icon = QtSvg.QSvgWidget(os.path.join(RESOURCES_PATH, "online.svg"))
        online_icon.setFixedSize(12, 12)
        
        badge_layout = QHBoxLayout()
        badge_layout.setContentsMargins(0, 0, 0, 0)
        badge_layout.setSpacing(4)
        badge_layout.addWidget(online_icon)
        badge_layout.addWidget(QLabel("Online"))
        
        status_badge = QLabel()
        status_badge.setLayout(badge_layout)
        status_badge.setStyleSheet(StyleHelper.get_badge_style())
        
        status_layout.addWidget(version_label)
        status_layout.addStretch()
        status_layout.addWidget(status_badge)
        
        main_layout.addWidget(status_bar)
        
        self.setCentralWidget(central_widget)
    
    def switch_page(self, index):
        # Desmarcar todos os botões exceto o selecionado
        for i, btn in enumerate(self.tab_buttons):
            if i != index:
                btn.setChecked(False)
        
        # Animar a transição para a nova página
        self.content_stack.slideInIdx(index)
    
    def create_card_widget(self):
        card = QWidget()
        card.setStyleSheet(StyleHelper.get_card_style())
        return card
    
    def create_aimbot_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)
        
        # Card principal
        card = self.create_card_widget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # Switches
        toggle_layout = QHBoxLayout()
        toggle_layout.setSpacing(30)
        
        enable_aim_layout = QHBoxLayout()
        enable_aim_label = QLabel("Enable Aimbot")
        enable_aim_label.setStyleSheet(StyleHelper.get_label_style())
        enable_aim_toggle = AnimatedToggle()
        enable_aim_toggle.setChecked(self.config["enableAim"])
        enable_aim_toggle.stateChanged.connect(lambda state: self.update_config("enableAim", bool(state)))
        
        enable_aim_layout.addWidget(enable_aim_label)
        enable_aim_layout.addStretch()
        enable_aim_layout.addWidget(enable_aim_toggle)
        
        controller_layout = QHBoxLayout()
        controller_label = QLabel("Controller Support")
        controller_label.setStyleSheet(StyleHelper.get_label_style())
        controller_toggle = AnimatedToggle()
        controller_toggle.setChecked(self.config["controllerOn"])
        controller_toggle.stateChanged.connect(lambda state: self.update_config("controllerOn", bool(state)))
        
        controller_layout.addWidget(controller_label)
        controller_layout.addStretch()
        controller_layout.addWidget(controller_toggle)
        
        toggle_layout.addLayout(enable_aim_layout, 1)
        toggle_layout.addLayout(controller_layout, 1)
        
        # Keybinds
        keybind_layout = QHBoxLayout()
        keybind_label = QLabel("Keybinds:")
        keybind_label.setStyleSheet(StyleHelper.get_label_style())
        
        keybind1 = KeybindButton(self.config["keybind"])
        keybind1.keybind_changed.connect(lambda kb: self.update_config("keybind", kb))
        
        keybind2 = KeybindButton(self.config["keybind2"])
        keybind2.keybind_changed.connect(lambda kb: self.update_config("keybind2", kb))
        
        keybind_layout.addWidget(keybind_label)
        keybind_layout.addStretch()
        keybind_layout.addWidget(keybind1)
        keybind_layout.addWidget(keybind2)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(StyleHelper.get_separator_style())
        
        # Sliders
        fov_slider = LabeledSlider("FOV", 100, 700, self.config["fovSize"], step=10)
        fov_slider.valueChanged.connect(lambda val: self.update_config("fovSize", val))
        
        confidence_slider = LabeledSlider("Confidence", 40, 95, self.config["confidence"], suffix="%")
        confidence_slider.valueChanged.connect(lambda val: self.update_config("confidence", val))
        
        smooth_slider = LabeledSlider("Aimbot Strength", 5, 200, self.config["aimSmooth"], step=5)
        smooth_slider.valueChanged.connect(lambda val: self.update_config("aimSmooth", val))
        
        # Dropdowns
        dropdown_layout = QGridLayout()
        dropdown_layout.setHorizontalSpacing(20)
        dropdown_layout.setVerticalSpacing(10)
        
        aim_bone_label = QLabel("Aim Bone:")
        aim_bone_label.setStyleSheet(StyleHelper.get_label_style())
        aim_bone_combo = QComboBox()
        aim_bone_combo.addItems(["Head", "Neck", "Body"])
        aim_bone_combo.setCurrentText(self.config["aimBone"])
        aim_bone_combo.setStyleSheet(StyleHelper.get_combobox_style())
        aim_bone_combo.currentTextChanged.connect(lambda text: self.update_config("aimBone", text))
        aim_bone_combo.setCursor(QCursor(Qt.PointingHandCursor))
        
        smoothing_label = QLabel("Humanization:")
        smoothing_label.setStyleSheet(StyleHelper.get_label_style())
        smoothing_combo = QComboBox()
        smoothing_combo.addItems(["Default", "Bezier", "Catmull-Rom", "Hermite", "B-Spline", "Sine", "Exponential"])
        smoothing_combo.setCurrentText(self.config["smoothingType"])
        smoothing_combo.setStyleSheet(StyleHelper.get_combobox_style())
        smoothing_combo.currentTextChanged.connect(lambda text: self.update_config("smoothingType", text))
        smoothing_combo.setCursor(QCursor(Qt.PointingHandCursor))
        
        dropdown_layout.addWidget(aim_bone_label, 0, 0)
        dropdown_layout.addWidget(aim_bone_combo, 0, 1)
        dropdown_layout.addWidget(smoothing_label, 0, 2)
        dropdown_layout.addWidget(smoothing_combo, 0, 3)
        
        # Botão Refresh
        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet(StyleHelper.get_button_style())
        refresh_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Ícone de refresh
        refresh_icon = QtSvg.QSvgWidget(os.path.join(RESOURCES_PATH, "refresh.svg"))
        refresh_icon.setFixedSize(16, 16)
        
        refresh_text = QLabel("Refresh")
        refresh_text.setStyleSheet("color: white; font-family: 'Poppins'; font-weight: 600; font-size: 13px;")
        
        refresh_layout = QHBoxLayout()
        refresh_layout.setSpacing(8)
        refresh_layout.addStretch()
        refresh_layout.addWidget(refresh_icon)
        refresh_layout.addWidget(refresh_text)
        refresh_layout.addStretch()
        
        refresh_button.setLayout(refresh_layout)
        
        # Adicionar widgets ao layout
        card_layout.addLayout(toggle_layout)
        card_layout.addLayout(keybind_layout)
        card_layout.addWidget(separator)
        card_layout.addWidget(fov_slider)
        card_layout.addWidget(confidence_slider)
        card_layout.addWidget(smooth_slider)
        card_layout.addLayout(dropdown_layout)
        card_layout.addWidget(refresh_button)
        
        scroll_layout.addWidget(card)
        scroll_layout.addStretch()
        
        layout.addWidget(scroll_area)
        
        self.content_stack.addWidget(page)
    
    def create_slots_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)
        
        # Card principal
        card = self.create_card_widget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # Enable Slots
        enable_slots_layout = QHBoxLayout()
        enable_slots_label = QLabel("Enable Weapon Slots")
        enable_slots_label.setStyleSheet(StyleHelper.get_label_style())
        enable_slots_toggle = AnimatedToggle()
        enable_slots_toggle.setChecked(self.config["enableSlots"])
        enable_slots_toggle.stateChanged.connect(lambda state: self.update_config("enableSlots", bool(state)))
        
        enable_slots_layout.addWidget(enable_slots_label)
        enable_slots_layout.addStretch()
        enable_slots_layout.addWidget(enable_slots_toggle)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(StyleHelper.get_separator_style())
        
        card_layout.addLayout(enable_slots_layout)
        card_layout.addWidget(separator)
        
        # Slots 1-5
        for i in range(1, 6):
            slot_key = f"slot{i}"
            slot_layout = QHBoxLayout()
            slot_layout.setSpacing(10)
            
            slot_label = QLabel(f"Slot {i}")
            slot_label.setStyleSheet(StyleHelper.get_label_style())
            slot_label.setFixedWidth(50)
            
            key_button = KeybindButton(self.config[slot_key]["key"])
            key_button.setFixedWidth(60)
            key_button.keybind_changed.connect(lambda kb, s=slot_key: self.update_slot_config(s, "key", kb))
            
            fov_slider = QSlider(Qt.Horizontal)
            fov_slider.setMinimum(120)
            fov_slider.setMaximum(800)
            fov_slider.setValue(self.config[slot_key]["fov"])
            fov_slider.setStyleSheet(StyleHelper.get_slider_style())
            fov_slider.valueChanged.connect(lambda val, s=slot_key: self.update_slot_config(s, "fov", val))
            fov_slider.setCursor(QCursor(Qt.PointingHandCursor))
            
            fov_value = QLabel(f"FOV: {self.config[slot_key]['fov']}")
            fov_value.setStyleSheet(StyleHelper.get_value_label_style())
            fov_value.setFixedWidth(80)
            fov_slider.valueChanged.connect(lambda val, label=fov_value: label.setText(f"FOV: {val}"))
            
            enable_toggle = AnimatedToggle()
            enable_toggle.setChecked(self.config[slot_key]["enabled"])
            enable_toggle.stateChanged.connect(lambda state, s=slot_key: self.update_slot_config(s, "enabled", bool(state)))
            
            slot_layout.addWidget(slot_label)
            slot_layout.addWidget(key_button)
            slot_layout.addWidget(fov_slider)
            slot_layout.addWidget(fov_value)
            slot_layout.addWidget(enable_toggle)
            
            card_layout.addLayout(slot_layout)
        
        # Slot 6 (Pickaxe)
        pickaxe_layout = QHBoxLayout()
        
        pickaxe_label = QLabel("Pickaxe")
        pickaxe_label.setStyleSheet(StyleHelper.get_label_style())
        pickaxe_label.setFixedWidth(50)
        
        pickaxe_key = KeybindButton(self.config["slot6"]["key"])
        pickaxe_key.setFixedWidth(60)
        pickaxe_key.keybind_changed.connect(lambda kb: self.update_slot_config("slot6", "key", kb))
        
        pickaxe_layout.addWidget(pickaxe_label)
        pickaxe_layout.addWidget(pickaxe_key)
        pickaxe_layout.addStretch()
        
        card_layout.addLayout(pickaxe_layout)
        
        scroll_layout.addWidget(card)
        scroll_layout.addStretch()
        
        layout.addWidget(scroll_area)
        
        self.content_stack.addWidget(page)
    
    def create_silent_aim_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)
        
        # Card principal
        card = self.create_card_widget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # Enable Silent Aim
        enable_flick_layout = QHBoxLayout()
        enable_flick_label = QLabel("Enable Silent Aim")
        enable_flick_label.setStyleSheet(StyleHelper.get_label_style())
        enable_flick_toggle = AnimatedToggle()
        enable_flick_toggle.setChecked(self.config["enableFlickBot"])
        enable_flick_toggle.stateChanged.connect(lambda state: self.update_config("enableFlickBot", bool(state)))
        
        enable_flick_layout.addWidget(enable_flick_label)
        enable_flick_layout.addStretch()
        enable_flick_layout.addWidget(enable_flick_toggle)
        
        # Keybind
        keybind_layout = QHBoxLayout()
        keybind_label = QLabel("Keybind:")
        keybind_label.setStyleSheet(StyleHelper.get_label_style())
        
        keybind = KeybindButton(self.config["flickbotKeybind"])
        keybind.keybind_changed.connect(lambda kb: self.update_config("flickbotKeybind", kb))
        
        keybind_layout.addWidget(keybind_label)
        keybind_layout.addStretch()
        keybind_layout.addWidget(keybind)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(StyleHelper.get_separator_style())
        
        # Settings Label
        settings_label = QLabel("Silent Aim Settings:")
        settings_label.setStyleSheet(StyleHelper.get_title_label_style())
        
        # Sliders
        strength_slider = LabeledSlider("Silent Aim Strength", 10, 90, self.config["flickScopeSens"], suffix="%")
        strength_slider.valueChanged.connect(lambda val: self.update_config("flickScopeSens", val))
        
        cooldown_slider = LabeledSlider("Cool Down", 5, 120, int(self.config["flickCooldown"] * 100), step=5, suffix="s")
        cooldown_slider.valueChanged.connect(lambda val: self.update_config("flickCooldown", val / 100))
        
        delay_slider = LabeledSlider("Shot Delay", 1, 10, int(self.config["flickDelay"] * 1000), step=1, suffix="s")
        delay_slider.valueChanged.connect(lambda val: self.update_config("flickDelay", val / 1000))
        
        # Adicionar widgets ao layout
        card_layout.addLayout(enable_flick_layout)
        card_layout.addLayout(keybind_layout)
        card_layout.addWidget(separator)
        card_layout.addWidget(settings_label)
        card_layout.addWidget(strength_slider)
        card_layout.addWidget(cooldown_slider)
        card_layout.addWidget(delay_slider)
        
        scroll_layout.addWidget(card)
        scroll_layout.addStretch()
        
        layout.addWidget(scroll_area)
        
        self.content_stack.addWidget(page)
    
    def create_visual_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)
        
        # Card principal
        card = self.create_card_widget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # Grid para switches
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(15)
        
        # Switches
        rainbow_layout = QHBoxLayout()
        rainbow_label = QLabel("Rainbow Visuals")
        rainbow_label.setStyleSheet(StyleHelper.get_label_style())
        rainbow_toggle = AnimatedToggle()
        rainbow_toggle.setChecked(self.config["useHue"])
        rainbow_toggle.stateChanged.connect(lambda state: self.update_config("useHue", bool(state)))
        
        rainbow_layout.addWidget(rainbow_label)
        rainbow_layout.addStretch()
        rainbow_layout.addWidget(rainbow_toggle)
        
        fov_layout = QHBoxLayout()
        fov_label = QLabel("FOV")
        fov_label.setStyleSheet(StyleHelper.get_label_style())
        fov_toggle = AnimatedToggle()
        fov_toggle.setChecked(self.config["showFov"])
        fov_toggle.stateChanged.connect(lambda state: self.update_config("showFov", bool(state)))
        
        fov_layout.addWidget(fov_label)
        fov_layout.addStretch()
        fov_layout.addWidget(fov_toggle)
        
        crosshair_layout = QHBoxLayout()
        crosshair_label = QLabel("Crosshair")
        crosshair_label.setStyleSheet(StyleHelper.get_label_style())
        crosshair_toggle = AnimatedToggle()
        crosshair_toggle.setChecked(self.config["showCrosshair"])
        crosshair_toggle.stateChanged.connect(lambda state: self.update_config("showCrosshair", bool(state)))
        
        crosshair_layout.addWidget(crosshair_label)
        crosshair_layout.addStretch()
        crosshair_layout.addWidget(crosshair_toggle)
        
        esp_layout = QHBoxLayout()
        esp_label = QLabel("ESP")
        esp_label.setStyleSheet(StyleHelper.get_label_style())
        esp_toggle = AnimatedToggle()
        esp_toggle.setChecked(self.config["showDetections"])
        esp_toggle.stateChanged.connect(lambda state: self.update_config("showDetections", bool(state)))
        
        esp_layout.addWidget(esp_label)
        esp_layout.addStretch()
        esp_layout.addWidget(esp_toggle)
        
        aimline_layout = QHBoxLayout()
        aimline_label = QLabel("Aimline")
        aimline_label.setStyleSheet(StyleHelper.get_label_style())
        aimline_toggle = AnimatedToggle()
        aimline_toggle.setChecked(self.config["showAimline"])
        aimline_toggle.stateChanged.connect(lambda state: self.update_config("showAimline", bool(state)))
        
        aimline_layout.addWidget(aimline_label)
        aimline_layout.addStretch()
        aimline_layout.addWidget(aimline_toggle)
        
        watermark_layout = QHBoxLayout()
        watermark_label = QLabel("Watermark")
        watermark_label.setStyleSheet(StyleHelper.get_label_style())
        watermark_toggle = AnimatedToggle()
        watermark_toggle.setChecked(self.config["showFPS"])
        watermark_toggle.stateChanged.connect(lambda state: self.update_config("showFPS", bool(state)))
        
        watermark_layout.addWidget(watermark_label)
        watermark_layout.addStretch()
        watermark_layout.addWidget(watermark_toggle)
        
        # Adicionar layouts ao grid
        grid_layout.addLayout(rainbow_layout, 0, 0)
        grid_layout.addLayout(fov_layout, 0, 1)
        grid_layout.addLayout(crosshair_layout, 1, 0)
        grid_layout.addLayout(esp_layout, 1, 1)
        grid_layout.addLayout(aimline_layout, 2, 0)
        grid_layout.addLayout(watermark_layout, 2, 1)
        
        # Box Type
        box_type_layout = QVBoxLayout()
        box_type_label = QLabel("Box Type:")
        box_type_label.setStyleSheet(StyleHelper.get_label_style())
        
        box_type_combo = QComboBox()
        box_type_combo.addItems(["Regular", "Corner", "Filled"])
        box_type_combo.setCurrentText(self.config["boxType"])
        box_type_combo.setStyleSheet(StyleHelper.get_combobox_style())
        box_type_combo.currentTextChanged.connect(lambda text: self.update_config("boxType", text))
        box_type_combo.setCursor(QCursor(Qt.PointingHandCursor))
        
        box_type_layout.addWidget(box_type_label)
        box_type_layout.addWidget(box_type_combo)
        
        # Adicionar layouts ao layout principal
        card_layout.addLayout(grid_layout)
        card_layout.addLayout(box_type_layout)
        
        scroll_layout.addWidget(card)
        scroll_layout.addStretch()
        
        layout.addWidget(scroll_area)
        
        self.content_stack.addWidget(page)
    
    def create_extra_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)
        
        # Card principal
        card = self.create_card_widget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # Grid para switches
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(15)
        
        # Switches
        tournament_layout = QHBoxLayout()
        tournament_label = QLabel("Tournament Mode")
        tournament_label.setStyleSheet(StyleHelper.get_label_style())
        tournament_toggle = AnimatedToggle()
        tournament_toggle.setChecked(self.config["cupModeOn"])
        tournament_toggle.stateChanged.connect(lambda state: self.update_config("cupModeOn", bool(state)))
        
        tournament_layout.addWidget(tournament_label)
        tournament_layout.addStretch()
        tournament_layout.addWidget(tournament_toggle)
        
        triggerbot_layout = QHBoxLayout()
        triggerbot_label = QLabel("Enable Triggerbot")
        triggerbot_label.setStyleSheet(StyleHelper.get_label_style())
        triggerbot_toggle = AnimatedToggle()
        triggerbot_toggle.setChecked(self.config["enableTriggerBot"])
        triggerbot_toggle.stateChanged.connect(lambda state: self.update_config("enableTriggerBot", bool(state)))
        
        triggerbot_layout.addWidget(triggerbot_label)
        triggerbot_layout.addStretch()
        triggerbot_layout.addWidget(triggerbot_toggle)
        
        require_keybind_layout = QHBoxLayout()
        require_keybind_label = QLabel("Use Keybind for Triggerbot")
        require_keybind_label.setStyleSheet(StyleHelper.get_label_style())
        require_keybind_toggle = AnimatedToggle()
        require_keybind_toggle.setChecked(self.config["requireKeybind"])
        require_keybind_toggle.stateChanged.connect(lambda state: self.update_config("requireKeybind", bool(state)))
        
        require_keybind_layout.addWidget(require_keybind_label)
        require_keybind_layout.addStretch()
        require_keybind_layout.addWidget(require_keybind_toggle)
        
        # Adicionar layouts ao grid
        grid_layout.addLayout(tournament_layout, 0, 0)
        grid_layout.addLayout(triggerbot_layout, 0, 1)
        grid_layout.addLayout(require_keybind_layout, 1, 0, 1, 2)
        
        # Keybind
        keybind_layout = QHBoxLayout()
        keybind_label = QLabel("Triggerbot Key:")
        keybind_label.setStyleSheet(StyleHelper.get_label_style())
        
        keybind = KeybindButton(self.config["autoFireKeybind"])
        keybind.keybind_changed.connect(lambda kb: self.update_config("autoFireKeybind", kb))
        
        keybind_layout.addWidget(keybind_label)
        keybind_layout.addStretch()
        keybind_layout.addWidget(keybind)
        
        # Sliders
        fov_slider = LabeledSlider("FOV Size", 4, 30, self.config["autoFireFovSize"])
        fov_slider.valueChanged.connect(lambda val: self.update_config("autoFireFovSize", val))
        
        confidence_slider = LabeledSlider("Confidence", 60, 100, self.config["autoFireConfidence"], suffix="%")
        confidence_slider.valueChanged.connect(lambda val: self.update_config("autoFireConfidence", val))
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(StyleHelper.get_separator_style())
        
        # Anti-recoil grid
        recoil_grid = QGridLayout()
        recoil_grid.setHorizontalSpacing(30)
        recoil_grid.setVerticalSpacing(15)
        
        # Anti-recoil switches
        bloom_layout = QHBoxLayout()
        bloom_label = QLabel("Reduce Bloom")
        bloom_label.setStyleSheet(StyleHelper.get_label_style())
        bloom_toggle = AnimatedToggle()
        bloom_toggle.setChecked(self.config["reduceBloom"])
        bloom_toggle.stateChanged.connect(lambda state: self.update_config("reduceBloom", bool(state)))
        
        bloom_layout.addWidget(bloom_label)
        bloom_layout.addStretch()
        bloom_layout.addWidget(bloom_toggle)
        
        recoil_layout = QHBoxLayout()
        recoil_label = QLabel("Enable Anti-Recoil")
        recoil_label.setStyleSheet(StyleHelper.get_label_style())
        recoil_toggle = AnimatedToggle()
        recoil_toggle.setChecked(self.config["antiRecoilOn"])
        recoil_toggle.stateChanged.connect(lambda state: self.update_config("antiRecoilOn", bool(state)))
        
        recoil_layout.addWidget(recoil_label)
        recoil_layout.addStretch()
        recoil_layout.addWidget(recoil_toggle)
        
        ads_layout = QHBoxLayout()
        ads_label = QLabel("Require ADS")
        ads_label.setStyleSheet(StyleHelper.get_label_style())
        ads_toggle = AnimatedToggle()
        ads_toggle.setChecked(self.config["requireADS"])
        ads_toggle.stateChanged.connect(lambda state: self.update_config("requireADS", bool(state)))
        
        ads_layout.addWidget(ads_label)
        ads_layout.addStretch()
        ads_layout.addWidget(ads_toggle)
        
        # Adicionar layouts ao grid
        recoil_grid.addLayout(bloom_layout, 0, 0)
        recoil_grid.addLayout(recoil_layout, 0, 1)
        recoil_grid.addLayout(ads_layout, 1, 0, 1, 2)
        
        # Slider de força
        strength_slider = LabeledSlider("Strength", 1, 10, self.config["antiRecoilStrength"])
        strength_slider.valueChanged.connect(lambda val: self.update_config("antiRecoilStrength", val))
        
        # Adicionar widgets ao layout
        card_layout.addLayout(grid_layout)
        card_layout.addLayout(keybind_layout)
        card_layout.addWidget(fov_slider)
        card_layout.addWidget(confidence_slider)
        card_layout.addWidget(separator)
        card_layout.addLayout(recoil_grid)
        card_layout.addWidget(strength_slider)
        
        scroll_layout.addWidget(card)
        scroll_layout.addStretch()
        
        layout.addWidget(scroll_area)
        
        self.content_stack.addWidget(page)
    
    def create_profile_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)
        
        # Card principal
        card = self.create_card_widget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # User Info
        user_info_title = QLabel("User Info:")
        user_info_title.setStyleSheet(StyleHelper.get_title_label_style())
        
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(8)
        
        key_label = QLabel(f"Your Key: {self.user_info['username']}")
        key_label.setStyleSheet(StyleHelper.get_label_style())
        
        purchased_label = QLabel(f"Purchased: {self.user_info['purchased']}")
        purchased_label.setStyleSheet(StyleHelper.get_label_style())
        
        expiry_label = QLabel(f"Expiry: {self.user_info['expiry']}")
        expiry_label.setStyleSheet(StyleHelper.get_label_style())
        
        last_login_label = QLabel(f"Last Login: {self.user_info['lastLogin']}")
        last_login_label.setStyleSheet(StyleHelper.get_label_style())
        
        user_info_layout.addWidget(key_label)
        user_info_layout.addWidget(purchased_label)
        user_info_layout.addWidget(expiry_label)
        user_info_layout.addWidget(last_login_label)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(StyleHelper.get_separator_style())
        
        # Hotkeys
        hotkeys_title = QLabel("Hotkeys:")
        hotkeys_title.setStyleSheet(StyleHelper.get_title_label_style())
        
        hotkeys_layout = QVBoxLayout()
        hotkeys_layout.setSpacing(8)
        
        quick_toggle_label = QLabel("Quick On/Off: <span style='color: " + PURPLE_PRIMARY + ";'>[F1]</span>")
        quick_toggle_label.setStyleSheet(StyleHelper.get_label_style())
        
        close_label = QLabel("Close: <span style='color: " + PURPLE_PRIMARY + ";'>[F2]</span>")
        close_label.setStyleSheet(StyleHelper.get_label_style())
        
        toggle_menu_label = QLabel("Toggle Menu: <span style='color: " + PURPLE_PRIMARY + ";'>[INS]</span>")
        toggle_menu_label.setStyleSheet(StyleHelper.get_label_style())
        
        hotkeys_layout.addWidget(quick_toggle_label)
        hotkeys_layout.addWidget(close_label)
        hotkeys_layout.addWidget(toggle_menu_label)
        
        # Botão Refresh
        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet(StyleHelper.get_button_style())
        refresh_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Ícone de refresh
        refresh_icon = QtSvg.QSvgWidget(os.path.join(RESOURCES_PATH, "refresh.svg"))
        refresh_icon.setFixedSize(16, 16)
        
        refresh_text = QLabel("Refresh")
        refresh_text.setStyleSheet("color: white; font-family: 'Poppins'; font-weight: 600; font-size: 13px;")
        
        refresh_layout = QHBoxLayout()
        refresh_layout.setSpacing(8)
        refresh_layout.addStretch()
        refresh_layout.addWidget(refresh_icon)
        refresh_layout.addWidget(refresh_text)
        refresh_layout.addStretch()
        
        refresh_button.setLayout(refresh_layout)
        
        # Adicionar widgets ao layout
        card_layout.addWidget(user_info_title)
        card_layout.addLayout(user_info_layout)
        card_layout.addWidget(separator)
        card_layout.addWidget(hotkeys_title)
        card_layout.addLayout(hotkeys_layout)
        card_layout.addStretch()
        card_layout.addWidget(refresh_button)
        
        scroll_layout.addWidget(card)
        scroll_layout.addStretch()
        
        layout.addWidget(scroll_area)
        
        self.content_stack.addWidget(page)
    
    def create_advanced_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)
        
        # Card principal
        card = self.create_card_widget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        
        # Single Class Switch
        single_class_layout = QHBoxLayout()
        single_class_label = QLabel("Detect Single Class Only")
        single_class_label.setStyleSheet(StyleHelper.get_label_style())
        single_class_toggle = AnimatedToggle()
        single_class_toggle.setChecked(self.config["useModelClass"])
        single_class_toggle.stateChanged.connect(lambda state: self.update_config("useModelClass", bool(state)))
        
        single_class_layout.addWidget(single_class_label)
        single_class_layout.addStretch()
        single_class_layout.addWidget(single_class_toggle)
        
        # Blob Size
        blob_size_layout = QVBoxLayout()
        blob_size_label = QLabel("Blob Size:")
        blob_size_label.setStyleSheet(StyleHelper.get_label_style())
        
        blob_size_combo = QComboBox()
        blob_size_combo.addItems(["320", "480", "640", "736", "832"])
        blob_size_combo.setCurrentText(self.config["imgValue"])
        blob_size_combo.setStyleSheet(StyleHelper.get_combobox_style())
        blob_size_combo.currentTextChanged.connect(lambda text: self.update_config("imgValue", text))
        blob_size_combo.setCursor(QCursor(Qt.PointingHandCursor))
        
        blob_size_layout.addWidget(blob_size_label)
        blob_size_layout.addWidget(blob_size_combo)
        
        # Model
        model_layout = QVBoxLayout()
        model_label = QLabel("Load Model:")
        model_label.setStyleSheet(StyleHelper.get_label_style())
        
        model_combo = QComboBox()
        model_combo.addItems(["Fortnite.pt", "FortnitePro.pt"])
        model_combo.setCurrentText(self.config["lastModel"])
        model_combo.setStyleSheet(StyleHelper.get_combobox_style())
        model_combo.currentTextChanged.connect(lambda text: self.update_config("lastModel", text))
        model_combo.setCursor(QCursor(Qt.PointingHandCursor))
        
        model_layout.addWidget(model_label)
        model_layout.addWidget(model_combo)
        
        # Sliders
        max_detections_slider = LabeledSlider("Max Detections", 1, 6, self.config["maxDetections"])
        max_detections_slider.valueChanged.connect(lambda val: self.update_config("maxDetections", val))
        
        model_fps_slider = LabeledSlider("Max FPS", 60, 360, self.config["modelFPS"])
        model_fps_slider.valueChanged.connect(lambda val: self.update_config("modelFPS", val))
        
        # Adicionar widgets ao layout
        card_layout.addLayout(single_class_layout)
        card_layout.addLayout(blob_size_layout)
        card_layout.addLayout(model_layout)
        card_layout.addWidget(max_detections_slider)
        card_layout.addWidget(model_fps_slider)
        
        scroll_layout.addWidget(card)
        scroll_layout.addStretch()
        
        layout.addWidget(scroll_area)
        
        self.content_stack.addWidget(page)
    
    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()
    
    def update_slot_config(self, slot_key, key, value):
        self.config[slot_key][key] = value
        self.save_config()
    
    def save_config(self):
        try:
            with open("config.json", "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_config(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
        except Exception as e:
            print(f"Error loading config: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EternityApp()
    window.show()
    sys.exit(app.exec_())