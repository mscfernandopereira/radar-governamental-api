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

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

Este projeto é construído 100% em Python e utiliza as seguintes bibliotecas principais:

* **Python 3.x**
* **`requests`**: Para fazer as requisições HTTP (GET) à API do governo.
* **`pandas`**: Para todo o tratamento, limpeza, agrupamento e análise dos dados.
* **`python-dotenv`**: Para carregar as variáveis de ambiente (segredos) do arquivo `.env`.
* **`dash` & `plotly`**: Para a construção do dashboard web interativo (front-end).

---

## ⚙️ Instruções de Instalação e Configuração

em desenvolvimento ...
