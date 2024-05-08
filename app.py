import streamlit as st
from dotenv import load_dotenv #for loading env variables

load_dotenv() 
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi  #get the transcript from youtube link

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """you are a youtube video transcript summarizer. You will be taking the 
ranscript text and summarize the entire video and then provide important summary 
within 250 words. please provide the summary here: 
"""

# to get transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]  #as the id is the links after = sign content to extract and save as video id
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id) 

        #as this is in a form of list i make a paragraph as follows
        transcript = ""
        for i in transcript_text:
            transcript += " " +i["text"]
        return transcript
    
    except Exception as e:
        raise e

# now to connect with gemini (summarising the transcript)
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

st.title("YOUTUBE Video To Summary")
youtube_link = st.text_input("Enter the YouTube Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("get Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)