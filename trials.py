import csv
import random
import openai
import re
import numpy as np

# Set up OpenAI API
openai.api_key =  'filler'   # Replace this with your OpenAI API key
number_of_participants = 60 
trials_per_participant = 30 #should be even so there can be 50/50 on polarity 
file_path_questions = 'experimentformatedqsandfiller.csv' # must have a column with the header "question"
file_path_answer = 'responses.csv'


def get_questions_from_csv(csv_file):
    """
    Read questions from a CSV file and return them

    Parameters: 
    csv_file: file path to the file the questions are saved in

    Returns:
    questions: list containing all the questions 
    """
    questions = []
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(( row['question']))
    return questions

def ask_question(question, context):
    """
    Ask the question to ChatGPT and return the response
    
    Parameters: 
        context(str): The cumulative context containing previous questions and responses,
                   used to provide continuity in interaction with the Chatbot.
        question(str): the current question of the trial
    Returns: 
        response: the Chatbots answer
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": question},
        ],
        temperature=0.7,  #the temperture of ChatGPT
        max_tokens=200,
    )
    return response.choices[0].message["content"]

def trial(context, responses):
    """
    Conducts a series of trials that ask the Chatbot questions based on adjectives 
    and their polarity. This function randomizes the order of questions and the 
    polarity of the adjectives to ensure a balanced presentation to participants.

    Parameters:
    context (str): The cumulative context containing previous questions and responses,
                   used to provide continuity in interaction with the Chatbot.
    responses (list of list): Each inner list represents a trial's data including:
                               responses[trial_index][0]: The response to the question.
                               responses[trial_index][1:5]: Metadata about the trial,
                               including polarity and adjective pairs.
    """
    # Get questions from CSV
    questions = get_questions_from_csv(file_path_questions)

    #determine the order the questions are asked in
    sentence_nr  = [i for i in range(trials_per_participant)]
    random.shuffle(sentence_nr)

    #decide with polarity of the adjective is used for each question
    polarity = [0] * (int)(trials_per_participant/2) + [1] * (int)(trials_per_participant/2)
    random.shuffle(polarity)

    # Process questions based on sentence_nr and polarity
    for idx in sentence_nr:
        question = questions[idx]
        # identify the polar adjective pair of the question 
        pattern = r'\w+/\w+'
        adj = re.findall(pattern, question)
        adj1, adj2 = adj[0].split('/')

        if polarity[idx] == 0:
            #format the qestion for neagtive polarity 
            question = re.sub(r'\w+/','',question)
            question = re.sub("word2",adj1,question)
            question = re.sub("word1",adj2,question)
            #save information about the trial 
            responses[idx][1:5] = [0, adj2, adj1, idx]

        else:
            #format the question for positive polarity 
            question = re.sub(r'/\w+','',question)
            question = re.sub("word1",adj1,question)
            question = re.sub("word2",adj2,question)
            #save information about the trial
            responses[idx][1:5] = [1, adj1, adj2, idx]

        # get the response for the question 
        response = ask_question(question, context)
        responses[idx][0] = response
        # add question and response to the context for the next question
        context = context + question + response
    return responses

def main():    
    for a in range(number_of_participants):
        print(a)
        # ask the questions 
        context = ""
        responses = [[None] * 6 for _ in range(trials_per_participant)]
        responses = trial(context, responses)

        # save the responses in a cvs file 
        with open(file_path_answer, mode='a+', newline='') as file:
            writer = csv.writer(file)
            for response in responses:
                response.append(a) # in case the session timed out add to a the already asked questions for an consistent id 
                writer.writerow(response)

           

if __name__ == "__main__":
    main()
