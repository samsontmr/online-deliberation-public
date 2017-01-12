import pandas as pd
import numpy as np

names = ['workforce', 'citizen', 'fertility']
moderations = ['h', 'l']
heterogeneities = ['1', '2', '3']
for name in names:
    for moderation in moderations:
        for heterogeneity in heterogeneities:
            df = pd.read_csv('datasets/cleaned/' + moderation + 'm' + heterogeneity +
                             '_' + name + '_cleaned.csv', encoding='utf-8')
            df = df.sort_values('CommentID', ascending=False)

            df.insert(df.columns.get_loc("SentimentValue") + 1, "AggregatedSentimentValue", 0)
            df.insert(df.columns.get_loc("SentimentType") + 1, "AggregatedP/NRatio", 0)
            df.insert(df.columns.get_loc("ParentCommentID") + 1, "NumChildren", 0)

            for index, row in df.iterrows():
                if row['ParentCommentID'] != row['CommentID']:
                    df.loc[df['CommentID'] == row['ParentCommentID'], 'NumChildren'] += 1
                    df.loc[df['CommentID'] == row['ParentCommentID'], 'AggregatedSentimentValue'] += row['SentimentValue']

            df.insert(df.columns.get_loc("AggregatedP/NRatio"), "AggregatedPositives", 0)
            df.insert(df.columns.get_loc("AggregatedP/NRatio"), "AggregatedNegatives", 0)

            for index, row in df.iterrows():
                if row['ParentCommentID'] != row['CommentID']:
                    if row['SentimentType'] == 'negative':
                        df.loc[df['CommentID'] == row['ParentCommentID'], 'AggregatedNegatives'] += 1.0
                    if row['SentimentType'] == 'positive':
                        df.loc[df['CommentID'] == row['ParentCommentID'], 'AggregatedPositives'] += 1.0

            df['AggregatedP/NRatio'] = (df['AggregatedPositives'] / df['AggregatedNegatives']).replace(np.inf, np.nan)
            df.drop(['AggregatedPositives', 'AggregatedNegatives'], axis=1, inplace=True)
            df.to_csv('datasets/with_aggregated_sentiments/' + moderation + 'm' + heterogeneity +
                      '_' + name + '_with_aggregated_sentiments.csv', index=False)
