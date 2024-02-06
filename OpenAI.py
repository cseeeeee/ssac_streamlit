import streamlit as st
import os 
from openai import OpenAI

os.environ['OPENAPI_API_KEY']= st.secrets['api_key']
st.title('이미지 생성기 입니다.')

with st.form("form"):
  #입력받는 곳
  user_input=st.text_input("그리고 싶은 그림은?")
  size=st.selectbox("size",['1024x1024','512x512','256x256'])
  submit=st.form_submit_button("submit")

if submit and user_input:
  gpt_prompt=[{
    ###role과 content는 고정
    "role":"system",  #만드는 llm에 역할을 줌 / 그 외: user, assistant
    "content":"Imagine the detail appeareance of the input.Response it shortly around 15 words",
  }]


  ###user_input을 따로 넣어주려고 append로 빼놓은거래
  gpt_prompt.append({
    "role":"user",
    "content": user_input
  })

  client = OpenAI()
  with st.spinner("Waiting for Chatgpt..."):
    gpt_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=gpt_prompt
    )

  dalle_prompt=gpt_response.choices[0].message.content
  st.write('dall-e prompt',dalle_prompt)
  with st.spinner("Waiting for Dall-e..."):
    dalle_response=client.images.generate(
      model="dall-e-2",
      prompt=dalle_prompt,
      size='1024x1024'
    )

    st.image(dalle_response.data[0].url)