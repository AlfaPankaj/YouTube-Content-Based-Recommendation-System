# YouTube Content-Based Recommendation System

📜 Project Overview
This project is a complete content-based recommendation system for YouTube videos. It includes a Python script to collect video data from the YouTube Data API, a data processing pipeline to clean and engineer features, and a recommendation model that suggests similar videos based on their text content. The data collection process is automated to run daily using a batch script and Windows Task Scheduler.

This project was developed as a practical exercise in data science, covering data scraping, ETL (Extract, Transform, Load), feature engineering, and unsupervised machine learning.

✨ Key Features
Data Collection: Gathers thousands of video metadata points using the YouTube Data API.

Data Cleaning: Processes raw data using Pandas to handle missing values, correct data types, and remove duplicates.

Feature Engineering: Creates new features from existing data, such as published_year, duration_in_seconds, and a combined "text soup" for modeling.

Content-Based Model: Uses TF-IDF and Cosine Similarity from Scikit-learn to find and recommend videos with similar text content.

Automation: Includes a Windows batch script and instructions for using Task Scheduler to automate data collection daily.

🛠️ Tech Stack
Language: Python 3.10

Libraries:
Pandas & NumPy for data manipulation
Scikit-learn for TF-IDF and Cosine Similarity
google-api-python-client for accessing the YouTube API
python-dotenv for managing environment variables
Automation: Windows Task Scheduler & Batch Scripting

📂 Project Structure
YouTube_Recommendation_System/
│
├── 1_Data_Collection/
│   ├── Manual_Collection/
│   │   ├── Starter_data-collection_script.ipynb
│   │   └── youtube_sample.csv
│   └── Merging_Data/
│       ├── code.ipynb
│       ├── Main1.csv
│       ├── Main2.csv
│       └── Main.csv
│
├── 2_Data_Preprocessing_and_Feature_Engineering/
│   ├── Data_preprocessing&feature_eng..ipynb
│   ├── Text_pipeline.ipynb
│   └── youtube_data_clean.csv
│
├── 3_Recommendation_Model/
│   ├── recommendations_models.ipynb
│   └── cleaned_text_pipeline.csv
│
├── 4_Visualization/
│   ├── 10_channels_visualization.ipynb
│   ├── Distribution of videos view count.png
│   ├── Number of videos Published per year.png
│   └── Top 10 channels by number of videos in dataset.png
│
├── run_youtube_script.bat
├── requirements.txt
├── README.md
└── Technical Architecture Diagram.pdf

🏗️ Technical Architecture
The project's architecture follows a standard machine learning pipeline, from data ingestion to model deployment and monitoring.

Data Ingestion: Data from the YouTube API and User Interaction Datasets are collected by scheduled Python jobs.

Raw Storage: The raw data is stored in formats like CSV or in cloud storage (GCS/S3).

ETL and Feature Engineering: A processing layer cleans the data and engineers features, which are categorized into Text Embeddings, Numeric Features, and Category Encodings.

Feature Store: Processed features are stored in an optimized format like Parquet or in a SQL database.

Modeling Layer: This is where different recommendation models can be built. The architecture supports multiple approaches:

Content-based: Uses text features (TF-IDF, USE) to find similar items. (This is the approach implemented in this project).

Collaborative: Uses user interaction data (SVD, LightFM) to find users with similar tastes.

Hybrid Combiner: Merges scores from different models using a weighted system.

Evaluation and Monitoring: The model's performance is evaluated offline, and the system includes a scheduler for monitoring and periodic retraining.


⚙️ Setup and Installation
Follow these steps to set up the project on your local machine.

1. Clone the Repository
git clone <your-repository-url>
cd <your-repository-name>

2. Create a Python Virtual Environment
It is highly recommended to use a virtual environment.
# Create the environment
python -m venv venv
# Activate the environment
venv\Scripts\activate

3. Install Dependencies
Create a file named requirements.txt and paste the following content into it:
pandas
numpy
scikit-learn
google-api-python-client
python-dotenv
jupyterlab
Now, install all the packages by running:
pip install -r requirements.txt

4. Set Up YouTube API Key
You need a YouTube Data API v3 key from the Google Cloud Console.
Create a new file in the project folder named .env.
Open the file and add your API key like this:
YOUTUBE_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
🚀 Usage

1. Manual Data Collection
To run the data collection process manually, simply execute the main Python script from your activated terminal:
python automatic_Starter_data-collection_script.py
This will generate the youtube_sample.csv and youtube_videos.db files.

2. Automated Data Collection (Windows)
The run_youtube_script.bat file is pre-configured to automate the data collection. You can either double-click it to run it instantly or schedule it using Windows Task Scheduler.
To schedule the task:
Open Task Scheduler.
Create a new task to run daily (e.g., at 12:31 PM).
Set the action to "Start a program".
In the "Program/script" box, provide the full path to your run_youtube_script.bat file.
Leave the "Arguments" and "Start in" boxes empty.

3. Getting Recommendations
Open the recommendation_model.ipynb notebook.
Run the cells in order. The notebook will load the cleaned data, build the TF-IDF and Cosine Similarity matrices, and define the get_recommendations function.
You can test the function by passing any video title from your dataset to it.

🧠 Methodology
The project follows a multi-step pipeline, from data acquisition to generating recommendations. Each step is handled by a specific script or notebook.

1. Data Collection and Merging
API Data Extraction: The process begins with the Starter_data-collection_script.ipynb. This script uses the YouTube Data API v3 to fetch video data. It searches for videos based on a predefined list of queries (e.g., "technology," "education," "gaming") for the Indian region (regionCode="IN").

Metadata Fetching: For each video found, the script retrieves detailed metadata, including the title, description, tags, channel title, view count, like count, and duration.

Storage: The collected data is then saved in two formats: a CSV file (youtube_sample.csv) and a SQLite database (youtube_videos.db) for flexibility.

Data Merging: The code.ipynb notebook is used to combine multiple data files (e.g., Main1.csv, Main2.csv) into a single master CSV file (Main.csv), ensuring a comprehensive dataset for processing.

2. Data Preprocessing and Feature Engineering
This stage, detailed in Data_preprocessing&feature_eng..ipynb, cleans the raw data and creates new, insightful features.

Data Cleaning:

Missing values in likeCount and commentCount are filled with 0.
Duplicate videos are removed based on their titles to ensure data integrity.
Data types are corrected, such as converting published_at from a string to a datetime object.

Feature Engineering:

title_length: The length of the video title.
Time-Based Features: published_year, published_month, and published_day_of_week are extracted from the published_at column.
duration_seconds: The ISO 8601 duration format (e.g., PT1M5S) is parsed into total seconds.
Engagement Ratios: like_ratio (likes/views) and comment_ratio (comments/views) are calculated to normalize engagement metrics.
The final cleaned and feature-engineered dataset is saved as youtube_data_clean.csv.

3. Text Processing and Vectorization
The Text_pipeline.ipynb notebook prepares the textual data for the recommendation model.

"Text Soup" Creation: A new feature, text_soup, is created by combining the text from the title, description, and tags of each video into a single string. This consolidated text serves as the basis for the content-based model.

TF-IDF Vectorization: The text_soup is converted into a numerical format using Term Frequency-Inverse Document Frequency (TF-IDF). This technique creates a matrix where each row represents a video and each column represents a word. The values in the matrix reflect the importance of a word to a specific video in the context of the entire dataset. The resulting TF-IDF matrix for this project had a shape of (5419, 76837).

4. Recommendation Model
The recommendations_models.ipynb notebook builds and implements the recommendation logic.

Similarity Calculation: Cosine Similarity is calculated between all video vectors in the TF-IDF matrix. The linear_kernel function from scikit-learn is used for this, as it's an efficient way to compute the similarity scores. The result is a matrix where each value represents the content similarity between two videos.

get_recommendations() Function: This function takes a video title as input and returns the top 10 most similar videos by:

Finding the index of the input video.
Retrieving its similarity scores against all other videos.
Sorting these scores in descending order.
Selecting the top 10 videos and returning their titles.

📊 Data Visualization
The 10_channels_visualization.ipynb notebook provides insights into the dataset through several plots:

Distribution of Video View Counts: A log-transformed histogram showing that most videos have a moderate number of views, with a long tail of highly popular videos.

Number of Videos Published Per Year: A bar chart indicating the volume of videos published annually in the dataset.

Top 10 Channels: A horizontal bar plot identifying the channels with the highest number of videos in the collected dataset.

