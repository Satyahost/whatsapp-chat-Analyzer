from nltk.corpus import stopwords
from tenacity import retry_unless_exception_type
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

# from Whatsapp_chat_analyzer.chat import selected_user

extractor= URLExtract()
def fetch_stats(selected_user,df):

      if selected_user != 'Overall':

          df = df[df['user'] == selected_user]
        # 1.fetch number of messages
      num_messages= df.shape[0]

         #2. number of words
      words=[]
      for messages in df['message']:
            words.extend(messages.split())

      #fetch number of media messages
      num_media_messages= df[df['message']=='<Media omitted>\n'].shape[0]

      #fetch numbers of media messages
      links=[]
      for message in df['message']:

          links.extend(extractor.find_urls(message))

      return num_messages,len(words),num_media_messages,len(links)


def most_busy_users(df):

    X= df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'count': 'percent'})
    return X,df

def create_wordcloud(selected_user,df):

      f = open('stop_hinglish.txt', 'r')

      stop_words = f.read()
      if selected_user != 'Overall':
          df = df[df['user'] == selected_user]

      temp = df[df['user'] != 'group_notification']
      temp = temp[temp['message'] != '<Media omitted>\n']

      def remove_stop_words(message):
          y=[]
          for word in message.lower().split():
              if word not in stop_words:
                  y.append(word)
          return " ".join(y)



      wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
      temp['message']=temp['message'].apply(remove_stop_words)
      df_wc= wc.generate(df['message'].str.cat(sep=" "))
      return df_wc


def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')

    stop_words= f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(30))
    return most_common_df

def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    if len(emojis) == 0:
        return pd.DataFrame(columns=['emoji', 'count'])

    emoji_counts = Counter(emojis)

    emoji_df = pd.DataFrame(
        emoji_counts.most_common(len(emoji_counts)),
        columns=['emoji', 'count']
    )

    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user !='Overall':
        df= df[df['user']== selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap


