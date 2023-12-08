import random
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def list_letters(phrase):
    list_of_letters = [i for i in phrase]
    return list_of_letters

def generate_random_numbers(letter):
    
    if letter.isalpha()==False:
        if letter == ' ':
            letter_value = 0
            # Generate 8 random numbers between -10 and 10
            random_numbers = [random.randint(-15, 15) for _ in range(8)]
            
            # Adjust the last number to ensure the sum is equal to 26 - the letter value
            random_numbers[-1] += (26 - letter_value - sum(random_numbers))
            
            return random_numbers
        else:
            return [0] * 8
    
    else:
        # Assign a value to the letter based on its position in the alphabet
        letter_value = ord(letter.lower()) - ord('a') + 1
        
        # Generate 8 random numbers between -10 and 10
        random_numbers = [random.randint(-15, 15) for _ in range(8)]
        
        # Adjust the last number to ensure the sum is equal to 26 - the letter value
        random_numbers[-1] += (26 - letter_value - sum(random_numbers))
        
        return random_numbers


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.title("Edgzzle")

phrase = st.text_input("Enter a phrase:")

if st.button("Generate Edgzzle"):

    list_of_letters = list_letters(phrase)
    cols = [i for i in range(len(list_of_letters))]
    blanks = []
    for x in list_of_letters:
        if x.isalpha()==False:
            blanks.append(x)
        else:
            blanks.append(' ')
    #blanks = [' '] * len(list_of_letters)
    black_row = dict(zip(cols,blanks))
    df = pd.DataFrame()
    for i, x in enumerate(list_of_letters):
        df[i] = generate_random_numbers(x)
    
    df = pd.concat([df.iloc[:4], pd.DataFrame([black_row]), df.iloc[4:]]).reset_index(drop=True)
    st.dataframe(df, hide_index=True)
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
