from ibapi.common import TagValueList, TickerId
from ibapi.contract import Contract, ContractDetails
from ibapi.client import EClient
from ibapi.common import BarData, TickerId
from ibapi.order_state import OrderState
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
from time import sleep
import pandas as pd
import sys

class IBapi(EWrapper, EClient):
    def __init__(self, symbol):
        EClient.__init__(self, self)
        self.df = [[], []]
        self.symbol = symbol
        self.minute1 = -1
        self.minute2 = -1
        self.currentbars1 = 0
        self.currentbars2 = 0
        self.barChecker = 0
        self.count = 0
        self.current_price = -1
        self.req_id_to_contract = {}
    def nextValidId(self, orderId: TickerId):
        con = Contract()
        con.symbol = "AAPL"
        con.secType = "STK"
        con.exchange = "SMART"
        con.currency = "USD"

        self.reqContractDetails(orderId, con)

    def contractDetails(self, reqId: TickerId, contractDetails: ContractDetails):
        print(contractDetails.contract)

        order = Order()
        order.orderId = reqId
        order.action = "BUY"
        # order.orderType = "MKT"
        order.account = "U11933889"
        order.orderType = "LMT"
        order.lmtPrice = 200
        order.totalQuantity = 10
        order.eTradeOnly = False
        order.firmQuoteOnly = False
        self.placeOrder(reqId, contractDetails.contract, order)
    
    def openOrder(self, orderId: TickerId, contract: Contract, order: Order, orderState: OrderState):
        print(f'orderid: {orderId}, contract: {contract}, order: {order}')
if __name__ == "__main__":
    def run_loop():
        app.run()
    if len(sys.argv) > 2:
        symbol = sys.argv[1]
        clientId = sys.argv[2]
        print(symbol)
        app = IBapi(symbol=symbol)
        app.connect('127.0.0.1', 7496, int(clientId))
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        sleep(1)
        reqID = 1
    else:
        print('sys argv <= 2')