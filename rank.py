import pandas as pd

df = pd.read_csv("data.csv")

country_codes = pd.read_csv("country_codes_ISO_3166-1_alpha-2.csv")["country_code"].values

indicators = [
    "NY.GDP.MKTP.CD",  # GDP (Current US$)
    "SP.POP.TOTL",  # Total Population
    "NY.GDP.PCAP.CD",  # GDP per Capita (Current US$)
    "NY.GDP.PCAP.PP.CD",  # GDP per Capita (Purchasing Power Parity)
    "SL.UEM.TOTL.ZS",  # Unemployment, Total (% of total labor force)
    "FP.CPI.TOTL.ZG",  # Inflation, Consumer Prices (annual %)
    "SI.POV.DDAY",  # Poverty headcount ratio at national poverty lines (% of population)
    "SI.POV.GINI",  # GINI index (Income inequality)
    "SH.DYN.MORT",  # Mortality rate, under-5 (per 1,000 live births)
    "SH.XPD.TOTL.ZS",  # Health expenditure, total (% of GDP)
    "SE.XPD.TOTL.GD.ZS",  # Education expenditure, total (% of GDP)
    "IT.NET.USER.ZS",  # Internet users (% of population)
    "NE.EXP.GNFS.ZS",  # Exports of goods and services (% of GDP)
    "NE.IMP.GNFS.ZS",  # Imports of goods and services (% of GDP)
    "AG.LND.TOTL.K2",  # Agricultural land (% of total land area)
    "EN.ATM.PM25.MC.M3",  # PM2.5 air pollution, population exposure (micrograms per cubic meter)
    "EG.USE.PCAP.KG.OE",  # Electric power consumption (kWh per capita)
    "TX.VAL.TOTL.GD.ZS",  # Tax revenue (% of GDP)
    "GC.TAX.TOTL.GD.ZS",  # General government tax revenue (% of GDP)
    "FI.RES.TOTL.M3",  # Domestic credit to private sector (% of GDP)
    "SL.TLF.TOTL.IN",  # Labor force participation rate, total (% of total population aged 15+)
    "GI.TAX.TOTL.ZS",  # General government revenue (% of GDP)
    "EG.USE.PCAP.KG.OE",  # Energy use (kg of oil equivalent per capita)
    "ST.INT.ARVL",  # International tourism, number of arrivals
    "NY.GDP.TOTL.ZS",  # GDP as % of the world GDP
    "SH.STA.MMRT",  # Maternal mortality ratio (per 100,000 live births)
    "SP.DYN.LE00.IN",  # Life expectancy at birth (total years)
    "SP.DYN.IMRT.IN",  # Infant mortality rate (per 1,000 live births)
    "CC.EST",  # Carbon dioxide emissions (metric tons per capita)
    "PV.EST",  # Total renewable energy consumption (% of total energy use)
    "RL.EST",  # Renewable energy consumption (% of total energy use)
    "IT.NET.SECR.P6",  # Internet security incidents reported
    "IE.PPI.WATR.CD",  # Population with access to clean water (%)
    "IP.PAT.RESD",  # Resident patent applications (per million population)
    "GB.XPD.RSDV.GD.ZS",  # Research and development expenditure (% of GDP)
    "IP.PAT.NRES",  # Non-resident patent applications (per million population)
    "VA.EST",  # Value added in manufacturing (% of GDP)
    "SM.POP.NETM",  # Net migration
    "MS.MIL.XPND.ZS"  # Military expenditure (% of GDP)
]

inverse_indicators = [
    "SL.UEM.TOTL.ZS", "FP.CPI.TOTL.ZG", "SI.POV.DDAY", "SI.POV.GINI", 
    "SH.DYN.MORT", "EN.ATM.PM25.MC.M3", "SH.STA.MMRT", "SP.DYN.IMRT.IN", 
    "CC.EST", "IT.NET.SECR.P6"
]

for i in indicators:
    if i in inverse_indicators:
        df[i] = -(df[i] - df[i].mean()) / df[i].std()
    else:
        df[i] = (df[i] - df[i].mean()) / df[i].std()

conts = {}

for i in range(len(country_codes)):
    conts[country_codes[i]] = df.iloc[i, 1:].mean()

conts = dict(reversed(sorted(conts.items(), key=lambda item: item[1])))

df = pd.read_csv("country_codes.csv")

country_dict = pd.Series(df['name'].values, index=df['alpha-2']).to_dict()

country = []
v = []

for i in conts:
    country.append(country_dict.get(i, "Country not found"))
    v.append(conts[i])

df = pd.DataFrame({"Country":country, "Score":v})

df.to_csv("rankings.csv", index=False)