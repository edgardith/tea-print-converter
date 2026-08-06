"""
TEA-Print Converter — App Streamlit

Interface gráfica para converter atividades pedagógicas originais em versões
adaptadas e prontas para impressão, para alunos com TEA (Educação Infantil).

Rodar localmente:
    streamlit run app.py

Hospedar de graça (para compartilhar por link, sem instalar nada):
    https://streamlit.io/cloud  (Streamlit Community Cloud)
"""
import streamlit as st

import core

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="TEA-Print Converter",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS — replica a paleta e o estilo do protótipo original (teal / âmbar)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
:root{
  --teal-50:#e1f5ee; --teal-100:#9fe1cb; --teal-500:#1d9e75; --teal-600:#0f6e56; --teal-700:#085041;
  --amber-500:#ef9f27; --amber-600:#ba7517;
  --gray-50:#f8f9fa; --gray-100:#f1efe8; --gray-200:#d3d1c7; --gray-400:#b4b2a9;
  --gray-500:#888780; --gray-600:#5f5e5a; --gray-900:#2c2c2a;
}
html, body, [class*="css"]  { font-family: 'Nunito', -apple-system, sans-serif; }
.stApp { background: linear-gradient(160deg, #e1f5ee 0%, #e6f1fb 100%); }

/* Cabeçalho */
.app-header{display:flex;align-items:center;gap:14px;margin-bottom:6px}
.app-logo{width:44px;height:44px;background:var(--teal-600);border-radius:12px;
  display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}
.app-name{font-size:24px;font-weight:800;color:var(--teal-700);letter-spacing:-.3px;margin:0}
.app-sub{font-size:13px;color:var(--gray-500);margin-top:2px}

/* Stepper */
.stepper{display:flex;align-items:flex-start;background:white;border-radius:12px;
  padding:16px 20px;margin:18px 0;box-shadow:0 1px 3px rgba(0,0,0,.07)}
.sitem{flex:1;display:flex;flex-direction:column;align-items:center;position:relative;gap:5px}
.sitem:not(:last-child)::after{content:'';position:absolute;top:14px;left:calc(50% + 16px);
  right:calc(-50% + 16px);height:2px;background:var(--gray-200);z-index:0}
.sitem.done:not(:last-child)::after,.sitem.active:not(:last-child)::after{background:var(--teal-500)}
.scirc{width:28px;height:28px;border-radius:50%;background:var(--gray-100);color:var(--gray-500);
  font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;
  position:relative;z-index:1;border:2px solid var(--gray-200)}
.sitem.active .scirc{background:var(--teal-600);color:white;border-color:var(--teal-600)}
.sitem.done .scirc{background:var(--teal-50);color:var(--teal-600);border-color:var(--teal-500)}
.slbl{font-size:11px;font-weight:700;color:var(--gray-400);text-align:center}
.sitem.active .slbl{color:var(--teal-700)}
.sitem.done .slbl{color:var(--teal-600)}

/* Card genérico */
.tea-card{background:white;border-radius:12px;padding:24px 26px;margin-bottom:14px;
  box-shadow:0 1px 3px rgba(0,0,0,.07)}
.ctit{font-size:19px;font-weight:800;color:var(--gray-900);margin-bottom:3px}
.csub{font-size:14px;color:var(--gray-500);margin-bottom:14px}

/* Nível selecionado (resumo textual) */
.level-pill{display:inline-block;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:700;
  background:var(--teal-50);color:var(--teal-700);border:1px solid var(--teal-100)}

/* Botões primários (Streamlit) */
div.stButton > button[kind="primary"]{
  background:var(--teal-600);border-color:var(--teal-600);font-weight:700;border-radius:8px;
}
div.stButton > button[kind="primary"]:hover{background:var(--teal-700);border-color:var(--teal-700)}
div.stButton > button:not([kind="primary"]){border-radius:8px;font-weight:600;color:var(--gray-600)}

/* Botão de download (PDF) */
div.stDownloadButton > button{
  background:var(--amber-500);border-color:var(--amber-500);color:white;font-weight:700;border-radius:8px;
}
div.stDownloadButton > button:hover{background:var(--amber-600);border-color:var(--amber-600)}

.ibanner{display:flex;gap:10px;padding:12px 14px;border-radius:8px;background:#e6f1fb;
  border:1.5px solid #b5d4f4;font-size:13px;color:#185fa5;margin-bottom:16px;line-height:1.5}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Estado da sessão
# ---------------------------------------------------------------------------
def _init_state():
    defaults = {
        "step": 1,
        "nivel": "1",
        "campo": "",
        "interesse": "",
        "titulo": "",
        "aluno": "",
        "usar_picto": True,
        "raw_text": "",
        "adaptado": None,
        "pdf_bytes": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()

STEP_LABELS = {1: "Importar", 2: "Configurar", 3: "Revisar", 4: "Baixar PDF"}


def ir_para(n):
    st.session_state.step = n
    st.rerun()


def render_stepper():
    cur = st.session_state.step
    html = '<div class="stepper">'
    for i in range(1, 5):
        cls = "active" if i == cur else ("done" if i < cur else "")
        html += (
            f'<div class="sitem {cls}"><div class="scirc">{i}</div>'
            f'<div class="slbl">{STEP_LABELS[i]}</div></div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Cabeçalho + Sidebar (chave de API)
# ---------------------------------------------------------------------------
st.markdown("""
<div class="app-header">
  <div class="app-logo">🧩</div>
  <div>
    <p class="app-name">TEA-Print Converter</p>
    <div class="app-sub">Adaptação pedagógica para impressão — Educação Infantil</div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔑 Chave da API Anthropic")
    st.caption(
        "Sua chave é usada apenas nesta sessão do navegador, nunca é salva em disco. "
        "Crie a sua em [console.anthropic.com](https://console.anthropic.com/settings/keys)."
    )
    api_key = st.text_input("Anthropic API Key", type="password", key="api_key_input")
    st.divider()
    st.caption(
        "💚 Pictogramas por [ARASAAC](https://arasaac.org) — Governo de Aragón, "
        "licença CC BY-NC-SA 4.0. Uso gratuito e não comercial."
    )

render_stepper()

# ---------------------------------------------------------------------------
# ETAPA 1 — Importar
# ---------------------------------------------------------------------------
if st.session_state.step == 1:
    st.markdown('<div class="tea-card">', unsafe_allow_html=True)
    st.markdown('<div class="ctit">Importar atividade</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Cole o texto ou envie um arquivo da atividade original</div>',
                unsafe_allow_html=True)

    modo = st.radio("Como você quer enviar a atividade?",
                     ["✏️ Colar texto", "📎 Enviar arquivo (PDF, DOCX, TXT, imagem)"],
                     horizontal=True, label_visibility="collapsed")

    texto_digitado = ""
    arquivo = None
    if modo.startswith("✏️"):
        texto_digitado = st.text_area(
            "Texto da atividade original", height=200,
            placeholder="Cole aqui o texto da atividade que você quer adaptar...",
            value=st.session_state.raw_text,
        )
    else:
        arquivo = st.file_uploader(
            "Arquivo da atividade original",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg", "webp"],
        )
        if arquivo is not None and arquivo.type.startswith("image"):
            st.image(arquivo, caption=arquivo.name, use_container_width=True)
        if arquivo is not None and arquivo.type.startswith("image") and not core.OCR_DISPONIVEL:
            st.warning(
                "⚠️ OCR não está disponível neste ambiente. Envie um PDF/DOCX/TXT, "
                "ou cole o texto manualmente."
            )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Próximo →", type="primary", use_container_width=True):
        if modo.startswith("✏️"):
            if not texto_digitado.strip():
                st.error("Por favor, insira o texto da atividade antes de continuar.")
            else:
                st.session_state.raw_text = texto_digitado
                ir_para(2)
        else:
            if arquivo is None:
                st.error("Por favor, envie um arquivo antes de continuar.")
            else:
                try:
                    with st.spinner("Lendo arquivo..."):
                        texto_extraido = core.ler_arquivo_upload(arquivo.name, arquivo.getvalue())
                    if not texto_extraido.strip():
                        st.error("Não foi possível extrair texto do arquivo enviado.")
                    else:
                        st.session_state.raw_text = texto_extraido
                        ir_para(2)
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {e}")

# ---------------------------------------------------------------------------
# ETAPA 2 — Configurar
# ---------------------------------------------------------------------------
elif st.session_state.step == 2:
    st.markdown('<div class="tea-card">', unsafe_allow_html=True)
    st.markdown('<div class="ctit">Configurar adaptação</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Defina o perfil pedagógico do aluno</div>', unsafe_allow_html=True)

    st.markdown("**Nível de suporte — DSM-5**")
    opcoes_nivel = {k: f"{v['nome']} — {v['desc']}" for k, v in core.NIVEIS.items()}
    nivel = st.radio(
        "Nível de suporte", options=list(opcoes_nivel.keys()),
        format_func=lambda k: opcoes_nivel[k],
        index=list(opcoes_nivel.keys()).index(st.session_state.nivel),
        label_visibility="collapsed",
    )
    st.session_state.nivel = nivel

    st.markdown("**Campo de Experiência — BNCC** *(opcional)*")
    campo = st.selectbox(
        "Campo BNCC", options=[""] + core.CAMPOS_BNCC,
        index=([""] + core.CAMPOS_BNCC).index(st.session_state.campo)
        if st.session_state.campo in core.CAMPOS_BNCC else 0,
        label_visibility="collapsed",
    )
    st.session_state.campo = campo

    st.session_state.interesse = st.text_input(
        "Interesse especial (opcional)",
        value=st.session_state.interesse,
        placeholder="Ex: Dinossauros, Planetas, Minecraft...",
    )
    st.session_state.titulo = st.text_input(
        "Título da atividade",
        value=st.session_state.titulo,
        placeholder="Ex: Caça-Palavras — Animais Marinhos",
    )
    st.session_state.aluno = st.text_input(
        "Nome do aluno (opcional)",
        value=st.session_state.aluno,
        placeholder="Deixar em branco para preencher à mão",
    )
    st.session_state.usar_picto = st.checkbox(
        "Buscar pictogramas reais no ARASAAC", value=st.session_state.usar_picto,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("← Voltar", use_container_width=True):
            ir_para(1)
    with col2:
        if st.button("✨ Adaptar atividade", type="primary", use_container_width=True):
            if not st.session_state.get("api_key_input"):
                st.error("Insira sua Anthropic API Key na barra lateral antes de continuar.")
            else:
                try:
                    with st.spinner("Adaptando atividade... isso pode levar alguns segundos."):
                        adaptado = core.adaptar_atividade(
                            api_key=st.session_state.api_key_input,
                            texto_original=st.session_state.raw_text,
                            nivel=st.session_state.nivel,
                            campo=st.session_state.campo,
                            interesse=st.session_state.interesse,
                        )
                    st.session_state.adaptado = adaptado
                    if not st.session_state.titulo:
                        st.session_state.titulo = adaptado.get("titulo", "")
                    st.session_state.pdf_bytes = None
                    ir_para(3)
                except Exception as e:
                    st.error(f"Erro ao adaptar a atividade: {e}")

# ---------------------------------------------------------------------------
# ETAPA 3 — Revisar
# ---------------------------------------------------------------------------
elif st.session_state.step == 3:
    adaptado = st.session_state.adaptado
    st.markdown('<div class="tea-card">', unsafe_allow_html=True)
    st.markdown('<div class="ctit">Revisar</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Confira o conteúdo gerado antes de baixar o PDF</div>',
                unsafe_allow_html=True)

    if not adaptado:
        st.warning("Nenhum conteúdo adaptado ainda. Volte à etapa anterior.")
    else:
        aba_aluno, aba_prof = st.tabs(["🧒 Atividade do aluno", "👩‍🏫 Orientações do professor"])
        with aba_aluno:
            st.markdown(f"**{adaptado.get('titulo', '')}**")
            for p in adaptado.get("passos", []):
                st.write(f"{p.get('numero')}. [🖼 {p.get('pictograma')}] {p.get('texto')}")
            if adaptado.get("banco_palavras"):
                st.write("**Banco de palavras:** " + "  |  ".join(adaptado["banco_palavras"]))
            if adaptado.get("zona_resposta"):
                st.caption("Zona de resposta: " + adaptado["zona_resposta"].get("descricao", ""))
        with aba_prof:
            o = adaptado.get("orientacoes", {})
            if o.get("objetivo"):
                st.write("**Objetivo (BNCC):** " + o["objetivo"])
            if o.get("como_apresentar"):
                st.write("**Como apresentar:**")
                for i, passo in enumerate(o["como_apresentar"], 1):
                    st.write(f"{i}. {passo}")
            if o.get("dificuldades"):
                st.write("**Dificuldades e estratégias:**")
                for d in o["dificuldades"]:
                    st.write(f"- *{d.get('problema')}* → {d.get('estrategia')}")
            if o.get("materiais"):
                st.write("**Materiais:** " + ", ".join(o["materiais"]))
            if o.get("caa"):
                st.write("**Uso de CAA:** " + o["caa"])

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar", use_container_width=True):
            ir_para(2)
    with col2:
        if st.button("Próximo →", type="primary", use_container_width=True, disabled=not adaptado):
            ir_para(4)

# ---------------------------------------------------------------------------
# ETAPA 4 — Baixar PDF
# ---------------------------------------------------------------------------
elif st.session_state.step == 4:
    adaptado = st.session_state.adaptado
    st.markdown('<div class="tea-card">', unsafe_allow_html=True)
    st.markdown('<div class="ctit">Baixar PDF</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">O arquivo é gerado no momento do clique — nada fica salvo em servidor</div>',
                unsafe_allow_html=True)

    if adaptado:
        nivel_info = core.NIVEIS[st.session_state.nivel]
        st.write(f"**Título:** {st.session_state.titulo or adaptado.get('titulo', '')}")
        st.write(f"**Aluno:** {st.session_state.aluno or '(preencher à mão)'}")
        st.write(f"**Nível:** {nivel_info['nome']}")
        st.write(f"**Campo BNCC:** {st.session_state.campo or '—'}")
        st.write(f"**Interesse especial:** {st.session_state.interesse or '—'}")

    st.markdown(
        '<div class="ibanner">📄 Gera um PDF com <b>2 páginas A4</b>: '
        'atividade do aluno e orientações do professor.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar para edição", use_container_width=True):
            ir_para(3)
    with col2:
        if st.button("Gerar PDF", type="primary", use_container_width=True, disabled=not adaptado):
            with st.spinner("Gerando PDF... buscando pictogramas no ARASAAC" if st.session_state.usar_picto
                             else "Gerando PDF..."):
                st.session_state.pdf_bytes = core.gerar_pdf_bytes(
                    adaptado,
                    titulo_atividade=st.session_state.titulo or adaptado.get("titulo", "Atividade Adaptada"),
                    nome_aluno=st.session_state.aluno,
                    nivel=st.session_state.nivel,
                    usar_pictogramas=st.session_state.usar_picto,
                )

    if st.session_state.pdf_bytes:
        nome_arquivo = (st.session_state.titulo or "atividade").lower()
        nome_arquivo = "".join(ch if ch.isalnum() else "-" for ch in nome_arquivo).strip("-") or "atividade"
        st.download_button(
            "⬇️ Baixar PDF",
            data=st.session_state.pdf_bytes,
            file_name=f"{nome_arquivo}-adaptada.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
