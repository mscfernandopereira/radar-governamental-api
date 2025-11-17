# 📈 Pipeline de Análise de Investimentos - RPPS Maricá (2025)

## 🎯 Objetivo do Projeto

O objetivo deste projeto é consumir a API `DAIR_CARTEIRA` do Governo Federal para extrair, tratar e analisar a **evolução mensal do patrimônio** da Previdência Pública de Maricá (RJ) para o ano de 2025.

O projeto utiliza um *pipeline* de dados modular que separa as responsabilidades de conexão com a API (`api.py`), processamento de dados (`processing.py`), execução (`main.py`) e visualização (`dashboard.py`).

---

## ✨ Estrutura e Funcionalidades

O projeto possui uma clara separação de responsabilidades:

### 🧠 `main.py` (O Orquestrador)
* Script principal que gera a execução do fluxo de extração de dados.
* Carrega as configurações (logs, `.env`, caminhos de arquivos).
* Chama o `api.py` para buscar os dados e verifica o sucesso.
* Chama as funções do `processing.py` para tratar, analisar e salvar o relatório mensal.

### 🚀 `api.py` (O Mensageiro)
* Contém a função `consumir_api_previdencia_marica`.
* Responsável *exclusivamente* por fazer a requisição à API `DAIR_CARTEIRA`.
* Implementa o tratamento de erros de conexão, timeout e status HTTP.

### 📊 `processing.py` (O Analista)
* Contém todas as funções de manipulação de dados com `pandas`.
* `tratar_dados_bruto`: Limpa os dados, converte colunas para numérico e mapeia os **meses** usando `pd.Categorical` para garantir a ordem cronológica correta.
* `vl_total_por_mes`: Calcula o montante total consolidado **mês a mês**.
* `salvar_resumo_em_csv`: Função reutilizável para salvar o relatório final.

### 🖥️ `dashboard.py` (O Visualizador)
* Uma aplicação web interativa construída com Dash e Plotly.
* Carrega o CSV gerado pelo `main.py`.
* Apresenta um gráfico de linha limpo mostrando a evolução mensal do patrimônio.
* Inclui um botão para download direto do arquivo `.csv` tratado.

---

## 📁 Relatório Gerado

O *pipeline* gera um único relatório focado na evolução mensal:

* **Localização**: `data/privado/`
* **Arquivo**: `investimentos_marica_2025_por_mes.csv`
* **Descrição**: Relatório com o montante total consolidado, mês a mês, em ordem cronológica.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Python 3.x**
* `requests`: Para fazer as requisições HTTP à API (em `api.py`).
* `pandas`: Para todo o tratamento, limpeza e agrupamento dos dados (em `processing.py`).
* `python-dotenv`: Para carregar as variáveis de ambiente (segredos) do arquivo `.env`.
* `dash`: Para a estrutura da aplicação web.
* `plotly`: Para a geração do gráfico de linha interativo.
* `dash-bootstrap-components`: Para o layout e estilo do dashboard.

---

## ⚙️ Instruções de Instalação e Execução

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

3.  Crie um arquivo `requirements.txt` com as bibliotecas:
    ```txt
    pandas
    requests
    python-dotenv
    dash
    plotly
    dash-bootstrap-components
    ```

4.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5.  Crie um arquivo `.env` na raiz do projeto e adicione suas variáveis:
    ```ini
    CNPJ_ENTIDADE="SEU_CNPJ_AQUI"
    UF_ENTIDADE="RJ"
    ANO_CONSULTA="2025"
    ```

6.  **Execute o pipeline em duas etapas:**

    * **Primeiro, gere o arquivo de dados:**
        ```bash
        python main.py
        ```
        *(Isso irá consumir a API e criar o arquivo .csv em `data/privado/`)*

    * **Depois, inicie o dashboard para ver os resultados:**
        ```bash
        python dashboard.py
        ```
        *(Acesse `http://127.0.0.1:8050/` no seu navegador para ver o gráfico)*