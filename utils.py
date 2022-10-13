import csv
import json

CSV_ADS = 'datasets/ad.csv'
CSV_CATEGORIES = 'datasets/category.csv'
CSV_LOCATION = 'datasets/location.csv'
CSV_USER = 'datasets/user.csv'
json_filename = ('datasets/ad.json', 'datasets/category.json',
                 'datasets/location.json', 'datasets/user.json',
                 'datasets/location_mtm.json')


def csv_to_json(csv_name, json_name, model_name):
    mydata = []

    with open(csv_name, encoding='utf-8') as csvfile:
        csv_read = csv.DictReader(csvfile)

        for rows in csv_read:
            if 'Id' in rows:
                pk = int(rows['Id'])
                del rows['Id']
            if 'id' in rows:
                pk = int(rows['id'])
                del rows['id']
            if 'is_published' in rows:
                rows['is_published'] = True if rows['is_published'] == 'TRUE' else False
            if 'price' in rows:
                rows['price'] = int(rows['price'])
            if 'author_id' in rows:
                rows['author_id'] = int(rows['author_id'])
            if 'category_id' in rows:
                rows['category_id'] = int(rows['category_id'])
            if 'lat' and 'lng' in rows:
                rows['lat'], rows['lng'] = float(rows['lat']), float(rows['lng'])
            if 'age' in rows:
                rows['age'] = int(rows['age'])
            if 'location_id' in rows:
                #rows['locations'] = int(rows['location_id'])
                del rows['location_id']

            rows = {
                'model': model_name,
                'pk': pk,
                'fields': {**rows},
            }
            mydata.append(rows)

    with open(json_name, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(mydata, indent=2, ensure_ascii=False))


def csv_to_json_mtm(csv_name, json_name, model_name):
    data = []
    with open(csv_name, encoding='utf-8') as file_1:
        csv_read = csv.DictReader(file_1)

        for row in csv_read:
            if 'id' in row:
                pk = int(row['id'])
            if 'location_id' in row:
                location_id = int(row['location_id'])
            row = {
                'model': model_name,
                'pk': pk,
                'fields': {
                    'user_id': pk,
                    'location_id': location_id
                },
            }
            data.append(row)

    with open(json_name, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(data, indent=2, ensure_ascii=False))


csv_to_json(CSV_ADS, json_filename[0], 'ads.ad')
csv_to_json(CSV_CATEGORIES, json_filename[1], 'ads.category')
csv_to_json(CSV_LOCATION, json_filename[2], 'users.location')
csv_to_json(CSV_USER, json_filename[3], 'users.user')
#csv_to_json_mtm(CSV_USER, json_filename[4], 'users.user.location')
