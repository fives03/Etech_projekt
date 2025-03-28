import tkinter as tk
from tkinter import ttk
import wave_simulation as ws
import subprocess
import sys


def create_input_fields():
    root = tk.Tk()
    root.title("Parameter Input")

    # Create main frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill="both", expand=True)

    # Input field configuration
    parameters = [
        ("Voltage", "V"),
        ("Wave Resistor", "Ω"),
        ("Reflection Resistor 1", "Ω"),
        ("Reflection Resistor 2", "Ω"),
        ("Length", "m"),
        ("Capacity per m", "pF/m"),
        ("Periods", ""),
    ]

    # Create validation command
    def validate_number(input):
        if input == "":  # Allow empty field
            return True
        try:
            float(input)
            return True
        except ValueError:
            return input == "-"  # Allow minus sign for negative numbers

    vcmd = (root.register(validate_number), "%P")

    # Create input fields
    entries = {}
    for row, (label, unit) in enumerate(parameters):
        # Create label
        ttk.Label(main_frame, text=f"{label}:").grid(
            row=row, column=0, sticky="e", padx=5, pady=5
        )

        # Create entry field
        entry = ttk.Entry(main_frame, validate="key", validatecommand=vcmd)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        # Create unit label
        ttk.Label(main_frame, text=unit).grid(
            row=row, column=2, sticky="w", padx=5, pady=5
        )

        entries[label] = entry

    # Configure grid weights
    main_frame.columnconfigure(1, weight=1)

    # Add submit button
    def show_values():
        #ws.simulate_func()
        for param, entry in entries.items():
            value = entry.get()
            print(f"{param}: {value if value else 'Empty'}")

    ttk.Button(main_frame, text="Submit", command=show_values).grid(
        row=len(parameters), column=1, pady=10
    )

    root.mainloop()


if __name__ == "__main__":
    create_input_fields()
