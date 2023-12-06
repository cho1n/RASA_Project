from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Dict, Any, List
import pymysql
from sqlalchemy.dialects import registry
from rasa_sdk.events import SlotSet
recommendStock, rememberName, email, conceptName, userStock = None, None, None, None, None

# Register the MySQL dialect with SQLAlchemy
registry.register("mysql", "sqlalchemy.dialects.mysql.mysqldb", "MySQLDialect_mysqldb")
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
                                                  f"Market Cap: {stock_info['market_cap'] * 1350 }₩\n"
                                                  f"Transfer Amount: {stock_info['Transfer_amount']}\n"
                                                  f"Fluctuation rate: {stock_info['fluctuation_price']}")
                else :
                    dispatcher.utter_message(text=f"I'm sorry. I don't have any information about {stock_name}.")

        finally:
            connection.close()

        return []

class ActionGetAllStocks(Action):

    def name(self) -> Text:
        return "action_get_all_stocks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_stock = "SELECT name FROM Info_Stock"
                cursor.execute(sql_stock)
                stocks_info = cursor.fetchall()

                if stocks_info:
                    stock_names = [stock['name'] for stock in stocks_info]
                    stock_names_str = ", ".join(stock_names)
                    dispatcher.utter_message(text=f"Sure! Here are the stock names: {stock_names_str}\n"
                                                    f"Do you need a more help ?")

        finally:
            connection.close()

        return []
    
class ActionGetAllConcepts(Action):

    def name(self) -> Text:
        return "action_get_all_concepts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_concept = "SELECT concept_name FROM stock_concept"
                cursor.execute(sql_concept)
                concept_info = cursor.fetchall()

                if concept_info:
                    concept_names = [concept['concept_name'] for concept in concept_info]
                    stock_names_str = ", ".join(concept_names)
                    dispatcher.utter_message(text=f"Here are the concept List: {stock_names_str}\n"
                                                    f"Do you need a more help ?")
                                             

        finally:
            connection.close()

        return []
    
class ActionGetConceptLink(Action):

    def name(self) -> Text:
        return "action_get_concept_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global conceptName
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_concept = f"SELECT concept_link FROM stock_concept WHERE concept_name='{conceptName}'"
                cursor.execute(sql_concept)
                concept_info = cursor.fetchall()

                if concept_info:
                    concept_link = concept_info[0]['concept_link']  # Assuming concept_info is a list of dictionaries
                    dispatcher.utter_message(text=f"Sure! I will give you more concept information: {concept_link}\n"
                                                  f"Please check this link. It has more information for you.\n"
                                                  f"Do you need more help?")

        finally:
            connection.close()

        return []

class ActionGetConceptContent(Action):

    def name(self) -> Text:
        return "action_get_concept_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global conceptName
        conceptName = next(tracker.get_latest_entity_values("conceptName"), None)
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_concept = f"SELECT concept_content FROM Stock_concept WHERE concept_name='{conceptName}'"
                cursor.execute(sql_concept)
                concept_info = cursor.fetchall()

                if concept_info:
                    concept_content = concept_info[0]['concept_content']  # Assuming concept_info is a list of dictionaries
                    dispatcher.utter_message(text=f"Sure! Here is the concept Content for you\n"
                                                  f"{conceptName}: {concept_content}\n"
                                                  f"Do you need more help?")


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
                    dispatcher.utter_message(text=f"Here is the analysis you want.\n"
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
        global rememberName, userStock
        rememberName = next(tracker.get_latest_entity_values("rememberName"), None)
        user_name = rememberName
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
                    WHERE User.name='{rememberName}'
                """
                cursor.execute(sql_user)
                user_info = cursor.fetchone()

                if user_info is not None:
                    user_name = user_info['name']
                    stock_name = user_info['stock_name']
                    stock_recent_price = user_info['recent_price']
                    stock_opening_price = user_info['opening_price']
                    stock_closing_price = user_info['closing_price']
                    stock_fluctuation_price = user_info['fluctuation_price']
                    stock_market_cap = user_info['market_cap']
                    stock_transfer_amount = user_info['Transfer_amount']

                    dispatcher.utter_message(text=f"Welcome {user_name} .\n"
                                                  f"Here is your interest Stock: {stock_name}.\n"
                                                  f"Recent Price of your interest Stock: {stock_recent_price * 1350} ₩\n"
                                                  f"Opening Price of your interest Stock: {stock_opening_price * 1350} ₩\n"
                                                  f"Closing Price of your interest Stock: {stock_closing_price * 1350} ₩\n"
                                                  f"Fluctuation Price of interest Stock: {stock_fluctuation_price}.\n"
                                                  f"Market Cap: {stock_market_cap * 1350 }₩\n"
                                                  f"Transfer Amount: {stock_transfer_amount}.\n"
                                                  f"Do you want to know about recommend stock ?")
                    rememberName = user_name
                    userStock = stock_name
                else :
                    dispatcher.utter_message(text=f"I'm sorry. {user_name}, you are not registered. Please sign up first.")

        finally:
            connection.close()

        return []

class ActionPutUserInfo(Action):

    def name(self) -> Text:
        return "action_put_user_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global rememberName, userStock
        rememberName = next(tracker.get_latest_entity_values("rememberName"), None)
        userStock = next(tracker.get_latest_entity_values("userStock"), None)

        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_user = f"SELECT * FROM User WHERE name='{rememberName}'"
                cursor.execute(sql_user)
                user_info = cursor.fetchone()

                if user_info is None:
                    sql_insert = f"INSERT INTO User (name, stock_name) VALUES ('{rememberName}', '{userStock}')"
                    cursor.execute(sql_insert)
                    connection.commit()

                    dispatcher.utter_message(text=f"Welcome {rememberName} .\n"
                                                  f"your interest Stock is : {userStock}.\n"
                                                  f"Do you need a more help ?")
                    rememberName = rememberName
                    userStock = userStock
        finally:
            connection.close()

        return []

class ActionGetRecommendStock(Action):

    def name(self) -> Text:
        return "action_get_recommend_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global recommendStock
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_stock = f"SELECT * FROM Info_Stock ORDER BY (market_cap / recent_price) DESC LIMIT 1;"
                cursor.execute(sql_stock)
                stock_info = cursor.fetchone()

                if stock_info is not None:
                    dispatcher.utter_message(text=f"Sure! Here is the Recommend Stock.\n"
                                                  f"The standard for this is set to PER.\n"
                                                  f"PER is the current stock price relative to the market cap.\n"
                                                  f"Stocks: {stock_info['name']}\n"
                                                  f"Recent price: {stock_info['recent_price'] * 1350 }₩\n"
                                                  f"Opening price: {stock_info['opening_price'] * 1350 }₩\n"
                                                  f"Closing price: {stock_info['closing_price'] * 1350 }₩\n"
                                                  f"Market Cap: {stock_info['market_cap'] * 1350 }₩\n"
                                                  f"Transfer Amount: {stock_info['Transfer_amount']}.\n"
                                                  f"Fluctuation rate: {stock_info['fluctuation_price']}.\n"
                                                  f"Do you want to update your interest stock for recommend stock ?"
                                                  )
                    recommendStock = stock_info['name']
                else :
                    dispatcher.utter_message(text=f"First, Ask me the recommended stock. If you did it already. I'm sorry. Today nothing to recommend.")

        finally:
            connection.close()

        return []
    
class ActionGetNotRecommendStock(Action):

    def name(self) -> Text:
        return "action_get_not_recommend_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_stock = f"SELECT * FROM Info_Stock ORDER BY (market_cap / recent_price) ASC LIMIT 1;"
                cursor.execute(sql_stock)
                stock_info = cursor.fetchone()

                if stock_info is not None:
                    dispatcher.utter_message(text=f"Sure! Here is the Not Recommend Stock.\n"
                                                  f"The standard for this is set to PER.\n"
                                                  f"PER is the current stock price relative to the market cap.\n"
                                                  f"This stock have a least PER.\n"
                                                  f"Stocks: {stock_info['name']}\n"
                                                  f"Recent price: {stock_info['recent_price'] * 1350 }₩\n"
                                                  f"Opening price: {stock_info['opening_price'] * 1350 }₩\n"
                                                  f"Closing price: {stock_info['closing_price'] * 1350 }₩\n"
                                                  f"Market Cap: {stock_info['market_cap'] * 1350 }₩\n"
                                                  f"Transfer Amount: {stock_info['Transfer_amount']}.\n"
                                                  f"Fluctuation rate: {stock_info['fluctuation_price']}")
                else :
                    dispatcher.utter_message(text=f"Great news. Today I don't have any not recommend stock")
        finally:
            connection.close()

        return []
        
class ActionGetRecommendStockNews(Action):

    def name(self) -> Text:
        return "action_get_recommend_stock_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global recommendStock

        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_news = f"SELECT * FROM Info_news WHERE stock_name='{recommendStock}'"

                cursor.execute(sql_news)
                news_info = cursor.fetchone()
                
                
                if news_info is not None:
                    dispatcher.utter_message(text=f"This is the news you want.\n"
                                                  f"Headline: {news_info['Headline']}\n"
                                                  f"Link: {news_info['Link']}")
                else :
                    dispatcher.utter_message(text=f"First, Ask me the recommended stock. If you did it already. I'm sorry. I don't have any news about that.")

        finally:
            connection.close()

        return []

class ActionGetRecommendStockAnalysis(Action):

    def name(self) -> Text:
        return "action_get_recommend_stock_analysis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global recommendStock
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql_analysis = f"SELECT * FROM Info_analysis WHERE stock_name='{recommendStock}'"
                cursor.execute(sql_analysis)
                analysis_info = cursor.fetchone()
            
                if analysis_info is not None:
                    dispatcher.utter_message(text=f"Here is the analysis you want.\n"
                                                  f"Stocks: {analysis_info['stock_name']}\n"
                                                  f"Technical analysis: {analysis_info['Technical_analysis']}\n"
                                                  f"Outlook: {analysis_info['Outlook']}")
                else :
                    dispatcher.utter_message(text=f"First, Ask me the recommended stock. If you did it already. I'm sorry. I don't have any analysis about that.")

        finally:
            connection.close()

        return []
        
class UpdateRecommendStock(Action):

    def name(self) -> Text:
        return "action_update_recommend_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global recommendStock, rememberName

        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                if rememberName is not None:
                    sql_update_stock = f"UPDATE User SET stock_name = '{recommendStock}' WHERE name = '{rememberName}';"
                    cursor.execute(sql_update_stock)
                    connection.commit()
                    dispatcher.utter_message(text=f"Sure, {rememberName} Your interest stock has been updated ! \n"
                                                  f"Than, Your interest Stock is : {recommendStock}.\n"
                                                  f"Do you need a more help ?"
                                             )
                else:
                    dispatcher.utter_message(text=f"Please sign up first.")
        finally:
            connection.close()

        return []
    
class UpdateMyStock(Action):

    def name(self) -> Text:
        return "action_update_my_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userStock, rememberName
        userStock = next(tracker.get_latest_entity_values("userStock"), None)
        print(rememberName)

        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                if rememberName is not None:
                    sql_update_stock = f"UPDATE User SET stock_name = '{userStock}' WHERE name = '{rememberName}';"
                    cursor.execute(sql_update_stock)
                    connection.commit()
                    dispatcher.utter_message(text=f"Sure, {rememberName} Your interest stock has been updated !\n"
                                                  f"Than, Your interest Stock is : {userStock}.\n"
                                                  f"Do you need a more help ?"
                                             )
                else:
                    dispatcher.utter_message(text=f"Please sign up first.")
        finally:
            connection.close()

        return []

class ActionGetMyStockAnalysis(Action):

    def name(self) -> Text:
        return "action_get_my_stock_analysis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userStock, rememberName
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_analysis = f"SELECT * FROM Info_analysis WHERE stock_name='{userStock}'"
                cursor.execute(sql_analysis)
                analysis_info = cursor.fetchone()

                if analysis_info is not None and rememberName is not None:
                    dispatcher.utter_message(text=f"Of course! Here is the analysis your interest stock.\n"
                                                  f"Technical analysis: {analysis_info['Technical_analysis']}\n"
                                                  f"Outlook: {analysis_info['Outlook']}")
                else :
                    dispatcher.utter_message(text=f"Please Log in first. If you already Log in. Then, I'm sorry. I don't have any analysis about that.")

        finally:
            connection.close()

        return []

class ActionGetMyStockInfo(Action):

    def name(self) -> Text:
        return "action_get_my_stock_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userStock, rememberName
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_analysis = f"SELECT * FROM Info_stock WHERE name='{userStock}'"
                cursor.execute(sql_analysis)
                stock_info = cursor.fetchone()

                if stock_info is not None and rememberName is not None:
                    dispatcher.utter_message(text=f"Yes! Here is the info your interest stock.\n"
                                                  f"Stocks: {stock_info['name']}\n"
                                                  f"Recent price: {stock_info['recent_price'] * 1350 }₩\n"
                                                  f"Opening price: {stock_info['opening_price'] * 1350 }₩\n"
                                                  f"Closing price: {stock_info['closing_price'] * 1350 }₩\n"
                                                  f"Market Cap: {stock_info['market_cap'] * 1350 }₩\n"
                                                  f"Fluctuation rate: {stock_info['fluctuation_price']}")
                else :
                    dispatcher.utter_message(text=f"Please Log in first. If you already Log in. Then, I'm sorry. I don't have any analysis about that.")

        finally:
            connection.close()

        return []

class ActionGetMyStockNews(Action):

    def name(self) -> Text:
        return "action_get_my_stock_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global userStock, rememberName

        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_news = f"SELECT * FROM Info_news WHERE stock_name='{userStock}'"
                cursor.execute(sql_news)
                news_info = cursor.fetchone()

                if news_info is not None and rememberName is not None:
                    dispatcher.utter_message(text=f"Sure! Here is the news you want.\n"
                                                  f"Headline: {news_info['Headline']}\n"
                                                  f"Link: {news_info['Link']}")
                else :
                    dispatcher.utter_message(text=f"Please Log in first. If you already Log in. Then, I'm sorry. I don't have any news about that.")

        finally:
            connection.close()

        return []
    
class ActionGetEmail(Action):

    def name(self) -> Text:
        return "action_get_email_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global email, rememberName
        email = next(tracker.get_latest_entity_values("email"), None)

        if email is not None :
            dispatcher.utter_message(text=f"Perfect! Here is your email: {email}.\n"
                                          f"I will send you the information every friday.\n")
        else :
            dispatcher.utter_message(text=f"Please input your email.")

        return []
    
class ActionGetHottestStock(Action):

    def name(self) -> Text:
        return "action_get_hottest_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='0623',
                             db='RASA',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                sql_stock = f"SELECT * FROM Info_Stock ORDER BY Transfer_amount DESC LIMIT 1;"
                cursor.execute(sql_stock)
                stock_info = cursor.fetchone()

                if stock_info is not None:
                    dispatcher.utter_message(text=f"This is the Hottest Stock.\n"
                                                  f"This stock have a large Transfer amount today.\n"
                                                  f"Stocks: {stock_info['name']}\n"
                                                  f"Recent price: {stock_info['recent_price'] * 1350 }₩\n"
                                                  f"Opening price: {stock_info['opening_price'] * 1350 }₩\n"
                                                  f"Closing price: {stock_info['closing_price'] * 1350 }₩\n"
                                                  f"Market Cap: {stock_info['market_cap'] * 1350 }₩\n"
                                                  f"Transfer Amount: {stock_info['Transfer_amount']}.\n"
                                                  f"Fluctuation rate: {stock_info['fluctuation_price']}")
                else :
                    dispatcher.utter_message(text=f"Bad news. Today nothing to recommend.")
        finally:
            connection.close()

        return []