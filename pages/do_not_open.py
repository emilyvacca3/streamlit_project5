import json
import streamlit as st
import streamlit.components.v1 as components

# Page configuration optimized for mobile & desktop view
st.set_page_config(
    page_title="Longer or Shorter? — Game Length",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 1. Load the database file (hltb.jsonlines)
jsonlines_text = ""
try:
  with open("hltb.jsonlines", "r", encoding="utf-8") as f:
    jsonlines_text = f.read()
except FileNotFoundError:
  st.error(
      "❌ **'hltb.jsonlines' not found!** Please place it in the same directory"
      " as app.py."
  )
  st.stop()

# 2. Load the HTML design file
html_code = ""
try:
  with open("hltb-higher-lower-redesign.html", "r", encoding="utf-8") as f:
    html_code = f.read()
except FileNotFoundError:
  st.error(
      "❌ **'hltb-higher-lower-redesign.html' not found!** Please make sure it's"
      " in the same directory."
  )
  st.stop()

# 3. Inject the dataset directly into the JavaScript to guarantee automatic loading
# This replaces the network fetch() call with the local python-loaded data instantly.
fetch_block = """// Try to fetch the dataset next to this page; if the browser blocks it (file://), offer a file picker.
    fetch(DATA_FILE)
      .then(r => { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(init)
      .catch(() => { $("picker").style.display = "block"; });"""

embedded_block = f"""
    // Automatically loaded via Streamlit backend
    const EMBEDDED_TEXT = `{jsonlines_text}`;
    init(EMBEDDED_TEXT);
    """

if fetch_block in html_code:
  html_code = html_code.replace(fetch_block, embedded_block)
else:
  # Fallback replacement safety
  html_code = html_code.replace(
      'fetch(DATA_FILE)\n  .then(r => { if (!r.ok) throw new Error(r.status); return r.text(); })\n  .then(init)\n  .catch(() => { $("picker").style.display = "block"; });',
      embedded_block,
  )

# 4. Render the game inside Streamlit using components.html
# Height is set to 780px to give ample room for the iPhone-optimized UI cards and bottom drawer
components.html(html_code, height=780, scrolling=False)