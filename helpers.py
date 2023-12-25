import pandas as pd
from openpyxl.worksheet.worksheet import Worksheet


def process_sheet(sheet_data, labels=['EQUIPO', 'MANO DE OBRA']):
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
