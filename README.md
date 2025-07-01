# Snake AI

This repository contains a Python-based AI for the classic Snake game, utilizing a genetic algorithm to evolve neural networks that control the snake’s movements. Built with Pygame for game rendering and NumPy for neural network operations, the project trains a population of 2000 snakes over 50 generations to optimize strategies for eating fruit and avoiding collisions. The system is designed for scalability with multiprocessing and is applicable to adaptive control systems in manufacturing.

## Table of Contents
- [Snake AI](#snake-ai)
  - [Project Overview](#project-overview)
  - [Approach](#approach)
  - [Tools and Technologies](#tools-and-technologies)
  - [Results](#results)
  - [Skills Demonstrated](#skills-demonstrated)
  - [Setup and Usage](#setup-and-usage)
  - [References](#references)

## Project Overview
The Snake AI project implements a neuroevolution system to train an AI agent to play the classic Snake game. Each snake is controlled by a three-layer feedforward neural network (24 inputs, 48 hidden neurons, 4 outputs) evolved using a genetic algorithm. The snake navigates a 600x600 pixel grid (20x20 blocks), aiming to eat fruit while avoiding walls and self-collisions. The system trains a population of 2000 snakes over 50 generations, with fitness based on snake length and survival time. Multiprocessing enables parallel evaluation, and results are saved for analysis, making the approach applicable to optimizing dynamic processes in manufacturing.

## Approach
The project is structured as a modular neuroevolution system:
- **Game Environment (`main.py`)**: Implements the Snake game using Pygame, with a 20x20 block grid (30x30 pixels per block). Each snake moves in one of four directions (north, south, east, west) based on neural network decisions, growing when it eats fruit and dying on wall or self-collision.
- **Neural Network (`Brain` class)**: A three-layer feedforward neural network with 24 inputs (distance to fruit, self, and walls in eight directions), 48 hidden neurons, and 4 outputs (movement directions). Uses sigmoid activation and random weight initialization (-1.0 to 1.0).
- **Genetic Algorithm**:
  - **Population**: 2000 snakes per generation, each with a unique neural network.
  - **Fitness Function**: Combines snake length (200 points per fruit eaten) and survival time (up to 200 steps, +100 per fruit), encouraging growth and survival.
  - **Selection**: Top 25% of snakes (500) are selected for breeding based on fitness.
  - **Crossover and Mutation**: Breeds new snakes using single-point crossover (random row/column split) and mutation (1% chance of random weight adjustment). Includes 1% alpha clones and 30% alpha-random pairs for diversity.
  - **Evaluation**: Parallel game evaluation using Python’s `multiprocessing.Pool` for efficiency.
- **Game Mechanics**:
  - Snakes start at a fixed position (10,10 in block coordinates) with a minimum length of 4.
  - Fruit spawns randomly, avoiding snake bodies.
  - Snakes have a time-of-life (TOL) limit (200 steps, +100 per fruit, max 500), preventing infinite loops.
- **Result Storage**: Saves the best snake’s neural network weights per generation to `snake_data/<id>/`, with metrics (generation fitness, rate of change, alpha fitness/size) logged for analysis.

The system evolves snake behaviors by iteratively testing, selecting, and breeding high-performing snakes, optimizing for fruit consumption and survival.

## Tools and Technologies
- **Python**: Core language for game logic and neural network implementation.
- **Pygame**: Rendering the Snake game environment and handling user input.
- **NumPy**: Matrix operations for neural network processing and weight management.
- **multiprocessing**: Parallel evaluation of snake fitness for scalability.
- **Genetic Algorithm**: Custom implementation for evolving neural networks.
- **File I/O**: Saving neural network weights and generation metrics to text files.

## Results
- **Training**: Evolved 2000 snakes over 50 generations, optimizing neural networks for fruit consumption and collision avoidance.
- **Performance**: Achieved adaptive snake behaviors, with fitness scores based on length (200 points per fruit) and survival time (up to 500 steps). Specific metrics logged to `snake_data/<id>/`.
- **Scalability**: Leveraged multiprocessing to evaluate 2000 snakes in parallel, reducing training time (e.g., ~seconds per generation, depending on hardware).
- **Analysis**: Saved best snake’s neural network weights and generation statistics (mean fitness, rate of change, alpha fitness/size) for post-training analysis.

## Skills Demonstrated
- **Neuroevolution**: Designed a genetic algorithm to evolve neural networks, applicable to optimizing manufacturing control systems.
- **Game Development**: Built a Snake game environment with Pygame, handling real-time rendering and input.
- **Parallel Processing**: Implemented multiprocessing for efficient evaluation of large populations.
- **Data Processing**: Managed neural network weights and metrics using NumPy and file I/O.
- **Algorithm Design**: Developed a custom fitness function and crossover/mutation strategies for neuroevolution.
- **Optimization**: Balanced exploration (mutation) and exploitation (alpha cloning) for robust AI training.

## Setup and Usage
1. **Prerequisites**:
   - Clone the repository: `git clone https://github.com/Javen-W/snake-AI`
   - Install dependencies: `pip install pygame numpy`
   - Python 3.6+ required.
2. **Running**:
- Run the training: `python Evolutionary/main.py`
- Set `SHOW_GRAPHICS=True` in `main.py` to visualize the snake’s gameplay (reduces performance).
- Adjust parameters in `main.py`:
  - `POPULATION_SIZE`: Number of snakes per generation (default: 2000).
  - `MAX_GENERATIONS`: Number of generations (default: 50).
  - `MUTATION_RATE`: Weight mutation probability (default: 0.01).
  - `BREEDING_THRESHOLD`: Fraction of top snakes for breeding (default: 0.25).
  - `BLUEPRINT_SNAKE_ID`: Optional ID to load pre-trained snake weights.
3. **Notes**:
- Training without graphics (`SHOW_GRAPHICS=False`) uses multiprocessing for faster evaluation.
- Results are saved to `snake_data/<id>/` with a unique run ID.
- Ensure write permissions for `snake_data/` to store neural network weights.

## References
- [Pygame Documentation](https://www.pygame.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Python multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [Neuroevolution of Augmenting Topologies (NEAT)](https://nn.cs.utexas.edu/?stanley:ec02)
- [Genetic Algorithm for Snake AI](https://github.com/greerviau/SnakeAI)[](https://github.com/greerviau/SnakeAI)
