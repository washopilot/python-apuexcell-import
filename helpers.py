import numpy as np
import pandas as pd


def process_sheet_between_tags(sheet_data, labels=['EQUIPO', 'MANO DE OBRA']):
    """
    This function processes a given worksheet data and returns a subset of the data based on the provided tags.

    Parameters
    ----------
    sheet_data : pandas.DataFrame
        The worksheet data to be processed.
    labels : list, optional
        The list of tags to be used for finding the start and end indices of the data subset, by default ['EQUIPMENT', 'LABOR']

    Returns
    -------
    pandas.DataFrame
        The processed worksheet data.

    Raises
    ------
    ValueError
        If the provided tags are not found in the worksheet data.

    """
    # Find the indices of rows using the provided labels
    label_indices = sheet_data[sheet_data[1].isin(labels)].index

    # Check if both labels were found
    if len(label_indices) == 2:
        # Create a subset of the DataFrame from the first label to the second label
        sheet_data = sheet_data.loc[label_indices[0] + 1: label_indices[1] - 2]

        # Remove rows and columns completely filled with NaN
        sheet_data = sheet_data.dropna(
            axis=0, how='all').dropna(axis=1, how='all')

        # Take the first row as headers
        new_headers = sheet_data.iloc[0]

        # Remove the first row from the original DataFrame
        sheet_data = sheet_data[1:]

        # Assign the new headers to the original DataFrame
        sheet_data.columns = new_headers

    else:
        raise ValueError("Both labels not found in the worksheet data.")

    sheet_data.columns.name = None
    return sheet_data


def clean_and_sort_dataframe(df, column_name='DESCRIPCIÓN', start_index=1):
    """
    Clean and sort a DataFrame by removing duplicates, dropping NaN values,
    and sorting based on the specified column.

    Parameters:
    - df: pandas DataFrame
        The input DataFrame to be cleaned and sorted.
    - column_name: str, default='DESCRIPCIÓN'
        The column based on which the DataFrame should be sorted.
    - start_index: int, default=1
        The starting index value for the DataFrame.

    Returns:
    - cleaned_df: pandas DataFrame
        The cleaned and sorted DataFrame.
    """
    # Drop duplicates, drop NaN values, and sort the DataFrame
    cleaned_df = df.drop_duplicates().dropna(
        axis=0, how='all').sort_values(by=column_name, ascending=True)

    # Reset the index starting from the specified value
    new_index = range(start_index, start_index + len(cleaned_df))
    cleaned_df = cleaned_df.set_index(pd.Index(new_index))

    return cleaned_df


def merge_dataframes(dfA, dfB, columns_to_show, result_column_name='CODIGO'):
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
            dfC.at[idx, result_column_name] = int(matching_indices[0])

    # Convert the result_column_name to a numeric type (float)
    dfC[result_column_name] = pd.to_numeric(dfC[result_column_name], errors='coerce')

    # Fill NaN with a placeholder, and then convert the entire column to int
    placeholder = -1  # Use an arbitrary placeholder for NaN values
    dfC[result_column_name] = dfC[result_column_name].fillna(placeholder).astype(int)

    # Replace the placeholder back to NaN
    dfC[result_column_name] = dfC[result_column_name].replace(placeholder, np.nan)

    # Select only the specified columns
    dfC_filtered = dfC[columns_to_show]

    return dfC_filtered

