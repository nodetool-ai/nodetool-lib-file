from pydantic import BaseModel, Field
import typing
from typing import Any
import nodetool.metadata.types as types
from nodetool.dsl.graph import GraphNode


class ConvertToMarkdown(GraphNode):
    """
    Converts various document formats to markdown using MarkItDown.
    markdown, convert, document

    Use cases:
    - Convert Word documents to markdown
    - Convert Excel files to markdown tables
    - Convert PowerPoint to markdown content
    """

    document: types.DocumentRef | GraphNode | tuple[GraphNode, str] = Field(default=types.DocumentRef(type='document', uri='', asset_id=None, data=None), description='The document to convert to markdown')

    @classmethod
    def get_node_type(cls): return "lib.file.markitdown.ConvertToMarkdown"


