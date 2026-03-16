import gradio as gr
import joblib
import json
import random
import time
import pandas as pd
from datetime import datetime

# Paths
MODEL_PATH     = "bankmate_assistant_pipeline.joblib"
RESPONSES_PATH = "Dataset/bankmate_responses.json"
CSV_DATA_PATH  = "Dataset/bankmate_intents_data.csv"

# Load model
pipeline = joblib.load(MODEL_PATH)

# Load responses
with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
    RESPONSES = json.load(f)["responses"]

# Stats
try:
    df_stats   = pd.read_csv(CSV_DATA_PATH)
    stats_text = f"{len(df_stats):,} examples · {df_stats['intent'].nunique()} intents"
except Exception:
    stats_text = "Model ready"

FALLBACKS = [
    "Sorry, I didn't quite get that — could you rephrase?",
    "Hmm, not sure I understand. Try saying it differently?",
    "I no too grab this one… Wetin you mean?",
    "Let me connect you to a human agent real quick…",
]

# Predict
def chatbot_predict(message, history):
    if not message.strip():
        return history, ""

    time.sleep(0.5)

    intent     = pipeline.predict([message])[0]
    confidence = pipeline.predict_proba([message]).max()
    replies    = RESPONSES.get(intent, FALLBACKS)
    reply      = random.choice(replies)

    if confidence < 0.65:
        reply += f"\n\n_Confidence {confidence:.0%}, try rephrasing if needed._"

    now = datetime.now().strftime("%H:%M")
    reply_stamped = f"{reply}\n\n<span class='ts'>{now}</span>"

    # New format for Gradio 3.40+: list of dicts
    history = history or []
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply_stamped})
    return history, ""


# Quick Questions
CHIPS = [
    ("💳", "Check my account balance"),
    ("🚨", "My card is lost or stolen"),
    ("🏦", "Apply for a loan"),
    ("⚡", "Pay electricity bill"),
    ("📱", "USSD code for transfer"),
    ("💰", "Open a savings account"),
    ("🔒", "Block my card"),
    ("📞", "Speak to an agent"),
]

header_html = f"""
<div id="bm-header-html">
  <div class="bm-badge">
    <span class="bm-badge-dot"></span>
    AI Banking Assistant
  </div>
  <div class="bm-logo-wrap">
    <div class="bm-logo-icon">🏦</div>
    <h1 class="bm-title">Bank<span>Mate</span></h1>
  </div>
  <p class="bm-sub">Your smart guide to all banking procedures</p>
  <div class="bm-stats">
    <span class="bm-stats-icon">🧠</span>
    {stats_text}
  </div>
</div>
"""

# Full CSS
css = """
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
/* ── Tokens ── */
:root { --brand:#1A6B4A; --brand-mid:#22885E; --brand-light:#E8F5EE; --brand-xlight:#F2FAF6; --surface:#FFFFFF; --surface-2:#F7F9FB; --surface-3:#EEF2F7; --border:#DDE3EC; --border-focus:#1A6B4A; --text-1:#0D1F2D; --text-2:#4A5E72; --text-3:#8A9BB0; --shadow-sm:0 1px 4px rgba(0,0,0,0.06); --shadow-md:0 4px 20px rgba(0,0,0,0.08); --shadow-lg:0 12px 48px rgba(0,0,0,0.10); --r-pill:9999px; --r-card:15px; --r-bubble:16px; }
/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
/* ── Shell ── */
body, .gradio-container, .gradio-container>.wrap { background: var(--surface-2) !important; font-family: 'Plus Jakarta Sans', sans-serif !important; color: var(--text-1); } footer { display: none !important; }
/* ── Page wrapper ── */
#bm-page { max-width:820px; margin:0 auto; padding:0 16px 56px; }
/* ── Header ── */
#bm-header-html{padding:40px 0 32px;text-align:center;}
.bm-badge{display:inline-flex;align-items:center;gap:8px;padding:5px 14px 5px 10px;border-radius:var(--r-pill);background:var(--brand-light);color:var(--brand);font-size:0.72rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:16px;}
.bm-badge-dot{width:7px;height:7px;border-radius:50%;background:var(--brand-mid);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.5;transform:scale(1.3);}}
.bm-logo-wrap{display:flex;align-items:center;justify-content:center;gap:14px;margin-bottom:8px;}
.bm-logo-icon{width:52px;height:52px;border-radius:14px;background:linear-gradient(145deg,var(--brand-mid),var(--brand));display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 6px 24px rgba(26,107,74,0.28);flex-shrink:0;}
.bm-title{font-family:'Lora',serif;font-size:2.5rem;font-weight:700;color:var(--text-1);letter-spacing:-0.01em;line-height:1;}
.bm-title span{color:var(--brand);}
.bm-sub{color:var(--text-2);font-size:0.92rem;letter-spacing:0.02em;margin-bottom:18px;font-weight:400;}
.bm-stats{display:inline-flex;align-items:center;gap:6px;padding:7px 18px;border-radius:var(--r-pill);background:var(--surface);border:1px solid var(--border);color:var(--text-2);font-size:0.78rem;font-weight:500;box-shadow:var(--shadow-sm);}
.bm-stats-icon{font-size:0.85rem;}
#bm-chat-card{background:var(--surface);border-radius:var(--r-card);border:1px solid var(--border);box-shadow:var(--shadow-lg);overflow:hidden;margin-bottom:0;padding:10px;}
#bm-chat-inner{border:none!important;border-radius:0!important;box-shadow:none!important;background:var(--surface)!important;}
#bm-chat-inner>.wrap{border:none!important;background:transparent!important;}
#bm-chat-inner ::-webkit-scrollbar{width:5px;}
#bm-chat-inner ::-webkit-scrollbar-track{background:transparent;}
#bm-chat-inner ::-webkit-scrollbar-thumb{background:var(--surface-3);border-radius:4px;}
#bm-chat-inner .message{font-size:0.91rem!important;line-height:1.65!important;max-width:90%!important;padding:10px!important;min-width:40%!important;}
#bm-chat-inner .message.user span,#bm-chat-inner .message.user p{color:#fff!important;}
#bm-chat-inner .message.user{background:linear-gradient(135deg,var(--brand-mid) 0%,var(--brand) 100%)!important;border-radius:var(--r-bubble) var(--r-bubble) 4px var(--r-bubble)!important;box-shadow:0 4px 14px rgba(26,107,74,0.25)!important;border:none!important;color:#fff!important;}
#bm-chat-inner .message.bot{background:var(--surface-2)!important;color:var(--text-1)!important;border-radius:var(--r-bubble) var(--r-bubble) var(--r-bubble) 4px!important;border:1px solid var(--border)!important;box-shadow:var(--shadow-sm)!important;}
.ts{font-size:0.70rem;color:var(--text-3);display:block;margin-top:5px;}
#bm-chat-inner .message.user .ts{color:rgba(255,255,255,0.65);}
#bm-chat-inner .avatar-container img{border:2px solid var(--brand-light)!important;border-radius:50%!important;box-shadow:0 2px 8px rgba(26,107,74,0.15)!important;}
#bm-input-panel{padding:14px 16px 16px;border-top:1px solid var(--border);background:var(--surface);}
.bm-pill-wrap{display:flex;align-items:center;gap:10px;background:var(--surface-2);border:1.5px solid var(--border);border-radius:var(--r-pill);padding:6px 6px 6px 20px;transition:border-color 0.2s,box-shadow 0.2s;}
.bm-pill-wrap:focus-within{border-color:var(--border-focus);box-shadow:0 0 0 3px rgba(26,107,74,0.10);}
#bm-textbox,#bm-textbox>label,#bm-textbox>.wrap{flex:1;background:transparent!important;border:none!important;box-shadow:none!important;padding:0!important;}
#bm-textbox label span{display:none!important;}
#bm-textbox textarea,#bm-textbox input{background:transparent!important;border:none!important;outline:none!important;box-shadow:none!important;padding:8px 0!important;color:var(--text-1)!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:0.93rem!important;resize:none!important;width:100%!important;min-height:unset!important;}
#bm-textbox textarea::placeholder,#bm-textbox input::placeholder{color:var(--text-3)!important;}
#bm-send-btn{flex-shrink:0;height:40px!important;min-width:88px!important;border-radius:var(--r-pill)!important;background:linear-gradient(135deg,var(--brand-mid),var(--brand))!important;color:#fff!important;font-weight:600!important;font-size:0.85rem!important;letter-spacing:0.04em!important;border:none!important;cursor:pointer!important;box-shadow:0 3px 12px rgba(26,107,74,0.30)!important;transition:opacity 0.18s,transform 0.15s,box-shadow 0.18s!important;}
#bm-send-btn:hover{opacity:0.9!important;transform:translateY(-1px)!important;box-shadow:0 6px 18px rgba(26,107,74,0.35)!important;}
#bm-send-btn:active{transform:translateY(0)!important;}
#bm-below{display:flex;align-items:center;padding:10px 4px 20px;}
#bm-clear-btn{border-radius:var(--r-pill)!important;border:1px solid var(--border)!important;background:transparent!important;color:var(--text-3)!important;font-size:0.80rem!important;padding:7px 18px!important;transition:all 0.18s!important;font-family:'Plus Jakarta Sans',sans-serif!important;}
#bm-clear-btn:hover{border-color:#e57373!important;color:#c0392b!important;background:#fef2f2!important;}
.bm-chip{display:inline-flex;align-items:center;gap:5px;padding:7px 15px;border-radius:var(--r-pill);border:1px solid var(--border);background:var(--surface);color:var(--text-2);font-size:0.82rem;font-weight:500;cursor:pointer;transition:all 0.18s;font-family:'Plus Jakarta Sans',sans-serif;box-shadow:var(--shadow-sm);user-select:none;}
.bm-chip:hover{border-color:var(--brand-mid);color:var(--brand);background:var(--brand-light);transform:translateY(-2px);box-shadow:0 4px 12px rgba(26,107,74,0.14);}
#bm-chat-inner > div:nth-child(1) {
    scroll-behavior: smooth;
}
"""

# Layout
with gr.Blocks(css=css, title="BankMate · AI Banking Assistant") as demo:

    with gr.Column(elem_id="bm-page"):
        gr.HTML(header_html)

        with gr.Column(elem_id="bm-chat-card"):
            chatbot_ui = gr.Chatbot(
                elem_id="bm-chat-inner",
                height=500,
                render_markdown=True,
            )

            # --- Smooth auto-scroll JS ---
            gr.HTML("""
<script>
function autoScrollChat() {
    const chatContainer = document.querySelector('#bm-chat-inner > div:nth-child(1)');
    if (!chatContainer) return;
    const observer = new MutationObserver(() => {
        chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
    });
    observer.observe(chatContainer, { childList: true });
}
// Run after DOM fully loaded
window.addEventListener('load', autoScrollChat);
</script>
""")

            with gr.Column(elem_id="bm-input-panel"):
                with gr.Row(elem_classes="bm-pill-wrap"):
                    text_input = gr.Textbox(
                        placeholder="Ask me anything about banking…",
                        show_label=False,
                        container=False,
                        elem_id="bm-textbox",
                        lines=1,
                        autofocus=True,
                        scale=9,
                    )
                    send_btn = gr.Button(
                        "Send ↑",
                        variant="primary",
                        elem_id="bm-send-btn",
                        scale=0,
                        min_width=88,
                    )

        with gr.Row(elem_id="bm-below"):
            clear_btn = gr.Button(
                "✕ Clear chat",
                variant="secondary",
                elem_id="bm-clear-btn",
                scale=0,
                min_width=120,
            )

        # Quick Questions
        with gr.Row():
            for icon, text in CHIPS:
                btn = gr.Button(f"{icon} {text}", elem_classes="bm-chip")
                btn.click(lambda t=text: t, [], text_input)

    text_input.submit(chatbot_predict, [text_input, chatbot_ui], [chatbot_ui, text_input])
    send_btn.click(chatbot_predict, [text_input, chatbot_ui], [chatbot_ui, text_input])
    clear_btn.click(lambda: ([], ""), None, [chatbot_ui, text_input], queue=False)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )
