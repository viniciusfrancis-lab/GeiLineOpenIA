# GUIA DE INTEGRAÇÃO - CONSULTA HIERÁRQUICA NO STREAMLIT

## 📋 O que foi adicionado?

Três novos componentes foram integrados ao seu app Streamlit:

### 1️⃣ DADOS HIERÁRQUICOS (linhas 22-103)
```python
DADOS_HIERARQUICOS = {
    "4": {
        "label": "Quantidade de alunos",
        "valor": 184_839,
        "subitens": {
            "4.1": {...},
            "4.2": {...},
            # ... mais subitens
        }
    }
}
```
- Estrutura em árvore que armazena todos os códigos hierárquicos
- Cada item tem: label, valor, e opcionalmente subitens

### 2️⃣ FUNÇÕES DE CONSULTA HIERÁRQUICA (linhas 274-305)

**`detectar_codigo_hierarquico(pergunta)`**
- Procura por padrões como "4", "4.3", "4.4.1" na pergunta
- Retorna o código encontrado ou None

**`buscar_item_hierarquico(dados, codigo)`**
- Busca recursivamente um código na árvore hierárquica
- Funciona para qualquer nível de profundidade

**`formatar_resposta_hierarquica(item, codigo)`**
- Formata o resultado de forma legível
- Exibe o item principal + todos os subitens

### 3️⃣ NOVO FLUXO NO CHAT (linhas 507-545)

Agora quando o usuário envia uma mensagem, o app verifica:

```
Usuário digita → Detecta código hierárquico?
                 ├─ SIM: Busca na árvore + formatação rápida
                 └─ NÃO: Fluxo normal (filtro + GPT)
```

---

## 🎯 COMO USAR?

### Exemplo 1: Consulta simples
```
Usuário: "4"
Resposta:
  4 - Quantidade de alunos
  Quantidade: 184,839
  
  Detalhamento:
  - 4.1: Quantidade de alunos no AEE → 9,090
  - 4.2: Quantidade de alunos no AC → 11,958
  - 4.3: Quantidade de alunos no Ensino Regular → 184,593
  - 4.4: Quantidade de alunos no Ensino Fundamental → 63,543
  - 4.5: Quantidade de alunos no Ensino Médio → 107,366
```

### Exemplo 2: Subnível
```
Usuário: "4.3"
Resposta:
  4.3 - Quantidade de alunos no Ensino Regular
  Quantidade: 184,593
  
  Detalhamento:
  - 4.3.1: Quantidade de alunos no turno Manhã → 51,938
  - 4.3.2: Quantidade de alunos no turno Tarde → 48,983
  - ... (até 4.3.7)
```

### Exemplo 3: Nível profundo
```
Usuário: "4.4.1"
Resposta:
  4.4.1 - Quantidade de alunos no Ensino Fundamental - Anos Iniciais
  Quantidade: 10,859
  
  Detalhamento:
  - 4.4.1.1: 1º ano → 1,950
  - 4.4.1.2: 2º ano → 2,155
  - ... (até 4.4.1.5)
```

### Exemplo 4: Pergunta normal (usa fluxo original)
```
Usuário: "quantos alunos tem no ensino médio?"
Resposta: Usa o fluxo normal (filtro + GPT)
```

---

## 🔧 DIFERENÇAS PRINCIPAIS

| Aspecto | Código Hierárquico | Pergunta Normal |
|---------|-------------------|-----------------|
| Detecção | Padrão regex: `4.x.x` | Palavras-chave |
| Processamento | Busca na árvore | Filtro + GPT |
| Velocidade | ⚡ Instantâneo | Normal |
| Tokens usados | ~5-50 | ~500-2000 |
| Resposta | Estruturada | Natural |

---

## 📝 COMO CUSTOMIZAR?

### Adicionar mais dados hierárquicos:

1. Abra o arquivo e encontre `DADOS_HIERARQUICOS = {`
2. Adicione novos itens seguindo a estrutura:

```python
"4.5.1.1": {
    "label": "1ª série do Ensino Médio",
    "valor": 30_382
}
```

Se tiver subitens:
```python
"4.5": {
    "label": "Quantidade de alunos no Ensino Médio",
    "valor": 107_366,
    "subitens": {
        "4.5.1": {...}
    }
}
```

### Mudar o prompt de boas-vindas:

Procure por:
```python
st.markdown(
    "Olá! Eu sou a **GEI-line**..."
)
```

E modifique conforme necessário.

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [ ] Substituir arquivo original pelo `streamlit_app_integrado.py`
- [ ] Testar com código simples: `4`
- [ ] Testar com subnível: `4.3`, `4.4.1`
- [ ] Testar pergunta normal: "quantos alunos"
- [ ] Verificar que o fluxo normal ainda funciona
- [ ] Adicionar mais dados hierárquicos se necessário

---

## 🚨 POSSÍVEIS AJUSTES

Se quiser que **TODOS** os códigos (não apenas "4.x") sejam detectados:

```python
# Mudar linha ~497 de:
match = re.search(r'\b(4(?:\.\d+)*)\b', pergunta)

# Para:
match = re.search(r'\b(\d+(?:\.\d+)*)\b', pergunta)
```

---

## 📊 ESTRUTURA DOS DADOS

```
4 (Total: 184,839)
├── 4.1 (AEE: 9,090)
├── 4.2 (AC: 11,958)
├── 4.3 (Ensino Regular: 184,593)
│   ├── 4.3.1 (Manhã: 51,938)
│   ├── 4.3.2 (Tarde: 48,983)
│   ├── 4.3.3 (Noite: 13,255)
│   ├── 4.3.4 (Integral 7h-Manhã: 48,989)
│   ├── 4.3.5 (Integral 7h-Tarde: 15,270)
│   ├── 4.3.6 (Integral 8h: 170)
│   └── 4.3.7 (Integral 9h30: 6,353)
├── 4.4 (Fundamental: 63,543)
│   ├── 4.4.1 (Anos Iniciais: 10,859)
│   │   ├── 4.4.1.1 (1º ano: 1,950)
│   │   ├── 4.4.1.2 (2º ano: 2,155)
│   │   ├── 4.4.1.3 (3º ano: 2,141)
│   │   ├── 4.4.1.4 (4º ano: 2,138)
│   │   └── 4.4.1.5 (5º ano: 2,475)
│   └── 4.4.2 (Anos Finais: 52,684)
│       ├── 4.4.2.1 (6º ano: 12,305)
│       ├── 4.4.2.2 (7º ano: 12,548)
│       ├── 4.4.2.3 (8º ano: 13,198)
│       └── 4.4.2.4 (9º ano: 14,633)
└── 4.5 (Médio: 107,366)
    └── 4.5.1 (Médio Regular: 81,894)
        └── 4.5.1.1 (1ª série: 30,382)
```

---

## 💡 DICAS

- O código detecta automaticamente qualquer nível de profundidade
- Respostas de código hierárquico não usam tokens do OpenAI (economia!)
- Perguntas normais continuam funcionando normalmente
- Você pode misturar: "quantos alunos? Use o código 4"
