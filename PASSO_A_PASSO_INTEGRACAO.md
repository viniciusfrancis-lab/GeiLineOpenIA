# MUDANÇAS ESPECÍFICAS - APLICAR NO SEU ARQUIVO

## OPÇÃO 1: Usar o arquivo pronto (RECOMENDADO)
Copie `streamlit_app_integrado.py` para sua pasta do projeto:
```bash
cp streamlit_app_integrado.py seu_projeto/
streamlit run streamlit_app_integrado.py
```

---

## OPÇÃO 2: Aplicar mudanças manualmente no seu arquivo original

### PASSO 1: Adicione os dados hierárquicos
**Adicione APÓS a linha 20 (depois de `st.set_page_config`)**

```python
# ========================
# DADOS HIERÁRQUICOS DE ALUNOS (NOVO)
# ========================
DADOS_HIERARQUICOS = {
    "4": {
        "label": "Quantidade de alunos",
        "valor": 184_839,
        "subitens": {
            "4.1": {
                "label": "Quantidade de alunos no Atendimento Educacional Especializado - AEE",
                "valor": 9_090
            },
            "4.2": {
                "label": "Quantidade de alunos no Atendimento Complementar - AC",
                "valor": 11_958
            },
            "4.3": {
                "label": "Quantidade de alunos no Ensino Regular",
                "valor": 184_593,
                "subitens": {
                    "4.3.1": {"label": "Quantidade de alunos no turno Manhã", "valor": 51_938},
                    "4.3.2": {"label": "Quantidade de alunos no turno Tarde", "valor": 48_983},
                    "4.3.3": {"label": "Quantidade de alunos no turno Noite", "valor": 13_255},
                    "4.3.4": {"label": "Quantidade de alunos no turno Integral 7h - Manhã", "valor": 48_989},
                    "4.3.5": {"label": "Quantidade de alunos no turno Integral 7h - Tarde", "valor": 15_270},
                    "4.3.6": {"label": "Quantidade de alunos no turno Integral 8h", "valor": 170},
                    "4.3.7": {"label": "Quantidade de alunos no turno Integral 9h30min", "valor": 6_353},
                }
            },
            "4.4": {
                "label": "Quantidade de alunos no Ensino Fundamental",
                "valor": 63_543,
                "subitens": {
                    "4.4.1": {
                        "label": "Quantidade de alunos no Ensino Fundamental - Anos Iniciais",
                        "valor": 10_859,
                        "subitens": {
                            "4.4.1.1": {"label": "1º ano do Ensino Fundamental - Anos Iniciais", "valor": 1_950},
                            "4.4.1.2": {"label": "2º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_155},
                            "4.4.1.3": {"label": "3º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_141},
                            "4.4.1.4": {"label": "4º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_138},
                            "4.4.1.5": {"label": "5º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_475},
                        }
                    },
                    "4.4.2": {
                        "label": "Quantidade de alunos no Ensino Fundamental - Anos Finais",
                        "valor": 52_684,
                        "subitens": {
                            "4.4.2.1": {"label": "6º ano do Ensino Fundamental - Anos Finais", "valor": 12_305},
                            "4.4.2.2": {"label": "7º ano do Ensino Fundamental - Anos Finais", "valor": 12_548},
                            "4.4.2.3": {"label": "8º ano do Ensino Fundamental - Anos Finais", "valor": 13_198},
                            "4.4.2.4": {"label": "9º ano do Ensino Fundamental - Anos Finais", "valor": 14_633},
                        }
                    },
                }
            },
            "4.5": {
                "label": "Quantidade de alunos no Ensino Médio",
                "valor": 107_366,
                "subitens": {
                    "4.5.1": {
                        "label": "Quantidade de alunos no Ensino Médio Regular",
                        "valor": 81_894,
                        "subitens": {
                            "4.5.1.1": {"label": "1ª série do Ensino Médio", "valor": 30_382},
                        }
                    },
                }
            },
        }
    }
}
```

---

### PASSO 2: Adicione as 3 funções de consulta
**Adicione APÓS a seção `# ======================== UTILIDADES DE NORMALIZAÇÃO`**

```python
# ========================
# FUNÇÕES PARA CONSULTA HIERÁRQUICA (NOVO)
# ========================
def detectar_codigo_hierarquico(pergunta: str) -> str | None:
    """
    Detecta se a pergunta contém um código hierárquico (4, 4.1, 4.3.1, etc.)
    Retorna o código encontrado ou None
    """
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
```

---

### PASSO 3: Atualize o prompt de boas-vindas
**MUDE esta parte (linha ~480):**

```python
# Antes:
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Olá! Eu sou a **GEI-line**, sua assistente virtual da Secretaria da "
            "Educação."
        )
```

**Para:**
```python
# Depois:
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Olá! Eu sou a **GEI-line**, sua assistente virtual da Secretaria da "
            "Educação.\n\n"
            "Você pode me perguntar sobre dados de alunos ou perguntar por um código hierárquico "
            "(ex: **4**, **4.3**, **4.4.1**) para ver o detalhamento completo! 📊"
        )
```

---

### PASSO 4: Atualize o placeholder do chat input
**MUDE esta parte (linha ~521):**

```python
# Antes:
user_message = st.chat_input("Faça uma pergunta sobre a Síntese Geral...")
```

**Para:**
```python
# Depois:
user_message = st.chat_input("Faça uma pergunta sobre a Síntese Geral ou digite um código (ex: 4, 4.3)...")
```

---

### PASSO 5: SUBSTITUIR O BLOCO DE TRATAMENTO DE MENSAGEM
**MUDE a seção completa starting em `if user_message:` (linha ~526)**

```python
# Antes (original):
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
```

**Para:**
```python
# Depois (novo):
if user_message:
    user_message = user_message.replace("$", r"\$")
    render_user_bubble(user_message)

    with st.chat_message("assistant"):
        # Detectar se é consulta hierárquica
        codigo_detectado = detectar_codigo_hierarquico(user_message)
        
        if codigo_detectado:
            # *** FLUXO DE CONSULTA HIERÁRQUICA (NOVO) ***
            item = buscar_item_hierarquico(DADOS_HIERARQUICOS, codigo_detectado)
            
            if item:
                response = formatar_resposta_hierarquica(item, codigo_detectado)
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
```

---

## ✅ CHECKLIST FINAL

- [ ] Adicionei `DADOS_HIERARQUICOS`
- [ ] Adicionei as 3 funções (`detectar_codigo_hierarquico`, `buscar_item_hierarquico`, `formatar_resposta_hierarquica`)
- [ ] Atualizei o prompt de boas-vindas
- [ ] Atualizei o placeholder do input
- [ ] Substituí o bloco `if user_message:`
- [ ] Testei com código: `4`, `4.3`
- [ ] Testei com pergunta normal

---

## 🧪 TESTES RECOMENDADOS

1. Digite `4` → deve retornar item 4 + subitens 4.1-4.5
2. Digite `4.3` → deve retornar item 4.3 + subitens 4.3.1-4.3.7
3. Digite `4.4.1` → deve retornar item 4.4.1 + subitens 4.4.1.1-4.4.1.5
4. Digite `999` → deve retornar "❌ Código não encontrado"
5. Digite pergunta normal → deve usar fluxo original (com GPT)

---

## 🆘 TROUBLESHOOTING

**Erro: "SyntaxError: invalid syntax"**
- Verifique se copiou todo o bloco `DADOS_HIERARQUICOS` corretamente
- Verifique aspas e vírgulas

**Código não é detectado**
- Certifique-se que a função `detectar_codigo_hierarquico` está depois das outras
- Verifique o import de `re` no topo

**Resposta não formata corretamente**
- Verifique se `formatar_resposta_hierarquica` usa `\n` para quebra de linhas
- Verifique a formatação Markdown (** para bold, - para listas)

---

## 📞 PRÓXIMOS PASSOS

1. Escolher OPÇÃO 1 (arquivo pronto) ou OPÇÃO 2 (mudanças manuais)
2. Testar o funcionamento
3. Adicionar mais dados hierárquicos conforme necessário
4. Integrar com Painel de Alertas se desejado
