from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TracingConfig(BaseModel):
    """
    Configuration for tracing with langfuse.

    Attributes:
        public_key (str): The public key for tracing.
        secret_key (str): The secret key for tracing.
        user_id (str): The user ID for tracing.
        host (str): The host URL for the tracing service. Default is "https://langfuse.poc.sun-asterisk.ai".
        flush_at (int): The number of events to flush at. Default is 2.
    """
    public_key: str
    secret_key: str
    user_id: str
    host: str = "https://langfuse.poc.sun-asterisk.ai"
    flush_at: int = 2


class AzureOpenAIConfig(BaseModel):
    """
    Configuration for Azure OpenAI.

    Attributes:
        endpoint (str): The endpoint for the Azure OpenAI service.
        key (str): The API key for accessing the Azure OpenAI service.
        gpt_deployment_name (str): The deployment name for GPT models.
        embed_deployment_name (str): The deployment name for embedding models.
        version (str): The version of the Azure OpenAI service.
    """
    endpoint: str
    key: str
    gpt_deployment_name: str
    embed_deployment_name: str
    version: str


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Configuration for nested environment variables.
        azure_openai (AzureOpenAIConfig): Configuration for Azure OpenAI.
        tracing (TracingConfig): Configuration for tracing.
    """
    model_config = SettingsConfigDict(env_nested_delimiter='__')
    azure_openai: AzureOpenAIConfig
    tracing: TracingConfig


def load_settings() -> Settings:
    """
    Load and return the application settings.

    Returns:
        Settings: The loaded application settings.
    """
    return Settings()
