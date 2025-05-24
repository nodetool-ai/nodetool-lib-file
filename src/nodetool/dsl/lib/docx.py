from pydantic import BaseModel, Field
import typing
from typing import Any
import nodetool.metadata.types
import nodetool.metadata.types as types
from nodetool.dsl.graph import GraphNode


class AddHeading(GraphNode):
    """
    Adds a heading to the document
    document, docx, heading, format
    """

    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DocumentRef(type="document", uri="", asset_id=None, data=None),
        description="The document to add the heading to",
    )
    text: str | GraphNode | tuple[GraphNode, str] = Field(
        default="", description="The heading text"
    )
    level: int | GraphNode | tuple[GraphNode, str] = Field(
        default=1, description="Heading level (1-9)"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.AddHeading"


class AddImage(GraphNode):
    """
    Adds an image to the document
    document, docx, image, format
    """

    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DocumentRef(type="document", uri="", asset_id=None, data=None),
        description="The document to add the image to",
    )
    image: types.ImageRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.ImageRef(type="image", uri="", asset_id=None, data=None),
        description="The image to add",
    )
    width: float | GraphNode | tuple[GraphNode, str] = Field(
        default=0, description="Image width in inches"
    )
    height: float | GraphNode | tuple[GraphNode, str] = Field(
        default=0, description="Image height in inches"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.AddImage"


class AddPageBreak(GraphNode):
    """
    Adds a page break to the document
    document, docx, format, layout
    """

    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DocumentRef(type="document", uri="", asset_id=None, data=None),
        description="The document to add the page break to",
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.AddPageBreak"


import nodetool.nodes.lib.docx


class AddParagraph(GraphNode):
    """
    Adds a paragraph of text to the document
    document, docx, text, format
    """

    ParagraphAlignment: typing.ClassVar[type] = (
        nodetool.nodes.lib.docx.ParagraphAlignment
    )
    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DocumentRef(type="document", uri="", asset_id=None, data=None),
        description="The document to add the paragraph to",
    )
    text: str | GraphNode | tuple[GraphNode, str] = Field(
        default="", description="The paragraph text"
    )
    alignment: nodetool.nodes.lib.docx.ParagraphAlignment = Field(
        default=nodetool.nodes.lib.docx.ParagraphAlignment.LEFT,
        description="Text alignment",
    )
    bold: bool | GraphNode | tuple[GraphNode, str] = Field(
        default=False, description="Make text bold"
    )
    italic: bool | GraphNode | tuple[GraphNode, str] = Field(
        default=False, description="Make text italic"
    )
    font_size: int | GraphNode | tuple[GraphNode, str] = Field(
        default=12, description="Font size in points"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.AddParagraph"


class AddTable(GraphNode):
    """
    Adds a table to the document
    document, docx, table, format
    """

    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DocumentRef(type="document", uri="", asset_id=None, data=None),
        description="The document to add the table to",
    )
    data: types.DataframeRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DataframeRef(
            type="dataframe", uri="", asset_id=None, data=None, columns=None
        ),
        description="The data to add to the table",
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.AddTable"


class CreateDocument(GraphNode):
    """
    Creates a new Word document
    document, docx, file, create
    """

    @classmethod
    def get_node_type(cls):
        return "lib.docx.CreateDocument"


class LoadWordDocument(GraphNode):
    """
    Loads a Word document from disk
    document, docx, file, load, input
    """

    path: str | GraphNode | tuple[GraphNode, str] = Field(
        default="", description="Path to the document to load"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.LoadWordDocument"


class SaveDocument(GraphNode):
    """
    Writes the document to a file
    document, docx, file, save, output
    """

    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DocumentRef(type="document", uri="", asset_id=None, data=None),
        description="The document to write",
    )
    path: types.FilePath | GraphNode | tuple[GraphNode, str] = Field(
        default=types.FilePath(type="file_path", path=""),
        description="The folder to write the document to.",
    )
    filename: str | GraphNode | tuple[GraphNode, str] = Field(
        default="",
        description="\n        The filename to write the document to.\n        You can use time and date variables to create unique names:\n        %Y - Year\n        %m - Month\n        %d - Day\n        %H - Hour\n        %M - Minute\n        %S - Second\n        ",
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.SaveDocument"


class SetDocumentProperties(GraphNode):
    """
    Sets document metadata properties
    document, docx, metadata, properties
    """

    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(
        default=types.DocumentRef(type="document", uri="", asset_id=None, data=None),
        description="The document to modify",
    )
    title: str | GraphNode | tuple[GraphNode, str] = Field(
        default="", description="Document title"
    )
    author: str | GraphNode | tuple[GraphNode, str] = Field(
        default="", description="Document author"
    )
    subject: str | GraphNode | tuple[GraphNode, str] = Field(
        default="", description="Document subject"
    )
    keywords: str | GraphNode | tuple[GraphNode, str] = Field(
        default="", description="Document keywords"
    )

    @classmethod
    def get_node_type(cls):
        return "lib.docx.SetDocumentProperties"
