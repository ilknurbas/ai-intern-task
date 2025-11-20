# LLM Agent Framework

A Python framework powered by LangChain and multiple LLMs that routes customer queries to the correct agent and returns the response. The system supports two agents: FAQ Agent for general store questions and Order Status Agent for checking order status. An LLM-based router decides which agent should handle each query and then the system outputs the agent’s final answer.

The framework uses the specified LLM models as a router to determine the intent of each query and forward it to the appropriate agent. If the query is classified as Order Status, the agent searches for an order ID within the query and retrieves the corresponding order information from mock data. If the query is classified as FAQ, the agent performs semantic information matching against the FAQ dataset to find the most relevant answer. Once the agent’s response is generated, it is passed back through the LLM to make the output more natural and human‑like before being returned to the customer.


## Setup

1. Clone the repository and navigate to the project folder
   ```bash
   git clone https://github.com/ilknurbas/nordhealth-ai-intern-task.git
   cd nordhealth-ai-intern-task
   ```

2. Create and activate a virtual environment
   ```bash
   conda create -n myenv python=3.10
   conda activate myenv
   ```

3. Install dependencies

   Please check your system requirements depending on your Python version and OS.
   Some packages (e.g., grpcio) may fail to install with certain versions.

   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file in the root directory and configure API keys
   ```ini
   OPENAI_API_KEY = your_openai_api_key
   ANTHROPIC_API_KEY = your_anthropic_api_key
   GOOGLE_API_KEY = your_google_api_key
   TOGETHER_API_KEY = your_together_api_key
   ```
5. Run the script

   ```bash
   python main.py
   ```

## Project Structure
   
   ```bash
   .
   ├── data
   │   ├── faq_data.py
   │   ├── orders_data.py
   │   └── test_data.py
   ├── main.py
   ├── README.md
   ├── requirements.txt
   ├── solution
   │   ├── agent_responses.txt
   │   └── logs.txt

   ```
   - `data/`: sample inputs and test data
   - `main.py`: LangChain-based script
   - `requirements.txt`: dependencies 
   - `solution/`: generated outputs
     - `agent_responses.txt`: responses to each query
     - `logs.txt`: output used only for evaluation purposes
 

## Evaluation 

Selected criteria for evaluation are as follows:

- **Execution Time (ms):** Measures how long each model takes to process the queries in the test set and determine the intent. 
 
- **Routing Accuracy (%):** Indicates how often the model correctly identifies the query intent (FAQ vs Order Status) and routes it to the appropriate agent.

- **Cost per 1M tokens (USD):** Represents the combined cost of processing 1 million tokens with the model.


| Model Name                          | Execution Time (ms) | Routing Accuracy (%) | Cost per 1M tokens (USD) |
|-------------------------------------|---------------------|----------------------|--------------------------|
| GPT‑4o Mini                         | 41029.23            | 95.00                | 0.75                     |
| GPT‑3.5 Turbo                       | 32994.24            | 95.00                | 2.00                     |
| GPT‑5 Nano                          | 80977.73            | 95.00                | 0.45                     |
| Claude Haiku 4.5                    | 53650.53            | 95.00                | 6.00                     |
| Claude Sonnet 4.5                   | 133950.94           | 95.00                | 18.00                    |
| Gemini 2.5 Flash                    | 92478.96            | 95.00                | 2.80                     |
| Gemini 2.5 Flash‑Lite               | 21600.69            | 95.00                | 0.50                     |
| Meta LLaMA 3.1 8B Instruct Turbo    | 17854.01            | 95.00                | 0.18                     |
| LLaMA 4 Maverick Instruct (17Bx128E)| 34686.69            | 95.00                | 1.12                     |
| DeepSeek V3.1                       | 70722.72            | 95.00                | 2.30                     |
| Mixtral‑8x7B Instruct v0.1          | 41794.04            | 87.50                | 0.60                     |



## Conclusion 

Overall, the models achieved high accuracy rates for the task. This shows that they can reliably distinguish between query intents and route them correctly. Mixtral‑8x7B’s lower accuracy can be explained by the fact that, while all other models misclassified exactly two queries out of 40, Mixtral misclassified five in total. What makes these extra mistakes notable is that they were not simple intent misclassifications, but rather cases where the model did select the correct agent yet still appended extra text to the output, despite the prompt explicitly instructing it to generate only the agent name. Because this violated the strict output format, those responses were counted as incorrect.

The differences in execution times across models are primarily explained by their size, architecture, and optimization level. Smaller, lightweight models such as LLaMA‑3 8B or Gemini Flash‑Lite require fewer parameters and computations, which makes them faster to process queries. Mid‑sized models like GPT‑3.5 Turbo, GPT‑4o Mini, or Mixtral include more layers and complexity, so their execution times naturally increase. Large‑scale models such as Claude Sonnet, DeepSeek V3.1, GPT‑5 Nano, or Gemini Flash contain more parameters and deeper architectures, which demand significantly more computational resources and therefore result in much longer execution times. 

To sum up, all models except Mixtral reached 95% accuracy for this task, so the main differentiators are execution time and cost. LLaMA‑3 8B (17k ms, $0.18) and Gemini Flash‑Lite (21k ms, $0.50) stand out as the fastest and cheapest options, making them ideal. GPT‑3.5 Turbo (32k ms, $2.00) and LLaMA‑4 (34k ms, $1.12) are solid but more expensive. Overall, LLaMA‑3 8B and Gemini Flash‑Lite are the most efficient choices for this task, which makes sense given their smaller parameter sizes and optimized architectures designed for speed and efficiency.

As future work, the system could be extended by adding more specialized agents, integrating with real data sources such as APIs or databases, and evaluating performance on larger test sets. These steps would improve both the coverage and reliability of the intent classification framework.



