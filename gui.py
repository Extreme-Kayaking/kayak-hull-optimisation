import customtkinter as ctk
from dataclasses import dataclass, fields
import sys

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue") 

class WeightSelector:
    """
    A modern GUI class to select optimization weights for result parameters.
    """
    def __init__(self, target_class, title="Optimization Configuration"):
        self.target_class = target_class
        self.title_text = title
        self.sliders = {}  
        self.final_weights = {}
        
        if hasattr(target_class, "__dataclass_fields__"):
            self.params = [f.name for f in fields(target_class)]
        elif hasattr(target_class, "__annotations__"):
            self.params = [k for k in target_class.__annotations__ if not k.startswith('_')]
        else:

            self.params = [k for k in dir(target_class) if not k.startswith('_') and not callable(getattr(target_class, k))]

    def _create_row(self, parent, param_name, row_idx):
        """Helper to create one label + slider + value display row."""
        
        label = ctk.CTkLabel(parent, text=param_name.replace("_", " ").title(), font=("Roboto", 14, "bold"))
        label.grid(row=row_idx, column=0, padx=20, pady=10, sticky="w")

        val_var = ctk.IntVar(value=0)
        self.sliders[param_name] = val_var

        val_label = ctk.CTkLabel(parent, text="0", width=30, font=("Roboto Mono", 14))
        val_label.grid(row=row_idx, column=2, padx=(10, 20), pady=10)

        def update_label(value):
            val_label.configure(text=f"{int(value)}")
            
        slider = ctk.CTkSlider(
            parent, 
            from_=0, 
            to=10, 
            number_of_steps=10, 
            variable=val_var, 
            command=update_label,
            width=300
        )
        slider.grid(row=row_idx, column=1, padx=10, pady=10)

    def run(self):
        """
        Builds the window, pauses execution until user finishes, 
        and returns the dictionary.
        """
 
        app = ctk.CTk()
        app.title(self.title_text)
        app.geometry("600x500")
        
        app.grid_columnconfigure(0, weight=1)
        app.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(app)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header = ctk.CTkLabel(header_frame, text=f"Configure: {self.target_class.__name__}", font=("Roboto", 20, "bold"))
        header.pack(pady=5)
        sub = ctk.CTkLabel(header_frame, text="Set importance (0=Ignore, 10=Critical)", text_color="gray")
        sub.pack(pady=(0, 5))

        scroll_frame = ctk.CTkScrollableFrame(app, label_text="Parameters")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for idx, param in enumerate(self.params):
            self._create_row(scroll_frame, param, idx)

        def on_confirm():

            for param, var in self.sliders.items():
                self.final_weights[param] = var.get()
            app.destroy() 

        btn = ctk.CTkButton(app, text="Confirm Weights", command=on_confirm, height=50, font=("Roboto", 16, "bold"))
        btn.pack(fill="x", padx=20, pady=20)

        app.mainloop()
        
        return self.final_weights

if __name__ == "__main__":
    
    @dataclass
    class GP_Result:
        hydro_drag: float
        static_stability: float
        material_cost: float
        passenger_comfort: float
        fuel_efficiency: float

    gui = WeightSelector(GP_Result)
    
    print("Waiting for user input via GUI...")
    
    user_weights = gui.run()
    
    print("\n--- User Selected Weights ---")
    if not user_weights:
        print("User closed window without confirming.")
    else:

        import json
        print(json.dumps(user_weights, indent=4))
        
        max_param = max(user_weights, key=user_weights.get)
        print(f"\nOptimization Focus: The user cares most about '{max_param}'")