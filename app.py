import openai
import streamlit as st
from PIL import Image
import os
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Mentsea Chatbot", page_icon=":robot:")

openai.api_key = st.secrets["openai_secret_key"]
# # And the root-level secrets are also accessible as environment variables:
# os.environ["openai_secret_key"] == st.secrets["openai_secret_key"]

page_bg = f"""
<style>
[data-testid="stSidebar"] {{
background-color:#EFEFE8;

}}

[data-testid="stToolbar"] {{
background-color:#FCFCFC;

}}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)
 
# Sidebar contents
with st.sidebar:
    # st.title('Beshie')

    image = Image.open('mentsea logo.png')
    st.image(image)
    st.markdown("<h1 style='text-align: left;> About </h1>", unsafe_allow_html= True)
    st.markdown("""
    <p style='text-align: left;'> Meet Mentsea, your friendly mental health chatbot for Southeast Asian Countries! Whether you're feeling down, anxious, or stressed, 
    Mentsea is here to help you navigate through your emotions and provide you with the guidance you need to feel better.
    With Mentsea, you can talk about your mental health concerns in a comfortable way, 
    using your national language slangs.  So don't hesitate to chat with Mentsea anytime, anywhere! </p>
    """, unsafe_allow_html=True)
    
    add_vertical_space(2)
    option = st.selectbox('Tell me where SEA countries you are located with:',
                          ('Philippines', 'Indonesia', 'Singapore', 'Malaysia',
                           'Thailand', 'Vietnam'), label_visibility="visible")

    if option == 'Philippines':
        word = 'Tagalog'
    elif  option == 'Indonesia':
        word = 'Indonesian'
    elif option == 'Singapore':
        word = 'Singaporean Mandarin'
    elif option == 'Malaysia':
        word = 'Malay'
    elif option == 'Thailand':
        word = 'Thai'
    elif option == 'Vietnam':
        word = 'Vietnamese'
    

    add_vertical_space(5)
    st.markdown("<p> Made with ❤️ by <a href='https://omaresguerra.github.io'>Omar Esguerra</a> </p>", unsafe_allow_html=True)



# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['Hello I am Mentsea, how may I help you?']
## past stores User's questions

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Layout of input/response containers
response_container = st.container()
input_container = st.container()


# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

# Clear input text
def clear_text():
    st.session_state["input"] = ""


## Applying the user input box
with input_container:
    user_input = get_text()
    st.button("Clear Text", on_click=clear_text)

messages = [{"role": "system", "content": "You are a friendly psychologist, providing an individual with guidance and advice on managing emotions, stress, anxiety, \
            and other mental health issues. You should use your knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods \
            in order to create strategies that the individual can implement in order to improve their overall wellbeing. Only respond for those queries related to mental health. \
            Make your responses friendly and include a one comforting " + word + " word with a beautiful meaning and emojis in your response."}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature=0,
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply


## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = CustomChatGPT(user_input)
        if len(st.session_state['past']) == 0:
             st.session_state.past.append('Location: '+ option)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    
    if (st.session_state['generated']):
        if (len(st.session_state['past']) == 0):
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["generated"][i], key=str(i))
        else:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))


 
