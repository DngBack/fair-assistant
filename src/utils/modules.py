from llama_index.core import Settings
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding  # type: ignore
from llama_index.llms.azure_openai import AzureOpenAI

from .settings import Settings as AppSettings


def setup_modules(settings: AppSettings):
    """
    Configure and set up the LLM and embedding models using Azure OpenAI settings.

    This function initializes the language model (LLM) and embedding model using 
    the Azure OpenAI configurations provided in the `settings`. The initialized models 
    are then set as default in the `Settings` module for use throughout the application.

    Args:
        settings (AppSettings): The application settings containing Azure OpenAI configurations.
            The settings should include:
                - azure_openai.key: The API key for accessing the Azure OpenAI service.
                - azure_openai.endpoint: The endpoint URL for the Azure OpenAI service.
                - azure_openai.version: The API version of the Azure OpenAI service.
                - azure_openai.gpt_deployment_name: The deployment name for the GPT model.
                - azure_openai.embed_deployment_name: The deployment name for the embedding model.

    Example:
        settings = load_settings()
        setup_modules(settings)
    """
    api_key = settings.azure_openai.key
    end_point = settings.azure_openai.endpoint
    version = settings.azure_openai.version
    gpt = settings.azure_openai.gpt_deployment_name
    embed = settings.azure_openai.embed_deployment_name

    llm = AzureOpenAI(
        deployment_name=gpt,
        azure_endpoint=end_point,
        api_key=api_key,
        api_version=version)
    embed_model = AzureOpenAIEmbedding(
        deployment_name=embed,
        azure_endpoint=end_point,
        api_version=version,
        api_key=api_key)

    Settings.llm = llm
    Settings.embed_model = embed_model
