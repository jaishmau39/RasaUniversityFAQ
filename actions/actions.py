# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from datetime import date
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#

# Python program to read an excel file

import pandas as pd
import csv
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from gensim.parsing.preprocessing import preprocess_string
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.parsing.preprocessing import preprocess_documents
from facebook_scraper import get_posts

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionAdmissionInfo(Action):

    def name(self) -> Text:
        return "action_admission_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        str((tracker.latest_message)['text'])
        dispatcher.utter_message(template="utter_admission_info")

        return []

class DisplayUpcomingHolidays(Action):

    def name(self) -> Text:
        return "display_upcoming_holidays"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        today = date.today()
        print("Today's date:", today)
        this_month = today.strftime("%m")
        df2 = pd.read_excel(r'Calender_2022.xlsx')
        df2['Date'] = pd.to_datetime(df2['Date'])
        current_month_df = df2[df2['Date'].dt.month == int(this_month)]
        content = 'Total of ' + str(current_month_df.shape[0]) + ' this month\n\n'
        for i in range(current_month_df.shape[0]):
            content = content + str(current_month_df['Date'].values[i])[:10] + '  -  ' + str(
                current_month_df['Holiday Description'].values[i]) + '\n'

        dispatcher.utter_message(text=content)

        return []

class ActionAdmissionInfo(Action):

    def name(self) -> Text:
        return "action_campus_facilities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/campus-life"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_campus_facilities", tracker, link=Link)
        return []

class ActionLatestEvents(Action):

    def name(self) -> Text:
        return "action_latest_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="What cuisine?")

        listposts = []
        for post in get_posts("lakeheaduniversity", pages=4):
            listposts.append(post)

        df = pd.DataFrame(listposts)
        df.dropna(subset=["text"], inplace=True)
        text_corpus = df['text'].values
        processed_corpus = preprocess_documents(text_corpus)
        tagged_corpus = [TaggedDocument(d, [i]) for i, d in enumerate(processed_corpus)]
        model = Doc2Vec(tagged_corpus, dm=0, vector_size=200, window=2, min_count=1, epochs=100, hs=1)

        # get last user message
        userMessage = tracker.get_slot("latest_event")
        # userMessage = tracker.latest_message['text']
        # find matching posts
        new_doc = preprocess_string(userMessage)
        test_doc_vector = model.infer_vector(new_doc)
        sims = model.docvecs.most_similar(positive=[test_doc_vector])
        # get the top 5 matches
        posts = [df['text'].iloc[s[0]] for s in sims[:5]]
        # send the bot answer to the user
        botResponse = f"These are the latest events from Lakehead University: {posts}.".replace('[', '').replace(']', '')
        dispatcher.utter_message(text=botResponse)
        return []

# -------

class ActionSearchProffInfo(Action):

    def name(self) -> Text:
        return "action_search_proff_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:



        #person = self.from_entity(entity="PERSON")
        person = tracker.get_slot("proff_full_name")
        # print(person)
        df3 = pd.read_csv(r'cs_faculty.csv')
        df_email = df3['email'][df3['name'] == person]
        email_info = str(df_email.values)
        email_info = email_info.replace("[", "")
        email_info = email_info.replace("]", "")
        email_info = email_info.replace("'", "")
        email_info = email_info.replace("'", "")


        dispatcher.utter_message(text=email_info)
        # print(df3.loc[person]['email'])

        # with open('cs_faculty.csv', 'r') as file:
        #     reader = csv.reader(file)
        #
        #     # get a list of universities in the desired location
        #
        #     output = [row for row in reader if row['name'] == proff_name]
        #
        #     if output:
        #
        #         reply = f"This is the information found on the {proff_name}:"
        #
        #         reply += "\n- " + "\n- ".join([item['email'] for item in output])
        #
        #         # utter the message
        #
        #         dispatcher.utter_message(reply)
        #
        #     else:  # the list is empty
        #
        #         dispatcher.utter_message(f"I could not find any information on {proff_name}")

        return []


class ActionFindProffName(Action):

    def name(self) -> Text:
        return "action_find_prof_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = tracker.get_slot("topic")
        print(topic)
        # query = {"expertise": {"$regex": topic}}
        # mydoc = myCol.find(query, {"_id": 0, "name": 1, "expertise": 1, "phone": 1, "about": 1}).limit(3)
        #
        # for x in mydoc:
        #     dispatcher.utter_message(text=f"Here what I have found: \n {x}")

        return []

class ActionAdmissionRequirements(Action):

    def name(self) -> Text:
        return "action_admission_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/admissions"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_admission_requirements", tracker, link=Link)
        return []