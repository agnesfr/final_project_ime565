
import streamlit as st
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

model_choice = st.session_state['model_choice'] 

st.markdown(
    f'<h2 style="text-align:center;">Additional Information and Model Insights for {model_choice} Model</h2>',
    unsafe_allow_html=True
)

# Load CSV file with metrics
metrics_df = pd.read_csv("model_performance.csv")

# Model performance metrics (from training/validation)


if model_choice== "Decision Tree":
    feature_imp="feature_imp_dt.svg"
    histogram= "residuals_hist_dt.svg"
    pred_vs_actual = "actual_vs_predicted_dt.svg"
    coverage = "prediction_intervals_dt.svg"
    RMSE = metrics_df.loc[metrics_df['Model']=='Decision Tree', 'RMSE'].values[0]
    R2 = metrics_df.loc[metrics_df['Model']=='Decision Tree', 'R2 Score'].values[0]
elif model_choice == "Random Forest":
    feature_imp="feature_imp_rf.svg"
    histogram= "residuals_hist_rf.svg"
    pred_vs_actual = "actual_vs_predicted_rf.svg"
    coverage = "prediction_intervals_rf.svg"
    RMSE = metrics_df.loc[metrics_df['Model']=='Random Forest', 'RMSE'].values[0]
    R2 = metrics_df.loc[metrics_df['Model']=='Random Forest', 'R2 Score'].values[0]
elif model_choice == "AdaBoost":
    feature_imp="feature_imp_ada.svg"
    histogram= "residuals_hist_ada.svg"
    pred_vs_actual = "actual_vs_predicted_ada.svg"
    coverage = "prediction_intervals_ada.svg"
    RMSE = metrics_df.loc[metrics_df['Model']=='AdaBoost', 'RMSE'].values[0]
    R2 = metrics_df.loc[metrics_df['Model']=='AdaBoost', 'R2 Score'].values[0]
elif model_choice == "Soft Voting":
    feature_imp="feature_imp_vote.svg"
    histogram= "residuals_hist_vote.svg"
    pred_vs_actual = "actual_vs_predicted_vote.svg"
    coverage = "prediction_intervals_vote.svg"
    RMSE = metrics_df.loc[metrics_df['Model']=='Voting Regressor', 'RMSE'].values[0]
    R2 = metrics_df.loc[metrics_df['Model']=='Voting Regressor', 'R2 Score'].values[0]

# --- Header ---
st.markdown("""
    <h3 style="margin-top: 1.5rem; text-align:center;">Model Performance</h3>
""", unsafe_allow_html=True)

# --- Metric Cards ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(255, 0, 128, 0.18);
        ">
            <h4 style="margin-bottom: 5px;">RMSE</h4>
            <p style="font-size: 32px; font-weight: 700;">
    """ + f"{RMSE:,.0f}" + """
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(255, 0, 128, 0.18);
        ">
            <h4 style="margin-bottom: 5px;">R²</h4>
            <p style="font-size: 32px; font-weight: 700;">
        """ + f"{R2:.3f}" + """
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- Insights header ---
st.markdown("""
    <h3 style="margin-top: 2rem; text-align:center;">Model Insights</h3>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Feature Importance", "Histogram of Residuals", "Predicted Vs. Actual", "Coverage Plot"])
with tab1:
    st.image(feature_imp, caption="Relative importance of features in prediction.")
with tab2:
    st.image(histogram, caption="Distribution of residuals to evaluate prediction quality.")
with tab3:
    st.image(pred_vs_actual, caption="Visual comparison of predicted and actual values.")
with tab4:
    st.image(coverage, caption="Range of predictions with confidence inte")