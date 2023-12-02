from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Dict, Any, List
import pymysql
from sqlalchemy.dialects import registry

# Register the MySQL dialect with SQLAlchemy
registry.register("mysql", "sqlalchemy.dialects.mysql.mysqldb", "MySQLDialect_mysqldb")

class ActionGetStockInfo(Action):

    def name(self) -> Text:
        return "action_get_stock_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_name = tracker.get_slot('stock_name')

        # MySQL 데이터베이스 접속
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='0623',
                                     db='RASA',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_stock = f"SELECT * FROM Info_Stock WHERE name='{stock_name}'"

                print(f"SQL Query - Stock: {sql_stock}")
                cursor.execute(sql_stock)
                stock_info = cursor.fetchone()
                print(f"Stock Info: {stock_info}")

                if stock_info is not None:
                    dispatcher.utter_message(text=f"Stocks: {stock_info['name']}\n"
                                                  f"Recent price: {stock_info['recent_price'] * 1350 }₩\n"
                                                  f"Opening price: {stock_info['opening_price'] * 1350 }₩\n"
                                                  f"Closing price: {stock_info['closing_price'] * 1350 }₩\n"
                                                  f"Fluctuation rate: {stock_info['fluctuation_price']}")
                else :
                    dispatcher.utter_message(text=f"Stocks: {stock_name}\n"
                                                  f"Recent price: 0₩\n"
                                                  f"Opening price: 0₩\n"
                                                  f"Closing price: 0₩\n"
                                                  f"Fluctuation rate: 0%")

        finally:
            connection.close()

        return []
    
class ActionGetStockNews(Action):

    def name(self) -> Text:
        return "action_get_stock_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_name = tracker.get_slot('stock_name')

        # MySQL 데이터베이스 접속
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='0623',
                                     db='RASA',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_news = f"SELECT * FROM Info_news WHERE stock_name='{stock_name}'"

                cursor.execute(sql_news)
                news_info = cursor.fetchone()
                
                if news_info is not None:
                    dispatcher.utter_message(text=f"Headline: {news_info['Headline']}\n"
                                                  f"Link: {news_info['Link']}")
                else :
                    dispatcher.utter_message(text=f"Headline: None\n"
                                                  f"Link: None")

        finally:
            connection.close()

        return []
    
class ActionGetStockAnalysis(Action):

    def name(self) -> Text:
        return "action_get_stock_analysis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_name = tracker.get_slot('stock_name')

        # MySQL 데이터베이스 접속
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='0623',
                                     db='RASA',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_analysis = f"SELECT * FROM Info_analysis WHERE stock_name='{stock_name}'"
                    

                cursor.execute(sql_analysis)
                analysis_info = cursor.fetchone()

                if analysis_info is not None:
                    dispatcher.utter_message(text=f"Technical analysis: {analysis_info['Technical_analysis']}\n"
                                                  f"Outlook: {analysis_info['Outlook']}")
                else :
                    dispatcher.utter_message(text=f"Technical analysis: None\n"
                                                  f"Outlook: None")

        finally:
            connection.close()

        return []

