# 📊 Dashboard de Acompanhamento de Discentes - PROGES

Este projeto consiste em um **painel interativo desenvolvido com Streamlit** para acompanhamento e análise de dados acadêmicos dos discentes. O dashboard foi desenvolvido para auxiliar a **PROGES** na visualização de informações sobre o perfil dos alunos, seu desempenho, progressão de curso e risco de evasão.

Este painel utiliza uma única fonte de dados (`comissoes.csv`) e aplica diversas limpezas e padronizações para gerar os gráficos.

---

## 🧩 Estrutura do Projeto

```
📁 dashboard_proges/
│
├── 📄 dashboard_proges.py        # Código principal do dashboard
├── 📄 comissoes.csv               # Base de dados de alunos calouros
├── 📄 readme.md                  # Este arquivo de documentação 
```

---

## 🚀 Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit** → para interface interativa e exibição de dashboards  
- **Pandas** → para manipulação e limpeza de dados  
- **NumPy** → para operações e agrupamentos  
- **Plotly Express** → para gráficos dinâmicos e interativos  
- **Regex (re)** → para tratamento e padronização textual

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Instale as dependências

No terminal, execute:
```bash
pip install streamlit pandas numpy plotly
```

### 2️⃣ Certifique-se de que o arquivo .csv esteja na mesma pasta do script:

- `comissoes.csv`

### 3️⃣ Navegue até a pasta onde o projeto está localizado

```bash
# Navegue até a pasta que contém os arquivos
cd /caminho/para/a/pasta
```

### 4️⃣ Execute o dashboard

```bash
streamlit run dashboard_proges.py
```

## 🧠 Funcionalidades Principais

O dashboard é organizado em **5 abas principais**, com filtros dinâmicos e interativos que permitem explorar os dados em diferentes níveis de detalhe.

### 🔹 Filtros Interativos
Na **barra lateral**, o usuário pode aplicar filtros para refinar as análises:

- **Unidade Acadêmica:** (ex: `ICED`, `ICTA`)  
- **Curso:** (ex: `PEDAGOGIA`, `DIREITO`)  
- **Grupo/Raça:** (6 categorias principais + `Não Informado`)

---

### 🔹 1. Visão Geral
- **Indicadores Chave:** Total de Alunos (geral) e Alunos Ativos (conforme filtros).  
- **Gráfico de Pizza:** Distribuição de alunos por Unidade Acadêmica.  
- **Gráfico de Barras:** Ranking dos 10 cursos com mais alunos.

---

### 🔹 2. Perfil do Aluno
- **Gráfico de Pizza:** Mostra a distribuição dos alunos por “Grupo/Raça”, conforme a coluna `ESTUDANTE`.

---

### 🔹 3. Desempenho Acadêmico
- **Gráfico de Barras:** Status oficial dos alunos (`Ativo`, `Formando`, etc.).  
- **Gráfico de Pizza:** Progresso acadêmico (`Regular` vs. `Atrasado`).  
- **Análise de Carga Horária:** Compara a **C.H. Esperada** e **C.H. Cursada** no semestre.  
- **Tabela de Alunos em Alerta:** Lista alunos com **reprovações por falta ou média**, com possibilidade de expansão para análise detalhada.

---

### 🔹 4. Perfil de Ingresso
- **Gráfico de Linha:** Evolução anual de alunos ingressantes.  
- **Gráfico de Barras:** Distribuição de alunos por `forma_ingresso` (ex: “Processo Seletivo”, “Reoferta”).

---

### 🔹 5. Situação de Matrícula (Análise de Risco)
- **Filtro Automático:** Considera apenas alunos com status `Ativo`.  
- **Gráficos Comparativos:** Mostra (em barras e pizza) a proporção de alunos `Matriculado` vs. `Não Matriculado` no semestre atual.  
- **Foco:** Identificação de **grupos de risco de evasão**.

---

## 🧹 Limpeza e Padronização dos Dados

Durante o carregamento, o script `dashboard_proges.py` executa uma série de etapas de limpeza e transformação dos dados:

| Etapa | Descrição |
|-------|------------|
| **Carregamento Completo** | Analisa todos os alunos do arquivo `comissoes.csv`. |
| **Padronização de Unidades** | Converte a coluna `unidade` para letras maiúsculas (ex: `ICED`, `ICTA`). |
| **Generalização de Grupo/Raça** | Normaliza os valores da coluna `ESTUDANTE` em 6 categorias principais + `Não Informado`. |
| **Padronização de Progressão** | Converte `ultrapassou_tempo_maximo?` em `Regular` ou `Atrasado`. |
| **Conversão de Reprovações** | Converte colunas de reprovação para valores numéricos, tratando erros e ausências como `0`. |

---

## 🧾 Estrutura Esperada do Arquivo `comissoes.csv`

Para o correto funcionamento do dashboard, o arquivo deve conter **as colunas abaixo com nomes exatos**:

| Coluna | Descrição |
|--------|------------|
| `nome` | Nome completo do aluno |
| `unidade` | Unidade acadêmica (ex: ICED, ICTA) |
| `curso` | Nome do curso |
| `ano_ingresso` | Ano de ingresso do aluno |
| `forma_ingresso` | Forma de ingresso (Processo Seletivo, Reoferta, etc.) |
| `ESTUDANTE` | Grupo/Raça (Indígena, Quilombola, etc.) |
| `status` | Status acadêmico (Ativo, Formando, etc.) |
| `STATUS ATUAL DE MATRÍCULA` | Situação de matrícula no semestre atual |
| `ultrapassou_tempo_maximo?` | Indica se o aluno ultrapassou o tempo máximo de curso |
| `n_reprovacoes_falta em 2025.1` | Número de reprovações por falta no semestre |
| `n_reprovacoes_media em 2025.1` | Número de reprovações por média no semestre |
| `ch_esperada para 2025.1` | Carga horária esperada no semestre |
| `ch_estava cursando em 2025.1` | Carga horária efetivamente cursada |

