import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import pulp
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import expected_returns
from pypfopt import risk_models
from pypfopt.efficient_frontier import EfficientFrontier
import sys

START = "2010-01-01"
# Define the ticker list
tickers_nifty50 = "ADANIPORTS.NS ASIANPAINT.NS AXISBANK.NS BAJAJ-AUTO.NS BAJFINANCE.NS BAJAJFINSV.NS BPCL.NS BHARTIARTL.NS BRITANNIA.NS CIPLA.NS COALINDIA.NS DIVISLAB.NS DRREDDY.NS EICHERMOT.NS GAIL.NS GRASIM.NS HCLTECH.NS HDFCBANK.NS HDFCLIFE.NS HEROMOTOCO.NS HINDALCO.NS HINDUNILVR.NS HDFC.NS ICICIBANK.NS ITC.NS IOC.NS INDUSINDBK.NS INFY.NS JSWSTEEL.NS KOTAKBANK.NS LT.NS M&M.NS MARUTI.NS NTPC.NS NESTLEIND.NS ONGC.NS POWERGRID.NS RELIANCE.NS SBILIFE.NS SHREECEM.NS SBIN.NS SUNPHARMA.NS TCS.NS TATAMOTORS.NS TATASTEEL.NS TECHM.NS TITAN.NS UPL.NS ULTRACEMCO.NS WIPRO.NS"
tickers_nifty100 = "ACC.NS ABBOTINDIA.NS ADANIGREEN.NS ADANIPORTS.NS ADANITRANS.NS ALKEM.NS AMBUJACEM.NS ASIANPAINT.NS AUROPHARMA.NS DMART.NS AXISBANK.NS BAJAJ-AUTO.NS BAJFINANCE.NS BAJAJFINSV.NS BAJAJHLDNG.NS BANDHANBNK.NS BANKBARODA.NS BERGEPAINT.NS BPCL.NS BHARTIARTL.NS BIOCON.NS BOSCHLTD.NS BRITANNIA.NS CADILAHC.NS CIPLA.NS COALINDIA.NS COLPAL.NS CONCOR.NS DLF.NS DABUR.NS DIVISLAB.NS DRREDDY.NS EICHERMOT.NS GAIL.NS GICRE.NS GODREJCP.NS GRASIM.NS HCLTECH.NS HDFCAMC.NS HDFCBANK.NS HDFCLIFE.NS HAVELLS.NS HEROMOTOCO.NS HINDALCO.NS HINDPETRO.NS HINDUNILVR.NS HINDZINC.NS HDFC.NS ICICIBANK.NS ICICIGI.NS ICICIPRULI.NS ITC.NS IOC.NS IGL.NS INDUSTOWER.NS INDUSINDBK.NS NAUKRI.NS INFY.NS INDIGO.NS JSWSTEEL.NS KOTAKBANK.NS LTI.NS LT.NS LUPIN.NS M&M.NS MARICO.NS MARUTI.NS MOTHERSUMI.NS MUTHOOTFIN.NS NMDC.NS NTPC.NS NESTLEIND.NS ONGC.NS OFSS.NS PETRONET.NS PIDILITIND.NS PEL.NS PFC.NS POWERGRID.NS PGHH.NS PNB.NS RELIANCE.NS SBICARD.NS SBILIFE.NS SHREECEM.NS SIEMENS.NS SBIN.NS SUNPHARMA.NS TCS.NS TATACONSUM.NS TATAMOTORS.NS TATASTEEL.NS TECHM.NS TITAN.NS TORNTPHARM.NS UPL.NS ULTRACEMCO.NS UBL.NS MCDOWELL-N.NS WIPRO.NS"
tickers_nifty200 = "ACC.NS AUBANK.NS AARTIIND.NS ABBOTINDIA.NS ADANIENT.NS ADANIGREEN.NS ADANIPORTS.NS ATGL.NS ADANITRANS.NS ABCAPITAL.NS ABFRL.NS AJANTPHARM.NS APLLTD.NS ALKEM.NS AMARAJABAT.NS AMBUJACEM.NS APOLLOHOSP.NS APOLLOTYRE.NS ASHOKLEY.NS ASIANPAINT.NS AUROPHARMA.NS DMART.NS AXISBANK.NS BAJAJ-AUTO.NS BAJFINANCE.NS BAJAJFINSV.NS BAJAJHLDNG.NS BALKRISIND.NS BANDHANBNK.NS BANKBARODA.NS BANKINDIA.NS BATAINDIA.NS BERGEPAINT.NS BEL.NS BHARATFORG.NS BHEL.NS BPCL.NS BHARTIARTL.NS BIOCON.NS BBTC.NS BOSCHLTD.NS BRITANNIA.NS CESC.NS CADILAHC.NS CANBK.NS CASTROLIND.NS CHOLAFIN.NS CIPLA.NS CUB.NS COALINDIA.NS COFORGE.NS COLPAL.NS CONCOR.NS COROMANDEL.NS CROMPTON.NS CUMMINSIND.NS DLF.NS DABUR.NS DALBHARAT.NS DHANI.NS DIVISLAB.NS LALPATHLAB.NS DRREDDY.NS EDELWEISS.NS EICHERMOT.NS EMAMILTD.NS ENDURANCE.NS ESCORTS.NS EXIDEIND.NS FEDERALBNK.NS FORTIS.NS FRETAIL.NS GAIL.NS GMRINFRA.NS GICRE.NS GLENMARK.NS GODREJAGRO.NS GODREJCP.NS GODREJIND.NS GODREJPROP.NS GRASIM.NS GUJGASLTD.NS GSPL.NS HCLTECH.NS HDFCAMC.NS HDFCBANK.NS HDFCLIFE.NS HAVELLS.NS HEROMOTOCO.NS HINDALCO.NS HINDPETRO.NS HINDUNILVR.NS HINDZINC.NS HUDCO.NS HDFC.NS ICICIBANK.NS ICICIGI.NS ICICIPRULI.NS ISEC.NS IDFCFIRSTB.NS ITC.NS IBULHSGFIN.NS INDHOTEL.NS IOC.NS IRCTC.NS IGL.NS INDUSTOWER.NS INDUSINDBK.NS NAUKRI.NS INFY.NS INDIGO.NS IPCALAB.NS JSWENERGY.NS JSWSTEEL.NS JINDALSTEL.NS JUBLFOOD.NS KOTAKBANK.NS L&TFH.NS LTTS.NS LICHSGFIN.NS LTI.NS LT.NS LUPIN.NS MRF.NS MGL.NS M&MFIN.NS M&M.NS MANAPPURAM.NS MARICO.NS MARUTI.NS MFSL.NS MINDTREE.NS MOTHERSUMI.NS MPHASIS.NS MUTHOOTFIN.NS NATCOPHARM.NS NMDC.NS NTPC.NS NATIONALUM.NS NAVINFLUOR.NS NESTLEIND.NS NAM-INDIA.NS OBEROIRLTY.NS ONGC.NS OIL.NS OFSS.NS PIIND.NS PAGEIND.NS PETRONET.NS PFIZER.NS PIDILITIND.NS PEL.NS POLYCAB.NS PFC.NS POWERGRID.NS PRESTIGE.NS PGHH.NS PNB.NS RBLBANK.NS RECLTD.NS RAJESHEXPO.NS RELIANCE.NS SBICARD.NS SBILIFE.NS SRF.NS SANOFI.NS SHREECEM.NS SRTRANSFIN.NS SIEMENS.NS SBIN.NS SAIL.NS SUNPHARMA.NS SUNTV.NS SYNGENE.NS TVSMOTOR.NS TATACHEM.NS TCS.NS TATACONSUM.NS TATAMOTORS.NS TATAPOWER.NS TATASTEEL.NS TECHM.NS RAMCOCEM.NS TITAN.NS TORNTPHARM.NS TORNTPOWER.NS TRENT.NS UPL.NS ULTRACEMCO.NS UNIONBANK.NS UBL.NS MCDOWELL-N.NS VGUARD.NS VBL.NS IDEA.NS VOLTAS.NS WHIRLPOOL.NS WIPRO.NS YESBANK.NS ZEEL.NS"
# Logger to log the console Verbose output and print it to Standard output


class Logger():
    stdout = sys.stdout
    messages = []

    def start(self):
        sys.stdout = self

    def stop(self):
        sys.stdout = self.stdout

    def write(self, text):
        self.messages.append(text)


log = Logger()


# -- Set page config
apptitle = "Lycan's Portfolio Optimizer"
st.set_page_config(page_title=apptitle, page_icon="chart_with_upwards_trend")

# Title the app
st.title("Lycan's Portfolio Optimizer")

st.markdown("""
 * Calculate the executed annualized returns and the annualized sample covariance matrix of the daily asset
 * Use the menu at left to select NIFTY Index and your investment amount
 * Your predicted portfolio stocks will apear below with their perfromance
""")

st.sidebar.markdown("## Select Index and Amount")
# -- Get list of events
# Nifty Index input
nifty_num = st.sidebar.radio("Select the NIFTY Index",
                             ('Nifty 50', 'Nifty 100', 'Nifty 200'))

# Portfolio amount
portfolio_val = st.sidebar.number_input(
    "Enter your Investment amount :", value=10000)

if nifty_num == 'Nifty 50':
    tickers = tickers_nifty50
elif nifty_num == 'Nifty 100':
    tickers = tickers_nifty100
elif nifty_num == 'Nifty 200':
    tickers = tickers_nifty200


@st.cache
def load_data(tickers):
    data = yf.download(tickers, START)['Adj Close']
    return data


data_load_state = st.text('Loading data...this may take a minute')
data = load_data(tickers)
data_load_state.text('Loading data... ✔️done!')

# data = data.set_index(pd.DatetimeIndex(data['Date'].values))
# data.drop(columns=['Date'], axis=1, inplace=True)
assets = data.columns

# Optimize the Portfolio - Calculate the execcuted annualized returns and the annualized sample covariance matrix of the daily asset
# Method 1
mu = expected_returns.mean_historical_return(data)
S = risk_models.sample_cov(data)

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()

cleaned_weights = ef.clean_weights()

# Log the console Verbose output and print it to Standard output
log.start()
ef.portfolio_performance(verbose=True)
log.stop()
st.subheader("Performance :")
for i in range(3):
    st.write(log.messages[2 * i])

# Portfolio Value
latest_prices = get_latest_prices(data)
weights = cleaned_weights
da = DiscreteAllocation(weights, latest_prices,
                        total_portfolio_value=portfolio_val)
allocation, leftover = da.lp_portfolio()
df_allocation = pd.DataFrame.from_dict(allocation, orient='index')
# df_allocation.index.rename('new name', inplace=True)
# df_allocation.rename(columns={"0": 'Quantity'}, inplace=True)

st.subheader('Discreate Allocation : ')
st.dataframe(df_allocation)
st.write('Funds Remaining : ₹', round(leftover, 2))

with st.beta_expander("See Additional Details"):
    df_load_state = st.text('Hold Tight....Loading Addditional data👉👈 ')
    # Store the company name into list
    company_name = []
    company_sector = []
    company_beta = []
    company_trailingPE = []
    company_previousClose = []
    discrete_allocation_list = []
    for symbol in allocation:
        data = yf.Ticker(symbol).info
        company_name.append(data['longName'])
        company_sector.append(data['sector'])
        company_beta.append(data['beta'])
        company_trailingPE.append(data['trailingPE'])
        company_previousClose.append(data['regularMarketPreviousClose'])
        discrete_allocation_list.append(allocation.get(symbol))

    # Create a Dataframe for Portfolio
    portfolio_df = pd.DataFrame(columns=['Company_Name', 'Allocated Quantity_'+str(portfolio_val), 'Company_Sector', 'Company_Beta',
                                         'Company_TrailingPE', 'Company_PreviousClose', 'Company_Ticker'])

    portfolio_df['Company_Name'] = company_name
    portfolio_df['Company_Ticker'] = allocation
    portfolio_df['Company_Sector'] = company_sector
    portfolio_df['Company_Beta'] = company_beta
    portfolio_df['Company_TrailingPE'] = company_trailingPE
    portfolio_df['Company_PreviousClose'] = company_previousClose
    portfolio_df['Allocated Quantity_' +
                 str(portfolio_val)] = discrete_allocation_list

    # Show the Portfolio
    df_load_state.text('Loading data... ✔️done!')
    st.dataframe(portfolio_df)
