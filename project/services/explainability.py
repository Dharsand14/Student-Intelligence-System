def explain_prediction(data):
    """
    Provides a heuristic explanation of the model's prediction based on input features.
    Returns a multi-line string where '+' denotes a positive factor and '-' a concern.
    """
    explanations = []
    
    study = float(data.get("study_hours", 0))
    att = float(data.get("attendance", 0))
    sleep = float(data.get("sleep_hours", 0))
    mental = float(data.get("mental_health", 0))
    
    # Study Hours Impact
    if study < 3:
        explanations.append("- Low study hours negatively impact your score.")
    elif study >= 6:
        explanations.append("+ High daily study commitment significantly boosts your grade.")
        
    # Attendance Impact
    if att < 80:
        explanations.append("- Poor attendance severely penalizes your prediction.")
    elif att >= 95:
        explanations.append("+ Perfect attendance is your strongest performance driver.")
        
    # Health/Sleep Impact
    if sleep < 6:
        explanations.append("- Inadequate sleep creates a cognitive deficit.")
    elif sleep >= 8:
        explanations.append("+ Optimal sleep patterns improve your test performance.")
        
    if mental < 4:
        explanations.append("- Low mental health rating is dragging down your focus.")
    elif mental >= 8:
        explanations.append("+ High mental health score supports stable exam success.")
        
    # Aggregate result if empty
    if not explanations:
        explanations.append("Balanced metrics result in a stable prediction.")
        
    return "\n".join(explanations)
