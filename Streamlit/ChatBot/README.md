# ShopEasy Customer Support Chatbot

## About
A simple AI-powered customer support chatbot for ShopEasy.

It handles greetings, product questions, delivery, returns, refunds,
payment methods, order tracking, and unknown questions.

## Technologies
- Python
- Hugging Face Transformers
- google/flan-t5-base
- Gradio

## Files
- chatbot.py - chatbot logic and model
- app.py - Gradio interface
- policies.py - ShopEasy policies and sample orders
- requirements.txt - required libraries
- README.md - project information

## Installation
Open the terminal in this folder and run:

pip install -r requirements.txt

## Run
python app.py

Then open the Gradio link shown in the terminal.

## Sample order IDs
ORD1234 -> Shipped
ORD5678 -> Processing
ORD9012 -> Delivered

## Test questions
1. Hi
2. Where is my order?
3. Can I return my product?
4. When will I get my refund?
5. How long does delivery take?
6. Do you accept UPI?
7. Is Cash on Delivery available?
8. My payment failed.
9. Do you have laptops?
10. How can I contact customer support?
