"""
Estilo visual Dark Mode Premium — preto, cinza chumbo e dourado.
CSS injetado via st.markdown.
"""

CUSTOM_CSS = """
<style>
:root {
    --bg-primary: #0d0d0d;
    --bg-secondary: #1a1a1a;
    --bg-card: #212121;
    --gold: #d4af37;
    --gold-light: #f0d878;
    --text-light: #e8e8e8;
    --text-muted: #a0a0a0;
    --border: #333333;
}

.stApp {
    background-color: var(--bg-primary);
    color: var(--text-light);
    font-family: 'Segoe UI', sans-serif;
}

/* Esconde elementos padrão do Streamlit */
#MainMenu, footer, header {visibility: hidden;}

/* HERO SECTION */
.hero-container {
    background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 60%, #2a2418 100%);
    border-radius: 18px;
    padding: 50px 30px;
    text-align: center;
    border: 1px solid var(--border);
    margin-bottom: 30px;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--gold);
    text-shadow: 0 0 20px rgba(212,175,55,0.3);
    margin-bottom: 10px;
}
.hero-sub {
    font-size: 1.15rem;
    color: var(--text-light);
    margin-bottom: 8px;
}
.hero-trust {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 20px;
}

/* CARDS DE SERVIÇO */
.service-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
    height: 100%;
    transition: 0.25s;
}
.service-card:hover {
    border-color: var(--gold);
    box-shadow: 0 0 18px rgba(212,175,55,0.2);
    transform: translateY(-4px);
}
.service-title {
    color: var(--gold);
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
}
.service-desc {
    color: var(--text-muted);
    font-size: 0.9rem;
}

/* BOTÕES */
div.stButton > button {
    background: linear-gradient(135deg, var(--gold), var(--gold-light));
    color: #0d0d0d;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    transition: 0.2s;
}
div.stButton > button:hover {
    box-shadow: 0 0 15px rgba(212,175,55,0.5);
    transform: scale(1.02);
}

/* CARD DEPOIMENTO */
.testimonial-card {
    background: var(--bg-card);
    border-left: 4px solid var(--gold);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
}
.stars { color: var(--gold); font-size: 1.1rem; }

/* SEÇÃO TÍTULO */
.section-title {
    color: var(--gold);
    font-size: 1.6rem;
    font-weight: 700;
    border-bottom: 2px solid var(--border);
    padding-bottom: 8px;
    margin: 30px 0 18px 0;
}

/* CONTATO FLUTUANTE */
.contact-badge {
    display: inline-block;
    background: var(--bg-card);
    border: 1px solid var(--gold);
    border-radius: 30px;
    padding: 10px 20px;
    color: var(--gold);
    text-decoration: none;
    font-weight: 600;
    margin: 5px;
}

/* STATUS BADGES ADMIN */
.badge-pendente { background:#5c4400; color:#ffd35c; padding:4px 10px; border-radius:6px; font-size:0.8rem;}
.badge-atendimento { background:#003a5c; color:#7fc6ff; padding:4px 10px; border-radius:6px; font-size:0.8rem;}
.badge-concluido { background:#0a4d0a; color:#8fe38f; padding:4px 10px; border-radius:6px; font-size:0.8rem;}
</style>
"""
