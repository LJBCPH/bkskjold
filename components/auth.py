"""Authentication components for Spond application."""

import streamlit as st
from datetime import datetime
import app_config


def check_admin_login():
    """Check if admin is logged in and session hasn't expired."""
    if not st.session_state.get('admin_logged_in', False):
        return False
    
    # Check session timeout (30 minutes)
    login_time = st.session_state.get('admin_login_time', 0)
    current_time = datetime.now().timestamp()
    session_timeout = 30 * 60  # 30 minutes in seconds
    
    if current_time - login_time > session_timeout:
        st.session_state.admin_logged_in = False
        st.session_state.pop('admin_login_time', None)
        return False
    
    return True


def admin_login():
    """Display admin login form."""
    st.title('🔐 Admin Login')
    
    with st.form('admin_login_form'):
        username = st.text_input('Brugernavn')
        password = st.text_input('Adgangskode', type='password')
        submitted = st.form_submit_button('Log ind')
        
        if submitted:
            # Check credentials from config
            if username == app_config.ADMIN_USERNAME and password == app_config.ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.session_state.admin_login_time = datetime.now().timestamp()
                st.success('Login vellykket! 🎉')
                st.rerun()
            else:
                st.error('Ugyldige loginoplysninger! 🚫')
    
    st.info(f'💡 **Loginoplysninger:** Brugernavn: `{app_config.ADMIN_USERNAME}`, Adgangskode: heyz33`{app_config.ADMIN_PASSWORD}`')


def admin_logout():
    """Logout admin user."""
    if st.sidebar.button('🚪 Log ud'):
        st.session_state.admin_logged_in = False
        st.rerun()