import pandas as pd # Optional, but good for visualizing
import numpy as np
import pickle
from typing import Tuple, Dict, Any, List


def get_category_heuristic(param_name: str) -> str:
    """Fallback logic to guess category if not in dictionary."""
    print("This should not be called")
    param_lower = param_name.lower()
    
    # Simple heuristics
    if 'speed' in param_lower or param_lower == 'v':
        return 'speed'
    if any(x in param_lower for x in ['angle', 'heel', 'yaw', 'leeway']):
        return 'angles'
    
    # Default fallback
    return 'shape'

def default_param_categories() -> Dict[str, str]:
    return {'heel': 'angles', 'length': 'shape', 'beam': 'shape', 'density': 'shape', 'draft': 'shape', 'section_shape_exponent': 'shape'}

def load_simulation_data(filepath: str) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Loads simulation data from a pickle file.
    Returns the X matrix, y matrix, and the list of column names corresponding to X.
    """

    raw_inputs = []
    raw_outputs = []

    with open(filepath, 'rb') as f:
        while True:
            try:
                row_data = pickle.load(f)
                
                # Assuming row_data is a tuple like (input_dict, output_tuple)
                input_data = row_data[0]
                output_data = row_data[1]
                assert len(output_data) == 2, f"length of output is wrong {len(output_data)}, output is {output_data}"
                assert len(output_data[0]) == 3, "length of output 1 is wrong"
                assert len(output_data[1]) == 2, "length of output 2 is wrong"
                # Ensure input is a dictionary (convert if it's a tuple of pairs)
                if not isinstance(input_data, dict):
                    input_data = dict(input_data)
                
                flat_outputs = []
                for group in output_data:

                    for val in group:
                        flat_outputs.append(float(val))

                raw_inputs.append(input_data)
                raw_outputs.append(flat_outputs)
                
            except EOFError:
                break
            except Exception as e:
                print(f"Skipping corrupted line: {e}")
                continue
    
    if not raw_inputs:
        print("No data loaded.")
        return np.array([]), np.array([]), []

    # 1. Determine the column order based on the first row's keys
    #    This ensures consistency for the entire X matrix construction.
    feature_order = list(raw_inputs[0].keys())
    
    print("-" * 40)
    print(f"Loaded {len(raw_inputs)} rows.")
    print(f"Data Column Order: {feature_order}")
    print("-" * 40)

    # 2. Build X matrix enforcing the specific feature_order
    X_list = []
    for d in raw_inputs:
        # Extract values in the exact order of feature_order
        row = [float(d[k]) for k in feature_order]
        X_list.append(row)

    X = np.array(X_list, dtype=np.float64)
    y = np.array(raw_outputs, dtype=np.float64)
        # --- DIAGNOSTIC CHECK START ---
    print("\n=== SHAPE VERIFICATION ===")

    # 1. Basic Shape Check
    print(f"X Shape (Inputs):  {X.shape}")
    print(f"y Shape (Outputs): {y.shape}")

    # 2. Row Alignment Check
    if X.shape[0] != y.shape[0]:
        print(f"❌ ALIGNMENT ERROR: X has {X.shape[0]} rows but y has {y.shape[0]} rows.")
    else:
        print(f"✅ Alignment OK: Both have {X.shape[0]} samples.")

    # 3. Flattening & Type Check for y
    # The GP will fail if y is 'object' type (meaning it contains lists/tuples inside cells)
    if y.dtype == object:
        print("❌ TYPE ERROR: y is an object array. It likely contains nested tuples.")
        print("   Example row:", y[0])
        print("   FIX NEEDED: y must be flattened into floats.")
    else:
        # If it is float/int, we check the columns
        print(f"✅ Type OK: y is {y.dtype}")
        
        # We expect 5 columns based on your tuple structure ((a,b,c), (d,e))
        expected_cols = 5
        if y.shape[1] == expected_cols:
            print(f"✅ Dimensions OK: y has {y.shape[1]} output columns (matches 3+2 structure).")
        else:
            print(f"⚠️ WARNING: y has {y.shape[1]} columns. Expected {expected_cols}?")

    print("==========================\n")
    # --- DIAGNOSTIC CHECK END ---
    return X, y, feature_order