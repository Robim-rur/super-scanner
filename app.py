import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =============================================================================
# SUPER SCANNER - ESTRATÉGIA DE EXAUSTÃO (EMA 69 + IFR2)
# =============================================================================
st.set_page_config(page_title="SUPER SCANNER - ALTA PRECISÃO", layout="wide")

def analisar_precisao(ticker):
    try:
        # Puxa 1 ano para ter dados sólidos da EMA 69
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df is None or len(df) < 70: return None
        
        # Limpeza de colunas (correção para novas versões do yfinance)
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        
        # CÁLCULO DOS INDICADORES
        df['EMA69'] = ta.ema(df['Close'], length=69)
        df['IFR2'] = ta.rsi(df['Close'], length=2)
        adx_df = ta.adx(df['High'], df['Low'], df['Close'], length=14)
        df = pd.concat([df, adx_df], axis=1)
        
        atual = df.iloc[-1]
        
        # REGRAS DO SUPER SCANNER (ALTA PROBABILIDADE)
        # 1. Tendência: Preço acima da EMA 69
        # 2. Exaustão: IFR de 2 períodos abaixo de 10 (Pânico de curto prazo)
        # 3. Força: ADX acima de 25 (Evita papéis "mortos")
        
        acima_ema69 = atual['Close'] > atual['EMA69']
        ifr_extremo = atual['IFR2'] < 10
        tendencia_forte = atual['ADX_14'] > 25
        
        if acima_ema69 and ifr_extremo and tendencia_forte:
            return {
                "Preço": round(float(atual['Close']), 2),
                "IFR2": round(atual['IFR2'], 1),
                "ADX": round(atual['ADX_14'], 1),
                "EMA 69": round(float(atual['EMA69']), 2)
            }
        return None
    except:
        return None

def main():
    st.title("🎯 Super Scanner de Alta Precisão")
    st.markdown("### Estratégia: IFR2 < 10 em Tendência de Alta (EMA 69)")

    # TODAS AS LISTAS UNIFICADAS
    acoes = [
        "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "ABEV3.SA", "JBSS3.SA", "ELET3.SA", 
        "WEGE3.SA", "RENT3.SA", "ITSA4.SA", "HAPV3.SA", "GGBR4.SA", "SUZB3.SA", "B3SA3.SA", "MGLU3.SA", 
        "LREN3.SA", "EQTL3.SA", "CSAN3.SA", "RDOR3.SA", "PRIO3.SA", "VIBR3.SA", "UGPA3.SA", "SBSP3.SA", 
        "ASAI3.SA", "CCRO3.SA", "RADL3.SA", "CMIG4.SA", "CPLE6.SA", "TOTS3.SA", "EMBR3.SA", "BRFS3.SA"
    ]
    
    bdrs = [
        "AAPL34.SA", "AMZO34.SA", "GOGL34.SA", "MSFT34.SA", "TSLA34.SA", "META34.SA", "NFLX34.SA", 
        "NVDC34.SA", "MELI34.SA", "BABA34.SA", "DISB34.SA", "PYPL34.SA", "VISA34.SA", "WMTB34.SA"
    ]
    
    etfs_fiis = [
        "BOVA11.SA", "IVVB11.SA", "SMAL11.SA", "HASH11.SA", "GOLD11.SA", "GARE11.SA", "HGLG11.SA", 
        "XPLG11.SA", "XPML11.SA", "VISC11.SA", "KNRI11.SA", "BTLG11.SA", "MXRF11.SA"
    ]

    lista_total = list(set(acoes + bdrs + etfs_fiis)) # Remove duplicatas caso existam

    if st.button('🚀 Iniciar Varredura em Todos os Mercados'):
        hits = []
        barra = st.progress(0)
        status = st.empty()
        
        for i, t in enumerate(lista_total):
            status.text(f"Analisando Ativo {i+1}/{len(lista_total)}: {t.replace('.SA', '')}")
            res = analisar_precisao(t)
            if res:
                hits.append({
                    "ATIVO": t.replace(".SA", ""),
                    "PREÇO": res["Preço"],
                    "IFR2": res["IFR2"],
                    "ADX": res["ADX"],
                    "EMA 69 (D)": res["EMA 69"]
                })
            barra.progress((i + 1) / len(lista_total))
        
        status.success("Varredura Global Finalizada!")
        
        if hits:
            st.subheader("🔥 Oportunidades de Exaustão Encontradas")
            st.table(pd.DataFrame(hits))
            st.info("💡 Estes ativos estão em 'pânico' de curto prazo dentro de uma tendência de alta. Geralmente revertem rápido.")
        else:
            st.warning("Nenhum ativo está em ponto de exaustão extrema (IFR2 < 10) no momento.")

if __name__ == "__main__":
    main()
