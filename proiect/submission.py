import pandas as pd, json
import os, regex as re
if not os.path.exists('./subtask_1'):
	os.mkdir('./subtask_1')
if not os.path.exists('./subtask_2'):
	os.mkdir('./subtask_2')
if not os.path.exists('./subtask_3'):
	os.mkdir('./subtask_3')
D = 1
#IN_NAME = './test_pred_small_25_context_va_final.jsonl'
IN_NAME = './test_pred_t5_context_va_final.jsonl'
DSET = 'restaurant' if D == 1 else 'laptop'
DSET_PRE = 'rest' if D == 1 else 'lap'
PREFIXES = [f'{DSET_PRE}26_aspect_va_dev_', f'{DSET_PRE}26_aste_dev_', f'{DSET_PRE}26_asqp_dev_']
data = pd.read_json(IN_NAME, lines=True)
print(data.shape)

for record in data.to_dict(orient='records'):
	for q in record['Quadruplet']:
		del q['Opinion']
		del q['Category']
data.columns = ['ID', 'Aspect_VA']
with open(f"./subtask_1/pred_eng_{DSET}.jsonl", 'w') as f:
	for item in data.to_dict(orient='records'):
		if re.match(f'{PREFIXES[0]}.*', item['ID']):
			f.write(json.dumps(item) + "\n")

data = pd.read_json(IN_NAME, lines=True)

for record in data.to_dict(orient='records'):
	for q in record['Quadruplet']:
		del q['Category']
data.columns = ['ID', 'Triplet']
with open(f"./subtask_2/pred_eng_{DSET}.jsonl", 'w') as f:
	for item in data.to_dict(orient='records'):
		if re.match(f'{PREFIXES[1]}.*', item['ID']):
			f.write(json.dumps(item) + "\n")


data = pd.read_json(IN_NAME, lines=True)
with open(f"./subtask_3/pred_eng_{DSET}.jsonl", 'w') as f:
	for item in data.to_dict(orient='records'):
		if re.match(f'{PREFIXES[2]}.*', item['ID']):
			f.write(json.dumps(item) + "\n")