import tkinter as tk
from tkinter import ttk
import automata

class CellularAutomataSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cellular Automata Simulator")
        self.root.geometry("1200x800")  # Increased window size
        self.root.configure(bg="#2d2d2d")

        # Initialize frames
        self.main_menu_frame = None
        self.simulation_frame = None

        # Grid properties
        self.current_width = 50
        self.current_height = 50
        self.cell_size = 10  # This will be calculated dynamically

        # Dynamic canvas dimensions - much larger to use available space
        self.max_canvas_width = 800   # Increased from 550
        self.max_canvas_height = 650  # Increased from 450

        # Cellular automata algorithms
        self.cellular_automata_algorithms = [
            "Majority rule CA",
            "Conway's Game of Life",
            "Langton's Ant",
            "Brian's Brain",
            "Wireworld"
        ]

        self.show_main_menu()

    def calculate_cell_size(self):
        """Calculate optimal cell size to maximize grid usage of available space"""
        if self.current_width <= 0 or self.current_height <= 0:
            return 10

        # Calculate maximum cell size that fits within canvas bounds
        max_cell_width = self.max_canvas_width // self.current_width
        max_cell_height = self.max_canvas_height // self.current_height

        # Use the smaller of the two to ensure both dimensions fit
        optimal_size = min(max_cell_width, max_cell_height)

        # Increased minimum and maximum cell sizes for better scaling
        min_cell_size = 2   # Minimum 2 pixels per cell
        max_cell_size = 50  # Increased maximum to 50 pixels per cell

        return max(min_cell_size, min(optimal_size, max_cell_size))

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
        # Bind event to update grid when width changes
        self.grid_width.bind('<KeyRelease>', self.on_grid_size_change)
        self.grid_width.bind('<FocusOut>', self.on_grid_size_change)

        tk.Label(fields_frame, text="Grid Height:", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(anchor="w", pady=(5, 2))
        self.grid_height = tk.Entry(fields_frame, font=("Arial", 10))
        self.grid_height.insert(0, "50")
        self.grid_height.pack(fill="x", pady=(0, 10))
        # Bind event to update grid when height changes
        self.grid_height.bind('<KeyRelease>', self.on_grid_size_change)
        self.grid_height.bind('<FocusOut>', self.on_grid_size_change)

        # Display current cell size info
        self.cell_size_label = tk.Label(
            fields_frame,
            text=f"Cell Size: {self.cell_size}px",
            font=("Arial", 9),
            bg="#e0e0e0",
            fg="#666666"
        )
        self.cell_size_label.pack(anchor="w", pady=(0, 10))

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

    def on_grid_size_change(self, event=None):
        """Handle grid size changes and update the visual representation"""
        try:
            new_width = int(self.grid_width.get())
            new_height = int(self.grid_height.get())

            # Validate input - cap at 300
            if new_width > 0 and new_height > 0 and new_width <= 300 and new_height <= 300:
                self.current_width = new_width
                self.current_height = new_height

                # Recalculate cell size based on new dimensions
                self.cell_size = self.calculate_cell_size()

                # Update cell size display
                if hasattr(self, 'cell_size_label'):
                    self.cell_size_label.config(text=f"Cell Size: {self.cell_size}px")

                # Update canvas size and redraw grid
                if hasattr(self, 'canvas'):
                    self.update_canvas_size()
                    self.draw_grid()
                    self.update_grid_info()

        except ValueError:
            # Invalid input, ignore
            pass

    def update_canvas_size(self):
        """Update canvas size to use maximum available space"""
        canvas_width = self.current_width * self.cell_size
        canvas_height = self.current_height * self.cell_size

        # Use the calculated size up to the maximum available space
        canvas_width = min(canvas_width, self.max_canvas_width)
        canvas_height = min(canvas_height, self.max_canvas_height)

        self.canvas.config(width=canvas_width, height=canvas_height)

    def update_grid_info(self):
        """Update the grid information display"""
        if hasattr(self, 'grid_info_label'):
            self.grid_info_label.config(
                text=f"Grid: {self.current_width}x{self.current_height} | Cell Size: {self.cell_size}px | Canvas: {self.current_width * self.cell_size}x{self.current_height * self.cell_size}"
            )

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

    def draw_grid(self):
        """Draw the entire grid with dynamic cell sizing"""
        self.canvas.delete("all")  # Clear canvas

        for row in range(self.current_height):
            for col in range(self.current_width):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Default empty cell (black)
                color = "black"

                # Only draw outline if cell size is large enough to see it
                outline_width = 1 if self.cell_size >= 3 else 0
                outline_color = "gray" if outline_width > 0 else "black"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=outline_color,
                    width=outline_width
                )

        # Draw a sample cell in the center to test
        center_row = self.current_height // 2
        center_col = self.current_width // 2
        self.draw_cell(center_row, center_col, True)

    def draw_cell(self, row, col, state):
        """Draw a single cell at the specified row and column"""
        # Validate coordinates
        if row < 0 or row >= self.current_height or col < 0 or col >= self.current_width:
            return

        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        color = "white" if state else "black"

        # Only draw outline if cell size is large enough to see it
        outline_width = 1 if self.cell_size >= 3 else 0
        outline_color = "gray" if outline_width > 0 else color

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline=outline_color,
            width=outline_width
        )

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

        # Calculate initial cell size and canvas dimensions
        self.cell_size = self.calculate_cell_size()
        canvas_width = min(self.current_width * self.cell_size, self.max_canvas_width)
        canvas_height = min(self.current_height * self.cell_size, self.max_canvas_height)

        # Create a frame to center the canvas
        canvas_frame = tk.Frame(content_frame, bg="#2d2d2d")
        canvas_frame.pack(fill="both", expand=True, pady=10)

        # Canvas for displaying the cellular automata - now much larger
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#1a1a1a",
            width=canvas_width,
            height=canvas_height,
            relief="sunken",
            borderwidth=2
        )
        self.canvas.pack(expand=True)  # Center the canvas in its frame

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

        # Grid info display - enhanced with more information
        self.grid_info_label = tk.Label(
            self.status_frame,
            text=f"Grid: {self.current_width}x{self.current_height} | Cell Size: {self.cell_size}px | Canvas: {canvas_width}x{canvas_height}",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#cccccc"
        )
        self.grid_info_label.pack()

        # Draw initial grid
        self.draw_grid()

    # Methods for Automata class integration
    def update_grid_from_automata(self, automata_grid):
        """Update the visual grid from an Automata object's grid"""
        self.canvas.delete("all")

        for row in range(self.current_height):
            for col in range(self.current_width):
                if hasattr(automata_grid, 'get'):
                    # Using FastGrid
                    state = automata_grid.get(col, row)
                else:
                    # Fallback for other grid types
                    state = False

                self.draw_cell(row, col, state)

    def get_grid_reference(self):
        """Return a reference that Automata can use to update the display"""
        return {
            'width': self.current_width,
            'height': self.current_height,
            'update_cell': self.draw_cell,
            'update_display': self.update_grid_from_automata,
            'cell_size': self.cell_size
        }

    def on_automata_selected(self, event):
        """Handle cellular automata type selection"""
        pass

    def start_simulation(self):
        """Start the cellular automata simulation"""
        self.status_label.config(text="Running")

    def pause_simulation(self):
        """Pause the simulation"""
        self.status_label.config(text="Paused")

    def reset_simulation(self):
        """Reset the simulation to initial state"""
        self.draw_grid()

    def step_simulation(self):
        """Execute a single step of the simulation"""
        pass

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CellularAutomataSimulator()
    app.run()
