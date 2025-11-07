import streamlit as st
import pandas as pd
import random
from openai import OpenAI

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Tribal Bazaar", page_icon="🪶", layout="wide")

# -------------------- OPENAI SETUP --------------------
openai_client = OpenAI(api_key="your_openai_api_key")  # replace with your API key

# -------------------- DATA STORAGE --------------------ompt = f"Write a short 3-line creative description for a handmade tribal product named '{name}' in the '{category}' category. Mention its cultural value and features like {keywords}."
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def generate_ai_image(category):
    """Generate AI image using OpenAI image model"""
    prompt = f"A realistic high-quality photo of an Indian tribal artisan-made {category}, detailed and vibrant."
    ai_image = openai_client.images.generate(model="gpt-image-1", prompt=prompt, size="512x512")
    return ai_image.data[0].url

# -------------------- HEADER --------------------
st.title("🪶 Tribal Bazaar")
st.subheader("Empowering Tribal Communities through Digital Commerce")

menu = st.sidebar.radio("Navigation", ["🏠 Home", "🛍️ Products", "➕ Add Product", "📈 Trending", "💡 AI Helper"])

# -------------------- HOME --------------------
if menu == "🏠 Home":
    st.image("https://images.unsplash.com/photo-1606152534829-6f8a7bffb403", use_container_width=True)
    st.markdown("""
    ### 🌿 Our Mission  
    Empowering tribal artisans to reach a global audience by showcasing their handmade crafts.  
    Supporting sustainability, culture, and livelihoods through technology.
    """)

# -------------------- ADD PRODUCT --------------------
elif menu == "➕ Add Product":
    st.header("🪴 Add a New Tribal Product")

    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        category = st.selectbox("Category", ["Handicraft", "Jewelry", "Textiles", "Art", "Food", "Other"])
        price = st.number_input("Price (₹)", min_value=10)
        keywords = st.text_input("Keywords (e.g., eco-friendly, bamboo, handmade)")
        image_url = st.text_input("Image URL (optional)")
        auto_desc = st.checkbox("✨ Generate AI Description")
        auto_image = st.checkbox("🎨 Generate AI Image")
        submit = st.form_submit_button("Add Product")

        if submit and name:
            desc = ""
            if auto_desc:
                with st.spinner("Generating AI description..."):
                    desc = generate_ai_description(name, category, keywords)
            else:
                desc = st.text_area("Enter Description")

            if not image_url and auto_image:
                with st.spinner("Generating AI image..."):
                    image_url = generate_ai_image(category)
            elif not image_url:
                image_url = "https://via.placeholder.com/150"

            new_product = pd.DataFrame({
                "Name": [name],
                "Category": [category],
                "Price": [price],
                "Description": [desc],
                "Image": [image_url],
                "Popularity": [random.randint(10, 100)]
            })
            st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
            st.success(f"✅ '{name}' added successfully!")

# -------------------- PRODUCTS --------------------
elif menu == "🛍️ Products":
    st.header("🧺 Browse Tribal Products")

    df = st.session_state.products
    if df.empty:
        st.warning("No products added yet! Add one from ➕ Add Product.")
    else:
        search = st.text_input("🔍 Search products by name or category")
        if search:
            df = df[df["Name"].str.contains(search, case=False) | df["Category"].str.contains(search, case=False)]

        for _, p in df.iterrows():
            with st.container():
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(p["Image"], width=180)
                with cols[1]:
                    st.subheader(p["Name"])
                    st.write(f"**Category:** {p['Category']}")
                    st.write(f"💰 Price: ₹{p['Price']}")
                    st.caption(p["Description"])
                    st.progress(p["Popularity"] / 100)

# -------------------- TRENDING --------------------
elif menu == "📈 Trending":
    st.header("🔥 Trending Products")
    df = st.session_state.products
    if df.empty:
        st.info("No products yet.")
    else:
        trending = df.sort_values(by="Popularity", ascending=False).head(5)
        for _, p in trending.iterrows():
            st.markdown(f"### {p['Name']} — ₹{p['Price']}")
            st.image(p["Image"], width=250)
            st.caption(p["Description"])
            st.progress(p["Popularity"] / 100)

# -------------------- AI HELPER --------------------
elif menu == "💡 AI Helper":
    st.header("🤖 AI Product Description Generator")

    product_name = st.text_input("Enter Product Name")
    category = st.selectbox("Select Category", ["Handicraft", "Jewelry", "Textiles", "Art", "Food", "Other"])
    keywords = st.text_input("Enter Keywords (eco-friendly, tribal art, etc.)")

    if st.button("✨ Generate Description"):
        if product_name:
            with st.spinner("Generating..."):
                desc = generate_ai_description(product_name, category, keywords)
            st.success("Here's your AI-generated product description:")
            st.write(desc)
        else:
            st.warning("Please enter a product name first.")
