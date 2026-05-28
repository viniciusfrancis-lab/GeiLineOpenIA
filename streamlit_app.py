"""
Consulta hierárquica de dados de alunos SEDU
Retorna um item e todos seus subitens automaticamente
"""

dados_alunos = {
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
                            "4.4.1.1": {"label": "Quantidade de alunos no 1º ano do Ensino Fundamental - Anos Iniciais", "valor": 1_950},
                            "4.4.1.2": {"label": "Quantidade de alunos no 2º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_155},
                            "4.4.1.3": {"label": "Quantidade de alunos no 3º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_141},
                            "4.4.1.4": {"label": "Quantidade de alunos no 4º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_138},
                            "4.4.1.5": {"label": "Quantidade de alunos no 5º ano do Ensino Fundamental - Anos Iniciais", "valor": 2_475},
                        }
                    },
                    "4.4.2": {
                        "label": "Quantidade de alunos no Ensino Fundamental - Anos Finais",
                        "valor": 52_684,
                        "subitens": {
                            "4.4.2.1": {"label": "Quantidade de alunos no 6º ano do Ensino Fundamental - Anos Finais", "valor": 12_305},
                            "4.4.2.2": {"label": "Quantidade de alunos no 7º ano do Ensino Fundamental - Anos Finais", "valor": 12_548},
                            "4.4.2.3": {"label": "Quantidade de alunos no 8º ano do Ensino Fundamental - Anos Finais", "valor": 13_198},
                            "4.4.2.4": {"label": "Quantidade de alunos no 9º ano do Ensino Fundamental - Anos Finais", "valor": 14_633},
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
                            "4.5.1.1": {"label": "Quantidade de alunos na 1ª série do Ensino Médio", "valor": 30_382},
                        }
                    },
                }
            },
        }
    }
}


def consultar_alunos(codigo):
    """
    Consulta dados hierárquicos de alunos
    Retorna o item solicitado e todos seus subitens
    
    Exemplos:
    - consultar_alunos("4") -> retorna 4, 4.1, 4.2, 4.3, 4.4, 4.5
    - consultar_alunos("4.3") -> retorna 4.3, 4.3.1, 4.3.2, ..., 4.3.7
    - consultar_alunos("4.4.1") -> retorna 4.4.1, 4.4.1.1, 4.4.1.2, ..., 4.4.1.5
    """
    
    def buscar_item(dados, codigo_procurado):
        """Busca recursivamente um item no dicionário"""
        if codigo_procurado in dados:
            return dados[codigo_procurado]
        
        for chave, valor in dados.items():
            if "subitens" in valor:
                resultado = buscar_item(valor["subitens"], codigo_procurado)
                if resultado:
                    return resultado
        return None
    
    def exibir_hierarquia(item, codigo, nivel=0):
        """Exibe o item e todos seus subitens de forma indentada"""
        indent = "  " * nivel
        print(f"{indent}{codigo} - {item['label']}")
        print(f"{indent}   Quantidade: {item['valor']:,}")
        
        if "subitens" in item:
            for sub_codigo, sub_item in item["subitens"].items():
                print()
                exibir_hierarquia(sub_item, sub_codigo, nivel + 1)
    
    item = buscar_item(dados_alunos, codigo)
    
    if item:
        print(f"\n{'='*70}")
        print(f"CONSULTA: {codigo}")
        print(f"{'='*70}\n")
        exibir_hierarquia(item, codigo)
        print(f"\n{'='*70}\n")
    else:
        print(f"❌ Código '{codigo}' não encontrado!")


def gerar_dataframe():
    """Gera um DataFrame com todos os dados (opcional para análise)"""
    import pandas as pd
    
    dados_flat = []
    
    def extrair_dados(item, codigo):
        dados_flat.append({
            "codigo": codigo,
            "label": item["label"],
            "quantidade": item["valor"]
        })
        if "subitens" in item:
            for sub_codigo, sub_item in item["subitens"].items():
                extrair_dados(sub_item, sub_codigo)
    
    extrair_dados(dados_alunos["4"], "4")
    return pd.DataFrame(dados_flat)


if __name__ == "__main__":
    # Exemplos de uso
    consultar_alunos("4")      # Retorna 4 e todos os subitens (4.1, 4.2, 4.3, 4.4, 4.5)
    
    # Descomente para mais exemplos:
    # consultar_alunos("4.3")    # Retorna 4.3 e seus subitens (4.3.1 até 4.3.7)
    # consultar_alunos("4.4")    # Retorna 4.4 e seus subitens (4.4.1, 4.4.2)
    # consultar_alunos("4.4.1")  # Retorna 4.4.1 e seus subitens (4.4.1.1 até 4.4.1.5)
    
    # Para gerar DataFrame com todos os dados:
    # df = gerar_dataframe()
    # print(df)
