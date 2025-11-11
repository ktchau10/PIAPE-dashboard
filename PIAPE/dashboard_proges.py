import streamlit as st
import pandas as pd
import re # Para expressões regulares (limpeza)
import numpy as np # Para agrupamento avançado
import plotly.express as px # Usado para o Gráfico de Pizza e Barras

# Configuração da Página: layout "wide" usa a tela inteira
st.set_page_config(layout="wide")

# =============================================================================
# CONFIGURAÇÃO GLOBAL DE COLUNAS (MAPEADO PARA 'comissoes.csv')
# =============================================================================
col_nome = 'nome'
col_unidade = 'unidade'
col_curso = 'curso'
col_ano_ingresso = 'ano_ingresso'
col_forma_ingresso = 'forma_ingresso'
col_grupo_raca_original = 'ESTUDANTE' # Coluna original
col_raca_normalizada = 'Grupo/Raça Normalizada' # Nova coluna limpa
col_status = 'status'
col_status_matricula = 'STATUS ATUAL DE MATRÍCULA' # Para nova aba
col_bolsa_situacao = 'SITUAÇÃO DE BOLSA/AUXÍLI_O'
col_ira = 'IRA em 2025.1'
col_progressao = 'ultrapassou_tempo_maximo?' # SIM/NÃO
col_rep_falta = 'n_reprovacoes_falta em 2025.1'
col_rep_media = 'n_reprovacoes_media em 2025.1'
# --- Novas colunas de Carga Horária ---
col_ch_esperada = 'ch_esperada para 2025.1'
col_ch_cursando = 'ch_estava cursando em 2025.1'
# --- Fim dos nomes das colunas ---


# =============================================================================
# CARREGAMENTO E LIMPEZA DOS DADOS (Função REESCRITA)
# =============================================================================

@st.cache_data
def carregar_alunos():
    """Carrega e limpa os dados do novo arquivo 'comissoes.csv'."""

    try:
        df_alunos = pd.read_csv('comissoes.csv')
    except FileNotFoundError:
        st.error("ERRO: Arquivo 'comissoes.csv' não encontrado. Verifique se ele está na mesma pasta do script.")
        st.stop() # Para a execução
    except Exception as e:
        st.error(f"Erro ao ler 'comissoes.csv': {e}")
        st.stop() # Para a execução

    if df_alunos.empty:
        st.warning("AVISO: A planilha 'comissoes.csv' está vazia.")
        st.stop() # Para a execução
        
    # --- Limpeza e Padronização ---
    
    # Perfil do Aluno
    for col in [col_nome, col_curso, col_status, col_forma_ingresso, col_status_matricula]:
        if col in df_alunos.columns:
            df_alunos[col] = df_alunos[col].fillna('Não Informado').str.strip().str.title()
            
    if col_unidade in df_alunos.columns:
        df_alunos[col_unidade] = df_alunos[col_unidade].fillna('Não Informado').str.strip().str.upper()

    # --- Generalizar dados de Raça/Grupo ---
    if col_grupo_raca_original in df_alunos.columns:
        series_raca = df_alunos[col_grupo_raca_original].str.lower().fillna('nao informado')
        condicoes_raca = [
            series_raca.str.contains('indigena|indígena', case=False),
            series_raca.str.contains('quilombola', case=False),
            series_raca.str.contains('preto|preta', case=False),
            series_raca.str.contains('pardo|parda', case=False),
            series_raca.str.contains('branco|branca', case=False),
            series_raca.str.contains('amarelo|amarela', case=False)
        ]
        escolhas_raca = ['Indígena', 'Quilombola', 'Preto', 'Pardo', 'Branco', 'Amarelo']
        df_alunos[col_raca_normalizada] = np.select(condicoes_raca, escolhas_raca, default='Não Informado')
    else:
        df_alunos[col_raca_normalizada] = 'Não Informado'

    # Desempenho
    if col_progressao in df_alunos.columns:
        df_alunos[col_progressao] = df_alunos[col_progressao].fillna('NÃO').str.strip().str.upper()
        df_alunos[col_progressao] = df_alunos[col_progressao].replace('SIM', 'Atrasado').replace('NÃO', 'Regular')
    else:
        df_alunos[col_progressao] = 'Não Informado'
        
    for col in [col_rep_falta, col_rep_media, col_ch_esperada, col_ch_cursando]:
        if col in df_alunos.columns:
            df_alunos[col] = pd.to_numeric(df_alunos[col], errors='coerce').fillna(0)
        else:
            df_alunos[col] = 0
            
    if col_ira in df_alunos.columns:
        df_alunos[col_ira] = pd.to_numeric(df_alunos[col_ira], errors='coerce') 

    # Ingresso e Auxílio
    if col_ano_ingresso in df_alunos.columns:
        df_alunos[col_ano_ingresso] = pd.to_numeric(df_alunos[col_ano_ingresso], errors='coerce')
        
    if col_bolsa_situacao in df_alunos.columns:
        df_alunos[col_bolsa_situacao] = df_alunos[col_bolsa_situacao].fillna('Não Informado').str.strip()
        df_alunos[col_bolsa_situacao] = df_alunos[col_bolsa_situacao].replace('-', 'Não Informado')
    else:
        df_alunos[col_bolsa_situacao] = 'Não Informado'
        
    return df_alunos

# --- Carrega todos os dados ---
df_alunos = carregar_alunos()

# =============================================================================
# INTERFACE DO DASHBOARD (STREAMLIT)
# =============================================================================

st.title('Dashboard de Acompanhamento de Discentes - PROGES')

# --- 1. BARRA LATERAL COM OS 3 FILTROS ---
st.sidebar.header('Filtros Interativos')

# Filtro 1: Unidade Acadêmica
lista_unidade = ['Todos'] + sorted(df_alunos[col_unidade].dropna().unique())
filtro_unidade = st.sidebar.selectbox('Filtrar por Unidade Acadêmica:', lista_unidade)

# Filtro 2: Curso
df_cursos_filtrados = df_alunos.copy()
if filtro_unidade != 'Todos':
    df_cursos_filtrados = df_cursos_filtrados[df_cursos_filtrados[col_unidade] == filtro_unidade]
lista_cursos = ['Todos'] + sorted(df_cursos_filtrados[col_curso].dropna().unique())
filtro_curso = st.sidebar.selectbox('Filtrar por Curso:', lista_cursos)

# Filtro 3: Grupo/Raça
lista_grupo_raca = ['Todos'] + sorted(df_alunos[col_raca_normalizada].dropna().unique())
filtro_grupo_raca = st.sidebar.selectbox('Grupo/Raça:', lista_grupo_raca)


# --- 2. APLICAÇÃO DOS FILTROS ---
df_filtrado = df_alunos.copy()

if filtro_unidade != 'Todos':
    df_filtrado = df_filtrado[df_filtrado[col_unidade] == filtro_unidade]
if filtro_curso != 'Todos':
    df_filtrado = df_filtrado[df_filtrado[col_curso] == filtro_curso]
if filtro_grupo_raca != 'Todos':
    df_filtrado = df_filtrado[df_filtrado[col_raca_normalizada] == filtro_grupo_raca]


# --- 3. CRIAÇÃO DAS NOVAS ABAS ---
tab_visao_geral, tab_perfil, tab_desempenho, tab_ingresso, tab_matricula = st.tabs([
    "📊 Visão Geral", 
    "👥 Perfil do Aluno",
    "📚 Desempenho Acadêmico",
    "🎓 Perfil de Ingresso",
    "⚠️ Situação de Matrícula"
])


# --- ABA 1: VISÃO GERAL ---
with tab_visao_geral:
    st.subheader('Indicadores Chave')
    col1, col2 = st.columns(2)
    
    col1.metric("Total de Alunos (Geral)", f"{df_alunos.shape[0]}")
    
    if not df_filtrado.empty:
         alunos_ativos = df_filtrado[df_filtrado[col_status] == 'Ativo'].shape[0]
         col2.metric("Alunos Ativos (no Filtro)", f"{alunos_ativos}")
    else:
         col2.metric("Alunos Ativos (no Filtro)", 0)
    
    st.divider() 
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader('Distribuição por Unidade Acadêmica')
        dados_unidade = df_filtrado[col_unidade].fillna('Não Informado').value_counts().reset_index()
        dados_unidade.columns = ['Unidade', 'Total']
        
        fig_unidade = px.pie(
            dados_unidade, 
            names='Unidade', 
            values='Total',
            title='Alunos por Unidade (Filtro)',
            hole=0.4
        )
        fig_unidade.update_traces(textposition='inside', textinfo='percent+label', sort=False)
        st.plotly_chart(fig_unidade, use_container_width=True)
        
    with col_g2:
        st.subheader('Distribuição por Curso (Top 10)')
        dados_curso = df_filtrado[col_curso].fillna('Não Informado').value_counts().head(10).reset_index()
        dados_curso.columns = ['Curso', 'Total']
        
        fig_curso = px.bar(
            dados_curso,
            x='Total',
            y='Curso',
            color='Curso',
            orientation='h',
            title="Alunos por Curso (Filtro)"
        )
        fig_curso.update_layout(showlegend=False, yaxis_title="Curso")
        st.plotly_chart(fig_curso, use_container_width=True)


# --- ABA 2: PERFIL DO ALUNO ---
with tab_perfil:
    st.subheader("Perfil por Grupo/Raça")
    
    dados_raca = df_filtrado[col_raca_normalizada].value_counts().reset_index()
    dados_raca.columns = ['Grupo/Raça', 'Total']
    
    fig_raca = px.pie(
        dados_raca, 
        names='Grupo/Raça', 
        values='Total', 
        title='Distribuição por Grupo/Raça',
        hole=0.4 
    )
    fig_raca.update_traces(textposition='inside', textinfo='percent+label', sort=False)
    st.plotly_chart(fig_raca, use_container_width=True)


# --- ABA 3: DESEMPENHO ACADÊMICO ---
with tab_desempenho:
    
    st.subheader('Status e Progressão')
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("**Status Acadêmico Atual**")
        dados_status = df_filtrado[col_status].value_counts().reset_index()
        dados_status.columns = [col_status, 'Total']
        fig_status = px.bar(
            dados_status,
            x=col_status, y='Total', color=col_status, 
            title="Contagem por Status Acadêmico"
        )
        fig_status.update_layout(showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)
            
    with col_d2:
        st.markdown("**Progressão de Curso**")
        dados_progressao = df_filtrado[col_progressao].value_counts().reset_index()
        dados_progressao.columns = ['Progressão', 'Total']
        fig_progressao = px.pie(
            dados_progressao,
            names='Progressão', values='Total',
            title='Progressão (Atrasado vs. Regular)',
            hole=0.4
        )
        fig_progressao.update_traces(textposition='inside', textinfo='percent+label', sort=False)
        st.plotly_chart(fig_progressao, use_container_width=True)

    st.divider()

    st.subheader('Análise de Carga Horária (Semestre 2025.1)')
    df_ch = df_filtrado[df_filtrado[col_ch_esperada] > 0]
    
    if not df_ch.empty:
        avg_esperada = df_ch[col_ch_esperada].mean()
        avg_cursando = df_ch[col_ch_cursando].mean()
        delta = avg_cursando - avg_esperada
        
        col_ch1, col_ch2 = st.columns(2)
        col_ch1.metric(
            "C.H. Média Esperada", 
            f"{avg_esperada:.1f}h",
            help="Média de carga horária que os alunos neste filtro deveriam estar cursando."
        )
        col_ch2.metric(
            "C.H. Média Cursada", 
            f"{avg_cursando:.1f}h", 
            f"{delta:.1f}h",
            help="Média de carga horária que os alunos neste filtro estão de fato cursando."
        )
    else:
        st.info("Nenhum dado de carga horária esperada (maior que 0) encontrado para os filtros selecionados.")

    st.divider() 
    
    st.subheader('Alunos em Situação de Alerta (com Reprovações)')
    df_filtrado['Total Reprovações'] = df_filtrado[col_rep_falta] + df_filtrado[col_rep_media]
    
    df_alerta = df_filtrado[df_filtrado['Total Reprovações'] > 0][
        [col_nome, col_curso, col_status, 'Total Reprovações']
    ]
    
    total_alerta = df_alerta.shape[0]
    st.info(f"**{total_alerta}** alunos encontrados com reprovações (nos filtros selecionados).")

    if total_alerta > 0:
        with st.expander("► Clique para ver a Lista Detalhada"):
            st.dataframe(
                df_alerta.sort_values('Total Reprovações', ascending=False),
                use_container_width=True
            )
    else:
        st.success("Nenhum aluno em situação de alerta (com reprovações) nos filtros selecionados.")


# --- ABA 4: PERFIL DE INGRESSO ---
with tab_ingresso:
    st.subheader("Perfil de Ingresso")
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.markdown("**Evolução de Ingressantes por Ano**")
        if col_ano_ingresso in df_filtrado.columns:
            df_plot_ano = df_filtrado.dropna(subset=[col_ano_ingresso])
            dados_ano = df_plot_ano[col_ano_ingresso].value_counts().sort_index().reset_index()
            dados_ano.columns = ['Ano', 'Total de Ingressantes']
            dados_ano = dados_ano[dados_ano['Ano'] > 2000] 
            
            if not dados_ano.empty:
                fig_ano = px.line(
                    dados_ano,
                    x='Ano',
                    y='Total de Ingressantes',
                    title='Ingressantes por Ano (Filtro)',
                    markers=True
                )
                fig_ano.update_xaxes(type='category')
                st.plotly_chart(fig_ano, use_container_width=True)
            else:
                st.info("Nenhum dado de ano de ingresso válido para exibir.")
            
    with col_i2:
        st.markdown("**Forma de Ingresso**")
        dados_ingresso = df_filtrado[col_forma_ingresso].value_counts().reset_index()
        dados_ingresso.columns = ['Forma de IngGresso', 'Total']
        fig_ingresso = px.bar(
            dados_ingresso,
            x='Total', y='Forma de IngGresso', color='Forma de IngGresso',
            orientation='h',
            title='Contagem por Forma de Ingresso'
        )
        fig_ingresso.update_layout(showlegend=False)
        st.plotly_chart(fig_ingresso, use_container_width=True)


# --- ABA 5: SITUAÇÃO DE MATRÍCULA (MODIFICADA) ---
with tab_matricula:
    st.subheader("Análise de Matrícula de Alunos 'Ativos' (Risco de Evasão)")
    st.markdown("""
    Este gráfico foca **apenas nos alunos com status 'Ativo'** e mostra quantos deles
    se matricularam ou não no semestre. Alunos 'Ativos' que estão 'Não Matriculado'
    são um ponto crítico de atenção para a gestão.
    """)
    
    if col_status in df_filtrado.columns and col_status_matricula in df_filtrado.columns:
        
        # --- MUDANÇA: Filtra o DF para incluir APENAS alunos 'Ativos' ---
        # (Lembre-se que 'status' foi limpo para 'Title Case', por isso 'Ativo')
        df_ativos_filtrados = df_filtrado[df_filtrado[col_status] == 'Ativo']
        
        if not df_ativos_filtrados.empty:
            # Agrupa os dados filtrados apenas pela situação de matrícula
            df_grouped = df_ativos_filtrados.groupby(col_status_matricula).size().reset_index(name='Total')

            # --- MUDANÇA: Layout em duas colunas para os gráficos ---
            col_m1, col_m2 = st.columns(2)

            with col_m1:
                st.markdown("**Contagem de Matrícula (Alunos 'Ativos')**")
                fig_matricula_bar = px.bar(
                    df_grouped,
                    x=col_status_matricula,
                    y='Total',
                    color=col_status_matricula,
                    title="Alunos 'Ativos' vs. Situação de Matrícula"
                )
                fig_matricula_bar.update_layout(
                    xaxis_title="Situação de Matrícula", 
                    yaxis_title="Total de Alunos",
                    showlegend=False
                )
                st.plotly_chart(fig_matricula_bar, use_container_width=True)

            with col_m2:
                st.markdown("**Proporção de Matrícula (Alunos 'Ativos')**")
                fig_matricula_pie = px.pie(
                    df_grouped,
                    names=col_status_matricula,
                    values='Total',
                    title="Proporção (Alunos 'Ativos')",
                    hole=0.4
                )
                fig_matricula_pie.update_traces(textposition='inside', textinfo='percent+label', sort=False)
                st.plotly_chart(fig_matricula_pie, use_container_width=True)
                
        else:
            st.info("Nenhum aluno com status 'Ativo' foi encontrado com os filtros selecionados.")
            
    else:
        st.error("Colunas de status de matrícula não encontradas.")