"""
Aplicação principal — Oficina de Pintura Automotiva
Execute com: streamlit run app.py
"""
import os
import io
from datetime import datetime

import streamlit as st
import qrcode
from PIL import Image

import database as db
from styles import CUSTOM_CSS
from components import render_service_cards, render_status_badge, render_stars

# ---------- CONFIGURAÇÕES GERAIS ----------
st.set_page_config(
    page_title="Oficina de Pintura Automotiva",
    page_icon="🚗",
    layout="wide",
)

UPLOAD_DIR = "uploads/portfolio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

WHATSAPP_NUMERO = "5581999999999"  # TODO: alterar para o número real
INSTAGRAM_URL = "https://instagram.com/suaoficina"  # TODO: alterar
ADMIN_SENHA = "admin123"  # TODO: alterar / mover para variável de ambiente

db.init_db()
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------- SIDEBAR: NAVEGAÇÃO ----------
st.sidebar.markdown("## 🚗 Menu")
pagina = st.sidebar.radio(
    "Navegação",
    ["🏠 Site do Cliente", "🔐 Painel Administrativo"]
)

# =====================================================================
# PÁGINA: SITE DO CLIENTE
# =====================================================================
if pagina == "🏠 Site do Cliente":

    # ---------- HERO SECTION ----------
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Pintura Automotiva Profissional</div>
            <div class="hero-title" style="font-size:1.4rem;">Reparos e Pintura Completa</div>
            <div class="hero-sub">🚗 Atendimento no local do cliente: comodidade total sem você precisar sair de casa!</div>
            <div class="hero-trust">Seu veículo com acabamento e brilho de zero km. Qualidade impecável, precisão técnica e garantia de satisfação.</div>
        </div>
    """, unsafe_allow_html=True)

    col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 1])
    with col_cta2:
        if st.button("💰 Orçamento sem Compromisso", use_container_width=True):
            st.session_state["scroll_to_orcamento"] = True

    # ---------- CATÁLOGO DE SERVIÇOS ----------
    st.markdown('<div class="section-title">Nossos Serviços</div>', unsafe_allow_html=True)
    render_service_cards()

    # ---------- SIMULADOR DE PRÉ-ORÇAMENTO ----------
    st.markdown('<div class="section-title">📋 Simulador de Pré-Orçamento</div>', unsafe_allow_html=True)
    with st.form("form_orcamento", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome completo *")
            telefone = st.text_input("Telefone / WhatsApp *")
            servico = st.selectbox(
                "Serviço desejado *",
                ["Pintura Completa", "Retoque/Reparo Rápido", "Polimento e Vitrificação",
                 "Restauração de Para-choques", "Outro / Não sei"]
            )
        with c2:
            veiculo = st.text_input("Marca e modelo do veículo *")
            estado_veiculo = st.selectbox(
                "Estado atual do veículo",
                ["Bom estado, apenas retoque", "Riscos/amassados moderados",
                 "Avarias significativas", "Restauração completa necessária"]
            )
            mensagem = st.text_area("Observações adicionais")

        enviar = st.form_submit_button("📩 Enviar Solicitação de Orçamento")

        if enviar:
            if nome and telefone and veiculo:
                db.add_lead(nome, telefone, servico, veiculo, estado_veiculo, mensagem)
                st.success("✅ Solicitação enviada com sucesso! Em breve entraremos em contato.")
            else:
                st.error("⚠️ Preencha os campos obrigatórios (*).")

    # ---------- AGENDAMENTO ONLINE ----------
    st.markdown('<div class="section-title">📅 Agendar Avaliação Técnica no Local</div>', unsafe_allow_html=True)
    with st.form("form_agendamento", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nome_ag = st.text_input("Nome *", key="nome_ag")
            telefone_ag = st.text_input("Telefone *", key="tel_ag")
            endereco_ag = st.text_input("Endereço para atendimento *", key="end_ag")
        with c2:
            data_ag = st.date_input("Data preferida *")
            hora_ag = st.time_input("Horário preferido *")
            obs_ag = st.text_area("Observações", key="obs_ag")

        agendar = st.form_submit_button("📌 Confirmar Agendamento")
        if agendar:
            if nome_ag and telefone_ag and endereco_ag:
                db.add_agendamento(nome_ag, telefone_ag, endereco_ag, data_ag, hora_ag, obs_ag)
                st.success("✅ Agendamento registrado! Confirmaremos por telefone/WhatsApp.")
            else:
                st.error("⚠️ Preencha os campos obrigatórios (*).")

    # ---------- PORTFÓLIO (ANTES E DEPOIS) ----------
    st.markdown('<div class="section-title">🖼️ Nosso Trabalho — Portfólio</div>', unsafe_allow_html=True)
    portfolio_items = db.get_portfolio()
    if portfolio_items:
        cols = st.columns(4)
        for i, item in enumerate(portfolio_items):
            with cols[i % 4]:
                if os.path.exists(item["caminho_imagem"]):
                    st.image(item["caminho_imagem"], use_container_width=True)
                st.caption(f"**{item['titulo']}**  \n{item['descricao']}")
    else:
        st.info("Em breve, novas fotos de trabalhos realizados serão exibidas aqui.")

    # ---------- PROVA SOCIAL: DEPOIMENTOS ----------
    st.markdown('<div class="section-title">💬 O que nossos clientes dizem</div>', unsafe_allow_html=True)
    depoimentos = db.get_depoimentos()
    cols = st.columns(3)
    for i, dep in enumerate(depoimentos):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="testimonial-card">
                    <div class="stars">{render_stars(dep['nota'])}</div>
                    <strong>{dep['nome_cliente']}</strong>
                    <p style="color:#a0a0a0;">"{dep['comentario']}"</p>
                </div>
            """, unsafe_allow_html=True)

    # ---------- CANAIS DE CONTATO + QR CODE ----------
    st.markdown('<div class="section-title">📞 Fale Conosco</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        wa_msg = "Olá! Gostaria de solicitar um orçamento para pintura automotiva."
        wa_link = f"https://wa.me/{WHATSAPP_NUMERO}?text={wa_msg.replace(' ', '%20')}"
        st.markdown(f'<a class="contact-badge" href="{wa_link}" target="_blank">💬 WhatsApp</a>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<a class="contact-badge" href="{INSTAGRAM_URL}" target="_blank">📷 Instagram</a>', unsafe_allow_html=True)
    with c3:
        # Gera QR Code apontando para o link do WhatsApp (ou site)
        qr_img = qrcode.make(wa_link)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="📱 Escaneie e fale com a gente", width=140)


# =====================================================================
# PÁGINA: PAINEL ADMINISTRATIVO
# =====================================================================
else:
    st.markdown('<div class="section-title">🔐 Área Administrativa</div>', unsafe_allow_html=True)

    if "admin_logado" not in st.session_state:
        st.session_state["admin_logado"] = False

    if not st.session_state["admin_logado"]:
        senha = st.text_input("Senha de acesso", type="password")
        if st.button("Entrar"):
            if senha == ADMIN_SENHA:
                st.session_state["admin_logado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
        st.stop()

    aba = st.tabs(["📋 Gestão de Leads", "📅 Agendamentos", "🖼️ Gestão de Portfólio"])

    # ---- ABA LEADS ----
    with aba[0]:
        leads = db.get_leads()
        st.write(f"**Total de solicitações:** {len(leads)}")
        for lead in leads:
            with st.expander(f"#{lead['id']} — {lead['nome']} ({lead['servico']})"):
                st.markdown(render_status_badge(lead["status"]), unsafe_allow_html=True)
                st.write(f"📞 Telefone: {lead['telefone']}")
                st.write(f"🚗 Veículo: {lead['veiculo']} — Estado: {lead['estado_veiculo']}")
                st.write(f"📝 Mensagem: {lead['mensagem'] or '—'}")
                st.write(f"🕒 Recebido em: {lead['criado_em'][:16]}")

                c1, c2, c3 = st.columns(3)
                with c1:
                    novo_status = st.selectbox(
                        "Status", ["Pendente", "Em Atendimento", "Concluído"],
                        index=["Pendente", "Em Atendimento", "Concluído"].index(lead["status"]),
                        key=f"status_{lead['id']}"
                    )
                    if novo_status != lead["status"]:
                        db.update_lead_status(lead["id"], novo_status)
                        st.rerun()
                with c2:
                    if st.button("🗑️ Excluir", key=f"del_lead_{lead['id']}"):
                        db.delete_lead(lead["id"])
                        st.rerun()

    # ---- ABA AGENDAMENTOS ----
    with aba[1]:
        agendamentos = db.get_agendamentos()
        st.write(f"**Total de agendamentos:** {len(agendamentos)}")
        for ag in agendamentos:
            with st.expander(f"#{ag['id']} — {ag['nome']} em {ag['data_preferida']} às {ag['hora_preferida']}"):
                st.write(f"📞 {ag['telefone']}")
                st.write(f"📍 Endereço: {ag['endereco']}")
                st.write(f"📝 Obs: {ag['observacoes'] or '—'}")

    # ---- ABA PORTFÓLIO ----
    with aba[2]:
        st.subheader("➕ Adicionar novo trabalho")
        with st.form("form_portfolio", clear_on_submit=True):
            titulo = st.text_input("Título do trabalho")
            descricao = st.text_area("Descrição")
            imagem = st.file_uploader("Foto do serviço (Antes/Depois)", type=["jpg", "jpeg", "png"])
            salvar = st.form_submit_button("Salvar no Portfólio")

            if salvar:
                if imagem and titulo:
                    nome_arquivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagem.name}"
                    caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
                    with open(caminho, "wb") as f:
                        f.write(imagem.getbuffer())
                    db.add_portfolio_item(titulo, descricao, caminho)
                    st.success("✅ Imagem adicionada ao portfólio!")
                    st.rerun()
                else:
                    st.error("⚠️ Título e imagem são obrigatórios.")

        st.divider()
        st.subheader("🗂️ Itens cadastrados")
        itens = db.get_portfolio()
        cols = st.columns(3)
        for i, item in enumerate(itens):
            with cols[i % 3]:
                if os.path.exists(item["caminho_imagem"]):
                    st.image(item["caminho_imagem"], use_container_width=True)
                st.caption(f"**{item['titulo']}**")
                if st.button("🗑️ Excluir", key=f"del_port_{item['id']}"):
                    if os.path.exists(item["caminho_imagem"]):
                        os.remove(item["caminho_imagem"])
                    db.delete_portfolio_item(item["id"])
                    st.rerun()
