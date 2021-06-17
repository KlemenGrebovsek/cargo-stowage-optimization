# Cargo-stowage-optimization

The idea behind this project was to solve a problem of cargo stowage optimization with help of evolutionary algorithms. In addition to solving a given problem, the solution also offers a comparison of evolutionary algorithms.

**Limitations**
 - 2D representation of cargo space and package
 - Same dimension of all the pakcages

**Requirements**
 - Python 3.6+
 - Pip
 
**Dependencies**
  - NiaPy==2.0.0rc4
  - numpy
  - pillow
  - matplotlib
  - imageio
  
## Usage

**Generate and save new dataset**

```python
   dataset_generator = BaseDatasetGenerator()
   csv_writer = CSVDatasetWriter()

   # title, total packages, total stations, cargo space dimensions.
   dataset = dataset_generator.make('randomNameDataset', 30, 5, 5)

   csv_writer.write(dir_path=DATASET_DIR, file_name='randomNameDataset', dataset=dataset)
```

**Set and run simulation**

```python
   dataset = CSVDatasetReader().read(os.path.join(DATASET_DIR, 'testSet2.csv'))
simulation = Simulation(dataset=dataset)

simulation.add_algorithm('GeneticAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
simulation.add_algorithm('FlowerPollinationAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
simulation.add_algorithm('GreyWolfOptimizer', np=POPULATION_SIZE, n_fes=N_FES)
simulation.add_algorithm('ArtificialBeeColonyAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
simulation.add_algorithm('ParticleSwarmAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
simulation.add_algorithm('BatAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)

# create folder to store results
result_dir_path = os.path.join(RESULT_DIR, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.mkdir(path=result_dir_path)

simulation.add_save_option(ConsoleOutputSaveOption())
simulation.add_save_option(GraphOutputSaveOption(dir_path=result_dir_path, file_name='graph123'))
simulation.add_save_option(TextOutputSaveOption(dataset=dataset, dir_path=result_dir_path, file_name='textFile123'))
simulation.add_save_option(GifOutputSaveOption(dataset=dataset, dir_path=result_dir_path))

simulation.run(sort_by_best=SortAttribute.fitness)
```



