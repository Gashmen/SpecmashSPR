#python -m PyQt5.uic.pyuic mainver03.ui -o mainver03.py
from src.ldap_auth import backend_auth

if __name__ == "__main__":
    backend_auth.run_app()

