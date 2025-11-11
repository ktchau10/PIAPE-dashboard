# 📊 Dashboard de Acompanhamento de Discentes PcD - PROGES

Este projeto consiste em um **painel interativo desenvolvido com Streamlit** para acompanhamento e análise de **discentes com deficiência (PcD)**, integrando dados de calouros, veteranos e bolsistas.  
O dashboard foi desenvolvido para auxiliar a **PROGES** na visualização de informações sobre alunos, cursos, campi, desempenho acadêmico e distribuição de recursos.

---

## 🧩 Estrutura do Projeto

```
📁 dashboard_proges/
│
├── 📄 dashboard_proges.py        # Código principal do dashboard
├── 📄 calouros.csv               # Base de dados de alunos calouros
├── 📄 veteranos.csv              # Base de dados de alunos veteranos
├── 📄 bolsistas.csv              # Base de dados de bolsistas ativos
└── 📄 README.md                  # Documentação do projeto
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

### 2️⃣ Certifique-se de que os arquivos `.csv` estejam na mesma pasta do script:

- `calouros.csv`
- `veteranos.csv`
- `bolsistas.csv`

### 3️⃣ Navegue até a pasta onde o projeto está localizado

```bash
# Navegue até a pasta que você acabou de baixar/clonar
cd nome-da-pasta/PIAPE
```

### 4️⃣ Execute o dashboard

```bash
streamlit run dashboard_proges.py
```

## 🧠 Funcionalidades Principais

### 🔹 1. **Visão Geral**
- Exibe indicadores globais: total de alunos, cursos, campi e bolsistas.
- Gráfico de pizza mostrando a distribuição de alunos por campus.

### 🔹 2. **Perfil do Aluno**
- Distribuição por tipo de deficiência e raça.
- Ranking dos cursos com mais alunos PcD.

### 🔹 3. **Desempenho Acadêmico**
- Gráfico de status acadêmico (ativos, trancados, etc.).
- Lista de alunos em situação de alerta (com reprovações).

### 🔹 4. **Gestão de Recursos**
- Tabela comparando **número de alunos PcD por campus** com **quantidade de bolsistas**.
- Indicador de alunos com deficiência auditiva por campus.

---

## 📁 Filtros Interativos

Na barra lateral do Streamlit, o usuário pode filtrar os dados por:
- **Unidade Acadêmica**
- **Curso**
- **Tipo de deficiência**

Esses filtros afetam dinamicamente os gráficos e métricas das abas “Visão Geral”, “Perfil do Aluno” e “Desempenho Acadêmico”.

---

## 📈 Exemplo de Visualizações

- **Gráfico de Pizza** — distribuição de alunos por campus.  
- **Gráficos de Barras** — tipo de deficiência, raça e cursos.  
- **Tabelas Dinâmicas** — alunos em alerta e distribuição de recursos.
