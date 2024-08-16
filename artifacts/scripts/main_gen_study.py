from llmAdapter import LlmApi
import csv
import time
import os

# Choose a model. Options:
# claude-3-haiku-20240307 || gpt-3.5-turbo-0125 || gemini-1.0-pro
MODEL_NAME = "claude-3-haiku-20240307"

# For the first prompt (zero-shot) and the third prompt (few-shot) this can be set to 1, to every other prompt, I used 100 tokens.
MAX_OUTPUT_TOKENS = 100
     
# The prompt_type defines witch prompt should be used
# Zero-shot = 1 || Think step-by-step = 2 || few-shot = 3 || CoT = 4
PROMPT_TYPE = 4

# apache_traffic_TD_dataset || owncloud_TD_dataset || ubc_thunder_TD_dataset || va_gov_debt_TD_dataset
DATASET = "va_gov_debt_TD_dataset"

# The LlmApi class creates a single interface to interact with the models
llm_api = LlmApi(MODEL_NAME, MAX_OUTPUT_TOKENS, PROMPT_TYPE)

# File path to the issues csv
file_path = f"../data/{DATASET}.csv"

# The output file is named after the model and prompt being used
output_file_name = f"{MODEL_NAME}_prompt{PROMPT_TYPE}.csv"
output_file_path = f"../data/results_{DATASET}/{output_file_name}"

# If the output csv does not exist it's created here, if it is it's appended to in the loop
if not os.path.exists(output_file_path):
    with open(output_file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "text", "Label" ,"Model_classification"])
        row_count = 0
else:
    # Count the number of rows already added to the output file
    with open(output_file_path, "r") as file:
        reader = csv.reader(file)
        row_count = sum(1 for _ in reader) - 1

# Open the input file
with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    current_row = 0
    for row in reader:
        # Skip rows that have already been added to the output file
        if current_row <= row_count:
            current_row += 1
            continue
        
        # Defining a hard limit to how many rows I want to read per execution of the program. 
        # This is useful for testing or to be safe that it didn't get extra expensive 
        # It's ok to comment this if statement if it's desired to run the whole dataset in only one go
        # rows_to_be_read = 1
        # if current_row > row_count + rows_to_be_read:
        #     break         
        
        # issue_type represents the "answer" based on the GTD classification
        issue_type = ""
        if int(row['label']) == 1:
            issue_type = "TD"
        elif int(row['label']) == 0:
            issue_type = "Not_TD"
        else:
            raise ValueError(f"Model: {MODEL_NAME} - Prompt: {PROMPT_TYPE} - Row: {row['id']} - Could not read the label column, text: {row['label']}")
        
        response_text = llm_api.call(row['text']).strip().upper()
        
        # Sometimes the model responds with YES or NO bolded in MD, be it "**YES**" or "**NO**", this line removes the bolding
        response_text = response_text.replace("*", "")
        
        # The variable response_issue_type represents the model's decision
        response_issue_type = ""

        if response_text.startswith("YES"):
            response_issue_type = "TD"
        elif response_text.startswith("NO"):
            response_issue_type = "Not_TD"
        else:
            raise ValueError("Invalid response from the model. Response text:", response_text)

        # Append the row to the csv file
        with open(output_file_path, "a") as file:
            writer = csv.writer(file)
            writer.writerow([row["id"], row["text"], issue_type, response_issue_type])

        # I only used this to debug or to keep track of what was happening during long data processing phases
        #print("Row Text:", row['text'])
        #print("RESPONSE TEXT:", response_text)
        print(f"Current row: {current_row} - Issue Id: {row['id']} - Issue type: {issue_type} - Model's prediction: {response_issue_type}")
        
        # Add a delay of 1 sec to make sure we won't hit the max requests allowed, feel free to change this
        time.sleep(1)
        current_row += 1