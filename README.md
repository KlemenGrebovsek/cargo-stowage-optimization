# Cargo-stowage-optimization

The idea behind this project was to solve a problem of cargo stowage optimization with help of evolutionary algorithms. In addition to solving a given problem, the solution also offers a comparison of  selected evolutionary algorithms. There are some limitations of this project like 2d representation of cargo space and same dimension of all the pakcages.

<br />

## Requirements
 - Python 3.6+
 - Pip
 
**Dependencies**
  - NiaPy==2.0.0rc4
  - numpy
  - pillow
  - matplotlib
  - imageio

<br />

## Usage

**General settings**

- DATA_SET_NAME -> Indicates dataset which will be used for optimization.

**Optimization settings**

- POPULATION_SIZE -> Indicates population size in evolutionary algorithms (np).
- NUMBER_OF_EVALUATIONS -> Indicates number of evaluations per solution (nfes)
- ALGORITHM_LIST -> Indicates algorithms which will be used for solving problem. Link : https://niapy.readthedocs.io/en/1.0.0rc2/api/algorithms.html

**Output settings**

- SAVE_TO_TXT -> Generate text file, which contains optimization results and settings. (True/False)
- CREATE_VISUALIZATION_GIF -> Generate gif file, which contains image of cargo space at each station. (True/False)
- CREATE_COMPARISON_GRAPH -> Generate comparison graph for solutions of selected algorithms. (True/False)

**Main functionalities**

Run optimization : 
```python
if __name__ == '__main__':
    run_optimization()
```

Generate new dataset : 
- Minimal number of total packages: 30
- Minimal number of stations: 5
- Cargo space width must be equivalent to height. e.g.(5x5, 3x3, ...)
- Size of cargo space must be greater than 80% of total packages.

```python
if __name__ == '__main__':
    create_new_dataset('datasetName', number-of-packages, number-of-stations, cargoS-width, cargoS-height)
```
<br />

## Disclaimer
The goal of this project is not optimization of evolutionary algorithms, but an example of solving cargo stowage problem.

