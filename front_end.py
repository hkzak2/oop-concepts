# front-end application with streamlit
import streamlit as st
from inventory_management import Product, Inventory


# streamlit config
st.set_page_config(
    page_title="Inventory Management",
    page_icon="📦",
    layout="wide",
)

# initialize empty list to store products
inventory = Inventory()

# create product objects with streamlit
product_name = st.text_input("Product Name")
product_price = st.number_input("Product Price", step=0.01)
product_quantity = st.number_input("Product Quantity", step=1)

# create product object
add_product = st.button("Add Product")

if add_product:
    product = Product(product_name, product_price, product_quantity)
    inventory.add_product(product)

# display inventory
for product in inventory.items:
    st.write(f"Product: {product.name} | Price: ${product.price} | Quantity: {product.quantity}")



# testing
# st.title("Inventory Management")

# st.text('This is my first applicaiton')

# st.latex(r''' e^{i\pi} + 1 = 0 ''')

# st.header('My header')

# st.subheader('My sub')

# st.code('for i in range(8): foo()')

# st.button('Click me')

# st.checkbox('I agree')

# with st.sidebar:
#     st.header('My sidebar')
#     st.radio('Radio', [1,2,3])