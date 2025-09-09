# Import libraries for environment variables and Azure client
from dotenv import load_dotenv  # Used to load environment variables from a .env file
import os                      # Used to access environment variables

# Import necessary classes from Azure SDK
from azure.core.credentials import AzureKeyCredential  # Used for API authentication
from azure.ai.language.questionanswering import QuestionAnsweringClient  # Client for QnA service

def main():
    try:
        # Load environment variables from the .env file
        load_dotenv()

        # Get configuration settings from environment variables
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')        # Endpoint URL for the Azure AI service
        ai_key = os.getenv('AI_SERVICE_KEY')                  # API key for authentication
        ai_project_name = os.getenv('QA_PROJECT_NAME')        # Name of the question answering project
        ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')  # Name of the deployment within the project

        # Create a credential object using the API key
        credential = AzureKeyCredential(ai_key)

        # Initialize the QuestionAnsweringClient with the endpoint and credential
        ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

        # Prepare to accept user questions and display answers
        user_question = ''

        # Loop to continually ask for questions until the user types 'quit'
        while True:
            user_question = input('\nQuestion:\n')  # Prompt user for a question

            if user_question.lower() == "quit":     # Exit the loop if user types 'quit'
                break

            # Send the user's question to the Azure Question Answering service
            response = ai_client.get_answers(
                question=user_question,
                project_name=ai_project_name,
                deployment_name=ai_deployment_name
            )

            # Iterate through the answers received and print them with confidence and source
            for candidate in response.answers:
                print(candidate.answer)  # Print the answer text
                print("Confidence: {}".format(candidate.confidence))  # Print how confident the system is
                print("Source: {}".format(candidate.source))  # Print the source of the answer

    except Exception as ex:
        # Print any errors that occur during execution
        print(ex)

# Check if the script is run as the main program and call the main function
if __name__ == "__main__":
    main()
