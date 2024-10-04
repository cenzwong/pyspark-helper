import itertools
from functools import reduce

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F


def create_map_from_dict(dict_: dict[str, int]) -> Column:
    """
    Generates a PySpark map column from a provided dictionary.

    This function converts a dictionary into a PySpark map column, with each key-value pair represented as a literal in the map.

    Parameters:
        dict_ (Dict[str, int]): A dictionary with string keys and integer values.

    Returns:
        Column: A PySpark Column object representing the created map.

    Examples:
        >>> dict_ = {"a": 1, "b": 2}
        >>> map_column = create_map_from_dict(dict_)
    """

    return F.create_map(list(map(F.lit, itertools.chain(*dict_.items()))))


def join_dataframes_on_column(
    column_name: str, *dataframes: DataFrame | list[DataFrame]
) -> DataFrame:
    """
    Joins a list of DataFrames on a specified column using an outer join.

    Args:
        column_name (str): The column name to join on.
        *dataframes (DataFrame): A list of DataFrames to join.

    Returns:
        DataFrame: The resulting DataFrame after performing the outer joins.
    """

    if not dataframes:
        raise ValueError("At least one DataFrame must be provided")

    if isinstance(dataframes[0], list):
        dataframes = dataframes[0]

    # Check if all DataFrames have the specified column
    if not all(column_name in df.columns for df in dataframes):
        raise ValueError(f"Column '{column_name}' not found in all DataFrames")

    # Use reduce to perform the outer join on all DataFrames
    joined_df = reduce(
        lambda df1, df2: df1.join(df2, on=column_name, how="outer"), dataframes
    )
    return joined_df


def union_dataframes(*dataframes: DataFrame | list[DataFrame]) -> DataFrame:
    """
    Unions a list of DataFrames.

    Args:
        *dataframes (DataFrame): A list of DataFrames to union.

    Returns:
        DataFrame: The resulting DataFrame after performing the unions.
    """
    # TODO: Check on the schema, if not align, raise error

    if not dataframes:
        raise ValueError("At least one DataFrame must be provided")

    # Flatten the list if the first argument is a list of DataFrames
    if isinstance(dataframes[0], list):
        dataframes = dataframes[0]

    return reduce(lambda df1, df2: df1.union(df2), dataframes)
