# front-end application with streamlit
import streamlit as st
from inventory_management import Product, Inventory


# streamlit config
st.set_page_config(
    page_title="Inventory Management",
    page_icon="📦",
    layout="wide",
)


with st.sidebar:
    menu = st.radio("Menu", ["Home", "Inventory", "About"])

if menu == "Home":
    st.title("Home")
    st.write("Welcome to the Inventory Management System")

    st.session_state['agree'] = st.button("Do you agree to the terms and conditions?")

    if st.session_state['agree']:
        
        st.success("Thank you for agreeing to the terms and conditions.")
    else:
        st.warning("You must agree to the terms and conditions.")

elif menu == "Inventory":

# streamlit app with emoji
    st.title("Inventory Management System 📦")

    st.write("Welcome to the Inventory Management System")

    # initialize session state
    if "inventory" not in st.session_state:
        st.session_state.inventory = Inventory()

    # create product objects with streamlit
    product_name = st.text_input("Product Name")
    product_price = st.number_input("Product Price", step=0.01)
    product_quantity = st.number_input("Product Quantity", step=1)

    # create product object
    add_product = st.button("Add Product")

    if add_product:
        product = Product(product_name, product_price, product_quantity)
        st.session_state.inventory.add_product(product)

    # display inventory
    if st.session_state.inventory.items:
        st.write("Inventory:")
        for product in st.session_state.inventory.items:
            st.write(f"Product: {product.name} | Price: ${product.price} | Quantity: {product.quantity}")
    else:
        st.write("Inventory is empty.")

