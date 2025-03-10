import io
from io import BytesIO
import pdfplumber
from typing import List, Optional, Any
from pydantic import Field
from nodetool.workflows.base_node import BaseNode
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.metadata.types import DocumentRef, ImageRef, DataframeRef, ColumnDef


class ExtractText(BaseNode):
    """
    Extract text content from a PDF file.
    pdf, text, extract

    Use cases:
    - Convert PDF documents to plain text
    - Extract content for analysis
    - Enable text search in PDF documents
    """

    pdf: DocumentRef = Field(
        default=DocumentRef(), description="The PDF file to extract text from"
    )
    start_page: int = Field(
        default=0, description="The start page to extract. 0-based indexing"
    )
    end_page: int = Field(
        default=4, description="The end page to extract. -1 for all pages"
    )

    async def process(self, context: ProcessingContext) -> str:
        pdf_data = await context.asset_to_bytes(self.pdf)
        text = []

        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            page_range = range(
                self.start_page,
                len(pdf.pages) if self.end_page == -1 else self.end_page,
            )
            for i in page_range:
                if i < 0 or i >= len(pdf.pages):
                    continue
                page = pdf.pages[i]
                text.append(page.extract_text(x_tolerance=2, y_tolerance=2))

        return "\n\n".join(text)


class ExtractImages(BaseNode):
    """
    Extract images from a PDF file.
    pdf, image, extract

    Use cases:
    - Extract embedded images from PDF documents
    - Save PDF images as separate files
    - Process PDF images for analysis
    """

    pdf: DocumentRef = Field(description="The PDF file to extract images from")
    start_page: int = Field(default=0, description="The start page to extract")
    end_page: int = Field(default=4, description="The end page to extract")

    async def process(self, context: ProcessingContext) -> List[ImageRef]:
        pdf_data = await context.asset_to_bytes(self.pdf)
        images = []

        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            page_range = range(
                self.start_page,
                len(pdf.pages) if self.end_page == -1 else self.end_page,
            )
            for i in page_range:
                if i < 0 or i >= len(pdf.pages):
                    continue
                page = pdf.pages[i]
                for image in page.images:
                    image_bytes = io.BytesIO(image["stream"].get_data())
                    images.append(
                        await context.image_from_bytes(image_bytes.getvalue())
                    )

        return images


class GetPageCount(BaseNode):
    """
    Get the total number of pages in a PDF file.
    pdf, pages, count

    Use cases:
    - Check document length
    - Plan batch processing
    """

    pdf: DocumentRef = Field(description="The PDF file to analyze")

    async def process(self, context: ProcessingContext) -> int:
        pdf_data = await context.asset_to_bytes(self.pdf)
        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            return len(pdf.pages)


class ExtractPageMetadata(BaseNode):
    """
    Extract metadata from PDF pages like dimensions, rotation, etc.
    pdf, metadata, pages

    Use cases:
    - Analyze page layouts
    - Get page dimensions
    - Check page orientations
    """

    pdf: DocumentRef = Field(description="The PDF file to analyze")
    start_page: int = Field(
        default=0, description="The start page to extract. 0-based indexing"
    )
    end_page: int = Field(
        default=4, description="The end page to extract. -1 for all pages"
    )

    async def process(self, context: ProcessingContext) -> List[dict]:
        pdf_data = await context.asset_to_bytes(self.pdf)
        metadata = []

        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            page_range = range(
                self.start_page,
                len(pdf.pages) if self.end_page == -1 else self.end_page,
            )
            for i in page_range:
                if i < 0 or i >= len(pdf.pages):
                    continue
                page = pdf.pages[i]
                metadata.append(
                    {
                        "page_number": i + 1,
                        "width": page.width,
                        "height": page.height,
                        "rotation": page.rotation,
                        "bbox": page.bbox,
                    }
                )

        return metadata


class ExtractTables(BaseNode):
    """
    Extract tables from a PDF file into dataframes.
    pdf, tables, dataframe, extract

    Use cases:
    - Extract tabular data from PDF documents
    - Convert PDF tables to structured data formats
    - Process PDF tables for analysis
    - Import PDF reports into data analysis pipelines
    """

    pdf: DocumentRef = Field(
        default=DocumentRef(), description="The PDF document to extract tables from"
    )

    start_page: int = Field(
        default=0,
        description="First page to extract tables from (0-based, None for first page)",
    )

    end_page: int = Field(
        default=4,
        description="Last page to extract tables from (0-based, None for last page)",
    )

    table_settings: dict = Field(
        default={
            "vertical_strategy": "text",
            "horizontal_strategy": "text",
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 3,
            "min_words_horizontal": 1,
            "keep_blank_chars": False,
            "text_tolerance": 3,
            "text_x_tolerance": 3,
            "text_y_tolerance": 3,
        },
        description="Settings for table extraction algorithm",
    )

    async def process(self, context: ProcessingContext) -> List[DataframeRef]:
        """
        Extract tables from PDF and convert them to dataframes.

        Returns:
            List[DataframeRef]: List of dataframes containing extracted tables
        """
        import pandas as pd

        pdf_data = await context.asset_to_bytes(self.pdf)
        dataframes = []

        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            # Convert 1-based page numbers to 0-based indices
            total_pages = len(pdf.pages)
            start_idx = (self.start_page - 1) if self.start_page is not None else 0
            end_idx = (
                (self.end_page - 1) if self.end_page is not None else (total_pages - 1)
            )

            # Validate page range
            start_idx = max(0, min(start_idx, total_pages - 1))
            end_idx = max(start_idx, min(end_idx, total_pages - 1))

            # Process each page in the range
            for page_num in range(start_idx, end_idx + 1):
                page = pdf.pages[page_num]

                # Extract tables from the page
                tables = page.extract_tables(table_settings=self.table_settings)

                # Convert each table to a dataframe
                for table in tables:
                    if not table:  # Skip empty tables
                        continue

                    # Convert table to dataframe
                    df = pd.DataFrame(table[1:], columns=table[0])

                    # Clean up the dataframe
                    df = df.replace("", None)  # Replace empty strings with None
                    df = df.dropna(how="all")  # Drop rows that are all NA
                    df = df.dropna(axis=1, how="all")  # Drop columns that are all NA

                    # Convert to DataframeRef
                    df_ref = await context.dataframe_from_pandas(df)
                    dataframes.append(df_ref)

        return dataframes
