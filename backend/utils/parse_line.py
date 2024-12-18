from utils.clean_name import clean_disease_name

def parse_line(line):
    try:
        # First clean the line of quotes and extra whitespace
        line = line.strip().replace('"', '')
        
        # Split on tab to separate data and count
        if '\t' not in line:
            return None
            
        key, count = line.split('\t')
        
        # Handle case of just disease and count (no symptoms or outcome)
        if '_' not in key:
            # Include disease-only entries with empty symptoms and no outcome
            return {
                'disease': clean_disease_name(key),
                'symptoms': [],
                'outcome': None,
                'count': int(count)
            }
            
        parts = [p for p in key.split('_') if p]  # Remove empty strings
        
        # Define valid symptoms and outcomes
        valid_symptoms = ['Fever', 'Cough', 'Fatigue', 'DifficultyBreathing']
        valid_outcomes = ['Positive', 'Negative']
        
        # Get the last part to check if it's an outcome
        last_part = parts[-1] if parts else None
        
        # If last part is an outcome, process normally
        if last_part in valid_outcomes:
            outcome = last_part
            symptoms = [p for p in parts[1:-1] if p in valid_symptoms]
            
            # Get disease (everything up to first symptom, joined with spaces)
            disease_parts = []
            for part in parts:
                if part in valid_symptoms or part in valid_outcomes:
                    break
                disease_parts.append(part)
                
            disease = clean_disease_name(' '.join(disease_parts))
            
        else:
            # If no valid outcome, treat as disease-only entry
            disease = clean_disease_name(key)
            symptoms = []
            outcome = None
            
        return {
            'disease': disease,
            'symptoms': symptoms,
            'outcome': outcome,
            'count': int(count)
        }
    except (ValueError, IndexError) as e:
        print(f"Error parsing line: {line}, Error: {str(e)}")
        return None