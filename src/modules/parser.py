from typing import List
from pathlib import Path
import warnings

from llama_index.core import (
    SimpleDirectoryReader,
    Document)
from llama_index.readers.file import (
    DocxReader,
    PDFReader)

from llmsherpa.readers import LayoutPDFReader


DEFAULT_LLMSHERPA_API_URL = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"


class Parser:
    def __init__(self,
                 llmsherpa_api_url: str = DEFAULT_LLMSHERPA_API_URL):
        self.pdf_reader = LayoutPDFReader(llmsherpa_api_url)
        lmi_pdf_extractor = PDFReader()
        lmi_docx_extractor = DocxReader()
        self.lmi_file_extractor = {
            ".pdf": lmi_pdf_extractor,
            ".docx": lmi_docx_extractor
        }

    def parse_file(self, file_path: str,
                   category: str = "Sun*") -> List[Document]:
        try:
            sherpa_documents = self.pdf_reader.read_pdf(file_path)
            documents = []
            # TODO: Convert Llmsherpa Document to Llama-index Document
            if len(sherpa_documents.chunks()) > 0:
                for i, chunk in enumerate(sherpa_documents.chunks()):
                    file_name = Path(file_path).name
                    text = chunk.to_context_text()
                    id = f"{file_path}_{i}"
                    documents.append(
                        Document(
                            text=text,
                            id_=id,
                            metadata={
                                "name": file_name,
                                "category": category
                            },
                            excluded_llm_metadata_keys=["file_path"]
                        )
                    )
        except Exception as e:
            warnings.warn(
                f"Unexpected error {e} while reading {file_path},"
                f"using default readers"
            )
            # TODO: Implement the metadata generation func
            raw_documents = SimpleDirectoryReader(
                input_files=[file_path], 
                file_extractor=self.lmi_file_extractor,
                filename_as_id=True
            ).load_data()

            documents = []
            file_name = Path(file_path).name
            for i, doc in enumerate(raw_documents):
                doc.metadata.update({"name": file_name, "category": category})
                doc.excluded_llm_metadata_keys = ["file_path"]
                documents.append(doc)

        return documents
