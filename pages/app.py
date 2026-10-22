import json
import os
import streamlit as st
import streamlit.components.v1 as components

# Set page config for maximum mobile usability
st.set_page_config(
    page_title="Longer or Shorter? — Game Length",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 1. Get the directory path where app.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "hltb.jsonlines")
html_path = os.path.join(BASE_DIR, "hltb-higher-lower-redesign.html")

# 2. Read dataset & html template
try:
  with open(db_path, "r", encoding="utf-8") as f:
    raw_jsonlines = f.read()
except FileNotFoundError:
  st.error(f"❌ File missing at: `{db_path}`")
  st.stop()

try:
  with open(html_path, "r", encoding="utf-8") as f:
    html_code = f.read()
except FileNotFoundError:
  st.error(f"❌ HTML template missing at: `{html_path}`")
  st.stop()

# 3. Safely encode the dataset into JSON string (prevents escaping/newline errors)
safe_dataset = json.dumps(raw_jsonlines)

# 4. Inject into HTML page
injection_script = f"""
<script>
  window.addEventListener('DOMContentLoaded', () => {{
    const dataset = {safe_dataset};
    if (typeof init === 'function') {{
      init(dataset);
    }}
  }});
</script>
</body>
"""

# Replace closing </body> with the injection script
if "</body>" in html_code:
  html_code = html_code.replace("</body>", injection_script)
else:
  html_code += injection_script

# 5. Render inside Streamlit iframe
# Adjust height to match mobile or desktop viewport nicely
components.html(html_code, height=820, scrolling=True)