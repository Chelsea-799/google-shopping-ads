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
    st.set_page_config(page_title="Google Shopping Ads – Dark Thinker", layout="wide")
    # Tighten Streamlit container paddings for better iframe fit
    st.markdown(
        """
        <style>
        .block-container {max-width: 100%; padding-top: 0.5rem; padding-bottom: 2rem;}
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
        height = st.slider("Chiều cao khung nhúng (px)", min_value=800, max_value=3000, value=1600, step=100)
        width = st.slider("Chiều rộng khung nhúng (px)", min_value=360, max_value=1600, value=1200, step=40)
        st.caption("Tip: PC ~1200px, Mobile ~380–420px. Dùng thanh cuộn trong khung để xem đầy đủ nội dung.")

    # Render full HTML (including <html> .. </html>) inside component iframe
    st_html(html_inlined, height=height, width=width, scrolling=True)


if __name__ == "__main__":
    main()


