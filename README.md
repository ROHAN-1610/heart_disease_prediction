# Heart Disease Prediction

This Django web application predicts the likelihood of heart disease based on patient health data using a machine learning model. Designed to be user-friendly, it provides real-time predictions to help with early diagnosis and better decision-making.

## Why This Model?🤖

We chose the **K-Nearest Neighbors (KNN)** algorithm for the following reasons:

```text
1. Easy to implement and interpret.
   - KNN is straightforward and doesn't require complex parameter tuning.
   
2. Performs well on structured data with relatively small dimensions.
   - It works efficiently with small datasets and structured data, making it a good fit for heart disease prediction.

3. Requires minimal assumptions about data distribution.
   - Unlike some other models, KNN does not make assumptions about the underlying distribution of the data, making it flexible for various types of datasets.


##Features 🔑
**A bullet-point list of key functionalities your project provides, like:**
- User-friendly interface to input health data.
- Real-time predictions powered by a trained KNN model.
- Secure user authentication and admin dashboard.

## Technologies Used 🛠️
- **Programming Language**: Python 🐍
- **Framework**: Django 🌐
- **Machine Learning**: Scikit-learn(for KNN model) 🤖
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 💻
- **Notebook Environment**: Jupyter Notebook(used for model development and analysis) 📓

- ## Machine Learning 📊

This project integrates a machine learning model to predict the likelihood of heart disease based on medical data. Below are the details of the approach:

### 1. Dataset 📅
The model was trained using a dataset that includes various health metrics such as:
- **Age**, **Gender**, **Chest Pain Type**
- **Cholesterol levels**, **Blood pressure**
- **blood sugar**, **Heart rate**
-**and more**

These variables are critical for determining heart disease risk, and the model analyzes patterns within the data to make predictions.

### 2. Data Preprocessing 🔧
Before feeding the data into the model, the following steps were performed:
- **Handling Missing Values**: Any missing or incomplete data was either filled in or removed to maintain consistency.
- **Feature Encoding**: Categorical features like chest pain type were converted into numerical values using one-hot encoding.
- **Feature Scaling**: The data was scaled using StandardScaler to ensure all features were on the same scale, which improves the accuracy of the KNN algorithm.

### 3. Machine Learning Model 🧠
We chose **K-Nearest Neighbors (KNN)** as the machine learning model due to its simplicity and effectiveness in classification problems. KNN works by comparing a new data point to its nearest neighbors and classifying it based on the majority class.

### 4. Training and Testing 📚
The dataset was divided into:
- **Training Set**: 80% of the data was used to train the model.
- **Testing Set**: The remaining 20% was used to test and evaluate the model's accuracy.

### 5. Model Evaluation 🏆
The model's performance was evaluated using:
- **Accuracy**: The percentage of correct predictions.
- **Confusion Matrix**: This helped in understanding the true positives, false positives, true negatives, and false negatives.
- **F1-Score**: This metric balances precision and recall, providing a better measure of performance.

### 6. Libraries Used 📚
- **Scikit-learn**: For implementing the KNN algorithm and preprocessing the data.
- **Pandas**: Used for handling and processing the dataset.
- **NumPy**: Used for numerical computations and data manipulation.
- **Matplotlib/Seaborn**: For visualizing the dataset and evaluation metrics.

## Installation ⚙️

To get the project up and running locally, follow these steps:

```bash
# Step 1: Clone the repository
git clone https://github.com/your-username/heart-disease-prediction.git
cd heart-disease-prediction

# Step 2: Install the required dependencies
pip install -r requirements.txt

# Step 3: Run database migrations
python manage.py makemigrations
python manage.py migrate

# Step 4: Start the Django development server
python manage.py runserver

# Step 5: Access the application in your browser
# Open the application at http://127.0.0.1:8000 or any server you want to run.

## How to Use 📝

Once the project is set up, follow these steps to use the application:

1. **Login or Register**: 
   - After starting the server, visit `http://127.0.0.1:8000` and log in with your credentials or create a new account.
   
2. **Input Health Data**:
   - Once logged in, navigate to the input form where you can enter various health metrics like age, cholesterol levels, blood pressure, etc.

3. **Get Prediction**:
   - After submitting the form, the model will predict the likelihood of heart disease and display the result on the screen.

4. **View Results**:
   - The result will show the probability of heart disease, and you can choose to enter new data or log out.


## Future Enhancements 🔮

We plan to improve the application by:
- **Adding more advanced machine learning models** for higher prediction accuracy.
- **Including a data visualization dashboard** to help users better understand the results.
- **Adding multi-language support** for wider accessibility.


## License 📄

This project is licensed under the **[MIT License]**.

**Built with passion 💻❤️ using Django and Machine Learning 🤖**
