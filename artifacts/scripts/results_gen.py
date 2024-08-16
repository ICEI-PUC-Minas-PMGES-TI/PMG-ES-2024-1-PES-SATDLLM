import csv

# Datasets
# 
datasets = ["apache_traffic_TD_dataset", "owncloud_TD_dataset", "ubc_thunder_TD_dataset", "va_gov_debt_TD_dataset"]
# Zero-shot, think step-by-step, few-shot, CoT
prompt_numbers = [1, 2, 3, 4]
# Tested models
model_types = ["claude-3-haiku-20240307","gpt-3.5-turbo-0125", "gemini-1.0-pro"]

datasets_metrics = {}  # {dataset: {metric: {"highest": value, model: model, "prompt": prompt}}}

def update_metrics(metric, value, model, prompt, dataset):
    if dataset not in datasets_metrics:
        datasets_metrics[dataset] = {
            "f1_score": {"highest": 0, "model": "", "prompt": ""},
            "precision": {"highest": 0, "model": "", "prompt": ""},
            "recall": {"highest": 0, "model": "", "prompt": ""},
            "td_percentage": {"highest": 0, "model": "", "prompt": ""},
            "not_td_percentage": {"highest": 0, "model": "", "prompt": ""},
            "total_percentage": {"highest": 0, "model": "", "prompt": ""},
            "accuracy": {"highest": 0, "model": "", "prompt": ""},
            "MCC": {"highest": 0, "model": "", "prompt": ""}
        }
    
    if value > datasets_metrics[dataset][metric]['highest']:
        datasets_metrics[dataset][metric]['highest'] = value
        datasets_metrics[dataset][metric]['model'] = model
        datasets_metrics[dataset][metric]['prompt'] = prompt

def calculate_metrics(file_path, model, prompt, dataset):
    true_positives = false_positives = false_negatives = true_negative = 0
    td_correct = td_total = not_td_correct = not_td_total = 0

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            GTD_classification = row["Label"].strip()
            Model_classification = row["Model_classification"].strip()
            
            if Model_classification not in ["TD", "Not_TD"]:
                raise ValueError(f"Row: {row['id']} - Could not read the model classification column, text: {row['Model_classification']}")

            if GTD_classification == "TD":
                td_total += 1
                if Model_classification == "TD":
                    true_positives += 1
                    td_correct += 1
                else:
                    false_negatives += 1
            elif GTD_classification == "Not_TD":
                not_td_total += 1
                if Model_classification == "Not_TD":
                    not_td_correct += 1
                    true_negative += 1
                else:
                    false_positives += 1
            else:
                raise ValueError(f"Row: {row['id']} - Could not read the label column, text: {row['Label']}")

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) != 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    accuracy = (true_positives + true_negative) / (true_positives + true_negative + false_negatives + false_positives) if (true_positives + true_negative + false_negatives + false_positives) != 0 else 0

    precision = round(precision, 2)
    recall = round(recall, 2)
    f1_score = round(f1_score, 2)
    precision = round(precision, 2)
    accuracy = round(accuracy, 2)
    
    mcc = (true_positives * true_negative - false_positives * false_negatives) / ((true_positives + false_positives) * (true_positives + false_negatives) * (true_negative + false_positives) * (true_negative + false_negatives)) ** 0.5 if ((true_positives + false_positives) * (true_positives + false_negatives) * (true_negative + false_positives) * (true_negative + false_negatives)) != 0 else 0

    mcc = round(mcc, 2)


    total = td_total + not_td_total
    total_correct = td_correct + not_td_correct
    
    td_percentage = (td_correct / td_total) * 100 if td_total != 0 else 0
    not_td_percentage = (not_td_correct / not_td_total) * 100 if not_td_total != 0 else 0
    total_percentage = (total_correct / total) * 100 if total != 0 else 0
    
    
    td_percentage = round(td_percentage, 2)
    not_td_percentage = round(not_td_percentage, 2)
    total_percentage = round(total_percentage, 2)

    update_metrics("f1_score", f1_score, model, prompt, dataset)
    update_metrics("precision", precision, model, prompt, dataset)
    update_metrics("recall", recall, model, prompt, dataset)
    update_metrics("accuracy", accuracy, model, prompt, dataset)
    update_metrics("td_percentage", td_percentage, model, prompt, dataset)
    update_metrics("not_td_percentage", not_td_percentage, model, prompt, dataset)
    update_metrics("total_percentage", total_percentage, model, prompt, dataset)
    update_metrics("MCC", mcc, model, prompt, dataset)
    
    
    print("###############################")
    print(f"DATASET: {dataset} - MODEL: {i} - PROMPT: {j}")
    print("F1 Score:", f1_score)
    print("Precision:", precision)
    print("Recall:", recall)
    print("Accuracy:", accuracy)
    print("MCC:", mcc)
    print("Percentage of correct predictions when it is TD:", "{:.2f}%".format((td_correct / td_total) * 100 if td_total != 0 else 0))
    print("Percentage of correct predictions when it is not TD:", "{:.2f}%".format((not_td_correct / not_td_total) * 100 if not_td_total != 0 else 0))
    print("Percentage of correct predictions in total:", "{:.2f}%".format(round((total_correct / total) * 100 if total != 0 else 0, 2)))

for k in datasets:
    for i in model_types:
        for j in prompt_numbers:
            file_path = f"../results_{k}/{i}_prompt{j}.csv"
            calculate_metrics(file_path, i, j, k)


for dataset in datasets_metrics:
    print(f"############################### {dataset} - BEST RESULTS ###############################")
    for metric in datasets_metrics[dataset]:
        print(f"{metric}: {datasets_metrics[dataset][metric]['highest']} - MODEL: {datasets_metrics[dataset][metric]['model']} PROMPT: {datasets_metrics[dataset][metric]['prompt']}")
