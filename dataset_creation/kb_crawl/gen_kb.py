import sys
import os
import csv

sys.path.append(os.getcwd())

import dataset_creation.kb_crawl.util.crawl as crawler

base_path = 'data/kb_crawl'

def read_materials(filename):
  path = os.path.join(base_path, filename)
  print(f'Reading from: {path}')
  with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    materials = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names: {", ".join(row)}')
            line_count += 1
        else:
          materials.append(row[0])
          line_count += 1
    print(f'Processed {line_count} lines')
  return materials
  
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

if __name__ == "__main__":
  materials = read_materials('example_materials_input.csv')
  print('Working...')
  materials_knowledge = crawler.crawl_comet_materials(materials)
  write_materials('example_materials_output.csv', materials_knowledge)