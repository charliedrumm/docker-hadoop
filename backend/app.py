
from flask import Flask, render_template_string
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the data from the file
def load_data():
    data_file_path = 'symptom_analysis_count.txt'
    data = []
    with open(data_file_path, 'r') as file:
        for line in file:
            disease, count = line.rsplit('\t', 1)
            data.append((disease, int(count)))
    return pd.DataFrame(data, columns=['Disease', 'Count'])

@app.route('/')
def home():
    df = load_data()
    # Sort the data by count and get the top 5
    top_5_df = df.sort_values(by='Count', ascending=False).head(5)

    # Create a bar chart for the top 5
    plt.figure(figsize=(10, 6))
    plt.bar(top_5_df['Disease'], top_5_df['Count'], color='skyblue')
    plt.xlabel('Disease')
    plt.ylabel('Count')
    plt.title('Top 5 Diseases by Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('static/top_5_chart.png')
    plt.close()

    # Generate the HTML to display the table and the chart
    html_template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Disease Counts</title>
      </head>
      <body>
        <h1>Top 5 Diseases by Count</h1>
        <table border="1">
          <tr>
            <th>Disease</th>
            <th>Count</th>
          </tr>
          {% for _, row in top_5_df.iterrows() %}
            <tr>
              <td>{{ row['Disease'] }}</td>
              <td>{{ row['Count'] }}</td>
            </tr>
          {% endfor %}
        </table>
        <h2>Bar Chart of Top 5 Diseases</h2>
        <img src="/static/top_5_chart.png" alt="Top 5 Diseases by Count">
      </body>
    </html>
    """
    return render_template_string(html_template, top_5_df=top_5_df)

if __name__ == "__main__":
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)

