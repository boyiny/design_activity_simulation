# Research Code

Welcome to our research code repository, accompanying our paper:

Design Activity Simulation: Opportunities and Challenges in Using Multiple Communicative AI Agents to Tackle Design Problems
Authors: [List of authors]
Published at: [Conference/Journal Name, Year]
[Link to paper / DOI]

## 📦 Design Activity Simulation

This is a multi-agent AI system that can automatically tackle design problems. 

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

Make sure you have: 
- Python ≥ 3.9.7 installed -> [Download here](https://www.python.org/downloads/)
- OpenAI API Key ready -> [Generate here](https://openai.com/index/openai-api/)

### Installation

1️⃣ **Clone the repository**
```bash
git clone git@github.com:boyiny/design_activity_simulation.git
cd design_activity_simulation
```

2️⃣ **(Recommended) Create a virtual environment**
```bash
python -m venv venv
# Activate on macOS/Linux
source venv/bin/activate
# OR activate on Windows
venv\Scripts\activate
```

3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the project
Run the main script
```bash
python main.py
```
Then you will see
```bash
Please input a design task: 
```
You can freely insert your design task. For example
```bash
Please input a design task: Design a virtual museum tour experience for remote visitors.
```
Please allow ~30min for AI agents tackling the design probelm for you. 

### Checking the result
You can find the system output in the "data/<timetag>" path.

## 🪪 License
This code is released under the **GNU Affero General Public License (AGPL v3)** for academic and non-commercial use. For commercial licensing, please contact:
```bash
by266@cam.ac.uk
```

## 💬 Citation
If you use this code in your research, please cite our paper:
```bash
@inproceedings{iflame2025,
  title={...},
  author={...},
  booktitle={...},
  year={2025}
}
```


