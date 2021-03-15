import pytest
from PyTradier.watchlist import WatchList


class TestWatchlist:

    watchlist = WatchList()

    def test_all(self, patch_get):
        """Test the get watchlist endpoint for all watchlists

        :param patch_get: fixture for monkeypatching the requests.get method
        :type patch_get: pytest.fixture
        """
        pass

    def test_one(self, patch_get):
        """Test the get watchlist endpoint for a single watchlist

        :param patch_get: fixture for monkeypatching the requests.get method
        :type patch_get: pytest.fixture
        """
        pass

    def test_create(self, patch_get):
        """Test creating watchlists

        :param patch_get: fixture for monkeypatching the requests.get method
        :type patch_get: pytest.fixture
        """
        pass

    def test_update(self, patch_get):
        """Test updating watchlist

        :param patch_get: fixture for monkeypatching the requests.get method
        :type patch_get: pytest.fixture
        """
        pass

    def test_delete(self, patch_get):
        """Test deleting 1 watchlist

        :param patch_get: fixture for monkeypatching the requests.get method
        :type patch_get: pytest.fixture
        """
        pass

    def test_add(self, patch_get):
        """Test adding symbols to a watchlist

        :param patch_get: fixture for monkeypatching the requests.get method
        :type patch_get: pytest.fixture
        """
        pass

    def test_remove(self, patch_get):
        """Test removing a single symbol from the watchlist

        :param patch_get: fixture for monkeypatching the requests.get method
        :type patch_get: pytest.fixture
        """
        pass
