"""
Create a visual score breakdown report
"""

def create_score_visualization(score_breakdown):
    """
    Create ASCII art visualization of score breakdown
    """
    components = {
        'Skills (35%)': score_breakdown.skill_match_score * 100,
        'Semantic (30%)': score_breakdown.semantic_similarity * 100,
        'Experience (20%)': score_breakdown.experience_score * 100,
        'Education (10%)': score_breakdown.education_score * 100,
        'Keywords (5%)': score_breakdown.keyword_score * 100
    }
    
    output = []
    output.append("\n" + "=" * 60)
    output.append("SCORE BREAKDOWN")
    output.append("=" * 60 + "\n")
    
    for component, score in components.items():
        # Create bar chart
        bar_length = int(score / 2)  # Scale to 50 chars max
        bar = "█" * bar_length + "░" * (50 - bar_length)
        
        # Color coding (simulated with symbols)
        if score >= 80:
            status = "✓"
        elif score >= 60:
            status = "~"
        else:
            status = "✗"
        
        output.append(f"{status} {component:20} [{bar}] {score:5.1f}%")
    
    output.append("\n" + "=" * 60)
    output.append(f"OVERALL SCORE: {score_breakdown.overall_score:.1f}/100")
    output.append("=" * 60 + "\n")
    
    return "\n".join(output)


def create_skill_comparison(matched_skills, missing_skills):
    """
    Create side-by-side comparison of matched vs missing skills
    """
    output = []
    output.append("\n" + "=" * 60)
    output.append("SKILL ANALYSIS")
    output.append("=" * 60 + "\n")
    
    # Matched skills
    output.append(f"✓ MATCHED SKILLS ({len(matched_skills)}):")
    output.append("-" * 60)
    if matched_skills:
        for skill in matched_skills[:10]:  # Show top 10
            output.append(f"  ✓ {skill}")
        if len(matched_skills) > 10:
            output.append(f"  ... and {len(matched_skills) - 10} more")
    else:
        output.append("  (none)")
    
    output.append("")
    
    # Missing skills
    output.append(f"✗ MISSING SKILLS ({len(missing_skills)}):")
    output.append("-" * 60)
    if missing_skills:
        for skill in missing_skills[:10]:  # Show top 10
            output.append(f"  ✗ {skill}")
        if len(missing_skills) > 10:
            output.append(f"  ... and {len(missing_skills) - 10} more")
    else:
        output.append("  (none - you have all required skills!)")
    
    output.append("\n" + "=" * 60 + "\n")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Demo
    from dataclasses import dataclass
    
    @dataclass
    class MockScoreBreakdown:
        overall_score: float = 68.5
        skill_match_score: float = 0.60
        semantic_similarity: float = 0.75
        experience_score: float = 0.80
        education_score: float = 0.50
        keyword_score: float = 0.40
    
    breakdown = MockScoreBreakdown()
    
    print(create_score_visualization(breakdown))
    
    matched = ['Python', 'SQL', 'Git', 'Docker', 'Communication']
    missing = ['GoLang', 'Kubernetes', 'AWS', 'Terraform']
    
    print(create_skill_comparison(matched, missing))
