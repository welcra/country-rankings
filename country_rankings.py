import requests
import pandas as pd
import time

country_codes = pd.read_csv("country_codes_ISO_3166-1_alpha-2.csv")["country_code"].values


indicators = [
    # Economic Indicators
    "NY.GDP.MKTP.CD",  # GDP (current US$)
    "NY.GDP.PCAP.PP.CD",  # GDP per capita (current US$) (PPP)
    "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
    "NE.EXP.GNFS.ZS",  # Exports of goods and services (% of GDP)
    "NE.IMP.GNFS.ZS",  # Imports of goods and services (% of GDP)
    "BX.KLT.DINV.CD.WD",  # Foreign direct investment, net inflows (BoP, current US$)
    "FR.INR.RINR",  # Real interest rate (%)
    "NY.GDP.DEFL.KD.ZG",  # Inflation, GDP deflator (annual %)
    "GC.DOD.TOTL.GD.ZS",  # Central government debt, total (% of GDP)
    "FP.CPI.TOTL",  # Inflation, consumer prices (annual %)
    "NE.CON.PRVT.ZS",  # Household consumption expenditure (% of GDP)
    "NE.GDI.TOTL.ZS",  # Gross capital formation (% of GDP)
    "FM.LBL.MQMY.GD.ZS",  # Domestic credit to private sector (% of GDP)
    "GC.REV.XGRT.GD.ZS",  # Revenue, excluding grants (% of GDP)
    "NE.TRD.GNFS.ZS",  # Trade (% of GDP)
    
    # Social Indicators
    "SP.POP.TOTL",  # Population, total
    "SP.POP.GROW",  # Population growth (annual %)
    "SP.DYN.LE00.IN",  # Life expectancy at birth, total (years)
    "SE.XPD.TOTL.GD.ZS",  # Government expenditure on education (% of GDP)
    "SE.ADT.LITR.ZS",  # Literacy rate, adult total (% of people aged 15+)
    "SH.XPD.CHEX.GD.ZS",  # Current health expenditure (% of GDP)
    "SH.DYN.MORT",  # Mortality rate, under-5 (per 1,000 live births)
    "SH.DYN.NMRT",  # Neonatal mortality rate (per 1,000 live births)
    "SH.STA.MMRT",  # Maternal mortality ratio (per 100,000 live births)
    "EG.ELC.ACCS.ZS",  # Access to electricity (% of population)
    "IT.NET.USER.ZS",  # Individuals using the Internet (% of population)
    "SH.IMM.IDPT",  # Immunization, DPT (% of children ages 12-23 months)
    "SH.STA.BRTC.ZS",  # Births attended by skilled health staff (% of total)
    "SH.HIV.INCD.TL.P3",  # Incidence of HIV (% of uninfected population ages 15-49)
    "SH.STA.SMSS.ZS",  # Smoking prevalence, males (% of adults)
    "SH.STA.SSMS.ZS",  # Smoking prevalence, females (% of adults)
    
    # Environmental Indicators
    "AG.LND.FRST.ZS",  # Forest area (% of land area)
    "EN.ATM.CO2E.PC",  # CO2 emissions (metric tons per capita)
    "EN.POP.SLUM.UR.ZS",  # Population living in slums (% of urban population)
    "EG.ELC.RNEW.ZS",  # Renewable electricity output (% of total electricity output)
    "EG.FEC.RNEW.ZS",  # Renewable energy consumption (% of total final energy consumption)
    "EN.ATM.PM25.MC.M3",  # PM2.5 air pollution, mean annual exposure (micrograms per cubic meter)
    "EN.CLC.MDAT.ZS",  # Land area under cereal production (% of total)
    "ER.H2O.INTR.PC",  # Renewable internal freshwater resources per capita (cubic meters)
    "EN.ATM.METH.KT.CE",  # Methane emissions (kt of CO2 equivalent)
    "EN.ATM.NOXE.KT.CE",  # Nitrous oxide emissions (thousand metric tons of CO2 equivalent)
    "AG.LND.TOTL.K2",  # Land area (sq. km)
    "AG.PRD.CROP.XD",  # Crop production index (2004-2006 = 100)
    "AG.PRD.FOOD.XD",  # Food production index (2004-2006 = 100)
    "AG.YLD.CREL.KG",  # Cereal yield (kg per hectare)
    "AG.SRF.TOTL.K2",  # Surface area (sq. km)
    
    # Governance Indicators
    "IQ.CPA.TRAN.XQ",  # Control of corruption (estimate)
    "IQ.CPA.GOVE.XQ",  # Government effectiveness (estimate)
    "IQ.CPA.PROP.XQ",  # Rule of law (estimate)
    "IQ.CPA.REG.XQ",  # Regulatory quality (estimate)
    "IQ.CPA.POLS.XQ",  # Political stability and absence of violence (estimate)
    "IQ.CPA.VACR.XQ",  # Voice and accountability (estimate)
    "IC.BUS.EASE.XQ",  # Ease of doing business score (1=most business-friendly regulations)
    "GC.TAX.TOTL.GD.ZS",  # Total tax revenue (% of GDP)
    "SL.UEM.TOTL.ZS",  # Unemployment, total (% of total labor force)
    "IC.REG.DURS",  # Time required to start a business (days)
    "SE.TER.CUAT.BA.ZS",  # Educational attainment, at least Bachelor's or equivalent (% ages 25+)
    "SE.PRM.CMPT.ZS",  # Primary completion rate, total (% of relevant age group)
    "SG.GEN.PARL.ZS",  # Proportion of seats held by women in national parliaments (%)
    
    # Infrastructure Indicators
    "IT.CEL.SETS.P2",  # Mobile cellular subscriptions (per 100 people)
    "IS.ROD.DNST.K2",  # Road density (km of road per sq. km of land area)
    "EG.IMP.CONS.ZS",  # Energy imports, net (% of energy use)
    "EG.USE.ELEC.KH.PC",  # Electric power consumption (kWh per capita)
    "IT.MLT.MAIN.P2",  # Fixed telephone subscriptions (per 100 people)
    "IS.AIR.PSGR",  # Air transport, passengers carried
    "IS.AIR.GOOD.MT.K1",  # Air transport, freight (million ton-km)
    "IS.RRS.GOOD.MT.K1",  # Railways, goods transported (million ton-km)
    "IS.RRS.PASG.KM",  # Railways, passengers carried (million passenger-km)
    "IS.VEH.NVEH.P3",  # Motor vehicles (per 1,000 people)
    
    # Inequality and Poverty Indicators
    "SI.POV.GINI",  # Gini index (World Bank estimate)
    "SI.POV.DDAY",  # Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)
    "SI.POV.NAHC",  # Poverty headcount ratio at national poverty lines (% of population)
    "SI.DST.05TH.20",  # Income share held by lowest 20%
    "SI.DST.10TH.10",  # Income share held by highest 10%
    "SI.POV.UMIC",  # Poverty headcount ratio at $5.50 a day (2017 PPP) (% of population)
    "SI.POV.LMIC",  # Poverty headcount ratio at $3.20 a day (2017 PPP) (% of population)
    "SI.POV.RUHC",  # Rural poverty headcount ratio at national poverty lines (% of rural population)
    "SI.POV.URHC",  # Urban poverty headcount ratio at national poverty lines (% of urban population)",
]


all_data = {}

for indicator in indicators:

    vs = {}

    for country_code in country_codes:
        try:

            url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json"

            response = requests.get(url)

            data = response.json()
            v = data[1][0]['value']
            vs[country_code] = v
        except:
            None

    all_data[indicator] = vs
    print(indicators.index(indicator)/len(indicators))
    #time.sleep(30)


df = pd.DataFrame(all_data)

df.to_csv("data.csv")