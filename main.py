from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import os

app = FastAPI()

# --- CONFIGURATION ---
FILE_NAME = "complaints.csv"
SEARCH_COLUMN = "Review"  # Now we search inside the Review text

@app.get("/")
def home():
    return {"message": "API is online. Go to /docs to search."}

@app.get("/search_reviews/")
def search_reviews(keyword: str = Query(..., description="Type 'good' or 'bad' to search in reviews")):
    
    # 1. Check if file exists
    if not os.path.exists(FILE_NAME):
        raise HTTPException(status_code=500, detail="CSV file not found.")

    try:
        # 2. Load the CSV
        df = pd.read_csv(FILE_NAME)
        df = df.fillna("") 

        # 3. Check if 'Review' column exists
        if SEARCH_COLUMN not in df.columns:
            raise HTTPException(status_code=500, detail=f"Column '{SEARCH_COLUMN}' not found.")

        # 4. FILTER: Find rows where the 'Review' contains the keyword (e.g., "good" or "bad")
        # case=False means "Bad", "bad", "BAD" all work.
        results = df[df[SEARCH_COLUMN].astype(str).str.contains(keyword, case=False, na=False)]

        # 5. SELECT COLUMNS: Only keep First Name, Last Name, and the Review itself
        # This filters the output so you don't get 50+ columns, just what you asked for.
        final_data = results[["First Name", "Last Name", "Review"]]

        return {
            "search_term": keyword,
            "count": len(final_data),
            "data": final_data.to_dict(orient="records") 
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
