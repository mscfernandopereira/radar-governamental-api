# 📈 Dashboard de Análise de Investimentos - RPPS Maricá (2025)

## 🎯 Objetivo do Projeto

O objetivo deste projeto é consumir a API `DAIR_CARTEIRA` do Governo Federal para extrair, tratar e analisar os dados de investimento da Previdência Pública de Maricá (RJ) para o ano de 2025.

O que começou como um desafio acadêmico para gerar um CSV simples, evoluiu para um *pipeline* de dados robusto. O projeto agora inclui tratamento de erros, logging, gerenciamento de segredos com `.env`, análises de portfólio (alocação por segmento) e a fundação para um dashboard web interativo com Dash.

## ✨ Funcionalidades Atuais

* **`consumir_api.py`**: Script robusto que consome a API `DAIR_CARTEIRA` de forma segura.
* **Logging**: Registra todas as operações, sucessos e falhas em `logs/consumir_api.log`.
* **Gerenciamento de Segredos (`.env`)**: Protege o CNPJ, UF e Ano, mantendo-os fora do código-fonte.
* **Tratamento de Erros**: Captura falhas de rede (Timeout, erros HTTP) e para a execução de forma segura, informando o log.
* **Relatório 1 (Total Bimestral)**: Gera `data/privado/investimentos_marica_2025.csv` com o montante total consolidado por bimestre.
* **Relatório 2 (Valor total e percentual por segmento)**: Escrevemos e executamos o código Python para a Análise de Alocação por Segmento.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

Este projeto é construído 100% em Python e utiliza as seguintes bibliotecas principais:

* **Python 3.x**
* **`requests`**: Para fazer as requisições HTTP (GET) à API do governo.
* **`pandas`**: Para todo o tratamento, limpeza, agrupamento e análise dos dados.
* **`python-dotenv`**: Para carregar as variáveis de ambiente (segredos) do arquivo `.env`.

---

## ⚙️ Instruções de Instalação e Configuração

Para executar este projeto em uma nova máquina, siga este guia.

### 1. Pré-requisitos

Garanta que você tenha os seguintes softwares instalados:

* [Git](https://git-scm.com/downloads) (Para baixar o projeto)
* [Python 3.8+](https://www.python.org/downloads/) (Para executar os scripts)

### 2. Instalação e Configuração

Abra seu terminal e siga os comandos:

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/StartCooper/radar-governamental-api.git
    cd radar-governamental-api
    ```

2.  **Crie e Ative um Ambiente Virtual:** (Altamente recomendado)
    ```bash
    python -m venv venv
    ```

    * **No Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **No macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Instale as Dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas (`pandas`, `requests`, `dash`, etc.) necessárias.
    ```bash
    pip install -r requirements.txt
    ```

4.  **⚠️ Crie o Arquivo de Segredos (.env):**
    Este é o passo manual mais importante, pois o `.env` original está (corretamente) no `.gitignore` e não é baixado.

    Crie um arquivo chamado `.env` na raiz do projeto e cole o seguinte conteúdo dentro dele:
    ```ini
    CNPJ_ENTIDADE=29131075000193
    UF_ENTIDADE=RJ
    ANO_CONSULTA=2025
    ```

### 3. Execução

O projeto é dividido em duas etapas que devem ser executadas nesta ordem:

1.  **Gerar os Dados (ETL):**
    Execute o script principal para consumir a API, tratar os dados e criar os arquivos CSV na pasta `data/`.
    ```bash
    python consumir_api.py
    ```

#### Em edição ...

<!-- 2.  **Iniciar o Dashboard Web:**
    Execute o script do dashboard para iniciar o servidor web local.
    ```bash
    python dashboard.py
    ```

3.  **Acesse o Dashboard:**
    Abra seu navegador e acesse o link:
    `http://127.0.0.1:8050/` -->
