from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings

from .settings import Settings as AppSettings


def setup_tracing(settings: AppSettings):
    """
    Configure and set up tracing for the application.

    This function initializes the tracing callback handler using the tracing 
    configurations provided in the `settings`. It then sets up the callback 
    manager in the `Settings` module with the initialized tracing handler.

    Args:
        settings (AppSettings): The application settings containing tracing configurations.
            The settings should include:
                - tracing.public_key: The public key for the tracing service.
                - tracing.secret_key: The secret key for the tracing service.
                - tracing.host: The host URL for the tracing service.
                - tracing.user_id: The user ID for the tracing service.

    Example:
        settings = load_settings()
        setup_tracing(settings)
    """
    callback_handler = LlamaIndexCallbackHandler(
        public_key=settings.tracing.public_key,
        secret_key=settings.tracing.secret_key,
        host=settings.tracing.host,
        user_id=settings.tracing.user_id
    )
    Settings.callback_manager = CallbackManager([callback_handler])
