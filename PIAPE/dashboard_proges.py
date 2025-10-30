import streamlit as st
import pandas as pd
import re # Para expressões regulares (limpeza)
import numpy as np # Para agrupamento avançado
import plotly.express as px # Usado para o Gráfico de Pizza

# Configuração da Página: layout "wide" usa a tela inteira
st.set_page_config(layout="wide")

# =============================================================================
# CONFIGURAÇÃO GLOBAL DE COLUNAS
# =============================================================================
# --- ATENÇÃO: Ajuste os nomes das colunas aqui ---
col_nome = 'Nome'
col_curso = 'Curso'
col_campus = 'Campus'
col_instituto = 'Instituto'
col_deficiencia = 'Deficiência'
col_status = 'Status acadêmico'
col_raca = 'Raça'
col_escola = 'Tipo de escola do Ensino Médio'
col_rep_falta = 'Rep.Falta'
col_rep_media = 'Rep.Média'
col_auxilio = 'Alunos que recebem auxílio'
# --- Fim dos nomes das colunas ---


# =============================================================================
# CARREGAMENTO E LIMPEZA DOS DADOS (Permanece Inalterado)
# =============================================================================

@st.cache_data
def carregar_alunos():
    """Carrega, une e limpa os dados de Veteranos e Calouros."""

    try:
        df_vet = pd.read_csv('veteranos.csv')
        df_cal = pd.read_csv('calouros.csv')
    except FileNotFoundError:
        st.error("ERRO: Arquivos 'veteranos.csv' ou 'calouros.csv' não encontrados. Verifique os nomes.")
        return pd.DataFrame()

    # 1. Adicionar coluna 'Fonte' e preencher dados faltantes dos Calouros
    df_vet['Fonte'] = 'Veterano'
    df_cal['Fonte'] = 'Calouro'
    
    if col_status not in df_cal.columns:
        df_cal[col_status] = 'Ativo'
    if col_rep_falta not in df_cal.columns:
        df_cal[col_rep_falta] = 0
    if col_rep_media not in df_cal.columns:
        df_cal[col_rep_media] = 0
    
    df_alunos = pd.concat([df_vet, df_cal], ignore_index=True, sort=False)
    
    # 3. Limpeza e Padronização
    if col_deficiencia in df_alunos.columns:
        series_def = df_alunos[col_deficiencia].str.lower().fillna('outras')
        condicoes = [
            series_def.str.contains('autista|tea', case=False),
            series_def.str.contains('deficit de atenção|tdah', case=False),
            series_def.str.contains('multipla|múltipla|surdocegueira', case=False),
            series_def.str.contains('auditiva|surd', case=False),
            series_def.str.contains('visual|visão|cegueira|baixa visão', case=False),
            series_def.str.contains('física|fisica|locomoção', case=False),
            series_def.str.contains('intelectual', case=False),
        ]
        escolhas = [
            'TEA', 'TDAH', 'Múltipla', 'Auditiva', 'Visual', 'Física', 'Intelectual'
        ]
        df_alunos[col_deficiencia] = np.select(condicoes, escolhas, default='Outras')
    else:
        st.warning(f"Coluna '{col_deficiencia}' não encontrada. Gráficos de perfil podem falhar.")
        df_alunos[col_deficiencia] = 'Não informado'

    if col_raca in df_alunos.columns:
        series_raca = df_alunos[col_raca].str.lower().fillna('nao informado')
        condicoes_raca = [
            series_raca.str.contains('preto|preta', case=False),
            series_raca.str.contains('pardo|parda', case=False),
            series_raca.str.contains('indigena|indígena', case=False),
            series_raca.str.contains('branco|branca', case=False),
        ]
        escolhas_raca = [ 'Preto', 'Pardo', 'Indígena', 'Branco' ]
        df_alunos[col_raca] = np.select(condicoes_raca, escolhas_raca, default='Não Informado')
    else:
        df_alunos[col_raca] = 'Não Informado'

    if col_status in df_alunos.columns:
        df_alunos[col_status] = df_alunos[col_status].str.split(' - ').str[0].str.strip().str.upper()
    else:
        df_alunos[col_status] = 'Não informado'
        
    if col_rep_falta in df_alunos.columns:
        df_alunos[col_rep_falta] = pd.to_numeric(df_alunos[col_rep_falta], errors='coerce').fillna(0)
    if col_rep_media in df_alunos.columns:
        df_alunos[col_rep_media] = pd.to_numeric(df_alunos[col_rep_media], errors='coerce').fillna(0)
        
    for col in [col_nome, col_curso, col_campus, col_instituto, col_escola, col_auxilio]:
        if col in df_alunos.columns:
            df_alunos[col] = df_alunos[col].str.strip().str.title()
        
    return df_alunos

@st.cache_data
def carregar_bolsistas():
    """Carrega e limpa os dados de bolsistas, agrupando por campus."""
    try:
        df = pd.read_csv(
            'bolsistas.csv', 
            header=None, names=['nome_ou_campus', 'vinculado', 'nao_mais_vinculado']
        )
    except FileNotFoundError:
        st.error("ERRO: Arquivo 'bolsistas.csv' não encontrado.")
        return pd.Series(name="Total de Bolsistas")

    df['campus'] = df['nome_ou_campus'].where(
        df['nome_ou_campus'].str.contains('CAMPUS|RU', na=False, flags=re.IGNORECASE)
    )
    df['campus'] = df['campus'].ffill() 
    bolsistas_ativos = df[df['vinculado'].str.strip() == 'X'].copy()
    bolsistas_ativos['campus'] = bolsistas_ativos['campus'].str.replace('CAMPUS DE ', '', case=False)
    bolsistas_ativos['campus'] = bolsistas_ativos['campus'].str.replace('CAMPUS ', '', case=False)
    bolsistas_ativos['campus'] = bolsistas_ativos['campus'].str.split(' - ').str[0]
    bolsistas_ativos['campus'] = bolsistas_ativos['campus'].str.title()
    bolsistas_por_campus = bolsistas_ativos.groupby('campus').size()
    bolsistas_por_campus.name = "Total de Bolsistas"
    return bolsistas_por_campus

# --- Carrega todos os dados ---
df_alunos = carregar_alunos()
df_bolsistas = carregar_bolsistas()


# =============================================================================
# INTERFACE DO DASHBOARD (STREAMLIT)
# =============================================================================

st.title('Dashboard de Acompanhamento de Discentes PcD - PROGES')

# --- 1. BARRA LATERAL COM FILTROS (Permanece fora das abas) ---
st.sidebar.header('Filtros Interativos')

if col_campus in df_alunos.columns:
    lista_campus = ['Todos'] + sorted(df_alunos[col_campus].dropna().unique())
    filtro_campus = st.sidebar.selectbox('Filtrar por Campus:', lista_campus)
else:
    filtro_campus = 'Todos'

if col_curso in df_alunos.columns:
    lista_cursos = ['Todos'] + sorted(df_alunos[col_curso].dropna().unique())
    filtro_curso = st.sidebar.selectbox('Filtrar por Curso:', lista_cursos)
else:
    filtro_curso = 'Todos'

if col_deficiencia in df_alunos.columns:
    lista_deficiencia = ['Todos'] + sorted(df_alunos[col_deficiencia].dropna().unique())
    filtro_deficiencia = st.sidebar.selectbox('Filtrar por Necessidade:', lista_deficiencia)
else:
    filtro_deficiencia = 'Todos'

# --- 2. APLICAÇÃO DOS FILTROS (Permanece fora das abas) ---
df_filtrado = df_alunos.copy()

if filtro_campus != 'Todos':
    df_filtrado = df_filtrado[df_filtrado[col_campus] == filtro_campus]
if filtro_curso != 'Todos':
    df_filtrado = df_filtrado[df_filtrado[col_curso] == filtro_curso]
if filtro_deficiencia != 'Todos':
    df_filtrado = df_filtrado[df_filtrado[col_deficiencia] == filtro_deficiencia]

# --- 3. CRIAÇÃO DO NOVO LAYOUT COM ABAS ---
tab_visao_geral, tab_perfil, tab_desempenho, tab_recursos = st.tabs([
    "📊 Visão Geral", 
    "👥 Perfil do Aluno", 
    "📈 Desempenho Acadêmico", 
    "⚙️ Gestão de Recursos"
])


# --- ABA 1: VISÃO GERAL (ATUALIZADA COM GRÁFICO DE PIZZA) ---
with tab_visao_geral:
    st.header('1. Visão Geral')
    
    # --- MÉTRICAS ---
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Total de Alunos (Geral)", f"{df_alunos.shape[0]}")
    alunos_ativos = df_filtrado[df_filtrado[col_status] == 'ATIVO'].shape[0]
    col2.metric("Alunos Ativos (no Filtro)", f"{alunos_ativos}")
    col3.metric("Cursos Atendidos (no Filtro)", f"{df_filtrado[col_curso].nunique()}")
    col4.metric("Campi Atendidos (no Filtro)", f"{df_filtrado[col_campus].nunique()}")
    col5.metric("Total Bolsistas (Geral)", f"{df_bolsistas.sum()}")
    
    st.divider() # Adiciona um separador
    
    # --- GRÁFICO DE PIZZA (SUBSTITUI O SUNBURST) ---
    st.subheader('Distribuição de Alunos por Campus (conforme filtros)')
    
    # Prepara os dados para o gráfico de pizza
    # .fillna() garante que alunos sem campus sejam contados
    dados_campus = df_filtrado[col_campus].fillna('Não Informado').value_counts().reset_index()
    dados_campus.columns = [col_campus, 'Total de Alunos'] # Renomeia colunas

    # Cria o gráfico de pizza com Plotly
    fig_campus = px.pie(
        dados_campus, 
        names=col_campus, 
        values='Total de Alunos',
        title='Alunos por Campus'
    )
    
    # Melhora a visualização dos rótulos
    fig_campus.update_traces(textposition='inside', textinfo='percent+label', sort=False)
    
    # Mostra o gráfico no Streamlit
    st.plotly_chart(fig_campus, use_container_width=True)


# --- ABA 2: PERFIL DO ALUNO (Inalterada) ---
with tab_perfil:
    st.header('2. Perfil dos Alunos')
    col_perfil1, col_perfil2 = st.columns(2)
    with col_perfil1:
        st.subheader('Necessidades Específicas Mais Comuns')
        if col_deficiencia in df_filtrado.columns:
            dados_def = df_filtrado[col_deficiencia].value_counts()
            st.bar_chart(dados_def)
    with col_perfil2:
        st.subheader('Perfil Socioeconômico (Raça)')
        if col_raca in df_filtrado.columns:
            dados_raca = df_filtrado[col_raca].value_counts()
            st.bar_chart(dados_raca)
            
    st.divider() 
    
    st.header('3. Distribuição Acadêmica')
    
    st.subheader('Alunos por Curso')
    if col_curso in df_filtrado.columns:
        dados_curso = df_filtrado[col_curso].value_counts().head(15) # Top 15
        st.bar_chart(dados_curso)
    

# --- ABA 3: DESEMPENHO ACADÊMICO (Inalterada) ---
with tab_desempenho:
    st.header('4. Desempenho e Risco Acadêmico')
    
    st.subheader('Status Acadêmico')
    if col_status in df_filtrado.columns:
        dados_status = df_filtrado[col_status].value_counts()
        st.bar_chart(dados_status, use_container_width=True)
        
    st.divider() 
    
    with st.expander("► Clique para ver a Lista de Alunos em Alerta (com Reprovações)"):
        st.subheader('Alunos em Situação de Alerta')
        
        if col_rep_falta in df_filtrado.columns and col_rep_media in df_filtrado.columns:
            df_filtrado['Total Reprovações'] = df_filtrado[col_rep_falta] + df_filtrado[col_rep_media]
            
            df_alerta = df_filtrado[df_filtrado['Total Reprovações'] > 0][
                [col_nome, col_curso, col_status, 'Total Reprovações']
            ]
            
            if df_alerta.empty:
                st.info("Nenhum aluno em situação de alerta (com reprovações) nos filtros selecionados.")
            else:
                status_unicos = sorted(df_alerta[col_status].unique())
                for status in status_unicos:
                    st.markdown(f"**Status: {status}**")
                    df_grupo = df_alerta[df_alerta[col_status] == status]
                    st.dataframe(
                        df_grupo.sort_values('Total Reprovações', ascending=False),
                        height=200,
                        use_container_width=True
                    )


# --- ABA 4: GESTÃO DE RECURSOS (Inalterada) ---
with tab_recursos:
    st.header('5. Gestão de Recursos (Visão Geral por Campus)')
    st.write("""
    Esta tabela **não é afetada pelos filtros acima** e mostra o quadro geral de
    recursos (Bolsistas) versus a demanda (Total de Alunos e Alunos com Def. Auditiva)
    em cada campus.
    """)
    
    df_demanda_total = df_alunos.groupby(col_campus).size().to_frame('Total Alunos PcD')
    df_demanda_auditiva = df_alunos[df_alunos[col_deficiencia] == 'Auditiva'].groupby(col_campus).size().to_frame('Alunos (Auditiva)')

    df_comparativo = pd.concat(
        [df_demanda_total, df_demanda_auditiva, df_bolsistas], 
        axis=1 
    )
    df_comparativo = df_comparativo.fillna(0).astype(int) 

    st.dataframe(df_comparativo, use_container_width=True)