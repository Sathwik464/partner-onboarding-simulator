import pandas as pd

def generate_health_report(validation_results: list) -> dict:
    df = pd.DataFrame(validation_results)
    
    # calculate health score — multiply mean by 100 and round to 2 decimal places
    health_score = round(df['passed'].mean() * 100, 2)
    
    # determine status label
    status = "Well done" if health_score >= 80 else "Not bad" if health_score >= 50 else "Needs immediate attention"
    
    return {
        "health_score": health_score,
        "status": status,
        "total_checks": len(df),
        "passed_checks": int(df['passed'].sum()),
        "failed_checks": int((df['passed'] == False).sum()),
        
        # critical failures only
        "critical_issues": df[
        (df['passed'] == False) & 
        (df['severity'] == 'critical')
        ][['check_type', 'message', 'fix']].to_dict('records'),

        # warnings only
        "warnings": df[
        (df['passed'] == False) & 
        (df['severity'] == 'warning')
        ][['check_type', 'message', 'fix']].to_dict('records')
    }