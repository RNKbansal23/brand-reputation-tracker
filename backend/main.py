from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all the services we have created
from services import news_aggregator, sentiment_analyzer, database

# Create an instance of the FastAPI class
app = FastAPI(title="Brand Tracker API")

# --- CORS Middleware Setup ---
# This is crucial for allowing your React frontend (running on a different port)
# to communicate with this backend.
origins = [
    "http://localhost:5173",  # The default port for Vite React dev server
    "http://localhost:3000",
    "https://brand-reputation-tracker-ten.vercel.app"
      # A common port for other React dev servers
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Specifies the allowed origins
    allow_credentials=True,    # Allows cookies to be included in requests
    allow_methods=["*"],       # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],       # Allows all headers
)
# -----------------------------


@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Brand Tracker API!"}


@app.get("/api/fetch-and-store/{brand_name}")
def fetch_and_store_mentions(brand_name: str):
    """
    This endpoint acts as a trigger to fetch new data, process it,
    and store it in the database. It's the "worker" endpoint.
    """
    print(f"Received request to fetch new mentions for: {brand_name}")
    
    # Step 1: Fetch raw mentions from the news aggregator service
    mentions = news_aggregator.fetch_mentions(brand_name)
    
    if not mentions:
        print(f"No new mentions found for {brand_name}.")
        return {"message": f"No new articles found for {brand_name}."}

    # Step 2: Loop through each mention, analyze sentiment, and save to DB
    new_mentions_count = 0
    for mention in mentions:
        # Combine title and description for a more comprehensive analysis
        text_to_analyze = f"{mention.get('title', '')}. {mention.get('text', '')}"
        
        # Get sentiment from our analyzer service
        sentiment = sentiment_analyzer.analyze_sentiment(text_to_analyze)
        
        # Add the sentiment result back into the mention dictionary
        mention['sentiment'] = sentiment
        
        # Step 3: Save the fully processed mention to the database
        # The save_mention function handles checking for duplicates
        if database.save_mention(mention):
            new_mentions_count += 1
            
    print(f"Process complete. Saved {new_mentions_count} new mentions.")
    return {"message": f"Process complete. Found and saved {new_mentions_count} new mentions for {brand_name}."}


@app.get("/api/dashboard-mentions")
def get_dashboard_mentions():
    """
    This is the new, fast endpoint our frontend will use. It only reads
    from the database and does not call any external APIs.
    """
    print("Received request for dashboard mentions.")
    
    # Retrieve the latest 100 mentions from our database service
    recent_mentions = database.get_recent_mentions(limit=100)
    
    print(f"Returning {len(recent_mentions)} mentions to the dashboard.")
    return {"mentions": recent_mentions}