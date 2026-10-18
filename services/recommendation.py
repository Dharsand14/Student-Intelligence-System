def get_study_recommendations(study_hours, attendance, sleep_hours, predicted_score):
    """
    Provides actionable advice to the student to improve their future scores.
    """
    recommendations = []
    
    if predicted_score >= 85:
        recommendations.append("Excellent trajectory! Keep up your current routine.")
    else:
        if attendance < 80:
            recommendations.append("Increase your attendance. Missing lectures is heavily correlated with lower scores.")
        if study_hours < 5:
            recommendations.append("Add at least 1-2 extra hours of self-study per day to see a substantial boost in your grades.")
        if sleep_hours < 6.5:
            recommendations.append("Prioritize your sleep. Your brain needs at least 7 hours for optimal memory retention.")
            
        if not recommendations:
            recommendations.append("Review your past exam mistakes and focus on active recall studying techniques.")
            
    return recommendations
