import streamlit as st
from duckduckgo_search import DDGS
from swarm import Swarm, Agent
from datetime import datetime
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
MODEL = "llama3.2:latest"
client = Swarm()

# Streamlit configuration
st.set_page_config(
    page_title="SA Smart Shopping Agent",
    page_icon="🛒",
    layout="wide"
)

st.title("South African Smart Shopping Assistant")

def search_sa_prices(item):
    """Search for product prices across South African retailers"""
    try:
        with DDGS() as ddg:
            # Search for current prices including major SA retailers
            results = ddg.text(
                f"{item} price South Africa Makro Checkers Shoprite Woolworths PnP {datetime.now().strftime('%Y-%m')}", 
                max_results=5
            )
            if results:
                price_results = "\n\n".join([
                    f"Store: {result['title'].split('-')[0].strip()}\nProduct: {result['title']}\nURL: {result['href']}\nDetails: {result['body']}\nTimestamp: {datetime.now().strftime('%Y-%m-%d')}" 
                    for result in results
                ])
                return price_results
            return f"No price information found for {item}."
    except Exception as e:
        logger.error(f"Error in search_sa_prices: {str(e)}")
        return f"Error searching prices: {str(e)}"

# Enhanced Agent Definitions for SA Market
price_search_agent = Agent(
    name="SA Price Searcher",
    instructions="""
    You are a specialized price comparison agent for South African grocery stores.
    
    PRIMARY TASK:
    - Find current prices across major SA retailers
    - Focus on Makro, Checkers, Shoprite, Woolworths, Pick n Pay, and other SA chains
    - Compare unit prices and special offers
    
    SEARCH PARAMETERS:
    - Current prices in South African Rand (ZAR)
    - Include Smart Shopper, Xtra Savings, and WRewards specials
    - Consider store locations and stock availability
    
    PROCESS:
    1. Price Search:
       - Search each major SA retailer
       - Include both in-store and online prices
       - Note any promotions (e.g., Checkers Sixty60 specials)
    
    2. Data Processing:
       - Extract exact prices in ZAR
       - Calculate unit prices
       - Note any quantity limitations
       - Include loyalty program benefits
    
    3. Output Formation:
       - Store name and location options
       - Exact product name, brand, and size
       - Current price and any discounts
       - Loyalty program benefits
    
    ERROR HANDLING:
    - Report when prices are unavailable
    - Note if prices may vary by region
    - Indicate when prices are estimates
    """,
    functions=[search_sa_prices],
    model=MODEL
)

analysis_agent = Agent(
    name="SA Price Analyzer",
    instructions="""
    You are an expert price analysis agent specializing in South African grocery prices.
    
    PRIMARY TASK:
    - Compare prices across SA stores
    - Identify best deals and savings
    - Consider loyalty programs (Smart Shopper, Xtra Savings, WRewards)
    
    ANALYSIS STEPS:
    1. Price Comparison:
       - Compare unit prices in ZAR
       - Account for package sizes
       - Consider bulk discounts (especially at Makro)
    
    2. Deal Analysis:
       - Evaluate current specials
       - Calculate potential savings
       - Consider loyalty program benefits
       - Include delivery options (e.g., Sixty60, PnP asap)
    
    3. Shopping Optimization:
       - Group items by store
       - Consider fuel costs
       - Account for store proximity
       - Factor in delivery fees vs travel costs
    
    OUTPUT REQUIREMENTS:
    - Best price per item in ZAR
    - Total potential savings
    - Recommended shopping plan
    - Loyalty program recommendations
    
    FORMAT:
    - Clear price breakdowns
    - Savings calculations
    - Store recommendations by region
    """,
    model=MODEL
)

recommendation_agent = Agent(
    name="SA Shopping Advisor",
    instructions="""
    You are a smart shopping advisor helping South African consumers make optimal purchasing decisions.
    
    PRIMARY TASK:
    - Create practical shopping recommendations for SA stores
    - Balance price savings with convenience
    - Provide actionable shopping plans
    
    CONTENT REQUIREMENTS:
    1. Shopping Plan:
       - Best store for each item
       - Total cost comparison in ZAR
       - Estimated savings
       - Alternative options
       - Delivery vs in-store comparison
    
    2. Additional Considerations:
       - Loyalty programs benefits
       - Bulk buying at Makro
       - Special promotional days
       - Store proximity and delivery zones
       - Load shedding impact on shopping
    
    FORMAT SPECIFICATIONS:
    - Clear store recommendations
    - Price breakdown in ZAR
    - Savings summary
    - Shopping and delivery tips
    
    OUTPUT REQUIREMENTS:
    - Practical recommendations
    - Clear cost comparisons
    - Time and money saving tips
    - Regional availability notes
    """,
    model=MODEL
)

def process_shopping_list(items):
    """Process shopping list and find best deals across SA stores"""
    try:
        with st.status("Processing shopping list...", expanded=True) as status:
            # Price Search Phase
            status.write("🔍 Searching for prices...")
            all_prices = []
            for item in items:
                search_response = client.run(
                    agent=price_search_agent,
                    messages=[{"role": "user", "content": f"Find current prices for {item} in South African stores"}]
                )
                all_prices.append(search_response.messages[-1]["content"])
            
            raw_prices = "\n\n---\n\n".join(all_prices)
            
            # Analysis Phase
            status.write("💰 Analyzing prices...")
            analysis_response = client.run(
                agent=analysis_agent,
                messages=[{
                    "role": "user",
                    "content": f"Analyze these South African prices and find the best deals:\n{raw_prices}"
                }]
            )
            price_analysis = analysis_response.messages[-1]["content"]
            
            # Recommendation Phase
            status.write("📋 Creating shopping plan...")
            recommendation_response = client.run(
                agent=recommendation_agent,
                messages=[{
                    "role": "user",
                    "content": f"Create a shopping plan for South African stores based on this analysis:\n{price_analysis}"
                }]
            )
            
            status.write("✅ Analysis complete!")
            return raw_prices, price_analysis, recommendation_response.messages[-1]["content"]
            
    except Exception as e:
        logger.error(f"Error in process_shopping_list: {str(e)}")
        raise Exception(f"Shopping list processing failed: {str(e)}")

# Enhanced User Interface
st.markdown("""
    ### 🛒 South African Smart Shopping Assistant
    Enter your shopping list to find the best deals across SA stores:
    - Compares prices across Makro, Checkers, Shoprite, Woolworths, and Pick n Pay
    - Finds the best deals and savings
    - Creates an optimal shopping plan
    - Considers loyalty programs and delivery options
""")

# Initialize session state for shopping list
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []

# User Input Section with improved list management
col1, col2 = st.columns([3, 1])
with col1:
    new_item = st.text_input("Add item to shopping list:", key="item_input")
    if st.button("Add Item"):
        if new_item:
            st.session_state.shopping_list.append(new_item)
            st.rerun()

# Display and manage shopping list
st.write("### Your Shopping List:")
for idx, item in enumerate(st.session_state.shopping_list):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"{idx + 1}. {item}")
    with col2:
        if st.button("Remove", key=f"remove_{idx}"):
            st.session_state.shopping_list.pop(idx)
            st.rerun()

# Action buttons
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    if st.button("Clear List"):
        st.session_state.shopping_list = []
        st.rerun()
with col2:
    process_button = st.button("Find Best Deals", type="primary")

# Optional region selection for more accurate results
region_options = [
    "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", 
    "Free State", "Mpumalanga", "North West", "Limpopo", "Northern Cape"
]
selected_region = st.selectbox("Select your region for more accurate prices:", region_options)

# Processing Section
if process_button:
    if st.session_state.shopping_list:
        try:
            raw_prices, price_analysis, shopping_plan = process_shopping_list(st.session_state.shopping_list)
            
            # Results Display
            st.header(f"🛍️ Shopping Analysis for {selected_region}")
            
            # Shopping Plan Tab
            st.subheader("Recommended Shopping Plan")
            st.info("💡 Prices shown include standard loyalty program discounts where applicable")
            st.markdown(shopping_plan)
            
            # Loyalty Program Summary
            st.subheader("Loyalty Program Benefits")
            with st.expander("View Available Discounts"):
                st.markdown("""
                    - **Checkers Xtra Savings**: Current specials and personalized discounts
                    - **Pick n Pay Smart Shopper**: Points and personalized discounts
                    - **Woolworths WRewards**: Member pricing and special offers
                    - **Makro mCard**: Bulk buying benefits and special pricing
                """)
            
            # Detailed View
            with st.expander("View Detailed Analysis"):
                tabs = st.tabs(["Price Analysis", "Raw Price Data"])
                
                with tabs[0]:
                    st.markdown("### 💰 Price Analysis")
                    st.markdown(price_analysis)
                
                with tabs[1]:
                    st.markdown("### 🔍 Raw Price Data")
                    st.markdown(raw_prices)
            
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")
            logger.error(f"Processing error: {str(e)}")
    else:
        st.error("Please add items to your shopping list!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Smart Shopping SA | Built with Streamlit</p>
        <p>Prices and availability may vary by region and store</p>
    </div>
""", unsafe_allow_html=True)