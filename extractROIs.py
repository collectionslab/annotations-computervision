### To be used on the stripped version of the csv file generated from zooniverse

import pandas as pd
import json

CSV_PATH = '/Users/silver/Desktop/buildUCLA/stripped-book-annotation-classification-classifications-11June2018.csv'

# ASSUMES FILES ARE .PNG FORMAT
META_DATA_PATH = '/Users/silver/Desktop/buildUCLA/phase2/annotations-computervision/books meta data.csv'

# WARNING CSV file is inconsistent with the key identifier for the key names. 'filename' 'manifest.csv' and 'uclaclark_QD25S87_0291.png' are keys to retrieve the file name
def extractROIs(csv_file_path):
	assert csv_file_path
	df = pd.read_csv(csv_file_path, usecols=['annotations', 'subject_data','subject_ids'])

	# need to add this bit to map file names to the randomized IDs
	df_meta = pd.read_csv(META_DATA_PATH, usecols=['ID','File Name'])
	name2id = dict()
	for index, row in df_meta.iterrows():
		name2id[row[1].replace('.png','.jpg')] = str(row[0])

	fileNames = []
	coordinates = []

	# gets all fileNames of images in rows that use 'filename' as the key
	for index, row in df.iterrows():

		s_id = str(row['subject_ids'])

		s_data = json.loads(row['subject_data'])

		try: # if this succeeds, then we can retrieve its annotations as well
			
			fn = s_data[s_id]['filename']

			# name2id to convert file name to our id naming convention
			fileNames.append(name2id[s_data[s_id]['filename']])
			
			tasks = json.loads(df.iloc[index]['annotations'])

			imageCoordinates = []

			for t in tasks:

				if t['task'] == 'T1':
					listOfCoordinates = t['value']

					for coord in listOfCoordinates:
						formattedCoord = coord['x'], coord['y'], coord['width'], coord['height']
						imageCoordinates.append(formattedCoord)

			coordinates.append(imageCoordinates)
		except:
			try: # if this succeeds, then we are getting all the clark images
			
				fn = s_data[s_id]['manifest.csv']

				fileNames.append(s_data[s_id]['manifest.csv'])
			
				tasks = json.loads(df.iloc[index]['annotations'])

				imageCoordinates = []

				for t in tasks:

					if t['task'] == 'T1':
						listOfCoordinates = t['value']

						for coord in listOfCoordinates:
							formattedCoord = coord['x'], coord['y'], coord['width'], coord['height']
							imageCoordinates.append(formattedCoord)

				coordinates.append(imageCoordinates)
			except:
				try: # if this succeeds, then we are getting all the remaining images
			
					fn = s_data[s_id]['uclaclark_QD25S87_0291.png']

					fileNames.append(s_data[s_id]['uclaclark_QD25S87_0291.png'])
			
					tasks = json.loads(df.iloc[index]['annotations'])

					imageCoordinates = []

					for t in tasks:

						if t['task'] == 'T1':
							listOfCoordinates = t['value']

							for coord in listOfCoordinates:
								formattedCoord = coord['x'], coord['y'], coord['width'], coord['height']
								imageCoordinates.append(formattedCoord)

					coordinates.append(imageCoordinates)
				except:
					pass	

	duplicatedRegionData = list(zip(fileNames,coordinates))

	print(duplicatedRegionData)



	d = dict()

	for pair in duplicatedRegionData:
		if pair[0] in d:
			[d[pair[0]].append(r) for r in pair[1]]
		else:
			d[pair[0]] = pair[1]

	print('This is the length of d: {}'.format(len(d)))

	for key in d.keys():
		print(type(key))

	print(d['779'])

	return d

regionData = extractROIs(CSV_PATH)
#for img in regionData.keys():
#	print(img)

print('There are {} elements in our zooniverse list'.format(sum(1 for _ in regionData)))