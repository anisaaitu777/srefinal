from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from prometheus_client import make_asgi_app, Counter, Histogram
import time
import os

app = FastAPI(title="Production-Ready E-Commerce Platform")

# SRE Metrics
HTTP_REQUESTS_TOTAL = Counter("ecommerce_requests_total", "Total HTTP requests", ["method", "endpoint", "status_code"])
HTTP_REQUEST_DURATION = Histogram("ecommerce_request_duration_seconds", "HTTP latency", ["method", "endpoint"])

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# In-memory database
PRODUCTS = [
    {"id": 1, "name": "Developer Laptop", "price": 999, "image": "💻"},
    {"id": 2, "name": "4K UltraWide Monitor", "price": 399, "image": "🖥️"},
    {"id": 3, "name": "Mechanical Keyboard", "price": 89, "image": "⌨️"},
    {"id": 4, "name": "Wireless Gaming Mouse", "price": 49, "image": "🖱️"}
]
CART = []

# Get current Kubernetes Pod Name from environment variables
POD_NAME = os.getenv("HOSTNAME", "local-development-node")

def get_html_template(content: str):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>E-Commerce Cluster Platform</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #fffdf6; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            header {{ border-bottom: 2px solid #f0edd5; padding-bottom: 20px; margin-bottom: 20px; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; margin-top: 30px; }}
            .card {{ background: white; border: 1px solid #f0edd5; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .card-img {{ font-size: 48px; margin-bottom: 10px; }}
            .price {{ font-size: 20px; color: #b58900; font-weight: bold; margin: 10px 0; }}
            button {{ background-color: #f7f4cf; border: 1px solid #d4ce96; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; }}
            button:hover {{ background-color: #ece7b4; }}
            .cart-section {{ background: #fcfbe7; border: 1px solid #eadd9b; padding: 20px; border-radius: 8px; margin-top: 40px; }}
            footer {{ margin-top: 30px; border-top: 2px solid #f0edd5; padding-top: 15px; font-size: 13px; color: #666; }}
            .badge {{ background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            {content}
            <footer>
                <p><strong>SRE Infrastructure Context:</strong> Request handled by K8s Pod: <span class="badge">{POD_NAME}</span></p>
            </footer>
        </div>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def index_page():
    start_time = time.time()
    HTTP_REQUESTS_TOTAL.labels(method="GET", endpoint="/", status_code="200").inc()
    
    # Render Product Catalog
    products_html = ""
    for p in PRODUCTS:
        products_html += f"""
        <div class="card">
            <div class="card-img">{p['image']}</div>
            <h3>{p['name']}</h3>
            <div class="price">${p['price']}</div>
            <form action="/add-to-cart" method="post">
                <input type="hidden" name="product_id" value="{p['id']}">
                <button type="submit">Add to Cart</button>
            </form>
        </div>
        """
        
    # Render Cart
    cart_html = "<ul>"
    total_price = 0
    for item in CART:
        cart_html += f"<li>{item['name']} — ${item['price']}</li>"
        total_price += item['price']
    cart_html += "</ul>"
    
    content = f"""
    <header>
        <h1>💻 Microservice E-Commerce Cluster</h1>
    </header>
    <div class="grid">
        {products_html}
    </div>
    <div class="cart-section">
        <h2>🛒 Shopping Cart ({len(CART)} items)</h2>
        {cart_html if CART else "<p>Your cart is empty.</p>"}
        <h3>Total Price: ${total_price}</h3>
    </div>
    """
    HTTP_REQUEST_DURATION.labels(method="GET", endpoint="/").observe(time.time() - start_time)
    return get_html_template(content)

@app.post("/add-to-cart")
async def add_to_cart(product_id: int = Form(...)):
    HTTP_REQUESTS_TOTAL.labels(method="POST", endpoint="/add-to-cart", status_code="200").inc()
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        CART.append(product)
    return HTMLResponse(content="<script>window.location.href='/'</script>", status_code=200)

@app.get("/healthz")
async def health_check():
    return {"status": "UP"}