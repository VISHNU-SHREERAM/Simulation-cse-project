# Predator-Prey Ecological Simulation

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-pygame%2Fmatplotlib-blue)

A visual simulation modeling the volatile dynamics traversing human and lion populations in a bounded 3D graphical landscape. It analyzes individual movements, demographic reproduction scaling, and interactive mortality vectors over iterative temporal periods.

## Table of Contents
- [Tech Stack & Architecture](#tech-stack--architecture)
- [Prerequisites](#prerequisites)
- [Installation & Local Setup](#installation--local-setup)
- [Usage & Running the App](#usage--running-the-app)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing Guidelines](#contributing-guidelines)
- [License and Contact](#license-and-contact)

## Tech Stack & Architecture

- **Visualizations**: Intersects `matplotlib` (3D graphing and slider UI) combined with `pygame` (audio bridging and rendering pipelines).
- **Computations**: Employs heavily optimized vectorized datasets mapping entities (`numpy`).
- **Data Models**: Structurally decoupled instances of `Person` and `Lion` interacting natively based on spatial coordinate proximity thresholds (range attributes).

**Architecture**: Both humans and lions exist on a unified plane where their distance dictates interactive logic (fleeing or hunting). Aggregative calculations simultaneously scale the harvest capabilities against environmental triggers (Rain, Disaster chance).

## Prerequisites

- Python 3.8+ globally installed.
- Appropriate audio playback drivers installed native to OS for PyGame audio streams.

## Installation & Local Setup

```bash
git clone https://github.com/VISHNU-SHREERAM/Simulation-cse-project.git
cd Simulation-cse-project
pip install -r requirements.txt
```

## Usage & Running the App

Execute the finalized simulation script encapsulating the 3D grid and interactive plotting parameters. (Caution: Adjust spatial zooming using the `ax.dist` bounds if viewing natively on smaller monitors.)

```bash
python "FINAL SIMULATION.py"
```

### Controls
The simulation interface leverages interactive Matplotlib Widgets: 
- `Pause` / `Play` animations seamlessly.
- Granular data metric generation on localized speed, range, and evolutionary adaptations visible in real-time nested subplots.

## Testing

No structured QA testing is currently orchestrated natively. The system outputs deterministic logging when encountering fatal array boundaries.

## Deployment

Intended strictly as an analytical desktop instance run natively through Python virtual environments. 

## Contributing Guidelines
The development spans multiple paths logged throughout discrete branch trees (`main` vs `master` methodologies). 
1. Branch from `master` (`git checkout -b simulation-tweaks`)
2. Format code and ensure matrix boundary exceptions operate natively within the matplotlib wrapper.

## License and Contact
- **Authors**: Vishnu Shreeram MP, G.Sai Rohith, Vaibhav Yadav
- **Organization**: CSE Projects
