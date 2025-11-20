import time
import os
import re
from data.test_data import test
from data.orders_data import orders
from data.faq_data import faq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_together import ChatTogether

# Load environment variables from a .env file.
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


MODEL_MAP = {
    "gpt4omini": ("openai", "gpt-4o-mini"),
    "gpt35turbo": ("openai", "gpt-3.5-turbo"),
    "gpt5nano": ("openai", "gpt-5-nano"),
    "claudehaiku": ("anthropic", "claude-haiku-4-5-20251001"),
    "claudesonnet": ("anthropic", "claude-sonnet-4-5-20250929"),
    "geminiflash": ("google", "gemini-2.5-flash"),
    "geminiflashlite": ("google", "gemini-2.5-flash-lite"),
    "llama318b": ("togetherai", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"),
    "llama4": ("togetherai", "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"),
    "deepseekv31": ("togetherai", "deepseek-ai/DeepSeek-V3.1"),
    "mistralai": ("togetherai", "mistralai/Mixtral-8x7B-Instruct-v0.1"),
}


class LLMRouter:
    # Manages intent routing by selecting the right agent (FAQ or Order) for customer queries
    def __init__(self, model_name: str, semantic_model: SentenceTransformer, faq_keys_embeddings):
        self.semantic_model = semantic_model
        self.faq_keys_embeddings = faq_keys_embeddings
        self.faq = faq
        self.orders = orders

        # Select the model based on the parameter
        provider, model = MODEL_MAP[model_name]

        if provider == "openai":
            self.llm = ChatOpenAI(
                model_name=model,
                temperature=0,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            self.llm = ChatAnthropic(
                model_name=model,
                temperature=0,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif provider == "google":
            self.llm = ChatGoogleGenerativeAI(
                model=model,
                temperature=0,
                api_key=os.getenv("GOOGLE_API_KEY")
            )
        elif provider == "togetherai":
            self.llm = ChatTogether(
                model=model,
                temperature=0,
                api_key=os.getenv("TOGETHER_API_KEY")
            )

        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system",
             """You are an intent router for a customer service bot.
             Your job is to analyze the user's query and based on the content decide which agent should respond.
             - Use 'FAQ-Agent' if the query is about general store information (e.g., policies). 
             - Use 'Order-Status-Agent' if the query is about checking the status of a specific order. 
             Return only one word: either 'FAQ-Agent' or 'Order-Status-Agent'. Do not generate any other text.
             """),
            ("human", "{query}")
        ])

    def route_queries(self, queries: list[str]):
        # Route a list of customer queries to the correct agent using the chosen LLM.
        outputs = []
        # keep tracks the time spent on LLM calls for test data
        total_time = 0

        # Iterate through all queries
        for q in queries:
            start = time.time()
            # Format the prompt with the question
            prompt = self.prompt_template.format_messages(query=q)
            # Send the prompt to the LLM and generate response
            response = self.llm.invoke(prompt)
            routed_intent = response.content.strip()
            end = time.time()
            total_time += (end - start) * 1000  # in ms

            # Retrieve agent response
            if routed_intent == "FAQ-Agent":
                agent_response = self.faq_agent(q)
            elif routed_intent == "Order-Status-Agent":
                agent_response = self.order_status_agent(q)
            else:
                agent_response = "Unknown intent."

            outputs.append({
                "query": q,
                "routed_intent": routed_intent,
                "agent_response": agent_response
            })

        return {
            "results": outputs,
            "total_time": total_time
        }

    def faq_agent(self, query: str) -> str:
        # Handles the query by finding the closest FAQ answer and generating a clear response

        if not self.faq or not self.faq_keys_embeddings.any():
            return "FAQ data is not available."

        # Encode query into embedding
        query_embedding = self.semantic_model.encode(query)
        # Find the most similar FAQ key to the query embedding
        scores = cos_sim(query_embedding, self.faq_keys_embeddings)[0]
        idx = scores.argmax().item()
        faq_keys = list(faq.keys())
        key = faq_keys[idx]
        ans = self.faq[key]

        # If the highest similarity score is below 0.2, treat it as no reliable FAQ match.
        # 0.2 is a threshold chosen to filter out weak matches; this value can be adjusted
        # depending on how strict you want the matching to be.
        if scores[idx].item() < 0.2:
            return "Sorry, we don't have an answer for that query. Please contact our support team."

        # Generate a clear, polite, conversational reply using FAQ answer
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             """ 
             The customer asked: "{query}".
             According to our company FAQ, the answer is: "{answer}".
             If the FAQ answer does not directly address the customer's question, 
             please understand what the FAQ answer actually covers,
             apply it logically to the query, and explain it shortly. 
             Do not leave unnecessary blank spaces and lines between the generated sentences.
              """),
            ("human", "{query}")
        ])
        prompt = prompt.format_messages(query=query, answer=ans)
        prompt_response = self.llm.invoke(prompt)

        return prompt_response.content.strip()

    def order_status_agent(self, query: str) -> str:
        # Check order status by extracting order IDs (numbers) from query
        numbers = re.findall(r"\d+", query)
        # remove duplicates
        numbers = set(numbers)
        matched_orders = []

        # If there are no orders at all
        if not self.orders:
            return "There are currently no orders in the system."

        # Check order IDs
        for order in self.orders:
            if order["id"] in numbers:
                matched_orders.append(
                    f"Order {order['id']} ({order['product']}) is {order['status']}."
                )
        if not matched_orders:
            return "Sorry, no matching order ID was found in the query."

        return " ".join(matched_orders)


def routing_accuracy(results: list[dict]) -> float:
    # Calculate accuracy of routed intents against expected intents
    tp = 0
    fp = []
    for i, r in enumerate(results):
        if r["routed_intent"] == test[i]["intent"]:
            tp += 1
        else:
            fp.append(i+1)

    # also return the mislabelled query numbers
    return (tp / len(test)) * 100, fp


def main():
    # Encode FAQ keys into embeddings for semantic search
    semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
    faq_keys = list(faq.keys())
    faq_keys_embeddings = semantic_model.encode(faq_keys)

    os.makedirs("solution", exist_ok=True)
    # Create file to save agent responses
    with open("solution/agent_responses.txt", "w", encoding="utf-8"):
        pass

    # Create file for evaluation
    with open("solution/logs.txt", "w", encoding="utf-8") as f:
        f.write("--- Model Comparison ---\n")
        f.write("Model Name | Execution Time (ms) | Accuracy (%) | Misclassified Query No\n")

    # Run routing logic for each predefined LLM model
    for model in MODEL_MAP.keys():
        router = LLMRouter(model, semantic_model, faq_keys_embeddings)
        evaluation = router.route_queries([t["query"] for t in test])

        print("Model:", model)
        # debugging purposes
        # for i, item in enumerate(evaluation["results"]):
        #     print(f"[{i}] query:", item["query"])
        #     print(f"[{i}] routed_intent:", item["routed_intent"])
        #     print(f"[{i}] agent_response:", item["agent_response"])
        # print("Total execution time in ms:", f"{evaluation['total_time']:.2f}")

        # Calculate the routing accuracy
        accuracy, misclassified = routing_accuracy(evaluation["results"])

        # Append agent responses into a text file
        with open("solution/agent_responses.txt", "a", encoding="utf-8") as f:
            f.write(f"--- Agent responses for model: {model} ---\n")
            for i, item in enumerate(evaluation["results"], start=1):
                f.write(f"{i}. {item['agent_response']}\n")

        # Append results to comparison file
        with open("solution/logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{model} | {evaluation['total_time']:.2f} | {accuracy:.2f} | {misclassified}\n")

    print("Customer service bot is complete. Check 'solution/agent_responses.txt' in your directory for the agent "
          "responses.")


if __name__ == "__main__":
    main()
