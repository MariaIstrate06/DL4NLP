import pandas as pd, regex as re, numpy as np
def postprocess(dataframe, stats):
	stats['dedup'] = 0
	for index, row in dataframe.iterrows():
		# remove duplicate quads
		seen = set()
		unique_quads = []
		for quad in row['Quadruplet']:
			quad_tuple = (quad['Aspect'], quad['Opinion'], quad['Category'])
			if quad_tuple not in seen:
				seen.add(quad_tuple)
				unique_quads.append(quad)
		row['Quadruplet'] = unique_quads
		stats['dedup'] += len(row['Quadruplet']) - len(unique_quads)
		if len(row['Quadruplet']) - len(unique_quads) != 0:
			print("Deduplicated quads for ID:", row['ID'])
	return dataframe


js = pd.read_json('subtask_3/pred_eng_laptop.jsonl', lines=True)
state = {'aspect_case': 0, 'opinion_case': 0, 'opinion_negation': 0}
js = postprocess(js, state)
#Count duplicate ids
id_counts = js['ID'].value_counts()
duplicate_id_count = (id_counts > 1).sum()
print(f"Number of duplicate IDs: {duplicate_id_count}")

print(state)
with open('test_pred_postprocessed.jsonl', 'w') as f:
	f.write(js.to_json(orient='records', lines=True))