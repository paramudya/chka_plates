import numpy as np

class EachSection:
    """
    A class that encodes categorical 'section' features by mapping them to the mean/most differing target value.
    Compatible with scikit-learn pipeline API with fit and transform methods.
    """
    def __init__(self, section_col_prefix='section', target_col='price'):
        """
        Initialize the encoder.
        
        Parameters
        ----------
        section_col_prefix : str, default='section'
            The prefix of the section column(s) to be encoded
        target_col : str, default='price'
            The name of the target column
        """
        self.section_col_prefix = section_col_prefix
        self.target_col = target_col
        self.mappings = {}
        
    def fit(self, X, y):
        """
        Fit the encoder by computing mean target values for each section.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The feature matrix
        y : pandas.Series or dict
            The target values, can be a Series or dict mapping IDs to values
        
        Returns
        -------
        self : returns an instance of self
        """
        # Create a working copy of X
        train = X.copy()
        
        # Add target values to the training data
        if isinstance(y, dict):
            train[self.target_col] = X['id'].map(y)
        else:
            train[self.target_col] = y
        
        # Find all section columns
        section_cols = [col for col in X.columns if col.startswith(self.section_col_prefix)]
        
        # Compute mean target for each section value
        for section_col in section_cols:
            self.mappings[section_col] = train.groupby(section_col)[self.target_col].mean().sort_values()
            
        return self
    
    def transform(self, X, sections='all', method='mean'):
        """
        Transform the data by replacing section values with their corresponding mean target values.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The feature matrix to transform
        sections : iter/str, default = 'all'
            Which section to be considered in the calculation (minimum of 1 and maximum of number of section columns)
            
        Returns
        -------
        X_transformed : pandas.DataFrame
            The transformed feature matrix
        """
        # Create a copy to avoid modifying the original data
        X_transformed = X.copy()

        if sections == 'all':
            sections = list(self.mappings.keys())
        
        # Apply the mapping to each section column
        for section_col, mapping in self.mappings.items():
            if section_col in sections:
                
                # no weights applied, at least not now                
                X_transformed[self.target_col + '_' + section_col] = X_transformed[section_col].map(mapping)
        p = X_transformed[[self.target_col + '_' + str(sect) for sect in sections]]
        if method=='mean':
            X_transformed['price']=p.mean(axis=1)
        elif method=='most differing':
            temp=[]
            print(type(self.mappings['section 1']),self.mappings['section 1'].values)
            mean = np.array([price for series_section_dct in self.mappings.values() for price in series_section_dct.values]).mean()
            for _,row in p.iterrows():
                most_differing=mean
                for col in p.columns:
                    if abs(row[col]-mean)>abs(most_differing-mean):
                        most_differing=row[col]
                # after going through all intended sctions
                temp.append(most_differing)
            # after going thru rows
            X_transformed['price']=temp

        return X_transformed

# def each_section(X, y, which_sect):
#     train = X
#     train['price']=X['id'].map(y)

#     # fit
#     mean_section_price = train.groupby(f'section {which_sect}')['price'].mean().sort_values()
#     # transform
#     test['price'] = test[f'section {which_sect}'].map(mean_section_price)
#     return test

