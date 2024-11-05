# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Embedding
# from sklearn.preprocessing import LabelEncoder
# from sqlalchemy import create_engine
# import random






# # Set up database connection
# engine = create_engine('sqlite:///your_database.db')  # Use your actual database URI

# # Load user interactions from the database
# query = '''
# SELECT user_id, video_id, topic, organization, timestamp
# FROM user_interactions
# ORDER BY user_id, timestamp
# '''
# data = pd.read_sql(query, engine)

# # Encode categorical features (topic and organization)
# topic_encoder = LabelEncoder()
# organization_encoder = LabelEncoder()

# data['topic_encoded'] = topic_encoder.fit_transform(data['topic'])
# data['organization_encoded'] = organization_encoder.fit_transform(data['organization'])

# # Group data by user and create sequences
# user_sequences = data.groupby('user_id').apply(
#     lambda x: list(zip(x['topic_encoded'], x['organization_encoded']))
# ).tolist()







# # Prepare sequences for LSTM training
# sequence_length = 5  # Define the length of the sequences for training
# X, y_topic, y_organization = [], [], []

# for sequence in user_sequences:
#     if len(sequence) > sequence_length:
#         for i in range(len(sequence) - sequence_length):
#             seq_x = sequence[i:i + sequence_length]
#             seq_y = sequence[i + sequence_length]

#             X.append(seq_x)  # Input sequence
#             y_topic.append(seq_y[0])  # Next topic
#             y_organization.append(seq_y[1])  # Next organization

# X = np.array(X)
# y_topic = np.array(y_topic)
# y_organization = np.array(y_organization)








# # Define LSTM model
# model = Sequential([
#     Embedding(input_dim=len(topic_encoder.classes_), output_dim=50, input_length=sequence_length),
#     LSTM(64, return_sequences=True),
#     LSTM(32),
#     Dense(len(topic_encoder.classes_), activation='softmax')  # Output for topic prediction
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Train the model on the topic prediction task
# model.fit(X, y_topic, epochs=5, batch_size=32, validation_split=0.2)  # Adjust epochs and batch size as needed






# def recommend_next_video(user_id, user_history):
#     # Encode user history (last few interactions) for LSTM input
#     user_history_encoded = [
#         (topic_encoder.transform([topic])[0], organization_encoder.transform([organization])[0])
#         for topic, organization in user_history
#     ]
#     # Use the last `sequence_length` interactions
#     if len(user_history_encoded) >= sequence_length:
#         user_history_encoded = user_history_encoded[-sequence_length:]
#     else:
#         return None  # Not enough history for recommendation
    
#     # Reshape for model input
#     user_history_encoded = np.array(user_history_encoded).reshape(1, sequence_length, 2)
    
#     # Predict next topic and organization
#     predicted_topic = model.predict(user_history_encoded)
#     predicted_topic_id = np.argmax(predicted_topic)
#     predicted_topic = topic_encoder.inverse_transform([predicted_topic_id])[0]

#     # Retrieve a random video from the predicted topic for recommendation
#     recommended_video = data[(data['topic'] == predicted_topic) & (data['user_id'] != user_id)]
#     if not recommended_video.empty:
#         return random.choice(recommended_video['video_id'].tolist())
#     else:
#         return None




import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine
import random

# Connect to the database
engine = create_engine('sqlite:///your_database.db')

# Load user interactions with video, topic, and captions
query = '''
SELECT user_id, video_id, topic, organization, caption, timestamp
FROM user_interactions
ORDER BY user_id, timestamp
'''
data = pd.read_sql(query, engine)





# Tokenize captions
tokenizer = Tokenizer(num_words=10000)  # Adjust as needed
tokenizer.fit_on_texts(data['caption'])

# Convert captions to sequences
data['caption_seq'] = tokenizer.texts_to_sequences(data['caption'])

# Pad sequences to ensure uniform length
max_caption_length = 20  # Define based on average caption length
data['caption_seq'] = pad_sequences(data['caption_seq'], maxlen=max_caption_length, padding='post').tolist()



# Encode topics
topic_encoder = LabelEncoder()
data['topic_encoded'] = topic_encoder.fit_transform(data['topic'])

# Encode video IDs
video_encoder = LabelEncoder()
data['video_encoded'] = video_encoder.fit_transform(data['video_id'])




sequence_length = 5  # Number of previous interactions to consider
X, y = [], []

for user_id, group in data.groupby('user_id'):
    if len(group) > sequence_length:
        for i in range(len(group) - sequence_length):
            seq_x = group.iloc[i:i + sequence_length][['topic_encoded', 'video_encoded', 'caption_seq']].values
            seq_y = group.iloc[i + sequence_length]['video_encoded']
            
            # Flatten and structure data for LSTM input
            X.append(seq_x)
            y.append(seq_y)

X = np.array(X)
y = np.array(y)




# Define the LSTM model
model = Sequential([
    Embedding(input_dim=len(video_encoder.classes_), output_dim=50, input_length=sequence_length),  # Video embeddings
    LSTM(64, return_sequences=True),
    LSTM(32),
    Dense(len(video_encoder.classes_), activation='softmax')  # Predict video ID
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=5, batch_size=32, validation_split=0.2)  # Adjust epochs and batch size as needed




def recommend_video(user_id, topic, data, sequence_length=5):
    # Get the user's history in the topic
    user_history = data[(data['user_id'] == user_id) & (data['topic'] == topic)]
    if len(user_history) < sequence_length:
        return None  # Not enough history for recommendation
    
    # Prepare the input sequence
    recent_interactions = user_history[-sequence_length:]
    input_sequence = recent_interactions[['topic_encoded', 'video_encoded', 'caption_seq']].values
    input_sequence = np.array(input_sequence).reshape(1, sequence_length, -1)

    # Predict the next video ID
    predicted_video_id = np.argmax(model.predict(input_sequence), axis=-1)
    recommended_video = video_encoder.inverse_transform([predicted_video_id])[0]
    
    return recommended_video


# # --------------------------------------Example usage to recommend a video within a specific topic---------------------------------------
# user_id = 123  # Replace with actual user ID
# topic = 'Machine Learning'  # Replace with known topic

# recommended_video = recommend_video(user_id, topic, data)
# if recommended_video:
#     print(f"Recommended Video ID: {recommended_video}")
# else:
#     print("No recommendation available.")
