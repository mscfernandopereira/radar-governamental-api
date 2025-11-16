# 📈 Pipeline de Análise de Investimentos - RPPS Maricá (2025)

## 🎯 Objetivo do Projeto

O objetivo deste projeto é consumir a API `DAIR_CARTEIRA` do Governo Federal para extrair, tratar e analisar os dados de investimento da Previdência Pública de Maricá (RJ) para o ano de 2025.

O que começou como um script único, evoluiu para um *pipeline* de dados modular e robusto. O projeto agora separa as responsabilidades de conexão com a API (`api.py`), processamento de dados (`processing.py`) e execução principal (`main.py`), incluindo tratamento de erros, logging, gestão de segredos com `.env` e múltiplas análises de portfólio.

---

## ✨ Estrutura e Funcionalidades

O projeto foi refatorado para ter uma clara separação de responsabilidades:

### 🧠 `main.py` (O Orquestrador)
* Script principal que gere a execução de todo o fluxo.
* Carrega as configurações (logs, `.env`, caminhos de ficheiros).
* Chama o `api.py` para buscar os dados e verifica o sucesso.
* Chama as funções do `processing.py` para tratar, analisar e salvar os dados.
* Controla o fluxo principal e o tratamento de exceções.

### 🚀 `api.py` (O Mensageiro)
* Contém a função `consumir_api_previdencia_marica`.
* Responsável *exclusivamente* por fazer a requisição à API `DAIR_CARTEIRA`.
* Implementa o tratamento de erros de conexão, timeout e status HTTP (ex: 404, 500).

### 📊 `processing.py` (O Analista)
* Contém todas as funções de manipulação de dados com `pandas`.
* `tratar_dados_bruto`: Limpa os dados, converte colunas para numérico de forma segura (com `pd.to_numeric(errors='coerce')`) e mapeia os bimestres.
* `vl_total_por_segmento`: Calcula a alocação percentual por segmento de investimento.
* `vl_total_por_bimestre`: Calcula o montante total consolidado por bimestre (e formata para CSV).
* `salvar_dados_em_excel`: Gera um backup dos dados brutos tratados.
* `salvar_resumo_em_csv`: Função reutilizável para salvar os relatórios de análise.

### 📁 Relatórios Gerados
Localizados em `data/privado/`:
* `investimentos_dados_brutos_tratados.xlsx`: Um "backup" completo dos dados limpos.
* `investimentos_por_segmento.csv`: Relatório de alocação por segmento (Renda Fixa, Variável, etc.).
* `investimentos_marica_2025.csv`: Relatório com o montante total consolidado por bimestre.

### 💡 Outras Funcionalidades
* **Logging**: Regista todas as operações, sucessos e falhas em `logs/consumir_api.log`.
* **Gestão de Segredos**: Protege o CNPJ, UF e Ano utilizando um ficheiro `.env`.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

Este projeto é construído 100% em Python e utiliza as seguintes bibliotecas principais:

* **Python 3.x**
* `requests`: Para fazer as requisições HTTP à API do governo (em `api.py`).
* `pandas`: Para todo o tratamento, limpeza, agrupamento e análise dos dados (em `processing.py`).
* `python-dotenv`: Para carregar as variáveis de ambiente (segredos) do arquivo `.env`.
* `dash` & `plotly`: Para a construção do dashboard web interativo (Em desenvolvimento).

---

## ⚙️ Instruções de Instalação e Configuração

1.  Clone este repositório.

2.  Crie um ambiente virtual (recomendado):
    ```bash
    python -m venv .venv
    ```
    E ative-o:
    ```bash
    # No Windows (PowerShell/CMD)
    .\.venv\Scripts\activate
    
    # No macOS/Linux
    source .venv/bin/activate
    ```

3.  Crie um ficheiro `requirements.txt` com as bibliotecas:
    ```txt
    pandas
    requests
    python-dotenv
    ```

4.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5.  Crie um ficheiro `.env` na raiz do projeto e adicione as suas variáveis:
    ```ini
    CNPJ_ENTIDADE="O_SEU_CNPJ"
    UF_ENTIDADE="RJ"
    ANO_CONSULTA="2025"
    ```

6.  Execute o script principal:
    ```bash
    python main.py
    ```