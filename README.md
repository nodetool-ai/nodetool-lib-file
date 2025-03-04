# Nodetool File Processing Library

A powerful and flexible library for processing various file formats as part of the Nodetool ecosystem. This library provides a collection of nodes for handling different file types including PDFs, Excel spreadsheets, Word documents, Markdown, and more.

## Features

### PDF Processing

- Text extraction with page range control
- Image extraction from PDF documents
- Table extraction with conversion to dataframes
- Page metadata extraction (dimensions, rotation, etc.)
- Page counting and document analysis

### Excel Processing

- Create new workbooks and worksheets
- Convert between DataFrames and Excel worksheets
- Apply cell formatting and styles
- Auto-fit column widths
- Save workbooks with customizable naming

### Document Processing

- Word document (.docx) handling
- Markdown processing
- Pandoc integration for document conversion
- PyMuPDF integration for advanced PDF processing

## Usage

Each file format is handled through specialized nodes that inherit from `BaseNode`. These nodes can be used individually or chained together in workflows.

### Example: PDF Processing

```python
# Extract text from a PDF
text_node = ExtractText(
    pdf=document_ref,
    start_page=0,
    end_page=4
)

# Extract tables from PDF
tables_node = ExtractTables(
    pdf=document_ref,
    start_page=0,
    end_page=-1  # All pages
)
```

### Example: Excel Processing

```python
# Create a new workbook
workbook_node = CreateWorkbook(
    sheet_name="Data"
)

# Write DataFrame to Excel
excel_writer = DataFrameToExcel(
    workbook=workbook_ref,
    dataframe=df_ref,
    sheet_name="Data",
    include_header=True
)
```

## Node Types

### PDF Nodes

- `ExtractText`: Extract text content from PDF files
- `ExtractImages`: Extract embedded images from PDFs
- `ExtractTables`: Convert PDF tables to dataframes
- `GetPageCount`: Count pages in PDF documents
- `ExtractPageMetadata`: Get page dimensions and properties

### Excel Nodes

- `CreateWorkbook`: Initialize new Excel workbooks
- `DataFrameToExcel`: Convert DataFrames to Excel worksheets
- `ExcelToDataFrame`: Import Excel data as DataFrames
- `FormatCells`: Apply styling to Excel cells
- `AutoFitColumns`: Optimize column widths
- `SaveWorkbook`: Export Excel files

### Document Nodes

- Word document processing
- Markdown conversion
- Document format conversion via Pandoc
- Advanced PDF manipulation with PyMuPDF

## Dependencies

The library relies on several Python packages for file processing:

- `pdfplumber`: PDF text and table extraction
- `openpyxl`: Excel file handling
- `python-docx`: Word document processing
- `pandoc`: Document format conversion
- `PyMuPDF`: Advanced PDF processing
- `markdown`: Markdown processing

## Use Cases

- Document data extraction and analysis
- Automated report generation
- Data conversion between formats
- Document format transformation
- Image extraction and processing
- Table data extraction and structuring
