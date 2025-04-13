import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import os
import requests
from pathlib import Path
import time
import io
import base64

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Custom colors
DARK_BG = "#101010"
DARK_SECONDARY = "#151515"
PURPLE_ACCENT = "#6200ed"
TEXT_COLOR = "#717171"
WHITE = "#ffffff"
BORDER_COLOR = "#1e1e1e"
SLOT_BG = "#1a1a1a"
TAB_ACTIVE_BG = "#1a1a1a"

# Create assets directory
assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

# Image URLs
LOGO_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/logo-yVy2pG25oDbUI6Fi6sghxyOgH2KInG.png"
MOUSE_ICON_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/mouse_icon-R4t4cGY3fksZVA2akEfdPMRoMgbMFz.png"
EYE_ICON_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/eye_icon-N1RrXql4SWveyCOVPNlxZjmZgOOXqb.png"
USER_ICON_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/user_icon-pP4s4YhokzW0tWXqni34XzCkAONSDB.png"

class CustomSwitch(ctk.CTkSwitch):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            text="",
            width=40,
            height=20,
            switch_width=36,
            switch_height=18,
            corner_radius=10,
            progress_color=PURPLE_ACCENT,
            button_color=WHITE,
            button_hover_color=WHITE,
            fg_color=DARK_SECONDARY,
            **kwargs
        )

class CustomSlider(ctk.CTkSlider):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            from_=0,
            to=100,
            number_of_steps=100,
            progress_color=PURPLE_ACCENT,
            button_color=WHITE,
            button_hover_color=WHITE,
            fg_color=DARK_SECONDARY,
            height=8,
            **kwargs
        )

class CustomEntry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=DARK_SECONDARY,
            border_width=0,
            text_color=WHITE,
            corner_radius=4,
            height=25,
            **kwargs
        )

class CustomDropdown(ctk.CTkOptionMenu):
    def __init__(self, master, values, **kwargs):
        super().__init__(
            master,
            values=values,
            fg_color=DARK_SECONDARY,
            button_color=DARK_SECONDARY,
            button_hover_color="#303030",
            dropdown_fg_color=DARK_SECONDARY,
            text_color=WHITE,
            dropdown_text_color=WHITE,
            corner_radius=4,
            **kwargs
        )

class AimbotSettingsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize variables
        self.current_section = "aimbot"
        self.current_tab = "aimbot"
        self.tab_buttons = {}
        self.content_frames = {}
        self.active_underlines = []
        
        # Configure window
        self.title("Aimbot Settings")
        self.geometry("800x500")
        self.configure(fg_color=DARK_BG)
        self.resizable(False, False)
        
        # Create main layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Download and load images
        self.download_images()
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Create all tabs
        self.create_aimbot_tab()
        self.create_slots_tab()
        self.create_recoil_tab()
        self.create_trigger_tab()
        self.create_visuals_tab()
        self.create_profile_tab()
        
        # Show aimbot tab by default
        self.switch_section("aimbot")
        self.show_tab("aimbot")
    
    def download_images(self):
        """Download and load all images"""
        try:
            # Download logo
            logo_path = self.download_image(LOGO_URL, "logo.png")
            self.logo_image = self.load_image(logo_path, (60, 60))
            
            # Download mouse icon
            mouse_path = self.download_image(MOUSE_ICON_URL, "mouse.png")
            self.mouse_image = self.load_image(mouse_path, (24, 24))
            
            # Download eye icon
            eye_path = self.download_image(EYE_ICON_URL, "eye.png")
            self.eye_image = self.load_image(eye_path, (24, 24))
            
            # Download user icon
            user_path = self.download_image(USER_ICON_URL, "user.png")
            self.user_image = self.load_image(user_path, (24, 24))
            
            print("All images downloaded and loaded successfully")
        except Exception as e:
            print(f"Error loading images: {e}")
            self.create_fallback_images()
    
    def download_image(self, url, filename):
        """Download an image from URL and save it to assets directory"""
        filepath = assets_dir / filename
        if not filepath.exists():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {filename}")
                else:
                    print(f"Failed to download {filename}: {response.status_code}")
                    raise Exception(f"Failed to download {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                raise e
        return filepath
    
    def load_image(self, filepath, size):
        """Load an image from file and return a CTkImage"""
        try:
            img = Image.open(filepath)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception as e:
            print(f"Error loading image {filepath}: {e}")
            raise e
    
    def create_fallback_images(self):
        """Create fallback images if loading fails"""
        # Logo
        logo_img = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(logo_img)
        draw.ellipse((5, 5, 55, 55), outline=PURPLE_ACCENT, width=3)
        self.logo_image = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(60, 60))
        
        # Mouse icon
        mouse_img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mouse_img)
        draw.rectangle((8, 4, 16, 20), outline=WHITE, width=1)
        self.mouse_image = ctk.CTkImage(light_image=mouse_img, dark_image=mouse_img, size=(24, 24))
        
        # Eye icon
        eye_img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(eye_img)
        draw.ellipse((4, 8, 20, 16), outline=WHITE, width=1)
        self.eye_image = ctk.CTkImage(light_image=eye_img, dark_image=eye_img, size=(24, 24))
        
        # User icon
        user_img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(user_img)
        draw.ellipse((8, 4, 16, 12), outline=WHITE, width=1)
        self.user_image = ctk.CTkImage(light_image=user_img, dark_image=user_img, size=(24, 24))
    
    def create_sidebar(self):
        """Create the sidebar with logo and navigation icons"""
        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            fg_color=DARK_BG, 
            width=145,
            corner_radius=0,
            border_width=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        # Logo container (top-left square) with border
        self.logo_container = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color=DARK_BG,
            width=145,
            height=145,
            corner_radius=0,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.logo_container.grid(row=0, column=0)
        self.logo_container.grid_propagate(False)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self.logo_container, 
            image=self.logo_image, 
            text="",
            fg_color="transparent"
        )
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Vertical separator
        self.v_separator = ctk.CTkFrame(
            self, 
            width=1, 
            fg_color=BORDER_COLOR
        )
        self.v_separator.place(x=145, y=0, relheight=1)
        
        # Horizontal separator below logo
        self.h_separator = ctk.CTkFrame(
            self.sidebar_frame,
            height=1,
            fg_color=BORDER_COLOR
        )
        self.h_separator.place(x=0, y=145, relwidth=1)
        
        # Navigation icons with borders
        icon_y_positions = [200, 260, 320]
        
        # Create icon containers with borders
        self.icon_containers = []
        for i, y_pos in enumerate(icon_y_positions):
            container = ctk.CTkFrame(
                self.sidebar_frame,
                width=40,
                height=40,
                fg_color="transparent",
                corner_radius=0,
                border_width=1,
                border_color=BORDER_COLOR
            )
            container.place(x=72, y=y_pos, anchor="center")
            self.icon_containers.append(container)
        
        # Mouse icon (Aimbot)
        self.mouse_button = ctk.CTkButton(
            self.icon_containers[0], 
            image=self.mouse_image, 
            text="",
            fg_color="transparent",
            hover_color="#333333",
            width=24,
            height=24,
            corner_radius=0,
            command=lambda: self.switch_section("aimbot")
        )
        self.mouse_button.place(relx=0.5, rely=0.5, anchor="center")
        
        # Eye icon (Visuals)
        self.eye_button = ctk.CTkButton(
            self.icon_containers[1], 
            image=self.eye_image, 
            text="",
            fg_color="transparent",
            hover_color="#333333",
            width=24,
            height=24,
            corner_radius=0,
            command=lambda: self.switch_section("visuals")
        )
        self.eye_button.place(relx=0.5, rely=0.5, anchor="center")
        
        # User icon (Profile)
        self.user_button = ctk.CTkButton(
            self.icon_containers[2], 
            image=self.user_image, 
            text="",
            fg_color="transparent",
            hover_color="#333333",
            width=24,
            height=24,
            corner_radius=0,
            command=lambda: self.switch_section("profile")
        )
        self.user_button.place(relx=0.5, rely=0.5, anchor="center")
    
    def create_main_content(self):
        """Create the main content area"""
        # Main content frame
        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color=DARK_BG, 
            corner_radius=0,
            border_width=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Tab navigation frame with border
        self.tab_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=DARK_BG,
            corner_radius=0,
            height=40,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.tab_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.tab_frame.grid_propagate(False)
        
        # Content container with border
        self.content_container = ctk.CTkFrame(
            self.main_frame,
            fg_color=DARK_BG,
            corner_radius=0,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Create tab navigation buttons
        self.create_tab_buttons()
    
    def create_tab_buttons(self):
        """Create tab navigation buttons"""
        # Clear existing buttons
        for widget in self.tab_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        # Clear existing underlines
        for underline in self.active_underlines:
            underline.destroy()
        self.active_underlines = []
        
        # Create new buttons based on current section
        if self.current_section == "aimbot":
            tabs = ["Aimbot", "Slots", "Recoil", "Trigger"]
        elif self.current_section == "visuals":
            tabs = ["Visuals"]
        elif self.current_section == "profile":
            tabs = ["Profile"]
        
        # Create tab buttons
        self.tab_buttons = {}
        for i, tab in enumerate(tabs):
            btn = ctk.CTkButton(
                self.tab_frame,
                text=tab,
                fg_color="transparent",
                text_color=TEXT_COLOR,
                hover_color=TAB_ACTIVE_BG,
                corner_radius=0,
                height=40,
                width=80,
                font=("Arial", 12),
                command=lambda t=tab.lower(): self.show_tab(t)
            )
            btn.place(x=20 + i*80, y=0)
            self.tab_buttons[tab.lower()] = btn
    
    def switch_section(self, section):
        """Switch between main sections (aimbot, visuals, profile)"""
        # Save previous section for animation
        prev_section = self.current_section
        
        # Update current section
        self.current_section = section
        
        # Reset all sidebar buttons and containers
        for container in self.icon_containers:
            container.configure(fg_color="transparent")
        
        # Highlight selected button container
        if section == "aimbot":
            self.icon_containers[0].configure(fg_color=DARK_SECONDARY)
        elif section == "visuals":
            self.icon_containers[1].configure(fg_color=DARK_SECONDARY)
        elif section == "profile":
            self.icon_containers[2].configure(fg_color=DARK_SECONDARY)
        
        # Update tab navigation
        self.create_tab_buttons()
        
        # Show appropriate tab
        if section == "aimbot":
            self.show_tab("aimbot")
        elif section == "visuals":
            self.show_tab("visuals")
        elif section == "profile":
            self.show_tab("profile")
        
        # Animate section change
        self.animate_section_change(prev_section, section)
    
    def animate_section_change(self, prev_section, new_section):
        """Animate the transition between sections"""
        # Hide all content frames with fade out effect
        for frame_name, frame in self.content_frames.items():
            if frame.winfo_viewable():
                self.animate_fade_out(frame)
        
        # Update after a short delay
        self.after(150, lambda: self.show_tab(self.current_tab))
    
    def animate_fade_out(self, widget):
        """Fade out animation for widgets"""
        # Create a flash effect
        orig_color = widget.cget("fg_color")
        
        def flash_step(step=0, opacity=1.0):
            if step < 5:
                # Gradually fade out
                opacity -= 0.2
                widget.configure(fg_color=self.blend_colors(orig_color, DARK_BG, opacity))
                self.after(20, lambda: flash_step(step+1, opacity))
            else:
                widget.grid_remove()
                widget.configure(fg_color=orig_color)
        
        flash_step()
    
    def animate_fade_in(self, widget):
        """Fade in animation for widgets"""
        widget.grid()
        
        # Create a fade-in effect
        orig_color = widget.cget("fg_color")
        
        def flash_step(step=0, opacity=0.0):
            if step < 5:
                # Gradually fade in
                opacity += 0.2
                widget.configure(fg_color=self.blend_colors(DARK_BG, orig_color, opacity))
                self.after(20, lambda: flash_step(step+1, opacity))
            else:
                widget.configure(fg_color=orig_color)
        
        flash_step()
    
    def blend_colors(self, color1, color2, ratio):
        """Blend two colors with the given ratio"""
        # For simplicity, just return the target color
        # In a real implementation, you would blend the colors
        return color2
    
    def show_tab(self, tab_name):
        """Show the selected tab content"""
        # Update current tab
        self.current_tab = tab_name
        
        # Reset all tab buttons
        for btn_name, btn in self.tab_buttons.items():
            btn.configure(fg_color="transparent", text_color=TEXT_COLOR)
        
        # Clear existing underlines
        for underline in self.active_underlines:
            underline.destroy()
        self.active_underlines = []
        
        # Highlight selected tab
        if tab_name in self.tab_buttons:
            self.tab_buttons[tab_name].configure(fg_color=TAB_ACTIVE_BG, text_color=WHITE)
            
            # Add underline effect for selected tab
            underline = ctk.CTkFrame(
                self.tab_frame,
                fg_color=PURPLE_ACCENT,
                height=2,
                width=80
            )
            
            # Position the underline under the selected tab
            tab_index = list(self.tab_buttons.keys()).index(tab_name)
            underline.place(x=20 + tab_index*80, y=38)
            self.active_underlines.append(underline)
        
        # Hide all content frames
        for frame_name, frame in self.content_frames.items():
            frame.grid_remove()
        
        # Show selected content with animation
        if tab_name in self.content_frames:
            self.animate_fade_in(self.content_frames[tab_name])
    
    def create_aimbot_tab(self):
        """Create the Aimbot tab content"""
        frame = ctk.CTkFrame(self.content_container, fg_color=DARK_BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        
        # Section header with border
        header_frame = ctk.CTkFrame(
            frame,
            fg_color=DARK_SECONDARY,
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Aimbot toggle
        self.create_toggle_setting(header_frame, "Aimbot", 0, with_border=False)
        
        # Field of View slider
        self.create_slider_setting(frame, "Field of View", "120", 1, 80)
        
        # Confidence slider
        self.create_slider_setting(frame, "Confidence", "45", 2, 40)
        
        # Strength slider
        self.create_slider_setting(frame, "Strength", "200", 3, 90)
        
        # Aim Hitbox dropdown
        self.create_dropdown_setting(frame, "Aim Hitbox", "Head", ["Head", "Body", "Limbs"], 4)
        
        # Humanization dropdown
        self.create_dropdown_setting(frame, "Humanization", "Default", ["Default", "Low", "Medium", "High"], 5)
        
        # Keybind
        self.create_keybind_setting(frame, 6)
        
        # Store the frame
        self.content_frames["aimbot"] = frame
    
    def create_slots_tab(self):
        """Create the Slots tab content exactly as in the Figma design"""
        frame = ctk.CTkFrame(self.content_container, fg_color=DARK_BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        
        # Section header with border
        header_frame = ctk.CTkFrame(
            frame,
            fg_color=DARK_SECONDARY,
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Enable Weapon Slots toggle
        self.create_toggle_setting(header_frame, "Enable Weapon Slots", 0, with_border=False)
        
        # Create a frame for the slots grid
        slots_grid = ctk.CTkFrame(frame, fg_color="transparent")
        slots_grid.grid(row=1, column=0, sticky="ew", pady=(20, 0))
        slots_grid.grid_columnconfigure((0, 1, 2), weight=1)
        slots_grid.grid_rowconfigure((0, 1), weight=1)
        
        # Create 6 weapon slot boxes (3x2 grid)
        slot_names = ["Slot 1", "Slot 2", "Slot 3", "Slot 4", "Slot 5", "Pickaxe"]
        
        for i, name in enumerate(slot_names):
            row = i // 3
            col = i % 3
            
            # Create slot box
            slot_box = self.create_weapon_slot(slots_grid, name)
            slot_box.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Store the frame
        self.content_frames["slots"] = frame
    
    def create_weapon_slot(self, parent, name):
        """Create a weapon slot box as shown in the Figma design"""
        # Create a frame with dark background and border
        slot_frame = ctk.CTkFrame(
            parent, 
            fg_color=SLOT_BG, 
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        slot_frame.grid_columnconfigure(0, weight=1)
        
        # Slot name and weapon selection
        name_frame = ctk.CTkFrame(slot_frame, fg_color="transparent")
        name_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        name_frame.grid_columnconfigure(0, weight=1)
        
        # Slot name
        name_label = ctk.CTkLabel(
            name_frame,
            text=name,
            text_color=WHITE,
            font=("Arial", 12)
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        # Weapon selection entry
        weapon_entry = CustomEntry(name_frame, width=80)
        weapon_entry.grid(row=0, column=1, sticky="e")
        
        # FOV slider
        slider_frame = ctk.CTkFrame(slot_frame, fg_color="transparent")
        slider_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        slider_frame.grid_columnconfigure(0, weight=1)
        
        # Slider
        slider = CustomSlider(slider_frame)
        slider.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        slider.set(60)
        
        # Value
        value_label = ctk.CTkLabel(
            slider_frame,
            text="120",
            text_color=WHITE,
            font=("Arial", 12)
        )
        value_label.grid(row=0, column=1, sticky="e")
        
        # Enable Aim toggle
        toggle_frame = ctk.CTkFrame(slot_frame, fg_color="transparent")
        toggle_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        toggle_frame.grid_columnconfigure(0, weight=1)
        
        # Toggle label
        toggle_label = ctk.CTkLabel(
            toggle_frame,
            text="Enable Aim",
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        toggle_label.grid(row=0, column=0, sticky="w")
        
        # Toggle switch
        toggle = CustomSwitch(toggle_frame)
        toggle.grid(row=0, column=1, sticky="e")
        toggle.select()
        
        return slot_frame
    
    def create_recoil_tab(self):
        """Create the Recoil tab content"""
        frame = ctk.CTkFrame(self.content_container, fg_color=DARK_BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        
        # Section header with border
        header_frame = ctk.CTkFrame(
            frame,
            fg_color=DARK_SECONDARY,
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Enable Recoil Control System toggle
        self.create_toggle_setting(header_frame, "Enable Recoil Control System", 0, with_border=False)
        
        # Anti-recoil slider
        self.create_slider_setting(frame, "Anti-recoil", "6", 1, 60)
        
        # Require ADS toggle
        self.create_toggle_setting(frame, "Require ADS", 2)
        
        # Reduce Bloom toggle
        self.create_toggle_setting(frame, "Reduce Bloom", 3)
        
        # Store the frame
        self.content_frames["recoil"] = frame
    
    def create_trigger_tab(self):
        """Create the Trigger tab content"""
        frame = ctk.CTkFrame(self.content_container, fg_color=DARK_BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        
        # Section header with border
        header_frame = ctk.CTkFrame(
            frame,
            fg_color=DARK_SECONDARY,
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Enable Triggerbot toggle
        self.create_toggle_setting(header_frame, "Enable Triggerbot", 0, with_border=False)
        
        # Enable Keybind toggle
        self.create_toggle_setting(frame, "Enable Keybind", 1)
        
        # Keybind
        self.create_simple_keybind_setting(frame, "Keybind", 2)
        
        # Field Of View slider
        self.create_slider_setting(frame, "Field Of View", "6", 3, 60)
        
        # Confidence slider
        self.create_slider  "Field Of View", "6", 3, 60)
        
        # Confidence slider
        self.create_slider_setting(frame, "Confidence", "60", 4, 40)
        
        # Store the frame
        self.content_frames["trigger"] = frame
    
    def create_visuals_tab(self):
        """Create the Visuals tab content"""
        frame = ctk.CTkFrame(self.content_container, fg_color=DARK_BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        
        # Section header with border
        header_frame = ctk.CTkFrame(
            frame,
            fg_color=DARK_SECONDARY,
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Watermark toggle
        self.create_toggle_setting(header_frame, "Watermark", 0, with_border=False)
        
        # Rainbow Visuals toggle
        self.create_toggle_setting(frame, "Rainbow Visuals", 1)
        
        # Crosshair toggle
        self.create_toggle_setting(frame, "Crosshair", 2)
        
        # Draw Field of View toggle
        self.create_toggle_setting(frame, "Draw Field of View", 3)
        
        # ESP Line toggle
        self.create_toggle_setting(frame, "ESP Line", 4)
        
        # ESP Box toggle
        self.create_toggle_setting(frame, "ESP Box", 5)
        
        # Type Box dropdown
        self.create_dropdown_setting(frame, "Type Box", "Corner", ["Corner", "2D", "3D"], 6)
        
        # Store the frame
        self.content_frames["visuals"] = frame
    
    def create_profile_tab(self):
        """Create the Profile tab content"""
        frame = ctk.CTkFrame(self.content_container, fg_color=DARK_BG, corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure((0, 1), weight=1)
        
        # Left column - License info
        left_frame = ctk.CTkFrame(
            frame, 
            fg_color=DARK_SECONDARY, 
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        left_frame.grid_columnconfigure(0, weight=1)
        
        # License info fields
        self.create_info_field(left_frame, "License Key:", "", 0)
        self.create_info_field(left_frame, "Purchased:", "", 1)
        self.create_info_field(left_frame, "Expiry in:", "", 2)
        self.create_info_field(left_frame, "Last Login:", "", 3)
        
        # Right column - Keybinds
        right_frame = ctk.CTkFrame(
            frame, 
            fg_color=DARK_SECONDARY, 
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Keybind fields
        self.create_keybind_info(right_frame, "Quick ON/OFF:", "[F1]", 0)
        self.create_keybind_info(right_frame, "Panic key:", "[F2]", 1)
        self.create_keybind_info(right_frame, "Open menu:", "[INS]", 2)
        
        # Settings section with border
        settings_frame = ctk.CTkFrame(
            frame,
            fg_color=DARK_SECONDARY,
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        settings_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        settings_frame.grid_columnconfigure(0, weight=1)
        
        # Enable Single Class toggle
        self.create_toggle_setting(settings_frame, "Enable Single Class", 0, with_border=False)
        
        # Blob Size dropdown
        self.create_dropdown_setting(frame, "Blob Size", "480", ["320", "480", "640"], 2, col_span=2)
        
        # Max Detections slider
        self.create_slider_setting(frame, "Max Detections", "4", 3, 40, col_span=2)
        
        # FPS Cheat slider
        self.create_slider_setting(frame, "FPS Cheat", "300", 4, 80, col_span=2)
        
        # Store the frame
        self.content_frames["profile"] = frame
    
    def create_toggle_setting(self, parent, label_text, row, col=0, col_span=1, with_border=True):
        """Create a toggle setting with label"""
        if with_border:
            frame = ctk.CTkFrame(
                parent, 
                fg_color=DARK_SECONDARY, 
                height=40,
                corner_radius=4,
                border_width=1,
                border_color=BORDER_COLOR
            )
        else:
            frame = ctk.CTkFrame(parent, fg_color="transparent", height=40)
            
        frame.grid(row=row, column=col, columnspan=col_span, sticky="ew", pady=(0, 15))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        toggle = CustomSwitch(frame)
        toggle.grid(row=0, column=1, sticky="e", padx=10)
        toggle.select()
        
        return frame
    
    def create_slider_setting(self, parent, label_text, value_text, row, slider_value, col=0, col_span=1):
        """Create a slider setting with label and value"""
        frame = ctk.CTkFrame(
            parent, 
            fg_color=DARK_SECONDARY, 
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        frame.grid(row=row, column=col, columnspan=col_span, sticky="ew", pady=(0, 15))
        frame.grid_columnconfigure(0, weight=1)
        
        # Label
        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        
        # Slider and value container
        slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
        slider_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        slider_frame.grid_columnconfigure(0, weight=1)
        
        # Slider
        slider = CustomSlider(slider_frame)
        slider.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        slider.set(slider_value)
        
        # Value
        value_entry = CustomEntry(slider_frame, width=60)
        value_entry.insert(0, value_text)
        value_entry.grid(row=0, column=1, sticky="e")
        
        return frame
    
    def create_dropdown_setting(self, parent, label_text, default_value, options, row, col=0, col_span=1):
        """Create a dropdown setting with label"""
        frame = ctk.CTkFrame(
            parent, 
            fg_color=DARK_SECONDARY, 
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        frame.grid(row=row, column=col, columnspan=col_span, sticky="ew", pady=(0, 15))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        dropdown = CustomDropdown(
            frame, 
            values=options,
            width=120
        )
        dropdown.set(default_value)
        dropdown.grid(row=0, column=1, sticky="e", padx=10)
        
        return frame
    
    def create_keybind_setting(self, parent, row, col=0, col_span=1):
        """Create a dual keybind setting with label"""
        frame = ctk.CTkFrame(
            parent, 
            fg_color=DARK_SECONDARY, 
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        frame.grid(row=row, column=col, columnspan=col_span, sticky="ew", pady=(0, 15))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame, 
            text="Keybind", 
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        keybind_frame = ctk.CTkFrame(frame, fg_color="transparent")
        keybind_frame.grid(row=0, column=1, sticky="e", padx=10)
        
        keybind1 = CustomEntry(keybind_frame, width=120)
        keybind1.grid(row=0, column=0, padx=(0, 10))
        
        keybind2 = CustomEntry(keybind_frame, width=120)
        keybind2.grid(row=0, column=1)
        
        return frame
    
    def create_simple_keybind_setting(self, parent, label_text, row, col=0, col_span=1):
        """Create a single keybind setting with label"""
        frame = ctk.CTkFrame(
            parent, 
            fg_color=DARK_SECONDARY, 
            corner_radius=4,
            border_width=1,
            border_color=BORDER_COLOR
        )
        frame.grid(row=row, column=col, columnspan=col_span, sticky="ew", pady=(0, 15))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        keybind = CustomEntry(frame, width=120)
        keybind.grid(row=0, column=1, sticky="e", padx=10)
        
        return frame
    
    def create_info_field(self, parent, label_text, value_text, row):
        """Create an info field with label and value"""
        frame = ctk.CTkFrame(parent, fg_color="transparent", height=40)
        frame.grid(row=row, column=0, sticky="ew", padx=15, pady=(15, 0))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        label.grid(row=0, column=0, sticky="w")
        
        value = ctk.CTkLabel(
            frame, 
            text=value_text, 
            text_color=WHITE,
            font=("Arial", 12)
        )
        value.grid(row=0, column=1, sticky="e")
        
        return frame
    
    def create_keybind_info(self, parent, label_text, value_text, row):
        """Create a keybind info field with label and value"""
        frame = ctk.CTkFrame(parent, fg_color="transparent", height=40)
        frame.grid(row=row, column=0, sticky="ew", padx=15, pady=(15, 0))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        )
        label.grid(row=0, column=0, sticky="w")
        
        value = ctk.CTkLabel(
            frame, 
            text=value_text, 
            text_color=WHITE,
            font=("Arial", 12)
        )
        value.grid(row=0, column=1, sticky="e")
        
        return frame

if __name__ == "__main__":
    app = AimbotSettingsApp()
    app.mainloop()