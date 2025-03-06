import pandas as pd

data_dir='data'
def check_test(df, id_column='id', target='price'):
    """
    Validate a DataFrame against specific criteria:
    - Must have exactly 100 rows
    - Price column must contain only numeric values
    - ID values must be within specified range
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to validate
    id_min : int, optional
        Minimum acceptable ID value (default 0)
    id_max : int, optional
        Maximum acceptable ID value (default 1000)
    id_column : str, optional
        Name of the ID column (default 'id')
    price_column : str, optional
        Name of the price column (default 'price')
        
    Returns:
    --------
    dict
        Dictionary containing validation results with the following keys:
        - 'valid': Boolean indicating if all checks passed
        - 'errors': List of error messages (empty if all checks passed)
    """
    idx = pd.read_csv(f'{data_dir}/sample_submission.csv')['id']

    id_min, id_max = min(idx),max(idx)
    errors = []
    
    # Check 1: DataFrame must have exactly 100 rows
    row_count = len(df)
    if row_count != len(idx):
        errors.append(f"DataFrame has {row_count} rows, expected 100")
    
    # Check 2: Price column must contain only numeric values
    if target not in df.columns:
        errors.append(f"Price column '{target}' not found in DataFrame")
    else:
        # Check if all values in price column are numeric
        non_numeric = df[~pd.to_numeric(df[target], errors='coerce').notna()]
        if len(non_numeric) > 0:
            error_indices = non_numeric.index.tolist()
            errors.append(f"Non-numeric values found in price column at indices: {error_indices}")
            print(df.head(5))
    
    # Check 3: ID values must be within specified range
    if id_column not in df.columns:
        errors.append(f"ID column '{id_column}' not found in DataFrame")
    else:
        out_of_range = df[(df[id_column] < id_min) | (df[id_column] > id_max)]
        if len(out_of_range) > 0:
            error_indices = out_of_range.index.tolist()
            errors.append(f"ID values out of range [{id_min}, {id_max}] at indices: {error_indices}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def submit(test_df: pd.DataFrame, filename: str):
    check_res = check_test(test_df)
    if not check_res['valid']:
        print('test data invalid:\n\n', check_res['errors'])
    else:
        sub=test_df[['id','price']]
        sub.to_csv(f'{data_dir}/subs/{filename}.csv',index=0)
        print(f'test data valid and saved as {filename}.csv')
