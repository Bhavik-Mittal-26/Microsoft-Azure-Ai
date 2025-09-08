# Import necessary libraries and namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

def main():
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Retrieve Azure AI service endpoint and key from environment variables
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create a credential object using the API key
        credential = AzureKeyCredential(ai_key)

        # Initialize the Text Analytics client with endpoint and credentials
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Define the folder containing text files to analyze
        reviews_folder = 'reviews'

        # Iterate over each file in the reviews folder
        for file_name in os.listdir(reviews_folder):
            # Print separator and file name for clarity
            print('\n-------------\n' + file_name)

            # Open and read the file contents with UTF-8 encoding
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Detect the primary language of the text
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))

            # Analyze the sentiment of the text
            sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
            print("\nSentiment: {}".format(sentimentAnalysis.sentiment))

            # Extract key phrases from the text
            phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))

            # Recognize named entities in the text
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities:")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))

            # Recognize linked entities (e.g., Wikipedia links) in the text
            entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nLinks:")
                for linked_entity in entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))

    except Exception as ex:
        # Print any exception that occurs during the process
        print(ex)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
