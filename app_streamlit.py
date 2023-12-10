import random
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import  numpy as np


def list_letters(phrase):
    list_of_letters = [i for i in phrase]
    return list_of_letters

def generate_random_numbers(letter, span):
    
    if letter.isalpha()==False:
        if letter == ' ':
            letter_value = 0
            # Generate 8 random numbers between -10 and 10
            random_numbers = [random.randint(span[0], span[1]) for _ in range(8)]
            
            # Adjust the last number to ensure the sum is equal to 26 - the letter value
            random_numbers[-1] += (26 - letter_value - sum(random_numbers))
            
            return random_numbers
        else:
            return ['°','ﬂ','€','^','{}','¿','±','~']
    
    else:
        # Assign a value to the letter based on its position in the alphabet
        letter_value = ord(letter.lower()) - ord('a') + 1
        
        # Generate 8 random numbers between -10 and 10
        random_numbers = [random.randint(span[0], span[1]) for _ in range(8)]
        
        # Adjust the last number to ensure the sum is equal to 26 - the letter value
        random_numbers[-1] += (26 - letter_value - sum(random_numbers))
        
        return random_numbers




def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def hint_row(list_of_letters, level):
    blanks = []
    for x in list_of_letters:
        if x.isalpha()==False:
            blanks.append(x)
        else:
            blanks.append(' ')
   
    cols = [i for i in range(len(list_of_letters))]
   
    if level == 'easy':
        hint_length = int(np.round(len(list_of_letters)/2))
        list_index = random.sample(range(0, len(list_of_letters)), hint_length)
        for i,x in enumerate(list_index):
            blanks[x] = list_of_letters[list_index[i]]    
        
        hint = dict(zip(cols,blanks))
        return hint
    
    elif level == 'medium':
        hint_length = int(np.round(len(list_of_letters)/4))
        list_index = random.sample(range(0, len(list_of_letters)), hint_length)
        for i,x in enumerate(list_index):
            blanks[x] = list_of_letters[list_index[i]]
        
        hint = dict(zip(cols,blanks))
        return hint
    
    else:
        hint = dict(zip(cols,blanks))
        return hint

def trigger():
    if 'df' not in st.session_state:
        st.session_state['df'] = True

st.title("Edgzzle")
st.write("1. Enter a phrase and select the difficulty level to generate a puzzle")
st.write("2. Sum the numbers in each column to get the pass number")
st.write("3. Subtract the pass number from 26: this is the number of the letter in the alphabet")

phrase = st.text_input("Enter a phrase:")

col1, col2, col3 = st.columns(3)



with col1:
    if st.button("Easy Edgzzle"):
        trigger()
        span = [-3, 3]
        list_of_letters = list_letters(phrase)
        hint_row = hint_row(list_of_letters, 'easy')
        

with col2:
    if st.button("Medium Edgzzle"):
        trigger()
        span = [-6, 6]
        list_of_letters = list_letters(phrase)
        hint_row = hint_row(list_of_letters, 'medium')
 
        

with col3:
    if st.button("Hard Edgzzle"):
        trigger()
        span = [-10, 10]
        list_of_letters = list_letters(phrase)
        hint_row = hint_row(list_of_letters, 'hard')
                
if 'df' in st.session_state:
    df = pd.DataFrame()
    for i, x in enumerate(list_of_letters):
        df[i] = generate_random_numbers(x, span)
    df = pd.concat([df.iloc[:4], pd.DataFrame([hint_row]), df.iloc[4:]]).reset_index(drop=True)
    st.dataframe(df, hide_index=True, use_container_width=True)
    # Create a Plotly table
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns),
        cells=dict(values=df.values.T)
    )])

    csv = convert_df(df)

    st.download_button(
        label="Download",
        data=csv,
        file_name='Edgzzle.csv',
        mime='text/csv',
    )

