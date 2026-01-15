import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =============================================================================
# SCANNER DE RETOMADA (PULLBACK NA EMA 69) - 173 ATIVOS
# =============================================================================
st.set_page_config(page_title="SCANNER DE RETOMADA - ELITE", layout="wide")

def analisar_retomada(ticker):
    try:
        df = yf.download(ticker, period="100d", interval="1d", progress=False)
        if df is None or len(df) < 70: return None
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        
        # Média de referência (Sua favorita)
        df['EMA69'] = ta.ema(df['Close'], length=69)
        
        # Pegamos os últimos 3 dias
        c0 = df.iloc[-1] # Hoje
        c1 = df.iloc[-2] # Ontem
        c2 = df.iloc[-3] # Anteontem
        
        # REGRAS DO SETUP DE RETOMADA:
        # 1. Tendência: Preço acima da EMA 69
        # 2. Pullback: Dois fechamentos seguidos de queda (c1 < c2 e c0 < c1)
        # 3. Proximidade: O preço não pode estar longe demais da média (até 5%)
        
        acima_ema69 = c0['Close'] > c0['EMA69']
        dois_dias_queda = (c1['Close'] < c2['Close']) and (c0['Close'] < c1['Close'])
        perto_da_media = c0['Close'] < (c0['EMA69'] * 1.05) 
        
        if acima_ema69 and dois_dias_queda and perto_da_media:
            return {
                "Preço Atual": round(float(c0['Close']), 2),
                "Máxima p/ Compra": round(float(c0['High']) + 0.01, 2),
                "EMA 69": round(float(c0['EMA69']), 2),
                "Distância %": round(((c0['Close'] / c0['EMA69']) - 1) * 100, 1)
            }
        return None
    except: return None

def main():
    st.title("🛡️ Scanner de Retomada (Pullback na EMA 69)")
    st.write("Foco: Comprar após 2 dias de correção em tendência de alta.")

    # LISTAS UNIFICADAS (MESMA BASE DE 173 ATIVOS)
    acoes_100 = ["RRRP3.SA", "ALOS3.SA", "ALPA4.SA", "ABEV3.SA", "ARZZ3.SA", "ASAI3.SA", "AZUL4.SA", "B3SA3.SA", "BBAS3.SA", "BBDC3.SA", "BBDC4.SA", "BBSE3.SA", "BEEF3.SA", "BPAC11.SA", "BRAP4.SA", "BRFS3.SA", "BRKM5.SA", "CCRO3.SA", "CMIG4.SA", "CMIN3.SA", "COGN3.SA", "CPFE3.SA", "CPLE6.SA", "CRFB3.SA", "CSAN3.SA", "CSNA3.SA", "CYRE3.SA", "DXCO3.SA", "EGIE3.SA", "ELET3.SA", "ELET6.SA", "EMBR3.SA", "ENEV3.SA", "ENGI11.SA", "EQTL3.SA", "EZTC3.SA", "FLRY3.SA", "GGBR4.SA", "GOAU4.SA", "GOLL4.SA", "HAPV3.SA", "HYPE3.SA", "ITSA4.SA", "ITUB4.SA", "JBSS3.SA", "KLBN11.SA", "LREN3.SA", "LWSA3.SA", "MGLU3.SA", "MRFG3.SA", "MRVE3.SA", "MULT3.SA", "NTCO3.SA", "PETR3.SA", "PETR4.SA", "PRIO3.SA", "RADL3.SA", "RAIL3.SA", "RAIZ4.SA", "RENT3.SA", "RECV3.SA", "SANB11.SA", "SBSP3.SA", "SLCE3.SA", "SMTO3.SA", "SUZB3.SA", "TAEE11.SA", "TIMS3.SA", "TOTS3.SA", "TRPL4.SA", "UGPA3.SA", "USIM5.SA", "VALE3.SA", "VIVT3.SA", "VIVA3.SA", "WEGE3.SA", "YDUQ3.SA", "AURE3.SA", "BHIA3.SA", "CASH3.SA", "CVCB3.SA", "DIRR3.SA", "ENAT3.SA", "GMAT3.SA", "IFCM3.SA", "INTB3.SA", "JHSF3.SA", "KEPL3.SA", "MOVI3.SA", "ORVR3.SA", "PETZ3.SA", "PLAS3.SA", "POMO4.SA", "POSI3.SA", "RANI3.SA", "RAPT4.SA", "STBP3.SA", "TEND3.SA", "TUPY3.SA"]
    bdrs_50 = ["AAPL34.SA", "AMZO34.SA", "GOGL34.SA", "MSFT34.SA", "TSLA34.SA", "META34.SA", "NFLX34.SA", "NVDC34.SA", "MELI34.SA", "BABA34.SA", "DISB34.SA", "PYPL34.SA", "JNJB34.SA", "PGCO34.SA", "KOCH34.SA", "VISA34.SA", "WMTB34.SA", "NIKE34.SA", "ADBE34.SA", "AVGO34.SA", "CSCO34.SA", "COST34.SA", "CVSH34.SA", "GECO34.SA", "GSGI34.SA", "HDCO34.SA", "INTC34.SA", "JPMC34.SA", "MAEL34.SA", "MCDP34.SA", "MDLZ34.SA", "MRCK34.SA", "ORCL34.SA", "PEP334.SA", "PFIZ34.SA", "PMIC34.SA", "QCOM34.SA", "SBUX34.SA", "TGTB34.SA", "TMOS34.SA", "TXN34.SA", "UNHH34.SA", "UPSB34.SA", "VZUA34.SA", "ABTT34.SA", "AMGN34.SA", "AXPB34.SA", "BAOO34.SA", "CATP34.SA", "HONB34.SA"]
    etfs_fiis_24 = ["BOVA11.SA", "IVVB11.SA", "SMAL11.SA", "HASH11.SA", "GOLD11.SA", "GARE11.SA", "HGLG11.SA", "XPLG11.SA", "VILG11.SA", "BRCO11.SA", "BTLG11.SA", "XPML11.SA", "VISC11.SA", "HSML11.SA", "MALL11.SA", "KNRI11.SA", "JSRE11.SA", "PVBI11.SA", "HGRE11.SA", "MXRF11.SA", "KNCR11.SA", "KNIP11.SA", "CPTS11.SA", "IRDM11.SA"]
    
    lista_total = sorted(list(set(acoes_100 + bdrs_50 + etfs_fiis_24)))

    if st.button('🚀 Varredura de Retomada (173 Ativos)'):
        hits = []
        barra = st.progress(0)
        for i, t in enumerate(lista_total):
            res = analisar_retomada(t)
            if res:
                hits.append({"ATIVO": t.replace(".SA", ""), "PREÇO": res["Preço Atual"], "GATILHO (MÁX)": res["Máxima p/ Compra"], "EMA 69": res["EMA 69"], "DIST %": res["Distância %"]})
            barra.progress((i + 1) / len(lista_total))
        
        if hits: st.table(pd.DataFrame(hits))
        else: st.info("Nenhum ativo em padrão de pullback hoje.")

if __name__ == "__main__":
    main()
