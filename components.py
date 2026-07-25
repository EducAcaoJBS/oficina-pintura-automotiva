"""
Componentes reutilizáveis de UI (cards, badges, etc.)
"""
import streamlit as st

SERVICOS = [
    {
        "titulo": "🎨 Pintura Completa e Personalizada",
        "desc": "Renovação total da pintura com cores originais ou personalizadas, acabamento de fábrica."
    },
    {
        "titulo": "🔧 Retoques e Reparos Rápidos",
        "desc": "Pintura localizada para riscos, amassados leves e pequenas avarias — rapidez e economia."
    },
    {
        "titulo": "✨ Polimento Técnico e Vitrificação",
        "desc": "Remoção de arranhões, oxidação e recuperação total do brilho com proteção vitrificada."
    },
    {
        "titulo": "🛠️ Restauração de Para-choques e Plásticos",
        "desc": "Reparo estrutural e estético de para-choques, spoilers e peças plásticas."
    },
]


def render_service_cards():
    cols = st.columns(4)
    for col, servico in zip(cols, SERVICOS):
        with col:
            st.markdown(f"""
                <div class="service-card">
                    <div class="service-title">{servico['titulo']}</div>
                    <div class="service-desc">{servico['desc']}</div>
                </div>
            """, unsafe_allow_html=True)


def render_status_badge(status):
    mapa = {
        "Pendente": "badge-pendente",
        "Em Atendimento": "badge-atendimento",
        "Concluído": "badge-concluido",
    }
    classe = mapa.get(status, "badge-pendente")
    return f'<span class="{classe}">{status}</span>'


def render_stars(nota):
    return "⭐" * int(nota) + "☆" * (5 - int(nota))
