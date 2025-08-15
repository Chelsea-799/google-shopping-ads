import re
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html as st_html


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def inline_assets(index_html: str, css_text: str, js_text: str) -> str:
    # Replace stylesheet link with inline <style>
    html_inlined = re.sub(
        r"<link[^>]+href=\"assets/styles.css\"[^>]*>",
        f"<style>\n{css_text}\n</style>",
        index_html,
        flags=re.IGNORECASE,
    )
    # Replace script src with inline <script>
    html_inlined = re.sub(
        r"<script[^>]+src=\"assets/app.js\"[^>]*></script>",
        f"<script>\n{js_text}\n</script>",
        html_inlined,
        flags=re.IGNORECASE,
    )
    return html_inlined


def main() -> None:
    # Main function for Google Shopping Ads curriculum interface
    st.set_page_config(page_title="Google Shopping Ads – Dark Thinker", layout="wide")
    # Tighten Streamlit container paddings for better iframe fit
    st.markdown(
        """
        <style>
        .block-container {max-width: 100%; padding-top: 1.25rem; padding-bottom: 2rem;}
        section.main > div {padding-left: 0 !important; padding-right: 0 !important;}
        /* Add a small top spacer to avoid the app being cropped at the top */
        .stApp { padding-top: 6px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    base_dir = Path(__file__).parent
    index_html = load_text(base_dir / "index.html")
    css_text = load_text(base_dir / "assets" / "styles.css")
    js_text = load_text(base_dir / "assets" / "app.js")

    if not index_html:
        st.error("Không tìm thấy file index.html trong thư mục ứng dụng.")
        return

    html_inlined = inline_assets(index_html, css_text, js_text)

    with st.sidebar:
        st.markdown("**Xem giao diện**")
        fullscreen = st.checkbox("Chế độ toàn màn hình (full width • full height)", value=False)
        st.caption("Tip: Bật 'toàn màn hình' để chiếm toàn bộ khung trình duyệt.")

    if fullscreen:
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] { display: none; }
            .block-container { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
            section.main > div { padding-left: 0 !important; padding-right: 0 !important; }
            /* Make the HTML component iframe fill the viewport */
            div[data-testid="stIFrame"] > iframe {
              position: fixed; /* overlay to use the whole viewport */
              inset: 0 0 0 0;
              width: 100vw !important;
              height: 100vh !important;
              border: 0 !important;
            }
            html, body, .stApp { overflow: hidden; padding-top: env(safe-area-inset-top, 0px); }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Render full HTML (including <html> .. </html>) inside component iframe
    # Width/height will be overridden by CSS in fullscreen mode
    st_html(html_inlined, height=(1000 if not fullscreen else 1000), width=(1000 if not fullscreen else 1000), scrolling=True)


if __name__ == "__main__":
    main()


