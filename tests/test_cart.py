import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

mock_con = MagicMock()

with patch('psycopg2.connect', return_value=mock_con):
    sys.modules['db'] = MagicMock(get_connection=lambda: mock_con)
    from routes.cart import cart_bp

def test_import():
    assert cart_bp is not None