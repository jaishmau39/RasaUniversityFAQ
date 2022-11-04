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
import numpy as np
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
        print(person)
        df3 = pd.read_csv(r'cs_faculty.csv', encoding='latin1')
        df_email = df3['email'][df3['name'] == person]
        email_info = str(df_email.values)
        email_info = email_info.replace("[", "")
        email_info = email_info.replace("]", "")
        email_info = email_info.replace("'", "")
        email_info = email_info.replace("'", "")
        print(email_info)

        dispatcher.utter_message(text=email_info)


        return []


class ActionFindProffName(Action):

    def name(self) -> Text:
        return "action_find_prof_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = tracker.get_slot("topic")
        topic1 = str(topic).lower()
        print(topic)
        print(topic1)

        df4 = pd.read_csv(r'cs_faculty.csv', encoding='latin1').apply(lambda x: x.astype(str).str.lower())
        # df_name = df4[df4["research areas"].dropna().str.contains(topic1)]['name'].values
        df_name = df4[df4["research areas"].dropna().str.contains(topic1)]['name']
        df_name = str(df_name.values)
        df_name = df_name.replace("'", "")
        df_name = df_name.replace("'", "")


        dispatcher.utter_message(text=df_name)
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

class ActionIeltsRequirements(Action):

    def name(self) -> Text:
        return "action_ielts_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/english-language-proficiency-requirements"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_ielts_requirements", tracker, link=Link)
        return []
class ActionAdmissionDeadline(Action):

    def name(self) -> Text:
        return "action_admission_deadline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program_intake = tracker.get_slot("program_intake")
        program_intake1 = str(program_intake).lower()
        print(program_intake1)

        df5 = pd.read_csv(r'ApplicationDeadlines.csv', encoding='latin1').apply(lambda x: x.astype(str).str.lower())
        df_deadline = df5[df5["Admission Deadlines"].dropna().str.contains(program_intake1)]['Dates']
        df_deadline = str(df_deadline.values)
        # df_name = df_name.replace("'", "")
        # df_name = df_name.replace("'", "")
        dispatcher.utter_message(text=df_deadline)

        if(program_intake1 == "audition"):
            Link = "https://www.lakeheadu.ca/studentcentral/applying/application-details-for-media-studies-and-music-applicants"
            str((tracker.latest_message)['text'])
            dispatcher.utter_template("utter_media_music", tracker, link=Link)


        return []

class ActionAlternateOffers(Action):

    def name(self) -> Text:
        return "action_alternate_offers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/alternate-offers-"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_alternate_offers", tracker, link=Link)
        return []

class ActionStudyPermit(Action):

    def name(self) -> Text:
        return "action_study_permit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/international/current/immigration#study"
        Link2 = "https://www.lakeheadu.ca/international/newly-accepted/immigration"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_study_permit", tracker, link=Link, link2=Link2)
        # Link2 = "https://www.lakeheadu.ca/international/newly-accepted/immigration"
        # str((tracker.latest_message)['text'])
        # dispatcher.utter_template("utter_study_permit", tracker, link2=Link2)
        return []