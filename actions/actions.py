# This files contains all the custom actions which is needed by some stories.

from datetime import date
from typing import Any, Text, Dict, List
import db
db_conn = db.Repo()

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from gensim.parsing.preprocessing import preprocess_string
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.parsing.preprocessing import preprocess_documents
from facebook_scraper import get_posts

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

class ActionSearchFacebook(Action):

    def name(self) -> Text:
        return "action_search_facebook"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
        userMessage = tracker.get_slot("search_term")
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

class ActionSearchProffInfo(Action):

    def name(self) -> Text:
        return "action_search_proff_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
        try:
            df5 = pd.read_csv(r'ApplicationDeadlines.csv', encoding='latin1').apply(lambda x: x.astype(str).str.lower())
            df_deadline = df5[df5["Admission Deadlines"].dropna().str.contains(program_intake1)]['Dates']
            df_deadline = str(df_deadline.values)
            dispatcher.utter_message(text=df_deadline)
        except Exception as e:
            print(e)
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
        return []

class ActionInternationalServices(Action):

    def name(self) -> Text:
        return "action_international_student_services"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/international/current/immigration"
        Link2 = "https://www.lakeheadu.ca/international/current/appointments"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_international_student_services", tracker, link=Link, link2=Link2)
        return []

class ActionApplicationSteps(Action):

    def name(self) -> Text:
        return "action_application_steps"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/general-information-about-applying"
        Link2 = "https://www.lakeheadu.ca/studentcentral/applying/applying-to-lakehead"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_application_steps", tracker, link=Link, link2=Link2)
        return []

class ActionBachelorsApplication(Action):

    def name(self) -> Text:
        return "action_bachelors_application_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.ouac.on.ca/"
        Link2 = "https://www.ouac.on.ca/apply/lakeheadugrad/en_CA/user/login"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_bachelors_application_link", tracker, link=Link, link2=Link2)
        return []

class ActionGraduateApplication(Action):

    def name(self) -> Text:
        return "action_graduate_application_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/admissions/how-to-apply/applying-to-graduate-studies"
        Link2 = "https://www.ouac.on.ca/apply/lakeheadugrad/en_CA/user/login"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_graduate_application_link", tracker, link=Link, link2=Link2)
        return []

class ActionSaveFeedback(Action):

    def name(self) -> Text:
        return "action_save_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db_conn.insert(tracker.get_slot('user_first_name'), tracker.get_slot('user_last_name'), tracker.get_slot('feedback'))
        dispatcher.utter_message(response="utter_feedback_slots")
        return []

class ActionKeepTab(Action):

    def name(self) -> Text:
        return "action_keep_tab"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/next-steps"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_keep_tab", tracker, link=Link)
        return []

class ActionAdmissionDecisionTimeline(Action):

    def name(self) -> Text:
        return "action_admission_decision_timeline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/admission-decision-timelines"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_admission_decision_timeline", tracker, link=Link)
        return []

class ActionmyInfo(Action):

    def name(self) -> Text:
        return "action_myinfo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/faculty-and-staff/departments/services/helpdesk/portals/myinfo"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_myInfo", tracker, link=Link)
        return []

class ActionPasswordTroubleshoot(Action):

    def name(self) -> Text:
        return "action_password_troubleshoot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/myinfo-troubleshooting"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_password_troubleshoot", tracker, link=Link)
        return []

class ActionAcceptAdmission(Action):

    def name(self) -> Text:
        return "action_accept_admission"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/checklist"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_accept_admission", tracker, link=Link)
        return []

class ActionConfirmationDeposit(Action):

    def name(self) -> Text:
        return "action_confirmation_deposit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/checklist"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_confirmation_deposit", tracker, link=Link)
        return []

class ActionPaymentOptions(Action):

    def name(self) -> Text:
        return "action_payment_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/students/finances/tuition-fees/paying-fees"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_payment_options", tracker, link=Link)
        return []
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_default", tracker, link=Link)
        return [UserUtteranceReverted()]

class ActionDeferAdmission(Action):

    def name(self) -> Text:
        return "action_defer_admission"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/studentcentral/applying/deferral-of-admission"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_defer_admission", tracker, link=Link)
        return []


class ActionTuitionFee(Action):

    def name(self) -> Text:
        return "action_tuition_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/admissions/newly-admitted-canadian-students/tuition-fees"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_tuition_fee", tracker, link=Link)
        return []

class ActionHousing(Action):

    def name(self) -> Text:
        return "action_housing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://www.lakeheadu.ca/campus-life/residence-dining"
        str((tracker.latest_message)['text'])
        dispatcher.utter_template("utter_housing", tracker, link=Link)
        return []