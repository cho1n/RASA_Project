from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Dict, Any, List
import pymysql
from sqlalchemy.dialects import registry

# Register the MySQL dialect with SQLAlchemy
registry.register("mysql", "sqlalchemy.dialects.mysql.mysqldb", "MySQLDialect_mysqldb")
user_stock, user_name = "", ""

class ActionGetStockInfo(Action):

    def name(self) -> Text:
        return "action_get_stock_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock_name = tracker.get_slot('stock_name')
        
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
                    dispatcher.utter_message(text=f"Sure! Here is the information you want.\n"
                                                  f"Stocks: {stock_info['name']}\n"
                                                  f"Recent price: {stock_info['recent_price'] * 1350 }₩\n"
                                                  f"Opening price: {stock_info['opening_price'] * 1350 }₩\n"
                                                  f"Closing price: {stock_info['closing_price'] * 1350 }₩\n"
                                                  f"Fluctuation rate: {stock_info['fluctuation_price']}")
                else :
                    dispatcher.utter_message(text=f"I'm sorry. I don't have any information about {stock_name}.")

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
                    dispatcher.utter_message(text=f"Sure! Here is the news you want.\n"
                                                  f"Headline: {news_info['Headline']}\n"
                                                  f"Link: {news_info['Link']}")
                else :
                    dispatcher.utter_message(text=f"I'm sorry. I don't have any news about {stock_name}.")

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
        print(stock_name)
        
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
                    dispatcher.utter_message(text=f"Sure! Here is the analysis you want.\n"
                                                  f"Technical analysis: {analysis_info['Technical_analysis']}\n"
                                                  f"Outlook: {analysis_info['Outlook']}")
                else :
                    dispatcher.utter_message(text=f"I'm sorry. I don't have any analysis about {stock_name}.")

        finally:
            connection.close()

        return []

class ActionGetUserInfo(Action):

    def name(self) -> Text:
        return "action_get_user_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot('name')

        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_user = f"""
                    SELECT User.*, info_stock.*
                    FROM User
                    LEFT JOIN info_stock ON User.stock_name = info_stock.name
                    WHERE User.name='{user_name}'
                """
                cursor.execute(sql_user)
                user_info = cursor.fetchone()

                if user_info is not None:
                    user_name = user_info['name']
                    stock_name = user_info['stock_name']
                    stock_recent_price = user_info['recent_price']
                    stock_opening_price = user_info['recent_price']
                    stock_closing_price = user_info['recent_price']
                    stock_fluctuation_price = user_info['recent_price']

                    dispatcher.utter_message(text=f"Welcome {user_name} .\n"
                                                  f"Here is your interest Stock: {stock_name}.\n"
                                                  f"Recent Price of your interest Stock: {stock_recent_price * 1350} ₩\n"
                                                  f"Opening Price of your interest Stock: {stock_opening_price * 1350} ₩\n"
                                                  f"Closing Price of your interest Stock: {stock_closing_price * 1350} ₩\n"
                                                  f"Fluctuation Price of interest Stock: {stock_fluctuation_price}.\n"
                                                  f"Do you need a more help ?")
                else :
                    dispatcher.utter_message(text=f"I'm sorry. Please sign up first.")

        finally:
            connection.close()

        return []

class ActionPutUserInfo(Action):

    def name(self) -> Text:
        return "action_put_user_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot('name')
        user_stock = tracker.get_slot('stock_name')
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_user = f"SELECT * FROM User WHERE name='{user_name}'"
                cursor.execute(sql_user)
                user_info = cursor.fetchone()

                if user_info is None:
                    sql_insert = f"INSERT INTO User (name, stock_name) VALUES ('{user_name}', '{user_stock}')"
                    cursor.execute(sql_insert)
                    connection.commit()

                    dispatcher.utter_message(text=f"Welcome {user_name} .\n"
                                                  f"your interest Stock is : {user_stock}.\n"
                                                  f"Do you need a more help ?")
        finally:
            connection.close()

        return []

