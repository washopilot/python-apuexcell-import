import numpy as np
import pandas as pd


def merge_dataframes(dfA, dfB, columns_to_show, result_column_name='Z'):
    """
    Merge two dataframes and add a new column to dfA based on the specified conditions.

    Parameters:
    - dfA (pd.DataFrame): The first dataframe.
    - dfB (pd.DataFrame): The second dataframe.
    - columns_to_show (list): A list of column names to include in the resulting dataframe.
    - result_column_name (str): The name of the new column to be added to dfA.

    Returns:
    pd.DataFrame: A new dataframe with specified columns showing the merged data.
    """

    # Create a new DataFrame dfC based on dfA
    dfC = dfA.copy()

    # Add a new column initialized with NaN
    dfC[result_column_name] = np.nan

    # Iterate over the rows of dfC and check the conditions
    for idx, row in dfC.iterrows():
        # Check if any row of dfB is included in the current row of dfA
        matching_indices = dfB.index[dfB.isin(row.values).all(axis=1)].tolist()

        if matching_indices:
            # If there are matches, assign the first found index to the new column
            dfC.at[idx, result_column_name] = matching_indices[0]

    # Preserve the original indices of dfA in dfC
    dfC.index = dfA.index

    # Select only the specified columns
    dfC_filtered = dfC[columns_to_show]

    return dfC_filtered


# Example usage:
# Assuming dfA, dfB, and columns_to_show are defined elsewhere
data_A = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
column_names_A = ['A', 'B', 'C']
dfA = pd.DataFrame(data_A, columns=column_names_A)

data_B = [
    [1, 4],
    [2, 5]
]
column_names_B = ['A', 'B']
# Indices
indices_B = [20, 21]
dfB = pd.DataFrame(data_B, columns=column_names_B, index=indices_B)

columns_to_show = ['C', 'Z']  # Add 'Z' to the columns to show
result_df = merge_dataframes(dfA, dfB, columns_to_show, result_column_name='Z')
print(result_df)
