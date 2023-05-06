from openai.embeddings_utils import distances_from_embeddings
import openai
import tiktoken
import pandas as pd
import numpy as np


class Recall:
    def __init__(self, path):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.df = pd.read_csv(path)
        self.df['embeddings'] = self.df['embeddings'].apply(lambda x: np.array(eval(x)))
        self.df['n_tokens'] = self.df['text'].apply(lambda x: len(self.tokenizer.encode(x)))

    def __call__(self,
                 question, max_len=1500
                 ):
        """
        Create a context for a question by finding the most similar context from the dataframe
        """

        # Get the embeddings for the question
        q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

        # Get the distances from the embeddings
        self.df['distances'] = distances_from_embeddings(q_embeddings, self.df['embeddings'].values,
                                                         distance_metric='cosine')

        returns = []
        cur_len = 0

        labels = []
        # Sort by distance and add the text to the context until the context is too long
        for i, row in self.df.sort_values('distances', ascending=True).iterrows():
            # Add the length of the text to the current length
            cur_len += row['n_tokens'] + 4
            # If the context is too long, break
            if cur_len > max_len:
                break
            # Else add it to the text that is being returned

            dic = dict(row)
            del dic['embeddings']
            returns.append(dic)

        # Return the context

        texts = ''
        for i, j in enumerate(returns):
            texts += f"文档id:{i + 1}:{j['text']}\n"
        return texts, returns


create_context = Recall('../data/data.csv')
