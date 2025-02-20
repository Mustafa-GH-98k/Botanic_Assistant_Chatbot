import pytest
from app import app
from Controllers.chatbot_controller import api_keys

@pytest.fixture
def client(): # yield used here because it manages a context
    #setup (before yield)
    app.testing = True  # Enable testing mode
    with app.test_client() as client:
        yield client # yield used only if cleanup required 
    # tear down (after yield)

@pytest.fixture
def api_keys_fixture():
    """Fixture to provide access to api_keys and reset it after each test."""
    original_api_keys = api_keys.copy()  # Save the original state
    yield api_keys  # Provide api_keys to the test
    api_keys.clear()  # Reset api_keys after the test
    api_keys.update(original_api_keys)  # Restore original state

