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
    writer.writerow(['material_1', 'material_2', 'property comparison'])
    
    for logic in knowledge:
      for mat_2 in logic.mat_2:
        writer.writerow([logic.mat_1, mat_2, logic.comp.name.lower() + ' ' + logic.prop.original])
  print('Completed')

def write_relations(filename, knowledge):
  path = os.path.join(base_path, filename)
  print(f'Writing to: {path}')
  with open(path, mode='w', newline='\n', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(['relation', 'property comparison'])
    
    for logic in knowledge:
      writer.writerow([logic.relation, logic.prop.original + ' ' + logic.comp.name.lower()])
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