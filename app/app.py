from flask import Flask, render_template, request
from models.ohm_model import OHM

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    market_condition = request.form['market_condition']
    parameters = {
        'steps': 10,  # Set the number of steps as needed
        'economic_outlook_scenarios': market_condition
    }

    model = OHM(parameters)
    results = model.run()

    # Convert the DataFrame to an HTML table
    table_html = results.variables.OHM.to_html(classes='table table-striped', index=False)

    # Return the 'result.html' template with the HTML table
    return render_template('index.html', table_html=table_html)


if __name__ == '__main__':
    app.run(debug=True)