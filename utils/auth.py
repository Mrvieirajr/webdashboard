import streamlit as st
from utils.database import Database

class Auth:
    def __init__(self):
        self.db = Database()

    def login(self, email: str, password: str) -> bool:
        """Authenticate user with email and password"""
        df = self.db.verify_user(email, password)
        if not df.empty:
            st.session_state['authenticated'] = True
            st.session_state['user'] = {
                'email': df.iloc[0]['email'],
                'name': df.iloc[0]['name']
            }
            return True
        return False

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)

    def logout(self):
        """Log out the current user"""
        st.session_state['authenticated'] = False
        if 'user' in st.session_state:
            del st.session_state['user']