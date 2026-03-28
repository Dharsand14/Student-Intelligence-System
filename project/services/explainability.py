def explain_prediction(study_hours, attendance, sleep_hours, mental_health):
    """
    Provides a heuristic explanation of the model's prediction based on input features.
    In a real-world scenario, you would integrate the SHAP library here.
    """
    explanations = []
    
    if study_hours < 4:
        explanations.append("- Low study hours negatively impacted the score.")
    elif study_hours >= 7:
        explanations.append("+ High study hours significantly boosted the score.")
        
    if attendance < 75:
        explanations.append("- Poor attendance severely penalized the prediction.")
        
    if sleep_hours < 6:
        explanations.append("- Lack of adequate sleep negatively affected cognitive metrics.")
        
    if mental_health < 50:
        explanations.append("- Low mental health score lowered the overall performance projection.")
        
    if not explanations:
        explanations.append("All metrics are balanced, resulting in a stable prediction.")
        
    return "\n".join(explanations)
