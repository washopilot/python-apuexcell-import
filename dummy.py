import pandas as pd


def merge_dataframes(dfA, dfB, column_names_C):
    """
    Merge DataFrames dfA and dfB into a new DataFrame dfC.

    Parameters:
    - dfA (pd.DataFrame): Source DataFrame with data organized by rows.
    - dfB (pd.DataFrame): DataFrame to be used for matching with dfA.
    - column_names_C (list): List containing column names for DataFrame dfC.

    Returns:
    - pd.DataFrame: Resulting DataFrame that combines information from dfA and dfB based on specified conditions.
    """
    # Create an empty DataFrame with specified columns
    dfC = pd.DataFrame(columns=column_names_C)

    # Iterate over the rows of dfA
    for index_A, row_A in dfA.iterrows():
        # Check if the row of dfA is included in any row of dfB
        matching_rows = dfB[dfB.apply(
            lambda row_B: row_B.isin(row_A).all(), axis=1)]

        if not matching_rows.empty:
            # Take the index of the first match
            index_B = matching_rows.index[0]
        else:
            # If no matches, assign None
            index_B = None

        # Get values of specified columns in column_names_C in dfA
        values_C = [row_A[col] for col in column_names_C[1:]]

        # Concatenate the result to dfC
        dfC = pd.concat([dfC, pd.DataFrame(
            [[index_B] + values_C], columns=column_names_C)], ignore_index=True)

    return dfC


# Data organized by rows
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

# Define the desired columns in dfC
column_names_C = ['Z', 'B', 'C']

# Call the function
dfC = merge_dataframes(dfA, dfB, column_names_C)

# Print the result
print(dfC)
