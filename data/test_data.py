test = [
    # FAQ
    {"query": "Do you have a return policy?", "intent": "FAQ-Agent"},
    {"query": "How long does delivery usually take?", "intent": "FAQ-Agent"},
    {"query": "What are the shipping methods you provide?", "intent": "FAQ-Agent"},
    {"query": "Can I pay with PayPal?", "intent": "FAQ-Agent"},
    {"query": "Can I pay with MobilePay?", "intent": "FAQ-Agent"},
    {"query": "What payment methods do you accept?", "intent": "FAQ-Agent"},
    {"query": "Do you sell gift cards?", "intent": "FAQ-Agent"},
    {"query": "You don't sell gift card, right?", "intent": "FAQ-Agent"},
    {"query": "Is there a student discount?", "intent": "FAQ-Agent"},
    {"query": "Do you ship to Canada?", "intent": "FAQ-Agent"},
    {"query": "Do you ship to Germany?", "intent": "FAQ-Agent"},
    {"query": "Do you provide refunds?", "intent": "FAQ-Agent"},

    {"query": "Can I send items back within a month?", "intent": "FAQ-Agent"},
    {"query": "I was wondering if after purchasing an item online, and then realizing two weeks later that I don’t "
              "actually need it, would I still be able to send it back?",
     "intent": "FAQ-Agent"},
    {"query": "How can I track my order?", "intent": "FAQ-Agent"},
    {"query": "How can I check if my order is delivered?", "intent": "FAQ-Agent"},
    {"query": "Do you offer free shipping for orders?", "intent": "FAQ-Agent"},
    {"query": "I want to know about returns", "intent": "FAQ-Agent"},
    {"query": "Do you have discounts?", "intent": "FAQ-Agent"},
    {"query": "Do you have a retunr polciy?", "intent": "FAQ-Agent"},  # typo on purpose

    # ORDER

    {"query": "Can you tell me the status of order #55551?", "intent": "Order-Status-Agent"},
    {"query": "Status for order 55551 please", "intent": "Order-Status-Agent"},
    {"query": "Order 55551 — what’s happening with it?", "intent": "Order-Status-Agent"},
    {"query": "Is my order 55557 ready for pickup?", "intent": "Order-Status-Agent"},
    {"query": "Has order 55559 been delivered yet?", "intent": "Order-Status-Agent"},
    {"query": "I’d like to know if my order 55551 has been processed?", "intent": "Order-Status-Agent"},

    {"query": "Check status of my order 55552 and 55552", "intent": "Order-Status-Agent"},
    {"query": "I want to check my order", "intent": "Order-Status-Agent"},
    {"query": "Has my order been shipped yet?", "intent": "Order-Status-Agent"},
    {"query": "Has my order #555 been shipped?", "intent": "Order-Status-Agent"},

    {"query": "Where is my package?", "intent": "Order-Status-Agent"},
    {"query": "Is my delivery on the way?", "intent": "Order-Status-Agent"},
    {"query": "Track my purchase", "intent": "Order-Status-Agent"},
    {"query": "Is the thing I ordered here yet?", "intent": "Order-Status-Agent"},
    {"query": "Did my stuff show up?", "intent": "Order-Status-Agent"},

    {"query": "I ordered something last week, can you tell me if it’s shipped?", "intent": "Order-Status-Agent"},
    {"query": "I bought a vacuum cleaner, is it on the way?", "intent": "Order-Status-Agent"},
    {"query": "Tell me about my last purchase", "intent": "Order-Status-Agent"},
    {"query": "Did my purchase go through?", "intent": "Order-Status-Agent"},
    {"query": "Is my delivry here?", "intent": "Order-Status-Agent"},  # typo on purpose
]