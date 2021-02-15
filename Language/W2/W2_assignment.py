#!/usr/bin/env python
# coding: utf-8

# ## String processing with Python
# 
# Using a text corpus found on the cds-language GitHub repo or a corpus of your own found on a site such as Kaggle, write a Python script which calculates collocates for a specific keyword.
# 
# The script should take a directory of text files, a keyword, and a window size (number of words) as input parameters, and a file called out/{filename}.csv
# These parameters can be defined in the script itself.
# 
# - Find out how often each word collocates with the target across the corpus
# - Use this to calculate mutual information between the target word and all collocates across the corpus
# - Save result as a single file consisting of four columns: collocate, raw_frequency, MI
# 
# 
# __General instructions__
# 
# For this assignment, you should upload a standalone .py script which can be executed from the command line.
# Save your script as collocation.py
# Make sure to include a requirements.txt file and your data
# You can either upload the scripts here or push to GitHub and include a link - or both!
# Your code should be clearly documented in a way that allows others to easily follow the structure of your script and to use them from the command line.

# __Libraries__

# In[4]:


import os
from pathlib import Path
import pandas as pd
import re #regex
import string

# pd.show_versions() # The pd version is 1.1.5


# ## Nice try solution

# In[ ]:


# The tokenize function splits an input string into words and store it in a list 
def tokenize(input_string):
    # Use regex to split at all characters
    tokenizer = re.compile(r"[^a-zA-Z']+") 
    # The input string is now split into tokens and stored in a list
    token_list = tokenizer.split(input_string) 
    return token_list

# The collocate_ish function 
def collocate_ish(path, keyword, window_size):
    # Creating a data frame
    data = pd.DataFrame(columns=["collocate", "raw_frequency", "MI", "keyword"])
    # Creating a list for collocates
    collocates_list = []
    
    # Setting keyword_count to 0 to keep track of occurrence 
    keyword_count = 0
    
    for filename in Path(path).glob("*.txt"):
        # Open and read the files
        with open (filename, "r", encoding = "utf-8") as file:
            text = file.read()
            # The texts get 'tokenized'
            token_list = tokenize(text)
            # Use enumerate to get a counter in a loop
            text_by_index = [for index, word in enumerate(token_list) if word == keyword]
            # Ad keyword count to the keyword_count list
            keyword_count = keyword_count + len(text_by_index)
            
            # Loop over keyword occurences
            for index in text_by_index:
                # Window start
                window_start = max(0, index - window_size) # max 0 - a negative value will be 0 instead.
                # Window end
                window_end = index + window_size
                # Finding tokens surrounding the keyword
                keyword_collocates = token_list[window_start : window_end]
                # Ad keyword_collocate to the list of collocates 
                collocates_list.extend(keyword_collocate)
                # Remove the keyword from the list of collocates - then only the collocates will be left 
                collocates_list.remove(keyword)
   
    # In the last part of the function, the information would be added to the data frame. 
    # I have not been able to get the information, but this is roughly what I would have done if I had the information 
    # data = data.append({}) 
    # return data

# Define behaviour when called from command line
if __name__=="__main__":
    main()   

