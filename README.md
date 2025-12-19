# SA-NLP: Sentiment Analysis & Topic Classification (2015-2024)

This project analyzes population trends and public sentiment based on news articles published between 2015 and 2024. It combines dynamic web scraping with advanced NLP models.

## 📁 Project Structure
- **/scraping**: Python scripts for data collection.
- **/notebooks**: Jupyter/Colab notebooks for data processing and model training.
- **/data**: Contains the Lexicon and the News NLP dataset (~28MB).

## 🛠 Setup & Requirements
### 1. Database Configuration (MySQL)
The scraping scripts are designed to store data in a MySQL database. To run them:
1. Ensure you have MySQL installed and running.
2. Create a database (e.g., `news_db`).
3. Update the connection strings in the scraping scripts with your local `host`, `user`, and `password`.

### 2. Environment
Install the necessary Python libraries in the file REQUIREMENTS.txt
