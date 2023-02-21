import streamlit as st
from revChatGPT.V1 import Chatbot
import requests
import json


def get_text(query_url):

    url = "https://api.diffbot.com/v3/article?url="+query_url+"&token=032f956e21895ee00941315009d62c45"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    data = json.loads(response.text)

    page_text = data['objects'][0]['text']
    return page_text



def get_pitch(page_text):
    chatbot = Chatbot(config={
      "email": "daniel.tynski@gmail.com",
      "password": "Nicksk8es"
    })


    prev_text = ""
    for data in chatbot.ask(
        '''
    Provide a list of bullet points, which encompass the main ideas in the following article, which has been extracted from a web page.  
    Your response should read as a list of the most interesting bullet points, with an emphasis on newsworthy information, which can be found in the following example:

    Example: 

    {0}
        '''.format(page_text),

    ):
        message = data["message"][len(prev_text) :]
        print(message, end="", flush=True)
        prev_text = data["message"]

    print("/n/n/n/ The final pitch /n/n/n")
    for data in chatbot.ask(
        '''
    Using the previous summary you created, please formulate a pitch i the form of an email, to a writer for the new york times, 
    who has covered similar types of stories in the past.  Write a compelling pitch that gives the writer interesting and newsworthy
    data points gleaned from the story summary you wrote previously.  Try to make the pitch personalized to the writer, who we know
    to be a writer who has covered similar topics and themes in the past.  Make the response the format of an email.  Please remember this is 
    not a pitch endorsing any product or service, it is simply an effort to get a writer to write a story about the interesting information contained inour article.

    {0}
        '''.format(page_text),

    ):
        message = data["message"][len(prev_text) :]
        print(message, end="", flush=True)
        prev_text = data["message"]

    return prev_text


form = st.form(key='my_form')
url = form.text_input(label='Enter Article URL')
submit_button = form.form_submit_button(label='Submit')


if submit_button:
	page_text = get_text(url)
	final_pitch = get_pitch(page_text)
	st.write(f'{final_pitch}')