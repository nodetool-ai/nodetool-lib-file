from pydantic import BaseModel, Field
import typing
from typing import Any
import nodetool.metadata.types
import nodetool.metadata.types as types
from nodetool.dsl.graph import GraphNode


class AutoFitColumns(GraphNode):
    """
    Automatically adjusts column widths to fit content.
    excel, format, columns

    Use cases:
    - Improve spreadsheet readability
    - Professional presentation
    """

    workbook: types.ExcelRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.ExcelRef(type="excel", uri="", asset_id=None, data=None),
        description="The Excel workbook to format",
    )
    sheet_name: str | GraphNode | tuple[GraphNode, str] = Field(
        default="Sheet1", description="Target worksheet name"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.excel.AutoFitColumns"


class CreateWorkbook(GraphNode):
    """
    Creates a new Excel workbook.
    excel, workbook, create

    Use cases:
    - Initialize new Excel files
    - Start spreadsheet creation workflows
    """

    sheet_name: str | GraphNode | tuple[GraphNode, str] = Field(
        default="Sheet1", description="Name for the first worksheet"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.excel.CreateWorkbook"


class DataFrameToExcel(GraphNode):
    """
    Writes a DataFrame to an Excel worksheet.
    excel, dataframe, export

    Use cases:
    - Export data analysis results
    - Create reports from data
    """

    workbook: types.ExcelRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.ExcelRef(type="excel", uri="", asset_id=None, data=None),
        description="The Excel workbook to write to",
    )
    dataframe: types.DataframeRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DataframeRef(
            type="dataframe", uri="", asset_id=None, data=None, columns=None
        ),
        description="DataFrame to write",
    )
    sheet_name: str | GraphNode | tuple[GraphNode, str] = Field(
        default="Sheet1", description="Target worksheet name"
    )
    start_cell: str | GraphNode | tuple[GraphNode, str] = Field(
        default="A1", description="Starting cell for data"
    )
    include_header: bool | GraphNode | tuple[GraphNode, str] = Field(
        default=True, description="Include column headers"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.excel.DataFrameToExcel"


class ExcelToDataFrame(GraphNode):
    """
    Reads an Excel worksheet into a pandas DataFrame.
    excel, dataframe, import

    Use cases:
    - Import Excel data for analysis
    - Process spreadsheet contents
    """

    workbook: types.ExcelRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.ExcelRef(type="excel", uri="", asset_id=None, data=None),
        description="The Excel workbook to read from",
    )
    sheet_name: str | GraphNode | tuple[GraphNode, str] = Field(
        default="Sheet1", description="Source worksheet name"
    )
    has_header: bool | GraphNode | tuple[GraphNode, str] = Field(
        default=True, description="First row contains headers"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.excel.ExcelToDataFrame"


class FormatCells(GraphNode):
    """
    Applies formatting to a range of cells.
    excel, format, style

    Use cases:
    - Highlight important data
    - Create professional looking reports
    """

    workbook: types.ExcelRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.ExcelRef(type="excel", uri="", asset_id=None, data=None),
        description="The Excel workbook to format",
    )
    sheet_name: str | GraphNode | tuple[GraphNode, str] = Field(
        default="Sheet1", description="Target worksheet name"
    )
    cell_range: str | GraphNode | tuple[GraphNode, str] = Field(
        default="A1:B10", description="Cell range to format (e.g. 'A1:B10')"
    )
    bold: bool | GraphNode | tuple[GraphNode, str] = Field(
        default=False, description="Make text bold"
    )
    background_color: str | GraphNode | tuple[GraphNode, str] = Field(
        default="FFFF00",
        description="Background color in hex format (e.g. 'FFFF00' for yellow)",
    )
    text_color: str | GraphNode | tuple[GraphNode, str] = Field(
        default="000000", description="Text color in hex format"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.excel.FormatCells"


class SaveWorkbook(GraphNode):
    """
    Saves an Excel workbook to disk.
    excel, save, export

    Use cases:
    - Export final spreadsheet
    - Save work in progress
    """

    workbook: types.ExcelRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.ExcelRef(type="excel", uri="", asset_id=None, data=None),
        description="The Excel workbook to save",
    )
    folder: types.FilePath | GraphNode | tuple[GraphNode, str] = Field(
        default=types.FilePath(type="file_path", path=""),
        description="The folder to save the file to.",
    )
    filename: str | GraphNode | tuple[GraphNode, str] = Field(
        default="",
        description="\n        The filename to save the file to.\n        You can use time and date variables to create unique names:\n        %Y - Year\n        %m - Month\n        %d - Day\n        %H - Hour\n        %M - Minute\n        %S - Second\n        ",
    )

    @classmethod
    def get_node_type(cls):
        return "lib.excel.SaveWorkbook"
