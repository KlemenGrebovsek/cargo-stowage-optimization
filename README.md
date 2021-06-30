# Cargo-stowage-optimization

The idea behind this project was to solve a problem of cargo stowage optimization with help of evolutionary algorithms.

**Main goals**
- Optimization of package placement in cargo space
- Comparison of evolutionary algorithms 

**Limitations**
 - 2D representation of cargo space and packages
 - Same dimensions for all packages 
 
**Requirements**
 - Python 3.6+
 - Pip
 
**Dependencies**
  - NiaPy==2.0.0rc4
  - numpy
  - pillow
  - matplotlib
  - imageio
  - marshmallow_dataclass
  
## Usage

**Configuration**

In most cases what we want to change are following properties:
- (dataset) - path to dataset
- (n_fes) - number of function evaluations
- (np) - population size
- (algorithms) - list names of evolutionary algorithms that will be included in simulation
 
Find more info about algoritms at: https://niapy.readthedocs.io/en/stable/api/algorithms.html

Sample config file:

```json
  {
    "dataset": "../datasets/testSet3.csv",
    "saveToDir" : "../results",
    "n_fes": 8000,
    "np": 50,
    "sortByBest": "fitness",
    "algorithms": [
      "GeneticAlgorithm",
      "GreyWolfOptimizer",
      "FlowerPollinationAlgorithm",
      "ArtificialBeeColonyAlgorithm",
      "ParticleSwarmAlgorithm",
      "BatAlgorithm"
    ],
    "outputOptions": [
      {
        "class": "ConsoleOutputOption",
        "included_kwargs": []
      },
      {
        "class": "GraphOutputOption",
        "included_kwargs": ["dir_path"]
      },
      {
        "class": "TextOutputOption",
        "included_kwargs": ["dir_path", "dataset"]
      },
      {
        "class": "GifOutputOption",
        "included_kwargs": ["dir_path", "dataset"]
      }
    ]
  }
```

**Output options**

Already existing output options should cover most cases, but you can define new ones by implementing following interface:

```python
class SaveOptionInterface:

    def save(self, simulation_results: list):
        """ Save simulation results.
        Args:
            simulation_results: A list of simulation results and best solution for each algorithm.
        Returns: void
        """
        pass
```

In case of adding custom output option don't forget to update config file and simulation output kwargs in simulation class constructor.

Simulation class is located at: src/core/simmulation/simulation.py

**Benchmarking**

Benchmark class is located at 'src/core/benchmark/benchmark.py'.

Currently defined formula to calculate solution fitness is probably not the most optimal.

Variables that can be included are: package movements,  layout distribution and weight distribution.

**Creating new dataset**

Method for generating new dataset is already implemented in main.py.
