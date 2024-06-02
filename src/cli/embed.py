import os
import typer
from tqdm import tqdm

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)

from src.modules.parser import Parser
from src.utils import initialize


def main(dotenv_path: str = "local.env",
         data_dir: str = "data/",
         persist_dir: str = "index/",
         category: str = "Sun*"):
    """
    Main function to create VectorStoreIndex from files in folder
    Args:
        dotenv_path (str): Path to dotenv file
        data_dir (str): Path to folder that contains files
        persist_dir (str): Path to save the VectorStoreIndex to disk
        category (str): category of the files in folder
    """
    initialize(dotenv_path)

    parser = Parser()
    documents = []
    for file in tqdm(os.listdir(data_dir), desc="Creating documents"):
        documents.extend(
            parser.parse_file(f"{data_dir}/{file}", category)
        )
    # If the index exist, simply load it up
    # Then refresh the index with docs
    if os.path.exists(persist_dir):
        storage_context = StorageContext.from_defaults(
            persist_dir=persist_dir
        )
        index = load_index_from_storage(storage_context)
        index.refresh_ref_docs(
            documents,
            insert_kwargs={"show_progress": True}
        )
        index.storage_context.persist(persist_dir)
    else:
        index = VectorStoreIndex.from_documents(
            documents, show_progress=True
        )
        index.storage_context.persist(persist_dir)


if __name__ == '__main__':
    typer.run(main)
