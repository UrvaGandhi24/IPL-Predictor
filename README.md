# IPL Match Predictor - Full Stack Web Development Project

An AI-powered web application that predicts the win probability of IPL matches using machine learning.

## Features

- Real-time win probability prediction
- Interactive team selection with team logos
- Detailed match statistics
- Visual probability gauge
- Match situation analysis
- Responsive and modern UI
- DataSet Taken From : https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020?resource=download

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ipl-match-predictor.git
cd ipl-match-predictor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run Code\ Files/app.py
```

## Usage

1. Select the batting and bowling teams
2. Choose the match venue
3. Enter match details:
   - Target score
   - Current score
   - Overs completed
   - Wickets fallen
4. Click "Predict Win Probability" to get the analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
