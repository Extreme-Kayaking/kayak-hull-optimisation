import numpy as np
from .gp import GaussianProcessSurrogate
from sklearn.metrics import mean_squared_error
from typing import List, Optional

def create_gp(
    model: GaussianProcessSurrogate,
    X_train: np.ndarray,
    y_train: np.ndarray,
    column_order: List[str],
    X_test: Optional[np.ndarray] = None,
    y_test: Optional[np.ndarray] = None
) -> float:
    """
    Fits the GP model for the first time. 
    Returns RMSE if test data is provided, otherwise returns None.
    """
    try:
        # Exactly the logic from the loop
        model.fit(X_train, y_train, column_order)
        
        if X_test is not None and y_test is not None:
            mu, _ = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, mu))
            return rmse
            
    except Exception as e:
        print(f"  Err creating model: {e}")
        return np.nan

def update_gp(
    model: GaussianProcessSurrogate,
    X_new_total: np.ndarray,
    y_new_total: np.ndarray,
    column_order: List[str],
    X_test: Optional[np.ndarray] = None,
    y_test: Optional[np.ndarray] = None
) -> float:
    """
    Refits the GP model with new/updated data.
    Returns RMSE if test data is provided, otherwise returns None.
    """
    try:
        # Exactly the logic from the loop (re-fitting with the new total set)

        X_total = np.vstack([model.X_train, X_new_total]) if model.X_train is not None else X_new_total
        y_total = np.vstack([model.y_train, y_new_total]) if model.y_train is not None else y_new_total
        print(f"Fitting on {len(X_total)} samples")
        model.fit(X_total, y_total, column_order)
        
        if X_test is not None and y_test is not None:
            mu, _ = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, mu))
            return rmse

    except Exception as e:
        print(f"  Err updating model:")
        import traceback
        traceback.print_exc()
        return np.nan
