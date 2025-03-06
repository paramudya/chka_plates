import numpy as np

def smape(actual, predicted):
    """
    Calculate SMAPE (Symmetric Mean Absolute Percentage Error) given the actual and predicted values.
    
    Args:
        actual (numpy.ndarray): Array of actual values.
        predicted (numpy.ndarray): Array of predicted values.
        
    Returns:
        float: SMAPE value.
    """
    # Calculate absolute difference and sum of absolute values
    absolute_diff = np.abs(actual - predicted)
    sum_absolute = np.abs(actual) + np.abs(predicted)
    
    # Avoid division by zero
    mask = sum_absolute != 0
    
    # Calculate SMAPE
    smape = np.mean(200 * (absolute_diff[mask] / sum_absolute[mask]))
    
    return smape