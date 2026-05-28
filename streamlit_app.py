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
GEI_AZUL = "#0C447C"
GEI_AZUL_CLARO = "#185FA5"
GEI_DOURADO = "#EF9F27"
GEI_VERDE = "#639922"

st.markdown(
    f"""
    <style>
    .block-container {{
        max-width: 880px;
        padding-top: 0rem;
        padding-bottom: 6rem;
        overflow: visible;
    }}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        overflow-x: hidden;
    }}

    [data-testid="stHeader"] {{
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }}

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
        width: 100vw;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        box-sizing: border-box;
    }}
    .gei-rodape {{
        text-align: center;
        font-size: 11px;
        color: rgba(120,120,120,0.85);
        margin-top: 28px;
    }}

    [data-testid="stChatMessage"] {{
        background: transparent;
        padding: 0.25rem 0;
        align-items: flex-start;
    }}

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

    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] > div:first-child {{
        background: rgba(0,0,0,0.04);
        border-radius: 14px 14px 14px 3px;
        padding: 9px 15px;
        width: fit-content;
        max-width: 100%;
    }}

    [data-testid="stChatMessageAvatarAssistant"] {{
        background: #E6F1FB !important;
        color: {GEI_AZUL} !important;
    }}

    [data-testid="stChatInput"] {{
        border-radius: 24px;
        border: 0.5px solid rgba(0,0,0,0.2);
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: rgba(0,0,0,0.4);
    }}

    [data-testid="stChatInputSubmitButton"] {{
        background: {GEI_AZUL} !important;
        color: #fff !important;
        border-radius: 50% !important;
    }}
    [data-testid="stChatInputSubmitButton"] svg {{
        fill: #fff !important;
        color: #fff !important;
    }}

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
MIN_TIME_BETWEEN_REQUESTS = datetime.timedelta(seconds=0)
MAX_LINHAS_CONTEXTO = 80


# ========================
# FUNÇÕES PARA CONSULTA HIERÁRQUICA (NOVO)
# ========================
def detectar_codigo_hierarquico(pergunta: str) -> str | None:
    """
    Detecta se a pergunta contém um código hierárquico (4, 4.1, 4.3.1, etc.)
    Retorna o código encontrado ou None
    """
    # Padrão: número.número.número... (ex: 4, 4.3, 4.3.1)
    match = re.search(r'\b(4(?:\.\d+)*)\b', pergunta)
    return match.group(1) if match else None


def buscar_item_hierarquico(dados: dict, codigo: str) -> dict | None:
    """Busca recursivamente um item no dicionário hierárquico"""
    if codigo in dados:
        return dados[codigo]
    
    for chave, valor in dados.items():
        if "subitens" in valor:
            resultado = buscar_item_hierarquico(valor["subitens"], codigo)
            if resultado:
                return resultado
    return None


def formatar_resposta_hierarquica(item: dict, codigo: str) -> str:
    """Formata a resposta hierárquica de forma legível"""
    linhas = []
    linhas.append(f"**{codigo}** - {item['label']}")
    linhas.append(f"**Quantidade: {item['valor']:,}**\n")
    
    if "subitens" in item:
        linhas.append("**Detalhamento:**\n")
        for sub_codigo, sub_item in item["subitens"].items():
            linhas.append(f"- {sub_codigo}: {sub_item['label']} → **{sub_item['valor']:,}**")
    
    return "\n".join(linhas)


# ========================
# UTILIDADES DE NORMALIZAÇÃO
# ========================
def normalizar(texto: str) -> str:
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
# CARREGA O EXCEL
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
            
            # Extrai código hierárquico (4, 4.1, 4.3.1, etc.)
            m = re.match(r"^([\d.]+)\.\s*(.*)", ind)
            codigo_hierarquico = m.group(1) if m else ""
            
            try:
                quant_valor = int(float(row["quant"]))
            except (ValueError, TypeError):
                continue  # Pula linhas com valores inválidos
            
            linhas.append({
                "indicador": ind,
                "quant": quant_valor,
                "hierarquia": codigo_hierarquico,  # Agora é string: "4", "4.1", etc
                "busca": normalizar(ind),
            })
    
    return linhas


# ========================
# FUNÇÕES PARA CONSULTA HIERÁRQUICA DINÂMICA (NOVO)
# ========================
def detectar_codigo_hierarquico(pergunta: str) -> str | None:
    """
    Detecta se a pergunta contém um código hierárquico (4, 4.1, 4.3.1, etc.)
    ou se pergunta é sobre "quantidade de alunos"
    Retorna o código raiz ou None
    """
    # Detectar "quantidade de alunos" → retorna "4"
    # Aceita: aluno, alunos, estudante, estudantes
    if re.search(r'\b(quantidade|quantos).*(aluno|estudante)s?\b', pergunta.lower()):
        return "4"
    
    # Padrão: número.número.número... (ex: 4, 4.3, 4.4.1)
    match = re.search(r'\b(\d+(?:\.\d+)*)\b', pergunta)
    return match.group(1) if match else None


def buscar_itens_hierarquicos(linhas, codigo_raiz: str) -> list:
    """
    Busca APENAS os subitens diretos do código raiz (1 nível abaixo)
    Ex: "4" retorna [4, 4.1, 4.2, 4.3, 4.4, 4.5]
    Ex: "4.3" retorna [4.3, 4.3.1, 4.3.2, 4.3.3, 4.3.4, 4.3.5, 4.3.6, 4.3.7]
    """
    # Encontrar o item principal
    item_principal = None
    subitens_diretos = []
    
    for l in linhas:
        if l["hierarquia"] == codigo_raiz:
            item_principal = l
        # Subitens diretos: começam com código_raiz + ponto, e têm apenas 1 nível a mais
        elif l["hierarquia"].startswith(codigo_raiz + "."):
            # Contar quantos pontos tem a diferença
            sufixo = l["hierarquia"][len(codigo_raiz) + 1:]  # Remove o código raiz e o ponto
            # Se tem exatamente 1 ponto, é subitem direto
            # Se tem 0 pontos, é subitem direto
            if sufixo.count(".") == 0:  # Sem mais pontos = nível direto
                subitens_diretos.append(l)
    
    # Retornar item principal + subitens diretos
    resultado = []
    if item_principal:
        resultado.append(item_principal)
    resultado.extend(sorted(subitens_diretos, key=lambda x: x["hierarquia"]))
    
    return resultado


def formatar_resposta_hierarquica(itens: list, codigo_raiz: str) -> str:
    """Formata a resposta hierárquica de forma legível"""
    if not itens:
        return f"❌ Nenhum dado encontrado para código `{codigo_raiz}`"
    
    linhas = []
    
    # Item principal (o código raiz exato)
    item_principal = None
    for item in itens:
        if item["hierarquia"] == codigo_raiz:
            item_principal = item
            break
    
    if item_principal:
        linhas.append(f"**{item_principal['hierarquia']}** - {item_principal['indicador']}")
        linhas.append(f"**Quantidade: {item_principal['quant']:,}**\n")
    
    # Todos os subitens
    subitens = [i for i in itens if i["hierarquia"] != codigo_raiz]
    
    if subitens:
        linhas.append("**Detalhamento:**\n")
        for subitem in subitens:
            # Remove o prefixo do código e o número para exibição limpa
            label_limpo = re.sub(r"^[\d.]+\.\s*", "", subitem["indicador"])
            linhas.append(f"- **{subitem['hierarquia']}**: {label_limpo} → **{subitem['quant']:,}**")
    
    return "\n".join(linhas)


def filtrar_linhas_relevantes(linhas, pergunta):
    palavras_chave = extrair_palavras_chave(pergunta)
    
    if not palavras_chave:
        return linhas[:MAX_LINHAS_CONTEXTO]
    
    resultado = []
    resultado_ids = set()
    
    for l in linhas:
        indicador_norm = normalizar(l["indicador"])
        indicador_palavras = set(re.findall(r"\b[a-z0-9º°ª]+\b", indicador_norm))
        
        if palavras_chave & indicador_palavras and id(l) not in resultado_ids:
            resultado.append(l)
            resultado_ids.add(id(l))
    
    if not resultado:
        # Se nenhum match por palavras, retorna primeiras linhas
        resultado = linhas[:MAX_LINHAS_CONTEXTO]
    
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
# CONTADOR DE TOKENS
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
        max_tokens=5120,
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

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Olá! Eu sou a **GEI-line**, sua assistente virtual da Secretaria da "
            "Educação.\n\n"
            "Você pode me perguntar sobre dados de alunos ou perguntar por um código hierárquico "
            "(ex: **4**, **4.3**, **4.4.1**) para ver o detalhamento completo! 📊"
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

user_message = st.chat_input("Faça uma pergunta sobre a Síntese Geral ou digite um código (ex: 4, 4.3)...")

if "prev_question_timestamp" not in st.session_state:
    st.session_state.prev_question_timestamp = datetime.datetime.fromtimestamp(0)

if user_message:
    user_message = user_message.replace("$", r"\$")
    render_user_bubble(user_message)

    with st.chat_message("assistant"):
        # Detectar se é consulta hierárquica
        codigo_detectado = detectar_codigo_hierarquico(user_message)
        
        if codigo_detectado:
            # *** FLUXO DE CONSULTA HIERÁRQUICA DINÂMICA (NOVO) ***
            itens = buscar_itens_hierarquicos(linhas_planilha, codigo_detectado)
            
            if itens:
                response = formatar_resposta_hierarquica(itens, codigo_detectado)
                st.markdown(response)
                tokens_resposta = estimar_tokens(response)
                st.caption(f"🔢 Tokens: **{tokens_resposta:,}** | 📋 Consulta hierárquica")
            else:
                response = f"❌ Código hierárquico `{codigo_detectado}` não encontrado nos dados."
                st.markdown(response)
        else:
            # *** FLUXO NORMAL (PLANILHA + GPT) ***
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
