import streamlit as st
import pandas as pd
import os

# Load or create CSV file
def load_data():
    file_path = "veg_indian_meals.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Dish Name", "Cuisine", "Meal Type", "Comfort Food", "Masala Food", "Dessert", 
                                     "Spice Level", "Cooking Time", "Mood-Based", "Weather-Based", "Dietary", 
                                     "Occasion", "Region"])

data = load_data()

st.title("🍲 Indian Veg Food Recommender")

# Create Tabs
tab1, tab2 = st.tabs(["🍽️ Recommend Food", "📋 Manage Food List"])

# Tab 1: Recommend Food
with tab1:
    st.header("Get a Food Suggestion for Today")

    col1, col2 = st.columns(2)

    with col1:
        meal_type = st.selectbox("Select Meal Type", sorted(data["Meal Type"].dropna().unique()))
        spice_level = st.selectbox("Select Spice Level", sorted(data["Spice Level"].dropna().unique()))
        weather = st.selectbox("Weather", sorted(data["Weather-Based"].dropna().unique()))

    with col2:
        comfort = st.checkbox("Comfort Food")
        masala = st.checkbox("Masala Food")
        dessert = st.checkbox("Dessert")

    # Filter logic
    filtered = data[
        (data["Meal Type"] == meal_type) &
        (data["Spice Level"] == spice_level) &
        (data["Weather-Based"] == weather)
    ]

    if comfort:
        filtered = filtered[filtered["Comfort Food"] == True]
    if masala:
        filtered = filtered[filtered["Masala Food"] == True]
    if dessert:
        filtered = filtered["Dessert"] == True

    st.subheader("Suggested Dishes:")
    if not filtered.empty:
        st.table(filtered[["Dish Name", "Cuisine", "Region"]])
    else:
        st.info("No dishes found. Try different filters.")

# Tab 2: Manage Food List
with tab2:
    st.header("Manage Food List")

    action = st.selectbox("Action", ["Read", "Add", "Update", "Delete"])

    if action == "Read":
        st.subheader("Current Food List")
        st.dataframe(data)

    elif action == "Add":
        st.subheader("Add a New Dish")
        with st.form("add_form"):
            new_row = {
                "Dish Name": st.text_input("Dish Name"),
                "Cuisine": st.selectbox("Cuisine", sorted(data["Cuisine"].dropna().unique().tolist() + ["Other"])),
                "Meal Type": st.selectbox("Meal Type", sorted(data["Meal Type"].dropna().unique().tolist() + ["Other"])),
                "Comfort Food": st.checkbox("Comfort Food"),
                "Masala Food": st.checkbox("Masala Food"),
                "Dessert": st.checkbox("Dessert"),
                "Spice Level": st.selectbox("Spice Level", ["Mild", "Medium", "Hot"]),
                "Cooking Time": st.selectbox("Cooking Time", ["Quick", "Moderate", "Elaborate"]),
                "Mood-Based": st.selectbox("Mood-Based", sorted(data["Mood-Based"].dropna().unique().tolist() + ["Other"])),
                "Weather-Based": st.selectbox("Weather-Based", sorted(data["Weather-Based"].dropna().unique().tolist() + ["Other"])),
                "Dietary": st.selectbox("Dietary", ["Veg"]),
                "Occasion": st.selectbox("Occasion", sorted(data["Occasion"].dropna().unique().tolist() + ["Other"])),
                "Region": st.selectbox("Region", sorted(data["Region"].dropna().unique().tolist() + ["Other"]))
            }
            submitted = st.form_submit_button("Add Dish")
            if submitted:
                data.loc[len(data)] = new_row
                data.to_csv("veg_indian_meals.csv", index=False)
                st.success("Dish added successfully!")

    elif action == "Update":
        st.subheader("Update Existing Dish")
        dish_to_update = st.selectbox("Select Dish to Update", data["Dish Name"].unique())
        selected = data[data["Dish Name"] == dish_to_update].iloc[0]
        with st.form("update_form"):
            updated_row = {
                "Dish Name": st.text_input("Dish Name", selected["Dish Name"]),
                "Cuisine": st.selectbox("Cuisine", sorted(data["Cuisine"].dropna().unique().tolist() + ["Other"]), index=sorted(data["Cuisine"].dropna().unique().tolist() + ["Other"]).index(selected["Cuisine"])),
                "Meal Type": st.selectbox("Meal Type", sorted(data["Meal Type"].dropna().unique().tolist() + ["Other"]), index=sorted(data["Meal Type"].dropna().unique().tolist() + ["Other"]).index(selected["Meal Type"])),
                "Comfort Food": st.checkbox("Comfort Food", selected["Comfort Food"]),
                "Masala Food": st.checkbox("Masala Food", selected["Masala Food"]),
                "Dessert": st.checkbox("Dessert", selected["Dessert"]),
                "Spice Level": st.selectbox("Spice Level", ["Mild", "Medium", "Hot"], index=["Mild", "Medium", "Hot"].index(selected["Spice Level"])),
                "Cooking Time": st.selectbox("Cooking Time", ["Quick", "Moderate", "Elaborate"], index=["Quick", "Moderate", "Elaborate"].index(selected["Cooking Time"])),
                "Mood-Based": st.selectbox("Mood-Based", sorted(data["Mood-Based"].dropna().unique().tolist() + ["Other"]), index=sorted(data["Mood-Based"].dropna().unique().tolist() + ["Other"]).index(selected["Mood-Based"])),
                "Weather-Based": st.selectbox("Weather-Based", sorted(data["Weather-Based"].dropna().unique().tolist() + ["Other"]), index=sorted(data["Weather-Based"].dropna().unique().tolist() + ["Other"]).index(selected["Weather-Based"])),
                "Dietary": st.selectbox("Dietary", ["Veg"], index=0),
                "Occasion": st.selectbox("Occasion", sorted(data["Occasion"].dropna().unique().tolist() + ["Other"]), index=sorted(data["Occasion"].dropna().unique().tolist() + ["Other"]).index(selected["Occasion"])),
                "Region": st.selectbox("Region", sorted(data["Region"].dropna().unique().tolist() + ["Other"]), index=sorted(data["Region"].dropna().unique().tolist() + ["Other"]).index(selected["Region"]))
            }
            submitted = st.form_submit_button("Update Dish")
            if submitted:
                data.loc[data["Dish Name"] == dish_to_update] = updated_row
                data.to_csv("veg_indian_meals.csv", index=False)
                st.success("Dish updated successfully!")

    elif action == "Delete":
        st.subheader("Delete a Dish")
        dish_to_delete = st.selectbox("Select Dish to Delete", data["Dish Name"].unique())
        if st.button("Delete"):
            data = data[data["Dish Name"] != dish_to_delete]
            data.to_csv("veg_indian_meals.csv", index=False)
            st.success(f"Deleted '{dish_to_delete}' successfully!")
