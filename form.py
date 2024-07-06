import requests
import pandas as pd
import streamlit as st

st.title("HoChu Finance Tracker")
st.info("""💰 Record your financial debauchery, track every single cent, uncover your spending habits.
        \n🛠️ App undergoing development and testing.""")

st.subheader("How to Use")
st.info("""🤓 Select your user.
        \n📝 Enter your transaction details in the fields below.
        \n➕ If you have multiple transactions to add, click the "Update" button after each transaction is recorded.
        \n✅ After you record all the transactions, click the "Submit" button to add the new data to the database.""")

if "transactions" not in st.session_state:
    st.session_state.transactions = {}

user = st.radio("Select user",
                options=["Ho", "Chu"]
)
item = st.text_input("Item")
mode_of_payment = st.radio("Mode of Payment", 
                            options=["💵 Cash", "💳 Credit Card"],
                            captions=["Ok lor you a lot of money lor", "So you wanna be in debt?"])
if mode_of_payment == "💳 Credit Card":
    mode_of_payment = "Credit Card"
    credit_card = st.selectbox("Choose your credit card, you baller", ("DBS Altitude", "HSBC Revolution"))
else:
    mode_of_payment = "Cash"
    credit_card = "Cash"
category = st.selectbox("Category", ("Meals", "Shopping", "Sports & Fitness", "Health", "Transport"))
amount = st.number_input("Amount Spent")
date = st.date_input("Date of Transaction", value="today").strftime('%d-%m-%Y')


if updated := st.button("Update"):
    if "user" not in st.session_state.transactions.keys():
        st.session_state.transactions["user"] = [user]
    else:
        st.session_state.transactions["user"].append(user)
        
    if "item" not in st.session_state.transactions.keys():
        st.session_state.transactions["item"] = [item]
    else:
        st.session_state.transactions["item"].append(item)
    
    if "mode_of_payment" not in st.session_state.transactions.keys():
        st.session_state.transactions["mode_of_payment"] = [mode_of_payment]
    else:
        st.session_state.transactions["mode_of_payment"].append(mode_of_payment)
    
    if "credit_card" not in st.session_state.transactions.keys():
        st.session_state.transactions["credit_card"] = [credit_card]
    else:
        st.session_state.transactions["credit_card"].append(credit_card)
    
    if "category" not in st.session_state.transactions.keys():
        st.session_state.transactions["category"] = [category]
    else:
        st.session_state.transactions["category"].append(category)

    if "amount" not in st.session_state.transactions.keys():
        st.session_state.transactions["amount"] = [amount]
    else:
        st.session_state.transactions["amount"].append(amount)
    
    if "date" not in st.session_state.transactions.keys():
        st.session_state.transactions["date"] = [date]
    else:
        st.session_state.transactions["date"].append(date)

st.subheader("Transactions Entered")
st.dataframe(data=st.session_state.transactions, use_container_width=True)

if st.session_state.transactions.keys():
    if submitted := st.button("Submit"):
        print(st.session_state.transactions)
        response = requests.post("http://127.0.0.1:8000/transactions/", json=st.session_state.transactions)

        if response.status_code == 200:
            st.success("Transactions added successfully!")
            st.rerun()
        else:
            st.error("Failed to add transaction!")