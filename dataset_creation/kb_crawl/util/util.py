import os
import csv

base_path = 'data/kb_crawl'

def read_file(filename):
  path = os.path.join(base_path, filename)
  print(f'Reading from: {path}')
  with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    properties = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names: {", ".join(row)}')
            line_count += 1
        else:
          properties.append(row[0])
          line_count += 1
    print(f'Processed {line_count} lines')
  return properties
  
def write_materials(filename, knowledge):
  path = os.path.join(base_path, filename)
  print(f'Writing to: {path}')
  with open(path, mode='w', newline='\n', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(['material_1', 'material_2', 'property comparison', 'material_1 token', 'material_2 token', 'property token'])
    
    for logic in knowledge:
      for mat_2_i, mat_2 in enumerate(logic.mat_2):
        writer.writerow(
          [
            logic.mat_1.name, 
            mat_2.name, 
            logic.comp.name.lower() + ' ' + logic.prop.original.name, 
            logic.mat_1.token, 
            logic.mat_2[mat_2_i].token,
            logic.prop.original.token
          ]
        )
  print('Completed')

def write_relations(filename, knowledge):
  path = os.path.join(base_path, filename)
  print(f'Writing to: {path}')
  with open(path, mode='w', newline='\n', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(['relation', 'property comparison', 'relation token', 'property token'])
    
    for logic in knowledge:
      writer.writerow(
        [
          logic.relation.name, 
          logic.prop.original.name + ' ' + logic.comp.name.lower(),
          logic.relation.token,
          logic.prop.original.token
        ]
      )
  print('Completed')

def write_properties(filename, knowledge):
  path = os.path.join(base_path, filename)
  print(f'Writing to: {path}')
  with open(path, mode='w', newline='\n', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(['property', 'property comparison'])
    
    for logic in knowledge:
      writer.writerow([logic.property, logic.comp.name.lower() + ' ' + logic.prop.original])
  print('Completed')

def write_comparisons(filename, knowledge):
  path = os.path.join(base_path, filename)
  print(f'Writing to: {path}')
  with open(path, mode='w', newline='\n', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(['property comparison', 'property comparison'])
    
    for logic in knowledge:
      writer.writerow([logic.property_comparison, logic.comp.name.lower() + ' ' + logic.prop.original])
  print('Completed')