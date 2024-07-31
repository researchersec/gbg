
import json
import requests
import os

# Read the JSON data from the file
with open('output.json', 'r') as file:
    data = json.load(file)

# Extract hits
hits = data['hits']['hits']

# Sort the data by 'sagsNummer'
sorted_hits = sorted(hits, key=lambda x: x['_source']['sagsNummer'])

# Create a directory to store the reports
os.makedirs('reports', exist_ok=True)

# Download the reports
for hit in sorted_hits:
    sags_nummer = hit['_source']['sagsNummer']
    cvr = str(hit['_source']['cvrNummer'])
    documents = hit['_source']['dokumenter']

    for doc in documents:
        url = doc['dokumentUrl']
        mime_type = doc['dokumentMimeType']
        ext = mime_type.split('/')[-1]
        #os.makedirs(cvr, exist_ok=True)
        file_name = f"reports/{sags_nummer}_{documents.index(doc)}.{ext}"

        # Download the document
        response = requests.get(url)

        # Save the document
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {file_name}")
