# ========================
# IMPORTS
# ========================
import streamlit as st
import datetime
import textwrap
import time
import re
import unicodedata
import pandas as pd
from PIL import Image
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

st.set_page_config(
    page_title="Olá, sou GeiLine sua Assistente Virtual",
    page_icon=Image.open("icon.png"),
    layout="wide",
)

# ========================
# ESTILO VISUAL (IDENTIDADE GOVERNO DO ESPÍRITO SANTO)
# ========================
# Apenas visual — não altera nenhuma lógica do aplicativo.
GEI_AZUL = "#0C447C"        # azul institucional
GEI_AZUL_CLARO = "#185FA5"  # azul de apoio (balão do usuário)
GEI_DOURADO = "#EF9F27"     # detalhe da bandeira capixaba
GEI_VERDE = "#639922"       # status / sucesso

st.markdown(
    f"""
    <style>
    /* ---- Largura central e respiro ---- */
    .block-container {{
        max-width: 880px;
<<<<<<< HEAD
        padding-top: 3rem;
=======
        padding-top: 0rem;
>>>>>>> ad7dabe (ajuste header full width)
        padding-bottom: 6rem;
        overflow: visible;
    }}
    /* Garante que o header largo não seja cortado horizontalmente */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        overflow-x: hidden;
    }}

<<<<<<< HEAD
    /* ---- Esconde o título e o caption nativos (substituídos pelo header) ---- */
    /* (mantidos no código, mas ocultados visualmente para não duplicar) */

    /* ---- Header institucional (largura total, ~1cm de borda lateral) ---- */
    .gei-header {{
        background: {GEI_AZUL};
        border-radius: 14px 14px 0 0;
        padding: 18px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: calc(100vw - 76px);
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        margin-top: 12px;
=======
    /* ---- Remove barra nativa do topo sem afetar outros elementos ---- */
    [data-testid="stHeader"] {{
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }}

    /* ---- Header institucional (largura total, sem espaços laterais) ---- */
    .gei-header {{
        background: {GEI_AZUL};
        border-radius: 0;
        padding: 18px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100vw;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        margin-top: 0;
        box-sizing: border-box;
>>>>>>> ad7dabe (ajuste header full width)
    }}
    .gei-header-left {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .gei-logo {{
        width: 46px;
        height: 46px;
        border-radius: 10px;
        background: rgba(255,255,255,0.16);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }}
    .gei-title {{
        font-size: 20px;
        font-weight: 600;
        color: #fff;
        margin: 0;
        letter-spacing: -0.2px;
        line-height: 1.1;
    }}
    .gei-subtitle {{
        font-size: 12px;
        color: rgba(255,255,255,0.82);
        margin: 2px 0 0 0;
    }}
    .gei-status {{
        display: flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.14);
        padding: 5px 11px;
        border-radius: 20px;
    }}
    .gei-status-dot {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: {GEI_VERDE};
        display: inline-block;
    }}
    .gei-status-text {{
        font-size: 11px;
        color: #fff;
    }}
    .gei-faixa {{
        height: 3px;
        background: {GEI_DOURADO};
        border-radius: 0;
        margin-bottom: 18px;
<<<<<<< HEAD
        width: calc(100vw - 76px);
        position: relative;
        left: 50%;
        transform: translateX(-50%);
=======
        width: 100vw;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        box-sizing: border-box;
>>>>>>> ad7dabe (ajuste header full width)
    }}
    .gei-rodape {{
        text-align: center;
        font-size: 11px;
        color: rgba(120,120,120,0.85);
        margin-top: 28px;
    }}

    /* ---- Balões de chat ---- */
    [data-testid="stChatMessage"] {{
        background: transparent;
        padding: 0.25rem 0;
        align-items: flex-start;
    }}

    /* === Mensagem do USUÁRIO: balão azul à DIREITA (HTML próprio) === */
    .gei-user-row {{
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin: 4px 0;
    }}
    .gei-user-bubble {{
        background: {GEI_AZUL_CLARO};
        color: #fff;
        border-radius: 14px 14px 3px 14px;
        padding: 9px 15px;
        max-width: 78%;
        font-size: 15px;
        line-height: 1.5;
        word-wrap: break-word;
    }}

    /* === Mensagem da ASSISTENTE: balão cinza à ESQUERDA === */
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] > div:first-child {{
        background: rgba(0,0,0,0.04);
        border-radius: 14px 14px 14px 3px;
        padding: 9px 15px;
        width: fit-content;
        max-width: 100%;
    }}

    /* ---- Avatar da assistente ---- */
    [data-testid="stChatMessageAvatarAssistant"] {{
        background: #E6F1FB !important;
        color: {GEI_AZUL} !important;
    }}

    /* ---- Barra de input arredondada ---- */
    [data-testid="stChatInput"] {{
        border-radius: 24px;
        border: 0.5px solid rgba(0,0,0,0.2);
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: rgba(0,0,0,0.4);
    }}

    /* ---- Botão de enviar com cor institucional ---- */
    [data-testid="stChatInputSubmitButton"] {{
        background: {GEI_AZUL} !important;
        color: #fff !important;
        border-radius: 50% !important;
    }}
    [data-testid="stChatInputSubmitButton"] svg {{
        fill: #fff !important;
        color: #fff !important;
    }}

    /* ---- Banner de sucesso mais discreto ---- */
    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ========================
# CONFIGURAÇÕES
# ========================
MODEL = "gpt-4.1-mini"

ARQUIVO_DADOS = "dados/dados.xlsx"

HISTORY_LENGTH = 20
SUMMARIZE_OLD_HISTORY = False
MIN_TIME_BETWEEN_REQUESTS = datetime.timedelta(seconds=2)
MAX_LINHAS_CONTEXTO = 20


# ========================
# UTILIDADES DE NORMALIZAÇÃO
# ========================
def normalizar(texto: str) -> str:
    """Remove acentos e lowercase, para comparação robusta."""
    texto = unicodedata.normalize("NFD", str(texto))
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.lower()


STOPWORDS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "ou", "em",
    "para", "por", "com", "sem", "que", "qual", "quais", "quantos", "quantas",
    "quanto", "quanta", "um", "uma", "uns", "umas", "no", "na", "nos", "nas",
    "ao", "aos", "se", "tem", "ha", "muito", "muitos", "muita", "muitas",
    "rede", "estadual", "estado", "ser", "sao", "ja", "la", "ate",
    "sobre", "sua", "seu", "suas", "seus", "este", "esta", "isso", "essa",
    "esse", "esses", "essas", "me", "diga", "diz", "fale", "informe",
    "mostre", "liste", "voce", "vc", "favor", "obrigado",
}


def extrair_palavras_chave(pergunta: str) -> set:
    pergunta_norm = normalizar(pergunta)
    palavras = re.findall(r"\b[a-z0-9º°ª]+\b", pergunta_norm)
    return {p for p in palavras if p not in STOPWORDS and len(p) >= 3}


# ========================
# CARREGA O EXCEL (ESTRUTURADO POR LINHA)
# ========================
@st.cache_data
def carregar_dados_estruturado():
    xl = pd.ExcelFile(ARQUIVO_DADOS)
    linhas = []
    for aba in xl.sheet_names:
        df = xl.parse(aba, header=None)
        df = df.iloc[:, -2:]
        df.columns = ["indicador", "quant"]

        df = df.dropna(subset=["indicador", "quant"], how="any")
        df["indicador"] = df["indicador"].astype(str).str.strip()
        df["quant"] = df["quant"].astype(str).str.strip()
        df = df[(df["quant"] != "") & (df["quant"] != "nan")]
        df = df[df["indicador"].str.lower() != "indicador"]

        for _, row in df.iterrows():
            ind = row["indicador"]
            m = re.match(r"^([\d.]+)\.\s*(.*)", ind)
            hierarquia = m.group(1) if m else ""
            linhas.append({
                "aba": aba,
                "hierarquia": hierarquia,
                "indicador": ind,
                "quant": row["quant"],
                "busca": normalizar(ind),
            })
    return linhas


def filtrar_linhas_relevantes(linhas, pergunta, max_linhas=MAX_LINHAS_CONTEXTO):
    palavras = extrair_palavras_chave(pergunta)

    if not palavras:
        return linhas[:max_linhas]

    matches = []
    for linha in linhas:
        score = sum(1 for p in palavras if p in linha["busca"])
        if score > 0:
            matches.append((score, linha))

    if not matches:
        return linhas[:max_linhas]

    matches.sort(key=lambda x: -x[0])
    matches = matches[:max_linhas]
    selecionadas_ids = {id(m[1]) for m in matches}

    hierarquias_inclusas = {m[1]["hierarquia"] for m in matches}
    pais_a_incluir = set()
    for h in hierarquias_inclusas:
        if not h:
            continue
        partes = h.split(".")
        for i in range(1, len(partes)):
            pai = ".".join(partes[:i])
            pais_a_incluir.add(pai)

    resultado_ids = set(selecionadas_ids)
    resultado = [m[1] for m in matches]
    for l in linhas:
        if l["hierarquia"] in pais_a_incluir and id(l) not in resultado_ids:
            resultado.append(l)
            resultado_ids.add(id(l))

    index_map = {id(l): i for i, l in enumerate(linhas)}
    resultado.sort(key=lambda l: index_map[id(l)])
    return resultado


def formatar_contexto(linhas_filtradas):
    if not linhas_filtradas:
        return ""
    texto = "indicador|quant\n"
    for l in linhas_filtradas:
        ind = re.sub(r"^[Qq]uantidade de\s+", "", l["indicador"])
        texto += f"{ind}|{l['quant']}\n"
    return texto


# ========================
# CONTADOR DE TOKENS (estimativa)
# ========================
def estimar_tokens(texto: str) -> int:
    return int(len(texto) / 3.5)


# ========================
# CLIENTE OPENAI
# ========================
@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ========================
# HELPERS
# ========================
TaskInfo = namedtuple("TaskInfo", ["name", "function", "args"])
TaskResult = namedtuple("TaskResult", ["name", "result"])

executor = ThreadPoolExecutor(max_workers=5)


def history_to_text(chat_history):
    return "\n".join(f"[{h['role']}]: {h['content']}" for h in chat_history)


def build_prompt(**kwargs):
    prompt = []
    for name, contents in kwargs.items():
        if contents:
            prompt.append(f"<{name}>\n{contents}\n</{name}>")
    return "\n".join(prompt)


def generate_chat_summary(messages):
    prompt = build_prompt(
        instructions="Seja gentil e delicada, informe as dados completos.",
        conversation=history_to_text(messages),
    )
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def build_question_prompt(question, linhas):
    linhas_filtradas = filtrar_linhas_relevantes(linhas, question)
    dados_contexto = formatar_contexto(linhas_filtradas)

    old_history = st.session_state.messages[:-HISTORY_LENGTH]
    recent_history = st.session_state.messages[-HISTORY_LENGTH:]
    recent_history_str = history_to_text(recent_history) if recent_history else None

    task_infos = []
    if SUMMARIZE_OLD_HISTORY and old_history:
        task_infos.append(
            TaskInfo("old_message_summary", generate_chat_summary, (old_history,))
        )

    results = executor.map(
        lambda t: TaskResult(name=t.name, result=t.function(*t.args)),
        task_infos,
    )
    context = {name: result for name, result in results}

    instructions = textwrap.dedent("""
    Você é um assistente especializado nos dados da Rede Estadual de Ensino do Espírito Santo.
    - Responda APENAS com base nos dados em <dados_planilha>.
    - Se a informação não estiver nos dados fornecidos, diga claramente que não foi encontrada.    
    - NUNCA inicie a resposta apenas com um número. Sempre use uma palavra antes (ex: "São 384 escolas" em vez de "384.").
    - Não invente dados. Não use conhecimento externo.
    - Se a pergunta for ambígua, peça esclarecimento.
    - Para cálculos, mostre o passo a passo usando apenas os dados fornecidos.
    - A palavra quantidade e numero são o mesmo comando.
    """)

    full_prompt = build_prompt(
        instructions=instructions,
        dados_planilha=dados_contexto,
        **context,
        recent_messages=recent_history_str,
        question=question,
    )
    return full_prompt, len(linhas_filtradas)


def get_response_stream(prompt):
    client = get_client()
    try:
        stream = client.chat.completions.create(
            model=MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except Exception as e:
        yield f"\n\n⚠️ Erro ao chamar a API: {str(e)}"


# ========================
# UI
# ========================
# ---- Header institucional (visual) ----
st.markdown(
    """
    <div class="gei-header">
        <div class="gei-header-left">
            <div class="gei-logo">✨</div>
            <div>
                <p class="gei-title">GEI-line</p>
                <p class="gei-subtitle">Assistente Virtual · Secretaria da Educação</p>
            </div>
        </div>
        <div class="gei-status">
            <span class="gei-status-dot"></span>
            <span class="gei-status-text">Online</span>
        </div>
    </div>
    <div class="gei-faixa"></div>
    """,
    unsafe_allow_html=True,
)

with st.spinner("Carregando planilha..."):
    try:
        linhas_planilha = carregar_dados_estruturado()
        planilha_ok = True
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: `{ARQUIVO_DADOS}`")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "total_perguntas" not in st.session_state:
    st.session_state.total_perguntas = 0

# ---- Mensagem de apresentação da GEI-line (aparece ao abrir) ----
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Olá! Eu sou a **GEI-line**, sua assistente virtual da Secretaria da "
            "Educação."
        )

with st.sidebar:
    st.markdown("### 📊 Uso de tokens")
    st.metric("Perguntas feitas", st.session_state.total_perguntas)
    st.metric("Tokens estimados (total)", f"{st.session_state.total_tokens:,}")
    if st.session_state.total_perguntas > 0:
        media = st.session_state.total_tokens // st.session_state.total_perguntas
        st.metric("Média por pergunta", f"{media:,}")

    st.divider()
    st.markdown("### ⚙️ Configuração")
    st.caption(f"Modelo: `{MODEL}`")
    st.caption(f"Indicadores na planilha: {len(linhas_planilha)}")
    st.caption(f"Máx. de linhas por pergunta: {MAX_LINHAS_CONTEXTO}")
    st.caption("Estimativa: ~3.5 chars/token")

def render_user_bubble(texto):
    """Renderiza a mensagem do usuário como balão azul alinhado à direita.
    Usa HTML puro para não depender de seletores CSS frágeis do Streamlit."""
    import html as _html
    texto_seguro = _html.escape(str(texto)).replace("\n", "<br>")
    st.markdown(
        f'<div class="gei-user-row">'
        f'<div class="gei-user-bubble">{texto_seguro}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        render_user_bubble(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

user_message = st.chat_input("Faça uma pergunta sobre a Síntese Geral...")

if "prev_question_timestamp" not in st.session_state:
    st.session_state.prev_question_timestamp = datetime.datetime.fromtimestamp(0)

if user_message:
    user_message = user_message.replace("$", r"\$")

    render_user_bubble(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Aguardando..."):
            now = datetime.datetime.now()
            diff = now - st.session_state.prev_question_timestamp
            st.session_state.prev_question_timestamp = now
            if diff < MIN_TIME_BETWEEN_REQUESTS:
                time.sleep(diff.seconds + diff.microseconds * 0.001)

        with st.spinner("Filtrando dados relevantes..."):
            full_prompt, n_linhas = build_question_prompt(user_message, linhas_planilha)
            tokens_prompt = estimar_tokens(full_prompt)

        with st.container():
            response = st.write_stream(get_response_stream(full_prompt))

            tokens_resposta = estimar_tokens(response)
            tokens_total = tokens_prompt + tokens_resposta

            st.session_state.total_tokens += tokens_total
            st.session_state.total_perguntas += 1

            st.caption(
                f"🔢 Tokens: **{tokens_total:,}** "
                f"(entrada: {tokens_prompt:,} | saída: {tokens_resposta:,}) | "
                f"📋 {n_linhas} indicadores enviados de {len(linhas_planilha)}"
            )

            st.session_state.messages.append({"role": "user", "content": user_message})
            st.session_state.messages.append({"role": "assistant", "content": response})

# ---- Rodapé institucional ----
st.markdown(
    '<div class="gei-rodape">GEI-line · Secretaria de Estado da Educação · '
    'Governo do Espírito Santo</div>',
    unsafe_allow_html=True,
)
