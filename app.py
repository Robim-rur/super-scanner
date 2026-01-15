import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =============================================================================
# SUPER SCANNER GLOBAL - 100 AÇÕES + BDRS + ETFS + FIIS
# =============================================================================
st.set_page_config(page_title="SUPER SCANNER GLOBAL - ELITE", layout="wide")

def analisar_precisao(ticker):
    try:
        # Puxa histórico para EMA 69 e IFR2
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df is None or len(df) < 70: return None
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        
        # CÁLCULO DOS INDICADORES
        df['EMA69'] = ta.ema(df['Close'], length=69)
        df['IFR2'] = ta.rsi(df['Close'], length=2)
        adx_df = ta.adx(df['High'], df['Low'], df['Close'], length=14)
        df = pd.concat([df, adx_df], axis=1)
        
        atual = df.iloc[-1]
        
        # REGRAS RÍGIDAS DE ALTA PRECISÃO
        # Preço > EMA 69 E IFR2 < 10 E ADX > 20
        if (atual['Close'] > atual['EMA69']) and (atual['IFR2'] < 10) and (atual['ADX_14'] > 20):
            return {
                "Preço": round(float(atual['Close']), 2),
                "IFR2": round(atual['IFR2'], 1),
                "ADX": round(atual['ADX_14'], 1),
                "EMA 69": round(float(atual['EMA69']), 2)
            }
        return None
    except: return None

def main():
    st.title("🎯 Super Scanner Global: Precisão Total")
    st.markdown("### Estratégia: IFR2 < 10 + Tendência EMA 69")

    # --- LISTA COMPLETA 100 AÇÕES B3 ---
    acoes_100 = [
        "RRRP3.SA", "ALOS3.SA", "ALPA4.SA", "ABEV3.SA", "ARZZ3.SA", "ASAI3.SA", "AZUL4.SA", "B3SA3.SA", "BBAS3.SA", "BBDC3.SA", 
        "BBDC4.SA", "BBSE3.SA", "BEEF3.SA", "BPAC11.SA", "BRAP4.SA", "BRFS3.SA", "BRKM5.SA", "CCRO3.SA", "CMIG4.SA", "CMIN3.SA", 
        "COGN3.SA", "CPFE3.SA", "CPLE6.SA", "CRFB3.SA", "CSAN3.SA", "CSNA3.SA", "CYRE3.SA", "DXCO3.SA", "EGIE3.SA", "ELET3.SA", 
        "ELET6.SA", "EMBR3.SA", "ENEV3.SA", "ENGI11.SA", "EQTL3.SA", "EZTC3.SA", "FLRY3.SA", "GGBR4.SA", "GOAU4.SA", "GOLL4.SA", 
        "HAPV3.SA", "HYPE3.SA", "ITSA4.SA", "ITUB4.SA", "JBSS3.SA", "KLBN11.SA", "LREN3.SA", "LWSA3.SA", "MGLU3.SA", "MRFG3.SA", 
        "MRVE3.SA", "MULT3.SA", "NTCO3.SA", "PETR3.SA", "PETR4.SA", "PRIO3.SA", "RADL3.SA", "RAIL3.SA", "RAIZ4.SA", "RENT3.SA", 
        "RECV3.SA", "SANB11.SA", "SBSP3.SA", "SLCE3.SA", "SMTO3.SA", "SUZB3.SA", "TAEE11.SA", "TIMS3.SA", "TOTS3.SA", "TRPL4.SA", 
        "UGPA3.SA", "USIM5.SA", "VALE3.SA", "VIVT3.SA", "VIVA3.SA", "WEGE3.SA", "YDUQ3.SA", "AURE3.SA", "BHIA3.SA", "CASH3.SA", 
        "CVCB3.SA", "DIRR3.SA", "ENAT3.SA", "GMAT3.SA", "IFCM3.SA", "INTB3.SA", "JHSF3.SA", "KEPL3.SA", "MOVI3.SA", "ORVR3.SA", 
        "PETZ3.SA", "PLAS3.SA", "POMO4.SA", "POSI3.SA", "RANI3.SA", "RAPT4.SA", "STBP3.SA", "TEND3.SA", "TUPY3.SA", "PETR4.SA"
    ]

    # --- LISTA BDRs (TOP LIQUIDEZ) ---
    bdrs = [
        "AAPL34.SA", "AMZO34.SA", "GOGL34.SA", "MSFT34.SA", "TSLA34.SA", "META34.SA", "NFLX34.SA", "NVDC34.SA", "MELI34.SA", 
        "BABA34.SA", "DISB34.SA", "PYPL34.SA", "JNJB34.SA", "PGCO34.SA", "KOCH34.SA", "VISA34.SA", "WMTB34.SA", "NIKE34.SA"
    ]

    # --- LISTA ETFs E FIIs (TIJOLO E PAPEL LÍQUIDOS) ---
    etfs_fiis = [
        "BOVA11.SA", "IVVB11.SA", "SMAL11.SA", "HASH11.SA", "GOLD11.SA", "GARE11.SA", "HGLG11.SA", "XPLG11.SA", "VILG11.SA", 
        "BRCO11.SA", "BTLG11.SA", "XPML11.SA", "VISC11.SA", "KNRI11.SA", "JSRE11.SA", "PVBI11.SA", "HGRE11.SA", "MXRF11.SA",
        "KNCR11.SA", "KNIP11.SA", "CPTS11.SA", "IRDM11.SA"
    ]

    # Unificação sem duplicatas
    lista_total = sorted(list(set(acoes_100 + bdrs + etfs_fiis)))

    st.write(f"🚀 **Monitorando {len(lista_total)} ativos** (100 Ações + BDRs + ETFs/FIIs)")

    if st.button('🎯 Iniciar Varredura Global'):
        hits = []
        barra = st.progress(0)
        status = st.empty()
        
        for i, t in enumerate(lista_total):
            status.text(f"Analisando {i+1}/{len(lista_total)}: {t.replace('.SA', '')}")
            res = analisar_precisao(t)
            if res:
                hits.append({
                    "ATIVO": t.replace(".SA", ""),
                    "PREÇO": res["Preço"],
                    "IFR2": res["IFR2"],
                    "ADX": res["ADX"],
                    "EMA 69": res["EMA 69"]
                })
            barra.progress((i + 1) / len(lista_total))
        
        status.success("Varredura Global Finalizada!")
        
        if hits:
            st.table(pd.DataFrame(hits))
        else:
            st.info("Nenhum ativo em ponto de exaustão extrema (IFR2 < 10) no momento.")

if __name__ == "__main__":
    main()
