# Fourier Square Wave Visualizer

An interactive visualization demonstrating how Fourier series harmonics progressively approximate a perfect square wave using OpenGL.

## Overview

This project provides an engaging, real-time visualization of the mathematical concept of Fourier series. It shows how a series of sinusoidal waves (harmonics) can be combined to reconstruct complex periodic signals—specifically, a square wave. The visualization dynamically displays individual harmonics, their cumulative sum, and the resulting approximation of the target square wave.

## Features

- **Real-time Visualization**: Watch as harmonics are progressively added to approximate the square wave
- **Interactive Controls**: Adjust the number of harmonics, animation speed, and visualization parameters
- **OpenGL Rendering**: High-performance graphics for smooth animation
- **Educational Purpose**: Perfect for learning about Fourier analysis and signal processing
- **Dynamic Updates**: See how each additional harmonic improves the approximation

## Requirements

- Python 3.7+
- OpenGL-capable graphics card
- PyOpenGL
- NumPy
- Matplotlib (optional, for additional visualization features)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/binsec01/Fourier_Square_Wave_Visualizer.git
cd Fourier_Square_Wave_Visualizer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or manually install the required packages:
```bash
pip install PyOpenGL numpy matplotlib
```

## Usage

Run the main visualization:
```bash
python main.py
```

### Controls

- **Number of Harmonics**: Increase/decrease to see how many sine waves are needed for a good approximation
- **Speed**: Adjust animation speed to see the harmonics being added at your preferred pace
- **Reset**: Reset the visualization to start over
- **Exit**: Close the window to exit

## Mathematical Background

A square wave can be represented as an infinite sum of odd harmonic sine waves:

```
f(x) = (4/π) * Σ [sin(n*x) / n] for odd n = 1, 3, 5, 7, ...
```

The visualization shows:
1. Individual harmonic waves (each sine component)
2. The cumulative sum of harmonics
3. How the approximation converges to the ideal square wave

As more harmonics are included, the ripples (Gibbs phenomenon) appear near the discontinuities, which is a characteristic behavior of Fourier approximations of discontinuous functions.

## Project Structure

```
Fourier_Square_Wave_Visualizer/
├── README.md
├── requirements.txt
├── main.py
└── [additional source files]
```

## How It Works

1. **Harmonic Generation**: Sinusoidal waves at odd multiples of the fundamental frequency are calculated
2. **Summation**: These harmonics are summed together to approximate the square wave
3. **Rendering**: OpenGL renders the individual components and their combined result
4. **Animation**: The visualization progressively adds harmonics, showing the convergence in real-time

## Learning Objectives

This project helps understand:
- Fourier series and Fourier analysis
- Signal decomposition and reconstruction
- Harmonic content of periodic signals
- The Gibbs phenomenon in signal approximation
- Real-time visualization of mathematical concepts

## Performance

The visualization is optimized for smooth performance:
- Efficient harmonic calculations using NumPy
- Hardware-accelerated rendering with OpenGL
- Responsive UI that doesn't freeze during animation

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve the documentation
- Optimize the code
- Add new visualization modes

## License

This project is open source. Please see the LICENSE file for details.

## References

- [Fourier Series - Wikipedia](https://en.wikipedia.org/wiki/Fourier_series)
- [Square Wave - Wikipedia](https://en.wikipedia.org/wiki/Square_wave)
- [Gibbs Phenomenon - Wikipedia](https://en.wikipedia.org/wiki/Gibbs_phenomenon)

## Author

**binsec01**

## Troubleshooting

### OpenGL Issues
- Ensure your graphics drivers are up to date
- If OpenGL is not available, check your graphics card capabilities
- On some systems, you may need to install additional OpenGL libraries

### Performance Issues
- Reduce the number of harmonics displayed
- Lower the visualization resolution
- Close other applications to free up system resources

---

Enjoy exploring the fascinating world of Fourier analysis!
