from ui.styles import inject_global_css
from ui.render import render_app

def main():
    inject_global_css()
    render_app()


if __name__ == "__main__":
    main()
