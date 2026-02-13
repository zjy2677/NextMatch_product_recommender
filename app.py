from ui.styles import inject_global_css
from ui.render import render_app
'''
This is the main entry point of the Streamlit app. It initializes the app 
by injecting global CSS styles and rendering the main app interface.
'''

def main():
    inject_global_css()
    render_app()


if __name__ == "__main__":
    main()
