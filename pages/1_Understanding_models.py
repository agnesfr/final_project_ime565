import streamlit as st

st.title("Understanding Models")
st.write(
    "Compare the available machine learning models for predicting apartment prices and choose the best one for your needs."
)

st.header("About the Models")

with st.expander("Decision Tree"):
    st.write("- A simple, interpretable model that splits data into branches based on features.")
    st.write("- Works well with small datasets and is easy to visualize.")
    st.markdown("**Why use it?** When interpretability and simplicity are more important than accuracy.")

with st.expander("Random Forest"):
    st.write("- Combines multiple decision trees to improve accuracy and reduce overfitting.")
    st.write("- Handles large datasets effectively and provides feature importance.")
    st.markdown("**Why use it?** When you need a balance of accuracy and generalization.")

with st.expander("AdaBoost"):
    st.write("- A boosting technique that builds models iteratively, focusing on difficult-to-predict samples.")
    st.write("- Improves performance for imbalanced datasets.")
    st.markdown("**Why use it?** When your data has significant class imbalances or misclassification costs are high.")

with st.expander("Soft Voting Classifier"):
    st.write("- Combines predictions from multiple models (Decision Tree, Random Forest, AdaBoost) by averaging their probabilities.")
    st.write("- Often achieves better performance than any single model.")
    st.markdown("**Why use it?** When you want the strengths of multiple models and can trade interpretability for accuracy.")

st.header("Choosing the Right Model")
st.write(
    "- Use Decision Tree for quick analysis or when interpretability is crucial.\n"
    "- Use Random Forest for a robust balance of accuracy and generalization.\n"
    "- Use AdaBoost for imbalanced datasets or when misclassification costs are high.\n"
    "- Use Soft Voting Classifier to maximize overall performance by leveraging the strengths of multiple models."
)
