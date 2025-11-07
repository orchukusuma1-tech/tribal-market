import streamlit as st
import pandas as pd
import openai
import requests

# ---------------------------
# SETUP
# ---------------------------
st.set_page_config(page_title="Tribal Bazaar", page_icon="🪶", layout="wide")

# Load API key from secrets (safer)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------------------
# AI HELPERS
# ---------------------------

def generate_ai_description(name, category, keywords):
    """Generate a creative AI description for the product"""
    prompt = f"Write a short 3-line creative description for a handmade tribal product named '{name}' in the '{category}' category. Mention its cultural value and features like {keywords}."
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()


def generate_ai_image(category):
    """Generate a product image using OpenAI's image model"""
    prompt = f"A realistic high-quality photo of an Indian tribal artisan-made {category}, detailed and vibrant."
    image = openai.Image.create(
        prompt=prompt,
        model="gpt-image-1",
        size="512x512"
    )
    return image["data"][0]["url"]

# ---------------------------
# STREAMLIT APP
# ---------------------------

st.title("🪶 Tribal Bazaar – Empowering Indigenous Artisans")
st.write("Support tribal artisans by exploring unique handmade products infused with culture and heritage.")

# Initialize product list
if "products" not in st.session_state:
    st.session_state["products"] = []

# Product upload section
st.subheader("🧺 Add New Tribal Product")

with st.form("add_product"):
    name = st.text_input("Product Name")
    category = st.selectbox("Category", ["Handicraft", "Jewelry", "Textile", "Home Decor", "Art", "Other"])
    price = st.number_input("Price (₹)", min_value=50, step=10)
    keywords = st.text_input("Product Features / Keywords")
    submit = st.form_submit_button("✨ Add Product")

    if submit and name:
        with st.spinner("Generating AI description and image..."):
            description = generate_ai_description(name, category, keywords)
            image_url = generate_ai_image(category)
        st.session_state["products"].append({
            "name": name,
            "category": category,
            "price": price,
            "description": description,
            "image": image_url
        })
        st.success(f"Product '{name}' added successfully!")

# ---------------------------
# Display Marketplace
# ---------------------------
st.subheader("🛍️ Tribal Marketplace")

if st.session_state["products"]:
    for product in st.session_state["products"]:
        with st.container():
            cols = st.columns([1, 2])
            with cols[0]:
                st.image(product["image"], use_container_width=True)
            with cols[1]:
                st.markdown(f"### {product['name']}")
                st.markdown(f"**Category:** {product['category']}")
                st.markdown(f"**Price:** ₹{product['price']}")
                st.markdown(product["description"])
                st.button("❤️ Support Artisan", key=product["name"])
else:
    st.info("No products yet. Add one above to get started!")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("💡 *Built with Streamlit + OpenAI to promote tribal entrepreneurship.*")
