import tkinter as tk
from tkinter import ttk

# Import your cellular automata module (commented out since we don't have the actual file)
# import celularautomata

class CellularAutomataSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cellular Automata Simulator")
        self.root.geometry("900x700")
        self.root.configure(bg="#2d2d2d")
        
        # Initialize frames
        self.main_menu_frame = None
        self.simulation_frame = None
        
        # Cellular automata algorithms (replace with actual imports from your celularautomata.py)
        self.cellular_automata_algorithms = [
            "Majority rule CA",
            "Conway's Game of Life",
            "Langton's Ant",
            "Brian's Brain",
            "Wireworld"
        ]
        
        self.show_main_menu()
        
    def show_main_menu(self):
        """Display the main menu screen"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.main_menu_frame = tk.Frame(self.root, bg="#2d2d2d")
        self.main_menu_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(
            self.main_menu_frame,
            text="Cellular Automata Simulator",
            font=("Arial", 26, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        title_label.pack(pady=60)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.main_menu_frame,
            text="Main Menu",
            font=("Arial", 16),
            bg="#2d2d2d",
            fg="#cccccc"
        )
        subtitle_label.pack(pady=15)
        
        # Simulate Automata Button
        simulate_button = tk.Button(
            self.main_menu_frame,
            text="Simulate Automata",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=40,
            pady=20,
            command=self.show_simulation_screen,
            cursor="hand2"
        )
        simulate_button.pack(pady=40)
        
        # Exit Button
        exit_button = tk.Button(
            self.main_menu_frame,
            text="Exit",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=25,
            pady=12,
            command=self.root.quit,
            cursor="hand2"
        )
        exit_button.pack(pady=15)
        
    def show_simulation_screen(self):
        """Display the simulation screen with left sidebar menu"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.simulation_frame = tk.Frame(self.root, bg="#2d2d2d")
        self.simulation_frame.pack(fill="both", expand=True)
        
        # Create left sidebar
        self.create_left_sidebar()
        
        # Create main content area
        self.create_main_content()
        
    def create_left_sidebar(self):
        """Create the left sidebar with cellular automata selection and info fields"""
        sidebar = tk.Frame(self.simulation_frame, bg="#e0e0e0", width=320)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False)
        
        # Back button
        back_button = tk.Button(
            sidebar,
            text="← Back to Main Menu",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            command=self.show_main_menu,
            cursor="hand2"
        )
        back_button.pack(pady=10, padx=10, fill="x")
        
        # Title for sidebar
        sidebar_title = tk.Label(
            sidebar,
            text="Cellular Automata Configuration",
            font=("Arial", 14, "bold"),
            bg="#e0e0e0",
            fg="#333333"
        )
        sidebar_title.pack(pady=15)
        
        # Dropdown menu for cellular automata algorithms
        tk.Label(sidebar, text="Select Cellular Automata Type:", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(pady=(10, 5), padx=10, anchor="w")
        
        self.selected_automata = tk.StringVar()
        self.selected_automata.set(self.cellular_automata_algorithms[0])
        
        automata_dropdown = ttk.Combobox(
            sidebar,
            textvariable=self.selected_automata,
            values=self.cellular_automata_algorithms,
            state="readonly",
            font=("Arial", 10),
            width=35
        )
        automata_dropdown.pack(pady=5, padx=10, fill="x")
        automata_dropdown.bind("<<ComboboxSelected>>", self.on_automata_selected)
        
        # Separator
        separator = tk.Frame(sidebar, height=2, bg="#cccccc")
        separator.pack(fill="x", pady=20, padx=10)
        
        # Info fields for cellular automata simulation
        self.create_info_fields(sidebar)
        
        # Control buttons
        self.create_control_buttons(sidebar)
        
    def create_info_fields(self, parent):
        """Create input fields for cellular automata configuration"""
        fields_frame = tk.Frame(parent, bg="#e0e0e0")
        fields_frame.pack(fill="x", padx=10)
        
        # Grid Size
        tk.Label(fields_frame, text="Grid Width:", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(anchor="w", pady=(5, 2))
        self.grid_width = tk.Entry(fields_frame, font=("Arial", 10))
        self.grid_width.insert(0, "50")
        self.grid_width.pack(fill="x", pady=(0, 10))
        
        tk.Label(fields_frame, text="Grid Height:", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(anchor="w", pady=(5, 2))
        self.grid_height = tk.Entry(fields_frame, font=("Arial", 10))
        self.grid_height.insert(0, "50")
        self.grid_height.pack(fill="x", pady=(0, 10))
        
        # Number of Generations
        tk.Label(fields_frame, text="Number of Generations:", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(anchor="w", pady=(5, 2))
        self.generations = tk.Entry(fields_frame, font=("Arial", 10))
        self.generations.insert(0, "100")
        self.generations.pack(fill="x", pady=(0, 10))
        
        # Initial Pattern
        tk.Label(fields_frame, text="Initial Pattern:", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(anchor="w", pady=(5, 2))
        self.initial_pattern = ttk.Combobox(
            fields_frame,
            values=["Random", "Single Cell", "Glider", "Block", "Custom"],
            state="readonly",
            font=("Arial", 10)
        )
        self.initial_pattern.set("Random")
        self.initial_pattern.pack(fill="x", pady=(0, 10))
        
        # Speed Control
        tk.Label(fields_frame, text="Animation Speed (ms):", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(anchor="w", pady=(5, 2))
        self.speed_scale = tk.Scale(
            fields_frame,
            from_=10,
            to=1000,
            orient="horizontal",
            bg="#e0e0e0",
            font=("Arial", 9)
        )
        self.speed_scale.set(100)
        self.speed_scale.pack(fill="x", pady=(0, 10))
        
    def create_control_buttons(self, parent):
        """Create control buttons for the simulation"""
        buttons_frame = tk.Frame(parent, bg="#e0e0e0")
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Start Simulation Button
        start_button = tk.Button(
            buttons_frame,
            text="Start Simulation",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=8,
            command=self.start_simulation,
            cursor="hand2"
        )
        start_button.pack(fill="x", pady=2)
        
        # Pause Button
        pause_button = tk.Button(
            buttons_frame,
            text="Pause",
            font=("Arial", 11),
            bg="#FF9800",
            fg="white",
            pady=8,
            command=self.pause_simulation,
            cursor="hand2"
        )
        pause_button.pack(fill="x", pady=2)
        
        # Reset Button
        reset_button = tk.Button(
            buttons_frame,
            text="Reset",
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            pady=8,
            command=self.reset_simulation,
            cursor="hand2"
        )
        reset_button.pack(fill="x", pady=2)
        
        # Step Button
        step_button = tk.Button(
            buttons_frame,
            text="Single Step",
            font=("Arial", 11),
            bg="#9C27B0",
            fg="white",
            pady=8,
            command=self.step_simulation,
            cursor="hand2"
        )
        step_button.pack(fill="x", pady=2)
        
    def create_main_content(self):
        """Create the main content area for simulation display"""
        content_frame = tk.Frame(self.simulation_frame, bg="#2d2d2d")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Title
        content_title = tk.Label(
            content_frame,
            text="Cellular Automata Simulation",
            font=("Arial", 16, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        content_title.pack(pady=15)
        
        # Canvas for displaying the cellular automata
        self.canvas = tk.Canvas(
            content_frame,
            bg="#1a1a1a",
            width=500,
            height=400,
            relief="sunken",
            borderwidth=2
        )
        self.canvas.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Status bar
        self.status_frame = tk.Frame(content_frame, bg="#2d2d2d")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to simulate",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#cccccc"
        )
        self.status_label.pack(side="left")
        
        self.generation_label = tk.Label(
            self.status_frame,
            text="Generation: 0",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#cccccc"
        )
        self.generation_label.pack(side="right")
        
    def on_automata_selected(self, event):
        """Handle cellular automata type selection"""
        # Empty method - no functionality needed
        pass
        
    def start_simulation(self):
        """Start the cellular automata simulation"""
        # Empty method - no functionality needed
        pass
        
    def pause_simulation(self):
        """Pause the simulation"""
        # Empty method - no functionality needed
        pass
        
    def reset_simulation(self):
        """Reset the simulation to initial state"""
        # Empty method - no functionality needed
        pass
        
    def step_simulation(self):
        """Execute a single step of the simulation"""
        # Empty method - no functionality needed
        pass
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CellularAutomataSimulator()
    app.run()

