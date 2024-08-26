#!/bin/sh

export US100Components="AAPL,ABNB,ADBE,ADI,ADP,ADSK,AEP,AMAT,AMD,AMGN,AMZN,ANSS,ARM,ASML,AVGO,AZN,BIIB,BKNG,BKR,CCEP,CDNS,CDW,CEG,CHTR,CMCSA,COST,CPRT,CRWD,CSCO,CSGP,CSX,CTAS,CTSH,DASH,DDOG,DLTR,DXCM,EA,EXC,FANG,FAST,FTNT,GEHC,GFS,GILD,GOOG,GOOGL,HON,IDXX,ILMN,INTC,INTU,ISRG,KDP,KHC,KLAC,LIN,LRCX,LULU,MAR,MCHP,MDB,MDLZ,MELI,META,MNST,MRNA,MRVL,MSFT,MU,NFLX,NVDA,NXPI,ODFL,ON,ORLY,PANW,PAYX,PCAR,PDD,PEP,PYPL,QCOM,REGN,ROP,ROST,SBUX,SNPS,TEAM,TMUS,TSLA,TTD,TTWO,TXN,VRSK,VRTX,WBA,WBD,WDAY,XEL,ZS"
echo $US100Components

# Convert the string into an array
# /Users/tp_mini/Desktop/IB/US100_mr.sh
IFS=',' read -r -a array <<< "$US100Components"

for item in "${array[@]}"; do
    # echo "Processing item: $item"
    python3 /Users/tp_mini/Desktop/IB/mr.py $item
    # You can perform any action on $item here
done