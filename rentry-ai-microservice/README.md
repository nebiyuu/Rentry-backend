# Rentry AI Microservice 🚀

A high-performance AI engine for a peer-to-peer rental marketplace, providing smart pricing, product recommendations, and automated quality control.

## 🧠 AI Features

### 1. Smart Pricing Engine (Machine Learning)
Uses **Linear Regression** with **Logarithmic Scaling** to predict fair rental prices. 
- **Tiered Logic:** Automatically adjusts rental percentages based on asset value (e.g., lower % for high-value cars vs. higher % for small electronics).
- **Fallback:** 5-section tiered logic for fail-safe pricing.

### 2. Product Recommendation (NLP)
Uses **Text Vectorization** and **Cosine Similarity** to suggest items to users.
- Analyzes product names and categories to find the best match for cross-selling.

### 3. Image Quality Validator (Computer Vision)
Uses **OpenCV** to ensure high-quality listings.
- **Blur Detection:** Uses Laplacian Variance math to detect out-of-focus photos.
- **Brightness Check:** Analyzes mean pixel intensity to flag photos that are too dark.

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Framework:** FastAPI (High-performance web API)
- **Libraries:** Scikit-Learn, OpenCV, Pandas, NumPy, Uvicorn

## 🚀 How to Run
1. Activate environment: `.\venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Start server: `python main.py`
4. View Documentation: Go to `http://localhost:8000/docs`